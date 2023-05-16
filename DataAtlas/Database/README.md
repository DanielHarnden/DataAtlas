## runDataAtlas.py

runDataAtlas.py is a python script that needs to be ran in powershell within the file directory to run the data atlas.
Docker must be installed and open for this to work.

## stopDataAtlas.py

stopDataAtlas.py is a python script that closes Data Atlas and corresponding Docker containters.
Run in the same powershell directory.

## keyList.json

keyList.json is a list of all keys introduced by data bases.

## flaskAPI.py

flaskAPI.py is a python script that calls the flask API -- downloaded when runDataAtlas.py is run -- and is the primary API used in image generation.

## dataAtlas.py

dataAtlas.py is the main program -- maps the texts and uses flaskAPI.py to generate an image.
