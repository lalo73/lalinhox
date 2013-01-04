__author__ = 'leandro'

from tools import tools

class HardDisk:
    def __init__(self):
        pass


class GeneralFileSystem:
    def __init__(self,name):
        self.name = name

class Directory(GeneralFileSystem):
    def __init__(self,name):
        super(Directory,self).__init__(name)
        self.filesAndDirectories = {}

    def addFile(self,path,file):
        tools.checkValidPathFormatToDir(path)
        if path == "/":
            self.filesAndDirectories[file.name] = file
        else:
            directories = path.split("/")
            directoryName = directories[0]
            newPath = "/".join(directories[1:])
            directory = self.getDir(directoryName)
            directory.addFile(newPath,file)

    def getDir(self,dirName):
        try:
            return self.filesAndDirectories[dirName]
        except KeyError:
            raise CantFindDirectory()

#Exceptions

class CantFindDirectory(Exception):
    def __init__(self):
        super(CantFindDirectory,self).__init__()

