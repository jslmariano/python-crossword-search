#!/usr/bin/env python

# -*- coding: utf-8 -*-

import unittest
import pprint

from WordSearch import WordSearch, WordSearchError

class ExtendedTestCase(unittest.TestCase):

  def assertRaisesWithMessage(self, msg, func, *args, **kwargs):
    """
    Assert the raised exception message

    :param      msg:     The message
    :type       msg:     string
    :param      func:    The function
    :type       func:    function
    :param      args:    The arguments
    :type       args:    list
    :param      kwargs:  The keywords arguments
    :type       kwargs:  dictionary
    """

    try:
      func(*args, **kwargs)
      self.assertFail()
    except WordSearchError as inst:
      self.assertEqual(str(inst), msg)

    def assertMultiLineEqual(self, first, second, msg=None):
        """Assert that two multi-line strings are equal.

        If they aren't, show a nice diff.

        """
        self.assertTrue(isinstance(first, str),
                'First argument is not a string')
        self.assertTrue(isinstance(second, str),
                'Second argument is not a string')

        if first != second:
            message = ''.join(difflib.ndiff(first.splitlines(True),
                                                second.splitlines(True)))
            if msg:
                message += " : " + msg
            self.fail("Multi-line strings are unequal:\n" + message)


class TestLogics(ExtendedTestCase):

    """Test the logical operations WordSearch"""

    def setUp(self):

       """This runs before the test cases are executed"""

       self.word_search = WordSearch()

    def tearDown(self):

       """This runs after the test cases are executed"""

       self.word_search = None

    def test_valid_input_output(self):
        """"""

        _file = "puzzle1.pzl"
        self.word_search.set_puzzle_file(_file)
        self.word_search.run_search()

        with open(self.word_search.get_output_path()) as f:
            lines = f.read()
            pprint.pprint(lines)
            self.assertMultiLineEqual(
                "CAT (1, 1)(1, 3)\nDOG (2, 2)(4, 2)\nCOW (2, 4)(4, 4)\n",
                lines
            )

    def test_valid_input_with_reverse(self):
        """"""

        _file = "suits.pzl"
        self.word_search.set_puzzle_file(_file)
        self.word_search.run_search()

        with open(self.word_search.get_output_path()) as f:
            lines = f.read()
            pprint.pprint(lines)
            self.assertMultiLineEqual(
                "DIAMOND (7, 1)(1, 1)\nHEART (7, 5)(5, 3)\n",
                lines
            )

    def test_valid_with_newlines(self):
        """"""

        _file = "puzzle_far_inputs.pzl"
        self.word_search.set_puzzle_file(_file)
        self.word_search.run_search()

        with open(self.word_search.get_output_path()) as f:
            lines = f.read()
            pprint.pprint(lines)
            self.assertMultiLineEqual(
                "CAT (1, 1)(1, 3)\nDOG (2, 2)(4, 2)\nCOW (2, 4)(4, 4)\n",
                lines
            )

    def test_valid_with_blank_each(self):
        """"""

        _file = "puzzle_has_blank_each_inputs.pzl"
        self.word_search.set_puzzle_file(_file)
        self.word_search.run_search()

        with open(self.word_search.get_output_path()) as f:
            lines = f.read()
            pprint.pprint(lines)
            self.assertMultiLineEqual(
                "CAT (1, 1)(1, 3)\nDOG (2, 2)(4, 2)\nCOW (2, 4)(4, 4)\n",
                lines
            )

    def test_valid_with_lost_word(self):
        """"""

        _file = "lostDuck.pzl"
        self.word_search.set_puzzle_file(_file)
        self.word_search.run_search()

        with open(self.word_search.get_output_path()) as f:
            lines = f.read()
            pprint.pprint(lines)
            self.assertMultiLineEqual(
                "CAT (1, 1)(1, 3)\nDOG (2, 2)(4, 2)\nDUCK not found\n",
                lines
            )

class TestErrors(ExtendedTestCase):

    """Test the erronous operations WordSearch"""

    def setUp(self):

       """This runs before the test cases are executed"""

       self.word_search = WordSearch()

    def tearDown(self):

       """This runs after the test cases are executed"""

       self.word_search = None


    def test_file_not_found(self):
        """"""

        no_file = "puzzle1.pzlssss"
        error = "file {} not found in puzzles directory".format(no_file)
        self.word_search.set_puzzle_file(no_file)
        self.assertRaisesWithMessage(error, self.word_search.run_search)


    def test_file_with_one_letter(self):
        """"""

        no_file = "puzzle_w_one_letter.pzl"
        error = "A should be more than 2 characters"
        self.word_search.set_puzzle_file(no_file)
        self.assertRaisesWithMessage(error, self.word_search.run_search)


    def test_file_invalid_search(self):
        """"""

        no_file = "puzzle_w_invalid_search.pzl"
        error = "@ is not a valid alphabet"
        self.word_search.set_puzzle_file(no_file)
        self.assertRaisesWithMessage(error, self.word_search.run_search)


    def test_file_invalid_crosswords(self):
        """"""

        no_file = "puzzle_w_invalid_crosswords.pzl"
        error = "CI@N is not a valid alphabet"
        self.word_search.set_puzzle_file(no_file)
        self.assertRaisesWithMessage(error, self.word_search.run_search)


    def test_file_uneven_puzzle(self):
        """"""

        no_file = "puzzle_uneven_matrix.pzl"
        error = "Puzzle file must have equal dimension (X,X)"
        self.word_search.set_puzzle_file(no_file)
        self.assertRaisesWithMessage(error, self.word_search.run_search)


def suite():

    """Test suite"""

    suite = unittest.TestSuite()
    suite.addTests(
       unittest.TestLoader().loadTestsFromTestCase(TestLogics)
    )
    suite.addTests(
       unittest.TestLoader().loadTestsFromTestCase(TestErrors)
    )
    return suite


if __name__ == "__main__":
    """
    Runs the  unittest

    """
    unittest.TextTestRunner(verbosity=2).run(suite())