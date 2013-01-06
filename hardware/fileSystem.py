__author__ = 'leandro'

from system_tools.systemTools import checkFileSystemObjectName, checkPathFormat

class HardDisk:
    def __init__(self, name="HardDisk"):
        self.name = name
        self.root = RootDirectory()

    def getObjectByPath(self, path):
        checkPathFormat(path)
        split_path = path.split("/")
        return self.__getObjectBySplitPath(split_path)

    def __getObjectBySplitPath(self, split_path):
        last_object = self.root
        size = len(split_path)
        for object_name in split_path:
            isDirectory = size > 1
            last_object = self.__nextObjectFrom(object_name, last_object, isDirectory)
            size -= 1

        return last_object

    def __nextObjectFrom(self, object_name, last_object, isDirectory):
        if object_name == "":
            return last_object
        elif isDirectory:
            return last_object.getDirectory(object_name)
        else:
            return last_object.getFile(object_name)


class GeneralFileSystemObject(object):
    def __unicode__(self):
        return u"%(name)s" % {"name": self.name}

    def __str__(self):
        return "%(name)s" % {"name": self.name}

    def __repr__(self):
        return "%(name)s" % {"name": self.name}

    def __init__(self, name):
        checkFileSystemObjectName(name)
        self.name = name

    def addObject(self, object):
        raise IsNotDirectory()

    def getDirectory(self, name):
        raise IsNotDirectory()

    def getFile(self, name):
        raise IsNotDirectory()

    def isDirectory(self):
        return False

    def getData(self):
        raise IsNotFile()

    def include(self, object_name):
        raise IsNotDirectory()

    def father(self):
        raise IsNotDirectory()


class File(GeneralFileSystemObject):
    def __init__(self, name, data=None):
        super(File, self).__init__(name)
        self.data = data

    def getData(self):
        return self.data


class Directory(GeneralFileSystemObject):
    def __init__(self, name, father=None):
        super(Directory, self).__init__(name)
        self.__father = father
        self.objects = {}

    def father(self):
        return self.__father

    def isDirectory(self):
        return True

    def addObject(self, object):
        name = object.name
        if object.isDirectory():
            name += "/"
            object.father = self
        self.objects[name] = object

    def getDirectory(self, name):
        return self.__getObjectByType(name, True)

    def getFile(self, name):
        return self.__getObjectByType(name, False)

    def includes(self, object_name):
        return object_name in self.objects.keys()

    def __getObjectByType(self, name, directory=True):
        def nameMatch(name, local_object_name, directory):
            local_name = name
            if directory:
                local_name = name + "/"
            return local_name == local_object_name

        for local_object_name in self.objects:
            if nameMatch(name, local_object_name, directory):
                object = self.objects[local_object_name]
                return object

        raise CantFindDirectoryOrFile()


class RootDirectory(Directory):
    def __init__(self, name="root"):
        super(RootDirectory, self).__init__(name, self)

#Exceptions

class CantFindDirectoryOrFile(Exception):
    def __str__(self):
        return "Can't find directory or file"


class IsNotDirectory(Exception):
    def __str__(self):
        return "This is not a directory"


class IsNotFile(Exception):
    def __str__(self):
        return "This is not a file"
