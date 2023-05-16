from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from dataAtlas import requestDatabases, beginAtlasing, generateImg
from PIL import Image
import os, io, re, string

# Flask API
app = Flask(__name__)
CORS(app)

# API Explaination:
# By default, Flask is hosted on http://localhost:5000
#@app.route("/example")  The URL that needs to be pinged to start the API. 
#def example():          The Python function that is run when
#    Any code would go here
#    return "Success!!!"

# This example would be pinged by the following React code:
# fetch(http://localhost:5000/example)

# Arguments can be added using the following template (the <> are necessary):
#@app.route("/example/<arg1>/<arg2>/<arg3>")
#def example(arg1, arg2, arg3):
#    return arg1 + arg2 + arg3



@app.route("/requestDatabases")
def APIrequestDatabases():
    # List of colors and unprintable characters to remove
    color_pattern = re.compile(r'\x1b\[[0-?]*[ -/]*[@-~]')
    printable_chars = set(string.printable)

    # Calls for database list, splits it
    databaseList = requestDatabases()
    splitList = databaseList.split()
    
    # Removes colors and unprintable characters
    for i in range(len(splitList)):
        splitList[i] = color_pattern.sub('', splitList[i])
        splitList[i] = ''.join(filter(lambda c: c in printable_chars, splitList[i]))

    # Filter out items containing "_updated"
    filtered_list = [item for item in splitList if "_updated" not in item]

    # Return JSON of printable items
    return jsonify(filtered_list)



@app.route("/beginAtlasing/<db>")
def APIbeginAtlasing(db):
    # Calls the dataAtlas.py function, which creates an image
    beginAtlasing(db, None)
    # Returns the generated image
    return APIreturnImg(db)

@app.route("/beginAtlasingTwo/<db>/<db2>")
def APIbeginAtlasingTwo(db, db2):
    # Calls the dataAtlas.py function, which creates an image
    beginAtlasing(db, db2)
    # Returns the generated image
    return APIreturnImgTwo(db, db2)



@app.route("/returnImg/<db>")
def APIreturnImg(db):
    # Updates the file name
    newFileName = db.split(".")[0] + "_updated.db"
    # Stores the path of the newly generated image
    imgPath = os.getcwd() + "\Dockers\\volume\generatedPngs\\" + newFileName + ".png"

    # Opens the file and reads the binary
    with open(imgPath, 'rb') as input:
        # Stores bytes in a buffer
        img_bytes = io.BytesIO(input.read())
        img = Image.open(img_bytes)

    # Saves the image to a new buffer
    output_buffer = io.BytesIO()
    img.save(output_buffer, 'png')
    output_buffer.seek(0)

    # Returns the image from the new buffer
    return send_file(output_buffer, mimetype='image/png')

@app.route("/returnImgTwo/<db>/<db2>")
def APIreturnImgTwo(db, db2):
    # Updates the file name
    newFileName = db.split(".")[0] + "and" + db2.split(".")[0] + "_updated.db"
    # Stores the path of the newly generated image
    imgPath = os.getcwd() + "\Dockers\\volume\generatedPngs\\" + newFileName + ".png"

    # Opens the file and reads the binary
    with open(imgPath, 'rb') as input:
        # Stores bytes in a buffer
        img_bytes = io.BytesIO(input.read())
        img = Image.open(img_bytes)

    # Saves the image to a new buffer
    output_buffer = io.BytesIO()
    img.save(output_buffer, 'png')
    output_buffer.seek(0)

    # Returns the image from the new buffer
    return send_file(output_buffer, mimetype='image/png')


    
# Starts the Flask API
if __name__ == '__main__':
    app.run()