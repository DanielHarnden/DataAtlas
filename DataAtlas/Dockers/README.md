# Docker (containerization)
Docker containers are used to achieve OS agnosticism for the Data Atlas, having the application run independently of the host OS.
Any system that is capable of running Python and Docker is able to use the application. Starting and stopping the application is as simple as turning on or off the docker containers.
Our Docker environment is split up into 3 areas for each area of the application: ReactJS for frontend, SchemaCrawler for middleware, ArangoDB for backend.

# ReactJS
The frontend container, where the user interaction takes place in a GUI.
The container makes use of HTML, CSS, and ReactJS, an open-source Javascript library for building GUIs.

# SchemaCrawler
The middleware container, where the databases are analyzed and the images are generated.
The container makes use of SchemaCrawler, an open-source database comprehension and discovery tool.

# ArangoDB
The backend container, where the database key relations are stored, as well as the reference database.
The container makes use of ArangoDB, an open-source database system, coupled with pyArango.


![Docker Environment](/Documentation/dockerEnvironment.png)
