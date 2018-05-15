import unittest
from pyrello import pyrello

class Test(unittest.TestCase):
    """
    Test the add function from the mymath library
    """

    def test_get_labels_column_two_labels(self):
        """
        Test the transformation of a Card Json into a CSV cell with two labels
        """
        csv_line = pyrello.get_labels_column([{'name':'foo'},{'name':'bar'}])
        self.assertEqual(csv_line, "foo,bar")

    def test_get_labels_column_one_label(self):
        """
        Test the transformation of a Card Json into a CSV cell with one label
        """
        csv_line = pyrello.get_labels_column([{'name':'foo'}])
        self.assertEqual(csv_line, "foo")

    def test_get_action_value_update_card(self):
        """
        Test id and date of a status transaction 
        """
        action = {
                'id': '5af4b2536330f85803a3a229', 
                'data': {
                    'listAfter': {
                        'name':'Backlog', 
                        'id': '57683d923017347909f9b904'
                    }
                }, 
                'type': 'updateCard', 
                'date': '2018-05-10T20:57:55.692Z' 
                }
        action_dict = pyrello.get_action_value(action)
        self.assertNotEqual(action_dict, None)
        self.assertEqual(action_dict['list_id'],
                action["data"]["listAfter"]["id"])
        self.assertEqual(action_dict['date'], action["date"][:10])


if __name__ == '__main__':
    unittest.main()
