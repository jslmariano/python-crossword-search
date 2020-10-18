#!/usr/bin/env python

# -*- coding: utf-8 -*-

class Grid:
    """
    This class describes a grid.
    """

    def __init__(self):
        """
        Constructs a new instance.
        """

        self.cells = []
        self.rows = []
        self.horizontals = []
        self.verticals = []
        self.row_count = 0;
        self.row_max_count = 0;
        self.column_count = 0;
        self.column_max_count = 0;

    def add_row(self, row):
        """
        Adds a row.

        :param      row:  The row
        :type       row:  string
        """

        self.rows.append(str(row).upper())
        if self.row_max_count < len(self.rows):
            self.row_max_count = len(self.rows)
        if self.column_max_count < len(row):
            self.column_max_count = len(row)
        return self

    def is_dimension_valid(self):
        """
        Determines if dimension valid.

        :returns:   True if dimension valid, False otherwise.
        :rtype:     boolean
        """

        if self.column_max_count != self.row_max_count:
            return False
        for row in self.rows:
            if len(row) != self.column_max_count:
                return False
        return True

    def generate_cells(self):
        """
        Generates the cell in 2D array
        """

        self.cells = [[letters for letters in rows] for rows in self.rows]
        return self

    def generate_horizontals(self):
        """
        Generate all horizontal string in the grid
        """

        self.horizontals = self.rows
        return self

    def generate_verticals(self):
        """
        Generate all verticals string in the grid
        """

        vertical_string = ""
        for column in range(0, self.column_max_count):
            vertical_string = ""
            for row in range(0, self.row_max_count):
                try:
                    vertical_string = vertical_string + self.cells[row][column]
                except IndexError:
                    vertical_string = vertical_string + ''
            self.verticals.append(vertical_string)
        return self

class Search:
    """
    This class describes a search.
    """

    BY_ROW    = "BY_ROW"
    BY_COLUMN = "BY_COLUMN"

    def __init__(self, word):
        """
        Constructs a new instance.

        :param      word:  The word
        :type       word:  string
        """

        self.word = str(word).upper()
        self.start_coord = None
        self.end_coord = None
        self.was_found = False
        self.found_by = None
        self.is_reverse = False
        self.current_index = 0
        self.pointer = None
        self.coordinates = None

    def create_coordinates(self):
        """
        Creates coordinates.
        """

        padding = len(self.word) - 1

        if self.found_by == Search.BY_COLUMN:
            if self.is_reverse:
                self.start_coord = (self.current_index, self.pointer)
                self.end_coord = (self.pointer + padding, self.current_index)
            else:
                self.start_coord = (self.pointer, self.current_index)
                self.end_coord = (self.current_index, self.pointer + padding)

        if self.found_by == Search.BY_ROW:
            self.start_coord = (self.pointer, self.current_index)
            self.end_coord = (self.pointer + padding, self.current_index)

        self.coordinates = (self.start_coord, self.end_coord)

        if self.is_reverse:
            self.coordinates = (self.end_coord, self.start_coord)
            pass

        return self.coordinates

    def print_coordinates(self, padding = 0):
        """
        Prints coordinates.

        :param      padding:  The padding
        :type       padding:  number
        """

        _from = (self.coordinates[0][0] + padding, self.coordinates[0][1] + padding)
        _to = (self.coordinates[1][0] + padding, self.coordinates[1][1] + padding)
        return '{}{}'.format(_from, _to)

class CrossWords:
    """
    This class describes cross words.
    """

    def __init__(self):
        """
        Constructs a new instance.
        """

        self.searches = []
        self.grid = Grid()
        self.has_result = False

    def add_row(self, row):
        """
        Adds a row.

        :param      row:  The row
        :type       row:  string
        """

        self.grid.add_row(row)
        self.grid.generate_horizontals()
        return self

    def init_puzzle(self):
        """
        Initializes the puzzle.
        """

        self.grid.generate_cells()
        self.grid.generate_verticals()
        return self

    def add_searches(self, word):
        """
        Adds searches.

        :param      word:  The word
        :type       word:  string
        """

        self.searches.append(Search(word))
        return self

    def get_searches(self):
        """
        Gets the searches.

        :returns:   The searches.
        :rtype:     list
        """

        return self.searches

    def is_in_puzzle(self, search):
        """
        Determines whether the specified search is in puzzle.

        :param      search:  The search
        :type       search:  string

        :returns:   True if the specified search is in puzzle, False otherwise.
        :rtype:     boolean
        """

        found = False

        # search in rows
        found = self.is_in_grid(search, self.grid.horizontals)
        if found:
            search.found_by = Search.BY_ROW
            return True

        # search in colmns
        found = self.is_in_grid(search, self.grid.verticals)
        if found:
            search.found_by = Search.BY_COLUMN
            return True

        return False

    def is_in_grid(self, search, straights):
        """
        Determines if in grid.

        :param      search:     The search
        :type       search:     Search
        :param      straights:  The straights
        :type       straights:  string

        :returns:   True if in grid, False otherwise.
        :rtype:     boolean
        """

        for index, straight in enumerate(straights):
            if search.word in straight or search.word[::-1] in straight:
                search.current_index = index
                search.was_found = True
                if search.word[::-1] in straight:
                    search.is_reverse = True
                return True
        return False

    def sync_pointer(self, search):
        """
        Sync the pointer position

        :param      search:  The search
        :type       search:  Search
        """

        pointer = None
        match = ''
        word = search.word

        if search.found_by == Search.BY_ROW:
            match = self.grid.horizontals[search.current_index]

        if search.found_by == Search.BY_COLUMN:
            match = self.grid.verticals[search.current_index]

        if search.is_reverse:
            word = word[::-1]

        search.pointer = match.find(word)
        self.has_result = True
        return self

    def preview_grid(self, padding = 0):
        """
        Prints out the puzzle grid

        :param      padding:  The padding for X/Y axis
        :type       padding:  number
        """

        row_guide = "  ".join([ str(num + padding) for num in range(0, self.grid.row_max_count) ])
        print("\n     " + row_guide + "\n")
        for r in range(0, self.grid.row_max_count):
            print("{0}   ".format(r + padding), end='')
            for c in range(0, self.grid.column_max_count):
                print(" %c " % self.grid.cells[r][c], end='')
            print()
        print()
