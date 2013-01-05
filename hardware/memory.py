__author__ = 'leandro'

class Memory:
    def __init__(self,length=1024):
        self.cells = []
        for i in range(length):
            self.cells.append(Cell())

    def __len__(self):
        return len(self.cells)

    def length(self):
        #Return the size of the memory or number of cells
        return len(self)

    def cellAt(self,index):
        #Returns the cell at position 'index'
        try:
            return self.cells[index]
        except IndexError:
            raise OutOfRange()

    def write(self,index,data):
        #Writes the 'data' in cell at position 'index'
        cell = self.cellAt(index)
        cell.write(data)

    def onUse(self,index):
        #Sets on use the cell at position 'index'
        cell = self.cellAt(index)
        cell.onUse()

    def release(self,index):
        #See 'free' method
        self.free(index)

    def free(self,index):
        #Release the cell at position 'index'
        cell = self.cellAt(index)
        cell.free()

    def read(self,index):
        #Returns the data of the cell at positioin 'index'
        cell =  self.cellAt(index)
        return cell.read()

    def isInUse(self,index):
        """
        Returns True if the cell at position 'index' has been setted as 'onUse',
          otherwise returns False
        """
        cell = self.cellAt(index)
        return cell.isInUse()

class Cell:
    def __init__(self):
        self.__inUse=False
        self.__data=None

    def isInUse(self):
        return self.__inUse

    def write(self,data):
        self.__data=data

    def read(self):
        return self.__data

    def onUse(self):
        self.__inUse=True

    def free(self):
        self.__inUse=False

#Exceptions

class OutOfRange(Exception):
    def __str__(self):
        return "there isn't a cell on this 'index'"