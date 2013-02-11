class ContiguousAllocation(object):
    def __init__(self, max_block_len=15):
        self.max_block_len = max_block_len

    def num_page_for(self, aPCB, instructions):
        return 1

    def max_block_len(self, aPCB, instructions):
        return self.max_block_len


class MMU(object):
    def __init__(self, memory, hardDisk, strategy=ContiguousAllocation(10)):
        self.__memory = memory
        self.__pageTable = PageTable()
        self.__hardDisk = hardDisk
        self.__strategy = strategy

    def page_specifications(self, aPCB, instructions):
        num_pages = self.num_page_for(aPCB, instructions)
        max_block_len = self.max_block_len(aPCB, instructions)
        return num_pages, max_block_len

    def num_page_for(self, aPCB, instructions):
        return self.__strategy.num_page_for(aPCB, instructions)

    def max_block_len(self, aPCB, instructions):
        return self.__strategy.max_block_len(aPCB, instructions)

    def get_disk(self):
        return self.__hardDisk

    def get_program_from_disk(self, program_path):
        disk = self.get_disk()
        program_file = disk.getObjectByPath(program_path)
        program = program_file.get_data()
        return program

    def paginate_instructions(self, instructions, max_block_len, num_pages):
        instructions_copy = instructions[:]
        paginated_instructions = []
        for num_page in range(num_pages):
            paginated_instructions.append(instructions_copy[:max_block_len])
            instructions_copy = instructions_copy[max_block_len:]
        return paginated_instructions

    def write_in_memory_or_swap(self, instructions, page):
        #TODO: Implement this!!
        pass

    def add_PCB(self, aPCB):
        #Getting the instructions
        program_path = aPCB.get_path()
        program = self.get_program_from_disk(program_path)
        instructions = program.get_instructions()

        table_entry = self.__pageTable.create_page_entry(aPCB)
        num_of_pages, max_block_len = self.page_specifications(aPCB, instructions)

        #Separate in blocks of size "max_block_len" as max length
        blocked_instructions = self.paginate_instructions(instructions, max_block_len, num_of_pages)
        for page_number in range(num_of_pages):
            instructions_to_memory = blocked_instructions[num_of_pages]
            page = table_entry.create_page(page_number, 0, len(instructions_to_memory))
            self.write_in_memory_or_swap(instructions_to_memory, page)

    #TODO: implement "get_instruction(aPCB,pc)" and "get_index_(aPCB,pc)"


class PageTable:
    def __init__(self):
        self.__pages_entries = {}

    def create_page_entry(self, aPCB):
        table_entry = TableEntry()
        self.__pages_entries[aPCB] = table_entry
        return table_entry

    def get_table_entry(self, aPCB):
        table_entry = self.__pages_entries[aPCB]
        return table_entry

    def create_page(self, aPCB, page_number, base=0, length=0, swapped=True):
        table_entry = self.get_table_entry(aPCB)
        table_entry.create_page(page_number, base, length, swapped)

    def get_page(self, aPCB, page_number):
        table_entry = self.get_table_entry(aPCB)
        return table_entry.get_page(page_number)

    def set_base(self, aPCB, page_number, new_base):
        page = self.get_page(aPCB, page_number)
        page.set_base(new_base)

    def get_base(self, aPCB, page_number):
        page = self.get_page(aPCB, page_number)
        return page.get_base()

    def set_length(self, aPCB, page_number, new_length):
        page = self.get_page(aPCB, page_number)
        page.set_length(new_length)

    def get_length(self, aPCB, page_number):
        page = self.get_page(aPCB, page_number)
        return page.get_length()

    def swap(self, aPCB, page_number):
        page = self.get_page(aPCB, page_number)
        page.swap()

    def unswap(self, aPCB, page_number):
        page = self.get_page(aPCB, page_number)
        page.unswap()

    def is_swapped(self, aPCB, page_number):
        page = self.get_page(aPCB, page_number)
        return page.is_swapped()


class DoesntExistPage(Exception):
    def __str__(self):
        return "The page doesn't exist"


class TableEntry:
    def __init__(self):
        self.__pages = {}

    def create_page(self, page_number, base=0, length=0, swapped=True):
        page = Page(base, length, swapped)
        self.__pages[page_number] = page
        return page

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