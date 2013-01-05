__author__ = 'leandro'

import unittest
from mockito import *
from hardware.memory import Cell

class TestCell(unittest.TestCase):

    def setUp(self):
        self.cell = Cell()

    def test_whenCreateANewCellItIsNotInUse(self):
        #A new cell is not in use
        self.assertFalse(self.cell.isInUse())

    def test_whenCreateANewCellItsDataIsNone(self):
        #The data of a new cell is None
        self.assertIsNone(self.cell.read())

    def test_whenWriteDataThenTheCurrentDataIsReplaced(self):
        #When write data on a cell the previous data is replaced
        mockData = mock()
        initialData = self.cell.read()

        self.cell.write(mockData)
        finalData = self.cell.read()

        self.assertNotEqual(initialData,finalData)
        self.assertEqual(mockData,finalData)

    def test_whenSetOnUseThenIsInUseReturnsTrue(self):
        #When a cell is setted as on use, then isInUse method returns True
        self.cell.onUse()

        self.assertTrue(self.cell.isInUse())

    def test_WhenSetFreeThenIsInUseReturnsFalse(self):
        #When a cell is setted as free, then isInUse method returns False
        self.cell.free()

        self.assertFalse(self.cell.isInUse())

suite = unittest.TestLoader().loadTestsFromTestCase(TestCell)
unittest.TextTestRunner(verbosity=2).run(suite)
