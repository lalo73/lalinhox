__author__ = 'leandro'

from hardware.memory import Memory,OutOfRange
import unittest
import random
from mockito import *

class MemoryTest(unittest.TestCase):

    def setUp(self):
        self.memory = Memory()

    def test_whenCreateAMemoryWithOutParamsThenItsSizeIs1024(self):
        self.assertEqual(self.memory.length(),1024)

    def test_whenCreateAMemoryWithParamItsSizeIsThanThisParam(self):
        memory = Memory(100)
        self.assertEqual(memory.length(),100)

    def test_whenTwoCellAtDifferentPositionThenTheyAreDifferentCells(self):
        cell_1 = self.memory.cellAt(0)
        cell_2 = self.memory.cellAt(1)
        cell_3 = self.memory.cellAt(1000)

        self.assertNotEqual(cell_1,cell_2)
        self.assertNotEqual(cell_1,cell_3)
        self.assertNotEqual(cell_2,cell_3)

    def test_theLastCellIsAtSizeOfMemoryMinusOne(self):
        last_cell = self.memory.cellAt(len(self.memory) - 1)
        try:
            last_cell = self.memory.cellAt(len(self.memory))
            self.fail("This cell shouldn't exist")
        except OutOfRange:
            pass

    def test_whenWriteDataOnCell(self):
        self.memory.cells[0] = mockCell = mock()
        mockData = mock()
        self.memory.write(0,mockData)
        verify(mockCell).write(mockData)
        verifyNoMoreInteractions(mockCell)

    def test_failWhenWriteOnCellWithOutOfRangeIndex(self):
        try:
            mockData = mock()
            self.memory.write(len(self.memory),mockData)
            self.fail("This cell shouldn't exist")
        except OutOfRange:
            pass

    def test_aNewMemoryHasAllItsCellReleased(self):
        memory = self.memory
        for index in range(len(memory)):
            cell = memory.cellAt(index)
            self.assertFalse(cell.isInUse())

    def test_aNewMemoryHasAnyCellReleased(self):
        cell_0 = self.memory.cellAt(0)
        cell_1 = self.memory.cellAt(1)
        cell_1000 = self.memory.cellAt(1000)
        last_cell = self.memory.cellAt(len(self.memory) - 1)
        random_index = int(random.uniform(1,len(self.memory)))
        cell_random = self.memory.cellAt(random_index)

        self.assertFalse(cell_0.isInUse())
        self.assertFalse(cell_1.isInUse())
        self.assertFalse(cell_1000.isInUse())
        self.assertFalse(last_cell.isInUse())
        self.assertFalse(cell_random.isInUse())

    def test_setOnUse(self):
        mockCell = mock()
        self.memory.cells[0] = mockCell
        self.memory.onUse(0)
        verify(mockCell).onUse()

    def test_whenSetOnUseACellThenIsInUseReturnsTrue(self):
        mockCell = mock()
        when(mockCell).isInUse().thenReturn(False).thenReturn(True)
        self.memory.cells[0] = mockCell
        self.assertFalse(self.memory.isInUse(0))
        self.memory.onUse(0)
        self.assertTrue(self.memory.isInUse(0))

    def test_whenReleaseACellThenIsOnUseReturnFalse(self):
        mockCell = mock()
        self.memory.cells[0] = mockCell
        when(mockCell).isInUse().thenReturn(False).thenReturn(False).thenReturn(True).thenReturn(False)
        initial_value = self.memory.isInUse(0)
        self.memory.free(0)
        initial_value_after_release = self.memory.isInUse(0)
        self.memory.onUse(0)
        settedAsOnUse = self.memory.isInUse(0)
        self.memory.release(0)
        final_value = self.memory.isInUse(0)

        self.assertFalse(initial_value)
        self.assertFalse(initial_value_after_release)
        self.assertTrue(settedAsOnUse)
        self.assertFalse(final_value)

    def test_theInitialDataOfAnyCellIsNone(self):
        cell_0 = self.memory.cellAt(0)
        cell_1 = self.memory.cellAt(1)
        cell_1000 = self.memory.cellAt(1000)
        last_cell = self.memory.cellAt(len(self.memory) - 1)
        random_index = int(random.uniform(1,len(self.memory)))
        cell_random = self.memory.cellAt(random_index)

        self.assertIsNone(cell_0.read())
        self.assertIsNone(cell_1.read())
        self.assertIsNone(cell_1000.read())
        self.assertIsNone(last_cell.read())
        self.assertIsNone(cell_random.read())

    def test_whenWriteADataThenReadReturnsThisData(self):
        mockCell = mock()
        mockData = mock()
        self.memory.cells[0] = mockCell
        when(mockCell).read().thenReturn(mockData)
        self.memory.write(0,mockData)
        verify(mockCell).write(mockData)
        self.assertEqual(mockData,self.memory.read(0))

suite = unittest.TestLoader().loadTestsFromTestCase(MemoryTest)
unittest.TextTestRunner(verbosity=2).run(suite)
