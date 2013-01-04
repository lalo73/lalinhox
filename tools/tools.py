__author__ = 'leandro'

def checkValidPathFormatToDir(aPath):
    if not aPath:
        raise InvalidPath()
    if not aPath.endsWith("/"):
        raise InvalidPath()

#exceptions

class InvalidPath(Exception):
    def __init__(self):
        super(InvalidPath,self).__init__()
