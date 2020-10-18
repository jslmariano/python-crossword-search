#!/usr/bin/env python

# -*- coding: utf-8 -*-

import sys
import os
import pprint
from puzzle import CrossWords, Search
dir_path = os.path.dirname(os.path.realpath(__file__))

class WordSearchError(Exception):
    """
    This class describes a word search error.
    """
    pass

class WordSearch(object):
    """
    This class describes a word search.

    Accepts a string as file path for the puzzle file and extract coordinates
    from it as results
    """

    def __init__(self):
        """
        Constructs a new instance.
        """

        self.puzzle_file = None
        self.result = None
        self.outputs_directory = "outputs"
        self.input_directory = "puzzles"
        self.puzzles = []
        self.searches = []
        self.crosswords = CrossWords()

    def set_puzzle_file(self, puzzle_file):
        """
        Sets the puzzle file.

        :param      puzzle_file:  The puzzle file
        :type       puzzle_file:  string
        """

        self.puzzle_file = puzzle_file;
        return self

    def run_search(self):
        """
        Run the search for words based on the puzzle file and output it to the
        outputs directory
        """

        self.read_puzzle_file()
        self.build_puzzle()
        self.build_searches()
        self.begin_search()
        self.output_result()

        return self

    def read_puzzle_file(self):
        """
        Reads a puzzle file.

        :raises     WordSearchError:  If puzzle file is missing
        """

        found_new_line = False
        found_string = False
        puzzle_path = '{}/{}'.format(self.input_directory, self.puzzle_file)

        if not os.path.exists(puzzle_path):
            raise WordSearchError("file {} not found in {} directory".format(
                self.puzzle_file, self.input_directory
            ))

        with open(puzzle_path, 'r') as reader:
            for line in reader.readlines():
                # Ignore the first new lines
                line = line.rstrip()
                if not line and not found_string:
                    continue
                else:
                    found_string = True

                if not line:
                    # Lock the first new line
                    found_new_line = True
                    continue

                if found_new_line:
                    """
                    While storing word needs to be searched, also ignores whitespaces
                    """
                    self.validate_line(line)
                    self.searches.append(line)
                else:
                    self.validate_line(line)
                    self.puzzles.append(line)

        return self

    def validate_line(self, word):
        """
        Validate Line

        :param      word:             The word
        :type       word:             string

        :raises     WordSearchError:  If the line is not valid alphabet or is
                                      one charcter only
        """

        if not str(word).isalpha():
            raise WordSearchError("{} is not a valid alphabet".format(word))
        if len(word) <= 1:
            raise WordSearchError("{} should be more than 2 characters".format(word))

        return self


    def build_puzzle(self):
        """
        Builds a puzzle.

        :raises     WordSearchError:  If no puzzle, or puzzle has incorrect
                                      dimension
        """

        if not len(self.puzzles):
            raise WordSearchError("There are no puzzles found in puzzle file")

        for row in self.puzzles:
            self.crosswords.add_row(row)

        self.crosswords.init_puzzle()

        if not self.crosswords.grid.is_dimension_valid():
            raise WordSearchError("Puzzle file must have equal dimension (X,X)")

        self._print("Puzzle Preview:")
        if not self.is_unittest_running():
            self.crosswords.preview_grid(1)

        return self

    def build_searches(self):
        """
        Builds searches.

        :raises     WordSearchError:  If there are no searches
        """

        if not len(self.searches):
            raise WordSearchError("There are no words to search found in puzzle file")

        self._print("Words to search:")
        for word in self.searches:
            self._print(word)
            self.crosswords.add_searches(word)

        return self

    def begin_search(self):
        """
        Begins a search.
        """

        for search in self.crosswords.get_searches():
            if not self.crosswords.is_in_puzzle(search):
                continue
            self.crosswords.sync_pointer(search)
            search.create_coordinates()

        return self

    def get_output_path(self):
        """
        Gets the output path.

        :returns:   The output path.
        :rtype:     string
        """

        input_file = self.puzzle_file
        input_file_name = os.path.splitext(input_file)
        output_path = '{}/{}.out'.format(self.outputs_directory, input_file_name[0])

        return output_path

    def output_result(self):
        """
        Output the result in output directory
        """

        output_path = self.get_output_path()
        with open(output_path, 'w') as output_file:
            for search in self.crosswords.get_searches():
                line = '{} {}\n'.format(search.word, 'not found')
                if search.was_found:
                    line = '{} {}\n'.format(
                        search.word, search.print_coordinates(1)
                    )
                output_file.write(line)

            self._print("Output file: {}".format(output_path))

    def _print(self, message):
        """
        Prints the message

        :param      message:  The message
        :type       message:  string
        """

        """Disable outut in unittest"""
        if not self.is_unittest_running():
            print(message)

    def is_unittest_running(self):
        """
        Determines if unittest running.

        :returns:   True if unittest running, False otherwise.
        :rtype:     boolean
        """

        return 'unittest' in sys.modules.keys()

if __name__ == "__main__":

    """Run as a script"""

    if len(sys.argv) <= 1:
        print("Missing puzzle file as first argument")
        print("EG: python WordSearch.py puzzle1.pzl")
        exit()

    try:
        word_search = WordSearch();
        word_search.set_puzzle_file(sys.argv[1]);
        word_search.run_search();
        print("\n")
        print("Done searching please see directory outputs")
    except Exception as e:
        print("\n")
        print("Problem running word search error : " + str(e))
    finally:
        print("\n")
        print("Done running word search")
