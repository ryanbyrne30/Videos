import pathlib
import os 

curDir = pathlib.Path(__file__).parent.absolute()
partialsDir = pathlib.PurePath(curDir, "partials")
partialImageNameLength = 9

if not os.path.exists(partialsDir):
    os.makedirs(partialsDir)