__author__ = 'lgomez'

class MMU:
    def __init__(self, memory, hardDisk):
        self.__memory = memory
        self.__pageTable = PageTable()
        self.__hardDisk = hardDisk

    def addPCB(self, aPCB):
        program_path = aPCB.path
        program = self.getProgram(program_path)
        instructions = program.instructions
        self.saveInstructions(aPCB, instructions)

    def getProgram(self, program_path):
        disk = self.__hardDisk
        program = disk.getObjectByPath(program_path)
        return program

    def getMemory(self):
        return self.__memory

    def getInstruction(self, aPCB, pc):
        pass

    def saveInstruction(self, aPCB, instructions):
        program_length = len(instructions)
        self.createTableEntry(aPCB,program_length)
        self.writeInstructions(aPCB,instructions)

    def createTableEntry(self,aPCB,program_length):
        strategy = self.strategy()
        strategy.createTableEntry(aPCB,program_length)


class contiguousAllocation:
    def saveInstructions(self, aPCB, instructions, mmu):
        necessary_length_block = len(instructions)


class PageTable:
    def __init__(self):
        self.__pages_entries = {}

    def createEmptyPageEntry(self, aPCB, numberOfPages):
        self.__pages_entries[aPCB] = TableEntry()
        #TODO:

    def removePageEntry(self, aPCB):
        del(self.__pages_entries[aPCB])

    def getMemoryIndex(self, aPCB, aPC):
        pass


class TableEntry:
    def __init__(self):
        self.__pages = {}

    def createPage(self, page_number,base=0,length=0,swapped=True):
        self.__pages[page_number] = Page(base,length,swapped)

class Page:
    def __init__(self,base=0,length=0,swapped=True):
        self.__base = base
        self.__length = length
        self.__swapped =swapped

    def base(self):
        return self.__base

    def length(self):
        return self.__length

    def swapped(self):
        return self.__swapped

    def setBase(self,new_base):
        self.__base = new_base

    def setLength(self,new_length):
        self.__length = new_length

    def swap(self):
        self.__swapped= True

    def unswap(self):
        self.__swapped = False