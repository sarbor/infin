import unittest
import json

from infin.validator import Validator

class TestValidator(unittest.TestCase):
   @classmethod
   def setUpClass(cls):
      with open('sample_data.json', 'r') as file:
         sample_data = json.load(file)
      
      cls.sample_data = sample_data
      cls.schema_filepath = 'api_schema.json'

   def test_get_schema(self):
      with open(self.schema_filepath, 'r') as file:
         ground_truth_schema = json.load(file)

      test_schema = Validator(self.schema_filepath).schema
      self.assertEqual(ground_truth_schema, test_schema)

   def test_validate(self):
      validator = Validator(self.schema_filepath)
      self.assertTrue(validator.validate(self.sample_data))


if __name__ == "__main__":
   unittest.main()
      