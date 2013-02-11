import unittest
from hardware.fileSystem import File, Directory, CantFindDirectoryOrFile, GeneralFileSystemObject
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

    def test_mk_directory(self):
        self.assertFalse(self.directory.includes("new directory/"))
        self.directory.mkDir("new directory")
        self.assertTrue(self.directory.includes("new directory/"))

    def test_is_directory(self):
        is_directory = self.directory.is_directory()
        self.assertTrue(is_directory)

    def test_remove_object_by_name_raises_a_exception_when_there_is_not_the_object(self):
        #method name too long?
        try:
            self.directory.remove_object_by_name("object name")
            self.fail("Shouldn't be a object")
        except CantFindDirectoryOrFile:
            pass

    def test_remove_object_by_name(self):
        self.directory.mkDir("new directory")
        self.assertTrue(self.directory.includes("new directory/"))
        self.directory.remove_object_by_name("new directory/")
        self.assertFalse(self.directory.includes("new directory/"))

    def test_directory_without_objects(self):
        sub_objects = self.directory.list_dir()
        self.assertTrue(len(sub_objects) == 0)

    def test_directory_with_one_object(self):
        self.directory.mkDir("new directory")
        sub_objects = self.directory.list_dir()
        self.assertTrue(len(sub_objects) == 1)

    def test_directory_with_some_objects(self):
        for i in range(10):
            self.directory.mkDir("new directory " + str(i))
        sub_objects = self.directory.list_dir()
        self.assertTrue(len(sub_objects) == 10)

    def test_add_object(self):
        mock_object = mock(GeneralFileSystemObject)
        when(mock_object).get_name().thenReturn("mock object")
        when(mock_object).get_father().thenReturn(self.directory)

        self.assertFalse(self.directory.includes(mock_object.get_name()))
        self.directory.add_object(mock_object)
        self.assertTrue(self.directory.includes(mock_object.get_name()))
        verify(mock_object).set_father(self.directory)

    def test_add_directory(self):
        other_directory = Directory("other directory")
        self.directory.add_object(other_directory)

        self.assertTrue(self.directory.includes(other_directory.get_name() + "/"))
        self.assertEqual(self.directory, other_directory.get_father())

    def test_get_directory(self):
        other_directory = Directory("other directory")
        self.directory.add_object(other_directory)
        self.assertEqual(self.directory.get_directory("other directory"), other_directory)

    def test_get_file(self):
        a_file = File("file", "No data")
        self.directory.add_object(a_file)
        self.assertEqual(self.directory.get_file("file"), a_file)

    def test_includes(self):
        other_directory = Directory("other directory")
        self.directory.add_object(other_directory)

        self.assertTrue(self.directory.includes("other directory/"))

    def test_clean(self):
        for i in range(10):
            directory = Directory("directory " + str(i))
            self.directory.add_object(directory)
        num_of_objects_before_clean = len(self.directory.list_dir())
        self.assertTrue(num_of_objects_before_clean > 0)
        self.directory.clean()
        num_of_objects_after_clean = len(self.directory.list_dir())
        self.assertTrue(num_of_objects_after_clean == 0)


suite1 = unittest.TestLoader().loadTestsFromTestCase(FileTest)
suite2 = unittest.TestLoader().loadTestsFromTestCase(DirectoryTest)

all_tests = unittest.TestSuite([suite1, suite2])
unittest.TextTestRunner(verbosity=2).run(all_tests)

__author__ = 'leandro'
