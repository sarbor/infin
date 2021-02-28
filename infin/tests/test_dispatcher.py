import unittest
import json
from time import sleep
from collections import namedtuple, defaultdict

from infin import DEFAULT_API_URL, DEFAULT_REFRESH_FREQ
from infin.dispacher import Dispatcher
from infin.cache import Cache
from infin.validator import Validator

class TestDispatcher(unittest.TestCase):
   @classmethod
   def setUpClass(cls):
      with open('sample_data.json', 'r') as file:
         sample_data = json.load(file)

      cls.sample_data = sample_data
      cls.schema_filepath = 'api_schema.json'

      cls.cache = Cache()
      cls.validator = Validator(cls.schema_filepath)

      cls.ground_truth_cache = Cache()
      cls.ground_truth_cache.insert(sample_data)



   def setUp(self):
      self.dispatcher = Dispatcher(DEFAULT_API_URL, DEFAULT_REFRESH_FREQ,
                                 self.validator, self.cache)
       
   def test_should_update_cache(self):
      self.assertTrue(self.dispatcher.should_update_cache())
      self.dispatcher.update_cache()
      self.assertFalse(self.dispatcher.should_update_cache())
      sleep(DEFAULT_REFRESH_FREQ)
      self.assertTrue(self.dispatcher.should_update_cache())

   def test_update_cache(self):
      self.dispatcher.update_cache()
      self.assertDictEqual(self.ground_truth_cache.cache, self.dispatcher.cache.cache)

   def test_query_data(self):
      self.dispatcher.update_cache()
      self.assertEqual(self.dispatcher.query_data([]), self.ground_truth_cache.get_all_items())

      all_categories = self.dispatcher.query_data([
         lambda all_data: list(map(lambda data: data[0], all_data))
      ])
      ground_truth_all_categories = [category for category, _ in self.ground_truth_cache.get_all_items()]
      
      self.assertListEqual(all_categories, ground_truth_all_categories)



if __name__ == "__main__":
   unittest.main()