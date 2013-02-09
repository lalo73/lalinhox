import unittest
from hardware.fileSystem import File, GeneralFileSystemObject, RootDirectory
from mockito import *

class FileTest(unittest.TestCase):
    def setUp(self):
        file_father = mock()
        self.file = File('test_file', "Some data", file_father)

    def test_GetData(self):
        data = self.file.getData()
        self.assertEqual(data, "Some data")


class GeneralFileSystemObjectTest(unittest.TestCase):
    def setUp(self):
        father = mock(RootDirectory)
        self.file_system_object = GeneralFileSystemObject("generalFileSystemObject")


    def test_treeOfGeneralFileSystemWithFather(self):
        pass

suite = unittest.TestLoader().loadTestsFromTestCase(FileTest)
unittest.TextTestRunner(verbosity=2).run(suite)

suite = unittest.TestLoader().loadTestsFromTestCase(GeneralFileSystemObjectTest)
unittest.TextTestRunner(verbosity=2).run(suite)

__author__ = 'leandro'
