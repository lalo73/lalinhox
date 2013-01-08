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

    def mkDirectory(self, path):
        split_path = path.split("/")
        if split_path[-1] == "":
            split_path = split_path[:-1]
        if len(split_path) == 1:
            if split_path[0] == "":
                raise FilePathRequired()
            else:
                dir_name = split_path[0]
                dir = self.root
        else:
            path = split_path[:-1]
            dir_name = split_path[-1]
            father_path = "/".join(path)
            father_path += "/"
            dir = self.getObjectByPath(father_path)
        return self.__mkDirectoryOnDirectory(dir_name, dir)

    def mkFile(self, path, data=None):
        split_path = path.split("/")

        pass

    def __mkDirectoryOnDirectory(self, new_directory_name, directory):
        dir = Directory(new_directory_name, self)
        directory.addObject(dir)
        return dir

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

    def __init__(self, name, father=None):
        checkFileSystemObjectName(name)
        self.setFather(father)
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

    def mkDir(self, name):
        raise IsNotDirectory()

    def removeObjectByName(self, name):
        raise IsNotDirectory()

    def listDir(self):
        raise IsNotDirectory()

    def father(self):
        return self.__father

    def setFather(self, newFather):
        self.__father = newFather

    def path(self):
        return self.father().path() + repr(self)


class File(GeneralFileSystemObject):
    def __init__(self, name, data=None, father=None):
        super(File, self).__init__(name, father)
        self.data = data

    def getData(self):
        return self.data


class Directory(GeneralFileSystemObject):
    def __unicode__(self):
        return super(Directory, self).__repr__() + "/"

    def __str__(self):
        return super(Directory, self).__repr__() + "/"

    def __repr__(self):
        return super(Directory, self).__repr__() + "/"

    def __init__(self, name, father=None):
        super(Directory, self).__init__(name, father)
        self.objects = {}

    def mkDir(self, name):
        dir = Directory(name, self)
        self.addObject(dir)
        return dir

    def isDirectory(self):
        return True

    def removeObjectByName(self, name):
        try:
            del(self.objects[name])
        except KeyError:
            raise CantFindDirectoryOrFile()

    def listDir(self):
        return self.objects.keys()

    def addObject(self, object):
        name = object.name
        if object.isDirectory():
            name += "/"
        object.setFather(self)
        self.objects[name] = object

    def getDirectory(self, name):
        return self.__getObjectByType(name, True)

    def getFile(self, name):
        return self.__getObjectByType(name, False)

    def includes(self, object_name):
        return object_name in self.objects.keys()

    def clear(self):
        keys = self.objects.keys()
        for key in keys:
            self.removeObjectByName(key)

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

    def path(self):
        return "/"

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


class FilePathRequired(Exception):
    def __str__(self):
        return "A path is required"