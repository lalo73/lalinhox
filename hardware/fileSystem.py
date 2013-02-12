from system_tools.systemTools import checkFileSystemObjectName, checkPathFormat

class HardDisk:
    def __init__(self, name="HardDisk"):
        self.name = name
        self.root = RootDirectory()

    def getObjectByPath(self, path):
        checkPathFormat(path)
        split_path = path.split("/")
        return self.__getObjectBySplitPath(split_path)

    def exist(self, path):
        try:
            self.getObjectByPath(path)
            return True
        except CantFindDirectoryOrFile:
            return False

    def mkDirectory(self, path):
        checkPathFormat(path)
        split_path = path.split("/")
        if split_path[-1] == "":
            split_path = split_path[:-1]
        if len(split_path) == 1:
            if split_path[0] == "":
                raise FilePathRequired()
            else:
                dir_name = split_path[0]
                directory = self.root
        else:
            path = split_path[:-1]
            dir_name = split_path[-1]
            father_path = "/".join(path)
            father_path += "/"
            directory = self.getObjectByPath(father_path)
        return self.__mkDirectoryOnDirectory(dir_name, directory)

    def mkFile(self, path, data=None):
        checkPathFormat(path)
        split_path = path.split("/")
        if len(split_path) == 1:
            if split_path[0] == "":
                raise FilePathRequired()
            else:
                file_name = split_path[0]
                directory = self.root
        else:
            path = split_path[:-1]
            file_name = split_path[-1]
            father_path = "/".join(path)
            father_path += "/"
            directory = self.getObjectByPath(father_path)
        return self.__mkFileOnDirectory(file_name, directory, data)

    def __mkFileOnDirectory(self, file_name, directory, data=None):
        new_file = File(file_name, data, directory)
        directory.add_object(file)
        return new_file

    def __mkDirectoryOnDirectory(self, new_directory_name, directory):
        new_directory = Directory(new_directory_name, self)
        directory.add_object(new_directory)
        return new_directory

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
            return last_object.get_directory(object_name)
        else:
            return last_object.get_file(object_name)


class GeneralFileSystemObject(object):
    def __unicode__(self):
        return u"%(name)s" % {"name": self.get_name()}

    def __str__(self):
        return "%(name)s" % {"name": self.get_name()}

    def __repr__(self):
        return "%(name)s" % {"name": self.get_name()}

    def __init__(self, name, father=None):
        checkFileSystemObjectName(name)
        self.set_father(father)
        self.set_name(name)

    def tree(self, father_base_space=0):
        return " " * father_base_space + str(self)

    def is_directory(self):
        return False

    def is_file(self):
        return False

    def get_father(self):
        return self.__father

    def set_father(self, new_father):
        self.__father = new_father

    def set_name(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    def path(self):
        return self.get_father().path() + repr(self)


class File(GeneralFileSystemObject):
    def __init__(self, name, data=None, father=None):
        super(File, self).__init__(name, father)
        self.__data = data

    def get_data(self):
        return self.__data

    def set_data(self, data):
        self.__data = data

    def is_file(self):
        return True


class Directory(GeneralFileSystemObject):
    def __unicode__(self):
        return super(Directory, self).__unicode__() + "/"

    def __str__(self):
        return super(Directory, self).__str__() + "/"

    def __repr__(self):
        return super(Directory, self).__repr__() + "/"

    def __init__(self, name, father=None):
        super(Directory, self).__init__(name, father)
        self.objects = {}

    def tree(self, father_base_space=0):
        tree = " " * father_base_space + str(self)
        base_space = " " * father_base_space + " " * len(str(self))
        for obj in self.objects:
            object_string = "\n" + self.objects[obj].tree(len(base_space))
            tree += object_string
        return str(tree)

    def mkDir(self, name):
        directory = Directory(name, self)
        self.add_object(directory)
        return directory

    def is_directory(self):
        return True

    def remove_object_by_name(self, name):
        try:
            del (self.objects[name])
        except KeyError:
            raise CantFindDirectoryOrFile()

    def list_dir(self):
        return self.objects.keys()

    def add_object(self, new_object):
        name = new_object.get_name()
        if new_object.is_directory():
            name += "/"
        new_object.set_father(self)
        self.objects[name] = new_object

    def get_directory(self, name):
        return self.__getObjectByType(name)

    def get_file(self, name):
        return self.__getObjectByType(name, False)

    def includes(self, object_name):
        return object_name in self.objects.keys()

    def clean(self):
        keys = self.objects.keys()
        for key in keys:
            self.remove_object_by_name(key)

    def __getObjectByType(self, name, directory=True):
        def nameMatch(name, local_object_name, directory):
            local_name = name
            if directory:
                local_name = name + "/"
            return local_name == local_object_name

        for local_object_name in self.objects:
            if nameMatch(name, local_object_name, directory):
                new_object = self.objects[local_object_name]
                return new_object

        raise CantFindDirectoryOrFile()


class RootDirectory(Directory):
    def __init__(self, name="root"):
        super(RootDirectory, self).__init__(name, self)

    def path(self):
        return "/"

# Exceptions


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

__author__ = 'leandro'