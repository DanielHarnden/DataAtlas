import os

def main():
    runningContainers = os.popen('docker container ls -a').read()
    
    if 'react' in runningContainers: os.system("docker stop react-app")
    if 'schemacrawler' in runningContainers: os.system("docker stop schemacrawler")

    networkCheck = os.popen('docker network ls').read()
    
    
if __name__ == "__main__":
    main()