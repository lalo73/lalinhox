import unittest
from hardware.fileSystem import File, Directory
from mockito import *


class FileTest(unittest.TestCase):
    def setUp(self):
        self.directory_father = mock()
        self.file = File('test_file', "Some data", self.directory_father)

    def test_get_data(self):
        data = self.file.get_data()
        self.assertEqual(data, "Some data")

    def test_set_data(self):
        old_data = self.file.get_data()
        new_data = "new data"
        self.file.set_data(new_data)
        self.assertNotEqual(old_data, new_data)

    def test_name(self):
        file_name = self.file.get_name()
        self.assertTrue("test_file", file_name)

    def test_set_father(self):
        old_father = self.file.get_father()
        new_father = mock()
        self.file.set_father(new_father)
        self.assertNotEqual(old_father, self.file.get_father())

    def test_get_father(self):
        father = self.directory_father
        self.assertTrue(father, self.file.get_father())

    def test_is_file(self):
        is_file = self.file.is_file()
        self.assertTrue(is_file)

    def test_is_not_directory(self):
        is_directory = self.file.is_directory()
        self.assertFalse(is_directory)

    def test_tree(self):
        tree = self.file.tree()
        self.assertEqual(tree, self.file.get_name())


class DirectoryTest(unittest.TestCase):
    def setUp(self):
        mock_root = mock()
        self.directory = Directory("directory_test", mock_root)



suite = unittest.TestLoader().loadTestsFromTestCase(FileTest)
unittest.TextTestRunner(verbosity=2).run(suite)

# suite = unittest.TestLoader().loadTestsFromTestCase(GeneralFileSystemObjectTest)
# unittest.TextTestRunner(verbosity=2).run(suite)

__author__ = 'leandro'
