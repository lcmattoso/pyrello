import unittest
from pyrello import pyrello

class Test(unittest.TestCase):
    """
    Test the add function from the mymath library
    """

    def test_get_labels_collumn_two_labels(self):
        """
        Test the transformation of a Card Json into a CSV cell with two labels
        """
        csv_line = pyrello.get_labels_collumn([{'name':'foo'},{'name':'bar'}])
        self.assertEqual(csv_line, "foo,bar")

    def test_get_labels_collumn_one_label(self):
        """
        Test the transformation of a Card Json into a CSV cell with one label
        """
        csv_line = pyrello.get_labels_collumn([{'name':'foo'}])
        self.assertEqual(csv_line, "foo")

if __name__ == '__main__':
    unittest.main()
