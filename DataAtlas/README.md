# Data Atlas

SAIC's Data Atlas is a tool useful for merging database schema's with the ultimate goal of merging various minor databases into one primary, centralized database. The software stack of Data Atlas is composed primarily of Python3 and networked Docker containers.

## Prerequisites
Before Data Atlas is installed, ensure that the system that will run Data Atlas has both a Python3 installation available and a docker install available.

## Running Data Atlas

To run Data Atlas, use Python to execute runDataAtlas.py. This will install the flask, flask_cors, and PIL Python libraries before attempting to run the Frontend, Middleware, and Backend Docker containers. A Flask API will then begin running in the prompt that you executed runDataAtlas.py.

Although Data Atlas will eventually require logging in, this implementation does not yet have it. You may circumvent login by using the developer button.

There will be a screen with a drop down menu requesting that you enter a database. A user would add a database schema or use one already entered then request a schema image to be created with the button below. Upon hitting the button, an image should display a diagram of the requested Schema.

There will be a second dropdown menu that is blank by default. If you enter a database, it will be merged into the first database.

## Stopping Data Atlas

Manually stop the Flask API, then execute stopDataAtlas.py to stop the Docker containers from running.

## Finding Generated Files

Data Atlas saves a .db file of the newly generated database, as well as an the image file, to the local machine. Databases can be found in the directory DataAtlas/Dockers/volume/databases in the format originalName_updated.db, and images can be found in the directory DataAtlas/Dockers/volume/generatedPngs in the format originalName_updated.sqlite.png

## Data Atlas Structure

Once Data Atlas is running, the end user is directed to a React webpage that hosts the GUI. The user is prompted to choose a database to be atlased. Once the database is chosen, React will call a Flask API which starts the long process of parsing, mapping, and generating an image based on the database (a visual representation of the process is below). Once the image is generated, the Flask API returns that image to the React webpage, which updates accordingly.

![Data Atlas Flowchard](/Documentation/DataAtlas.png)
