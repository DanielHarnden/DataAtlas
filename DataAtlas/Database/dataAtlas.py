import os, subprocess, sys
import json
import sqlite3

# Returns a string of the databases stored in Dockers/volume/databases
def requestDatabases():
    try:
        subprocess.check_call("docker exec -it schemacrawler ls /volume/databases", stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    except:
        print("dataAtlas.py: error in requestDatabases() using command: " + command + "\nPlease make sure that the SchemaCrawler Docker container is running.")
        sys.exit()

    return os.popen('docker exec -it schemacrawler ls /volume/databases').read()



# Data Atlas has five main steps:
# Reference the Readme for a visual representation of this code
def beginAtlasing(db, db2):
    if db2 is None:
        # Step 1: Generate a txt file based on the inputted schema (without relations) using SchemaCrawler
        generateTxt(db)

        # Step 2: Parse the generated txt file to get a list of table names and keys
        parsedTxt = beginParseTxt(db)

        # Step 3: Map the keys to each other so relations can be found and formed
        # Used to be manual, now it's automatic. Simply change which function is called to switch
        for table in parsedTxt: table.pop(0)
        mapTxt(parsedTxt)

        # Step 4: Generate a database file using the mapped information
        parsedTxt = beginParseTxt(db)
        dbFileName = convertToDB(parsedTxt, db, None)

        # Step 5: Generate an image of the schema using SchemaCrawler
        generateImg(dbFileName)

    else: 
        # Step 1: Generate a txt file based on the inputted schema (without relations) using SchemaCrawler
        generateTxt(db)
        generateTxt(db2)

        # Step 2: Parse the generated txt file to get a list of table names and keys
        parsedTxt = beginParseTxt(db)
        parsedTxt += beginParseTxt(db2)

        # Step 3: Map the keys to each other so relations can be found and formed
        # Used to be manual, now it's automatic. Simply change which function is called to switch
        for table in parsedTxt: table.pop(0)
        mapTxt(parsedTxt)

        # Step 4: Generate a database file using the mapped information
        parsedTxt = beginParseTxt(db)
        parsedTxt += beginParseTxt(db2)

        dbFileName = convertToDB(parsedTxt, db, db2)

        # Step 5: Generate an image of the schema using SchemaCrawler
        generateImg(dbFileName)



# Step 1: Generate a txt file based on the inputted schema (without relations) using SchemaCrawler
# SchemaCrawler does the heavy lifting here, only requiring a call to a shell file to execute the SC command
def generateTxt(db):
    print("Generating a txt file based on the inputted Schema...")

    command = 'docker exec -it schemacrawler sh -c "/generateParsableTxt.sh ' + db + '"'

    try:
        subprocess.check_call(command, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    except:
        print("dataAtlas.py: error in generateTxt() using command: " + command + "\nPlease make sure that the SchemaCrawler Docker container is running.")
        sys.exit()

    print("Generated!\n")



# Step 2: Parse the generated txt file to get a list of table names and keys
# The path of the generated txt file is passed as an argument to Step 2.5
def beginParseTxt(txt):
    print("Parsing the generated txt...")

    path = os.getcwd() + "\Dockers\\volume\generatedTxts\\" + txt + ".txt"

    try:
        parsed = parseTxt(path)
    except:
        print("dataAtlas.py: error in parseTxt(): Unable to find .txt at path " + path + "\nPlease make sure that SchemaCrawler successfully generated a .txt file.")
        sys.exit()

    print("Parsed!\n")
    return parsed

# Step 2.5: The function that does the actual parsing
# Returns a list of lists in the format [ [Table_Name1, key1, ..., keyN], ..., [Table_NameN, key1, ..., keyN] ] to be mapped
def parseTxt(filename):
    # Checks to see if file exists
    try:
        schema_file = filename
    except Exception as err:
        print("USAGE:\t parseTxt(\"filename\")")
        print(Exception, err)
        sys.exit()
        
    # Lists that will be used to clean the data
    lines = list()
    table = list()
    linesByTable = list()

    # Opens file
    with open(schema_file) as f:
        data = f.read()
        # Checks each line...
        for line in data.split('\n'):
            # ... to see if it has useful content, and...
            if line != '' and isGoodString(line) is True:
                # ...adds it to the list of lines
                if '[table]' in line:
                    # Lines with [table] don't have any extra data at the end of the string...
                    lines.append(line.replace(' ',''))
                else:
                    # ...but other lines do, and the extra data is useless
                    trimInfo = line.split('     ', 1)[0]
                    if trimInfo != '':
                        lines.append(trimInfo.replace(' ',''))
    
    # Everything before the =s is useless, so it gets deleted
    for line in lines:
        if '=====' in line:
            index = lines.index(line)
            while index >= 0:
                lines.pop(index)
                index -= 1

    # Splits each table into separate lists
    for line in lines:
        if '[table]' in line:
            if table:
                linesByTable.append(table)
            table = list()
            table.append(line)
        else:
            if line not in table:
                table.append(line)
    # Adds the final list to the table
    linesByTable.append(table)

    # Returns a list of lists
    return linesByTable

# Step 2.5.5: Some lines contain useless data, this function determines whether the input is useless
def isGoodString(line):
    badStrings = ['----------', '<--', '-->', 'foreign key', 'foreignkey', 'primary key', 'primarykey', 'indexes', 'non-unique index', 'autoindex']

    # Returns false if the string contains useless input
    for item in badStrings:
        if item in line.lower() or line.lower() == item:
            return False
    return True



def mapTxt(inputKeys):
    print("Beginning mapping function...")

    with open(os.getcwd() + "\Database\keyList.json") as f:
        try:
            data = json.load(f)
            dataDict = {item: item for item in data}
        except:
            dataDict = {}

    for item in inputKeys:
        for key in item:
            if key not in dataDict:
                print("Adding", key, "as new type of entry.")
                dataDict.update({key: key})

    with open(os.getcwd() + "\Database\keyList.json", 'w') as f:
        json.dump(dataDict, f, indent =4 , separators = (',',': '))

    print("Database mapped!\n")



# Step 4: Generate a database file using the mapped information
# Converts the key list into a format that SchemaCrawler can read
def convertToDB(parsedTxt, db, db2):
    keyList = {}
    with open(os.getcwd() + "\Database\keyList.json") as f:
        keyList = json.load(f)

    generateSqlFile(parsedTxt, keyList, 1)
    
    if db2 is None:
        return convertSqlToDb(db, None)
    else:
        return convertSqlToDb(db, db2)
    

# Step 4.3: Next, we need to use those keys to make a brand new SQL table by hand. Fun.
def generateSqlFile(parsedTxt, keyList, foreignKeyNum):
    # Resets and opens the temporary SQL file
    if os.path.exists("temp.sql"):
        os.remove("temp.sql")
    filename = "temp.sql"
    f = open(filename, "w")

    # The dictonary of NEWLY GENERATED primary keys
    primaryKeys = {}
    # Important for SQL syntax
    noComma = True

    # Iterates through all of the tables from the original txt of the inputted database
    for tableList in parsedTxt:
        # A temp list of added keys to avoid duplicates
        tempKeys = []
        # Iterates through each table from the original txt of the inputted database
        for i, key in enumerate(tableList):

            if "[table]" in key:
                # Creates each table in SQL
                tableName = key[0:key.index("[")]
                f.write(f"CREATE TABLE IF NOT EXISTS `{tableName}` (")
                noComma = True
            else:
                # Determines if they key has to be renamed based on the mapping
                if key in keyList:
                    key = keyList[key]

                    # Checks to see if remapped key is a duplicate as to not add multiples
                    if key not in tempKeys:
                        tempKeys.append(key)
                        # Adds every key as a varchar(50)
                        if noComma:
                            f.write(f"\n\t`{key}` varchar(50) DEFAULT NULL")
                            noComma = False
                        else:
                            f.write(f",\n\t`{key}` varchar(50) DEFAULT NULL")

            # If we've reached the end of this table...
            if i == len(tableList) - 1:
                # ... we set the number of foreign keys we want to add to the number specified previously...
                foreignKeysLeft = foreignKeyNum
                # ... then loop through each key in this table again
                for j, key in enumerate(tableList):
                    # The name of the table is stored
                    if j == 0:
                        table = key[0:key.index("[")]

                    # The first key in the list is added as the primary key (j == 0 is the table name)
                    if j == 1:
                        f.write(f",\n\tPRIMARY KEY (`{keyList[key]}`)")

                    # Iterates through the pairs of mapped keys
                    if key in keyList:
                        # Checks to see if this key has appeared before in the new database. If not, it is set as the primary key of the new database, and any subsequent mentions of the key will reference the key/table it first appears
                        if keyList[key] in primaryKeys:
                            # Checks to see if there are any foreign key additions left for this table and checks to ensure the table is not referencing itself
                            if foreignKeysLeft > 0 and table is not primaryKeys[keyList[key]]:
                                f.write(f",\n\tFOREIGN KEY (`{keyList[key]}`) REFERENCES {primaryKeys[keyList[key]]}(`{keyList[key]}`)")
                                foreignKeysLeft = foreignKeysLeft - 1
                        else:
                            primaryKeys[keyList[key]] = table

        # Ends the table :)
        f.write("\n);\n\n")

# Step 4.5: Finally, we convert that .sql file into a .db file using sqlite3 magic
def convertSqlToDb(db, db2):
    if db2 is None:
        # Names the file [database name]_updated.db
        newFileName = db.split(".")[0] + "_updated.db"
    else:
        # Names the file [database name]and[database two name]_updated.db
        newFileName = db.split(".")[0] + "and" + db2.split(".")[0] + "_updated.db"

    # Creates a new file using the new name
    path = os.getcwd() + "\Dockers\\volume\databases\\" + newFileName

    # Checks to see if file exists and delete it
    if os.path.exists(path):
        os.remove(path)

    # Never ask a woman her age, a man his salary, or me how this code works
    conn = sqlite3.connect(path)
    with open('temp.sql', 'r') as f:
        script = f.read()
    conn.executescript(script)
    conn.close()

    if os.path.exists("temp.sql"):
        os.remove("temp.sql")

    return newFileName



# Step 5: Generate an image of the schema using SchemaCrawler
# Again, SchemaCrawler does the heavy lifting here, only requiring a call to a different shell file to execute the SC command
def generateImg(fileName):
    print("Generating an img file based on the inputted Schema...")

    # Deletes the image if it exists, as to ensure it is up to date
    path = os.getcwd() + "\Dockers\\volume\generatedPngs\\" + fileName + ".png"
    if os.path.exists(path):
        os.remove(path)

    # Creates the image using SchemaCrawler
    command = 'docker exec -it schemacrawler sh -c "/exportDatabaseGraph.sh ' + fileName + '"'
    try:
        subprocess.check_call(command, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    except:
        print("dataAtlas.py is unable to generate an image. Please make sure that the SchemaCrawler Docker container is running.")
        sys.exit()

    print("Image generated!")



if __name__ == "__main__":
    print("Error: Please do not run this file directly.")
    sys.exit()