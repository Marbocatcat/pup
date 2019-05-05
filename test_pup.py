#!/usr/bin/python3

import unittest

from pup import pup


class PupTestCase(unittest.TestCase):

    def test_check_upgrade(self):
        self.assertTrue(pup.check_upgrade())


if __name__ == "__main__":
    unittest.main()
