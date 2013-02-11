__author__ = 'leandro'


def checkFileSystemObjectName(name):
    if "/" in name:
        raise BadNameFormat("/")


def checkPathFormat(path):
    if " " in path:
        raise BadPatFormat()


#Exceptions
class BadNameFormat(Exception):
    def __init__(self, invalid=""):
        self.invalid_character = invalid

    def __str__(self):
        return "invalid character '%(invalid)s' in name" % {"invalid": self.invalid_character}


class BadPatFormat(Exception):
    def __init__(self, invalid=""):
        self.invalid_character = invalid

    def __str__(self):
        return "invalid character '%(invalid)s' in name" % {"invalid": self.invalid_character}