__author__ = 'leandro'


class Memory:
    def __init__(self, length=1024):
        self.cells = []
        for i in range(length):
            self.cells.append(Cell())

    def __len__(self):
        return len(self.cells)

    def length(self):
        #Return the size of the memory or number of cells
        return len(self)

    def cell_at(self, index):
        #Returns the cell at position 'index'
        try:
            return self.cells[index]
        except IndexError:
            raise OutOfRange()

    def write(self, index, data):
        #Writes the 'data' in cell at position 'index'
        cell = self.cell_at(index)
        cell.write(data)

    def set_in_use(self, index):
        #Sets on use the cell at position 'index'
        cell = self.cell_at(index)
        cell.set_in_use()

    def release(self, index):
        #See 'free' method
        self.free(index)

    def free(self, index):
        #Release the cell at position 'index'
        cell = self.cell_at(index)
        cell.free()

    def read(self, index):
        #Returns the data of the cell at position 'index'
        cell = self.cell_at(index)
        return cell.read()

    def is_in_use(self, index):
        """
        Returns True if the cell at position 'index' has been set as 'in_use',
          otherwise returns False
        """
        cell = self.cell_at(index)
        return cell.is_in_use()


class Cell:
    def __init__(self):
        self.__in_use = False
        self.__data = None

    def is_in_use(self):
        return self.__in_use

    def write(self, data):
        self.__data = data

    def read(self):
        return self.__data

    def set_in_use(self):
        self.__in_use = True

    def free(self):
        self.__in_use = False

#Exceptions

class OutOfRange(Exception):
    def __str__(self):
        return "there isn't a cell on this 'index'"