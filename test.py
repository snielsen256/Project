import unittest

# Import the module or functions you want to test
from app import *
from GUI import *

class TestApp(unittest.TestCase):
    def setUp(self):
        """
        This method is called before each test. Used to set up any preconditions or variables.
        """
        self.sample_data = {"key": "value"}

    def test_function(self):
        
        result = function(self.sample_data)
        expected = "expected_result"
        self.assertEqual(result, expected, "your_function did not return the expected result")

 
if __name__ == "__main__":
    unittest.main()