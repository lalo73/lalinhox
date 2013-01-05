__author__ = 'leandro'


class HardDisk:
    def __init__(self):
        pass


class GeneralFileSystemObject:
    def __init__(self,name):
        self.name = name

class Directory(GeneralFileSystemObject):
    def __init__(self,name):
        super(Directory,self).__init__(name)
        self.filesAndDirectories = {}

    def addFile(self,file,path=""):
        pass


#Exceptions

class CantFindDirectory(Exception):
    def __init__(self):
        super(CantFindDirectory,self).__init__()

