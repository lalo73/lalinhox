__author__ = 'leandro'

class Memory:
    def __init__(self,length=1024):
        self.cells = []
        for i in length:
            self.cells.append(Cell())

    def length(self):
        return len(self.cells)

    def write(self,index,data):
        cell = self.cells[index]
        cell.write(data)
        cell.onUse()

    def read(self,index):
        cell =  self.cells[index]
        return cell.read()

    def isInUse(self,index):
        cell = self.cells[index]
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

