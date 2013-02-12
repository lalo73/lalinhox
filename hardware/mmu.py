from hardware.fileSystem import HardDisk


class ContiguousAllocation(object):
    def num_page_for(self, instructions):
        return 1

    def max_block_len(self, instructions):
        return len(instructions)

    def there_is_space_for(self, mmu, instructions):
        pass

    def get_base_for_instructions(self, instructions, mmu):
        memory = mmu.get_memory()
        counting = False
        instructions_length = len(instructions)
        current_block_length = 0
        current_base = None
        current_index = 0
        while current_block_length < instructions_length:
            if memory.is_in_use(current_index):
                counting = False
                current_base = None
                current_block_length = 0
            else:
                if not counting:
                    counting = True
                    current_base = current_index
                current_block_length += 1
            current_index += 1
        return current_base


class Pagination(object):
    def __init__(self, max_block_len=15):
        self.max_block_len = max_block_len

    def num_page_for(self, instructions):
        num_instructions = len(instructions)
        num_pages = num_instructions / self.max_block_len
        if num_instructions % self.max_block_len > 0:
            num_pages += 1
        return num_pages

    def max_block_len(self, instructions):
        return self.max_block_len


class MMU(object):
    def __init__(self, memory, hardDisk=HardDisk(), strategy=ContiguousAllocation(), swapped_location="/mmu_files/"):
        self.__memory = memory
        self.__pageTable = PageTable()
        self.__hardDisk = hardDisk
        self.__strategy = strategy
        self.__swapped_location = swapped_location
        hardDisk.mkDirectory(swapped_location)

    def get_memory(self):
        return self.__memory

    def get_hardDisk(self):
        return self.__hardDisk

    def swapped_instructions_location(self):
        return self.__swapped_location

    def page_specifications(self, instructions):
        num_pages = self.num_page_for(instructions)
        max_block_len = self.max_block_len(instructions)
        return num_pages, max_block_len

    def num_page_for(self, instructions):
        return self.__strategy.num_page_for(instructions)

    def max_block_len(self, instructions):
        return self.__strategy.max_block_len(instructions)

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

    def there_is_space_for(self, instructions):
        return self.__strategy.there_is_space_for(instructions, self)

    def get_base_for_instructions(self, instructions):
        return self.__strategy.get_base_for_instructions(instructions, self)

    def write_in_memory_or_swap(self, instructions, page, page_number, aPCB):
        if self.there_is_space_for(instructions):
            base = self.get_base_for_instructions(instructions)
            memory = self.__memory
            count = 0
            for instruction in instructions:
                memory.write(base + count, instruction)
                count += 1
            page.set_base(base)
            page.set_length(len(instructions))
            page.unswap()
        else:
            disk = self.__hardDisk
            swapped_instructions_path = self.swapped_instructions_location()
            pcb_directory_path = swapped_instructions_path + str(aPCB.get_id()) + "/"
            if not disk.exist(pcb_directory_path):
                disk.mkDirectory(pcb_directory_path)

            file_name = str(page_number)
            file_path = pcb_directory_path + file_name
            disk.mkFile(file_path, instructions)
            page.swap()

    def add_PCB(self, aPCB):
        #Getting the instructions
        program_path = aPCB.get_path()
        program = self.get_program_from_disk(program_path)
        instructions = program.get_instructions()

        table_entry = self.__pageTable.create_page_entry(aPCB)
        num_of_pages, max_block_len = self.page_specifications(instructions)

        #Separate in blocks of size "max_block_len" as max length
        blocked_instructions = self.paginate_instructions(instructions, max_block_len, num_of_pages)
        for page_number in range(num_of_pages):
            instructions_to_memory = blocked_instructions[num_of_pages]
            page = table_entry.create_page(page_number, 0, len(instructions_to_memory))
            self.write_in_memory_or_swap(instructions_to_memory, page, page_number, aPCB)

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
        self.__swapped = True

    def unswap(self):
        self.__swapped = False


__author__ = 'lgomez'