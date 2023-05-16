import os, importlib, webbrowser, subprocess, sys

def main():
    checkDockerRunning()
    checkForPackages()
    checkForImages()
    checkRunning()
    openReactPage()



# Checks to see if Docker Desktop is running, otherwise the rest of the program can't run
def checkDockerRunning():
    print("Determining if Docker Desktop is running...")

    try:
        subprocess.check_call('docker ps', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    except:
        print("Docker Desktop is not running. Please turn it on and rerun Data Atlas.")
        temp = input()
        sys.exit()

    print("Docker Desktop is running!\n")



# Checks to see if the proper Python packages exist
def checkForPackages():
    print("Determining if the correct Python packages are installed...")

    # The list of packages that should be installed using pip
    packages = ['flask', 'flask-cors', 'Pillow']

    for package in packages:
        # Attempts to import the module; if it can not, that means it is not installed.
        try:
            if package == "Pillow":
                importlib.import_module("PIL")
            elif package == "flask-cors":
                importlib.import_module("flask_cors")
            else:
                importlib.import_module(package)
        except ModuleNotFoundError:
            print(package + " is not downloaded on the local machine. Downloading " + package + "...")
            command = "pip install " + package
            # Attempts to execute the command, throws an error and ends the program if the command does not run as intended.
            try:
                subprocess.check_call(command)
            except:
                print("There was an error importing the " + package + " package. Please make sure that pip is installed.")
                temp = input()
                sys.exit()
            
    print("All packages installed!\n")


# Checks to see if the Docker images exist
def checkForImages():
    print("Determining if Docker images are built...")

    # Checks the list of Docker images for the Data Atlas images
    dockerImages = os.popen('docker image ls -a').read()
    if 'react' not in dockerImages: buildImage("React")
    if 'schemacrawler' not in dockerImages: buildImage("SchemaCrawler")

    print("All images built!\n")

# Builds the Docker image if it does not exist
def buildImage(folder):
    print("The " + folder + " Docker image is currently not built. Building image...")

    # Saves the current directory, then moves to the directory with the Dockerfile
    originalPath = os.getcwd()
    path = os.getcwd() + "\Dockers\\" + folder
    os.chdir(path)

    if folder == "React": command = "docker build --tag react:dataAtlas ."
    if folder == "SchemaCrawler": command = "docker build --tag schemacrawler:dataAtlas ."

    # Attempts to build the Docker image, throws an error and ends the program if the command does not run as intended.
    try:
        subprocess.check_call(command, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    except:
        print("There was an error building the " + folder + " Docker image using command:\n" + command + "\nPlease make sure that there is a Dockerfile in the DataAtlas\Dockers\\" + folder + " directory.")
        temp = input()
        sys.exit()

    os.chdir(originalPath)

    print(folder + " Docker image built!")
    


# Checks to see if the Docker container is running
def checkRunning():
    print("Determining if Docker containers are running...")

    # Checks the list of currently running Docker containers for the Data Atlas containers
    runningContainers = os.popen('docker container ls -a').read()
    if 'react' not in runningContainers: runContainer("React")
    if 'schemacrawler' not in runningContainers: runContainer("SchemaCrawler")

    print("All containers running!\n")

# Runs the Docker container if it is not running
def runContainer(name):
    if name == "React": command = "docker run --name react-app --rm -itd -v " + os.getcwd() + "/Dockers/React/src:/app -e WATCHPACK_POLLING=true -p 3000:3000 react:dataAtlas"
    if name == "SchemaCrawler": command = "docker run --name schemacrawler --rm -di --mount type=bind,source=" + os.getcwd() + "/Dockers/volume,target=/volume -p 3010:3010 schemacrawler:dataAtlas"   

    # Attempts to run the Docker container, throws an error and ends the program if the command does not run as intended.
    try:
        subprocess.check_call(command)
    except:
        print("There was an error starting the " + name + " Docker container using command:\n" + command)
        temp = input()
        sys.exit()



# Opens the React page in the user's web browser
def openReactPage():
    webbrowser.open('http://localhost:3000/Login/Dashboard')

    print("Attempting to start the Flask API...")
    subprocess.check_call("python .\\Database\\flaskAPI.py")


if __name__ == "__main__":
    main()