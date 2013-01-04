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
        self.inUse=False
        self.data=None

    def isInUse(self):
        return self.inUse

    def write(self,data):
        self.data=data

    def read(self):
        return self.data

    def onUse(self):
        self.inUse=True

    def free(self):
        self.inUse=False

