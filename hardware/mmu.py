class MMU:
    def __init__(self, memory, hardDisk):
        self.__memory = memory
        self.__pageTable = PageTable()
        self.__hardDisk = hardDisk

    def add_PCB(self, aPCB):
        pass


class PageTable:
    def __init__(self):
        self.__pages_entries = {}

    def create_page_entry(self, aPCB):
        self.__pages_entries[aPCB] = TableEntry()

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