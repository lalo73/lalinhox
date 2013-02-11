class MMU:
    def __init__(self, memory, hardDisk):
        self.__memory = memory
        self.__pageTable = PageTable()
        self.__hardDisk = hardDisk

    def add_PCB(self, aPCB):
        program_path = aPCB.path
        program = self.get_program(program_path)
        instructions = program.instructions
        self.save_instructions(aPCB, instructions)

    def get_program(self, program_path):
        disk = self.__hardDisk
        program = disk.getObjectByPath(program_path)
        return program

    def get_memory(self):
        return self.__memory

    def get_instruction(self, aPCB, pc):
        pass

    def save_instruction(self, aPCB, instructions):
        program_length = len(instructions)
        self.create_table_entry(aPCB, program_length)
        self.write_instructions(aPCB, instructions)

    def create_tableEntry(self, aPCB, program_length):
        strategy = self.strategy()
        strategy.createTableEntry(aPCB, program_length)


class contiguousAllocation:
    def save_instructions(self, aPCB, instructions, mmu):
        necessary_length_block = len(instructions)


class PageTable:
    def __init__(self):
        self.__pages_entries = {}

    


class DoesntExistPage(Exception):
    def __str__(self):
        return "The page doesn't exist"


class TableEntry:
    def __init__(self):
        self.__pages = {}

    def create_page(self, page_number, base=0, length=0, swapped=True):
        self.__pages[page_number] = Page(base, length, swapped)

    def get_page(self, page_number):
        try:
            page = self.__pages[page_number]
            return page
        except KeyError:
            raise DoesntExistPage()

    def set_base(self, page_number, new_base):
        page = self.get_page(page_number)
        page.set_base(new_base)

    def get_base(self, page_number):
        page = self.get_page(page_number)
        return page.get_base()

    def get_length(self, page_number):
        page = self.get_page(page_number)
        return page.length()

    def set_length(self, page_number, new_length):
        page = self.get_page(page_number)
        page.set_length(new_length)

    def is_swapped(self, page_number):
        page = self.get_page(page_number)
        return page.is_swapped()

    def swap(self, page_number):
        page = self.get_page(page_number)
        page.swap()

    def unswap(self, page_number):
        page = self.get_page(page_number)
        page.unswap()


class AlreadySwappedPageException(Exception):
    def __str__(self):
        return "This page is already swapped"


class AlreadyUnswappedPageException(Exception):
    def __str__(self):
        return "This page is already unswapped"


class Page:
    def __init__(self, base=0, length=0, swapped=True):
        self.__base = base
        self.__length = length
        self.__swapped = swapped

    def __len__(self):
        return self.__length

    def set_length(self, new_length):
        self.__length = new_length

    def length(self):
        return self.__length

    def get_base(self):
        return self.__base

    def set_base(self, new_base):
        self.__base = new_base

    def is_swapped(self):
        return self.__swapped

    def swap(self):
        if self.is_swapped():
            raise AlreadySwappedPageException()
        self.__swapped = True

    def unswap(self):
        if not self.is_swapped():
            raise AlreadyUnswappedPageException()
        self.__swapped = False


__author__ = 'lgomez'