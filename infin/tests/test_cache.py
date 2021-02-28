import unittest
import json

from infin.cache import Cache
from collections import defaultdict, namedtuple

class TestCache(unittest.TestCase):
   @classmethod
   def setUpClass(cls):
      cls.ground_truth_cache = defaultdict(set)

      with open('sample_data.json', 'r') as file:
         sample_data = json.load(file)
      
      cls.sample_data = sample_data
      Capability = namedtuple('Capability', sample_data[0].keys())

      for data in sample_data:
         category = data['category']
         capability = Capability(**data)
         cls.ground_truth_cache[category].add(capability)
      

   def test_insert(self):
      cache = Cache()
      cache.insert(self.sample_data)
      self.assertDictEqual(self.ground_truth_cache, cache.cache)
   
   def test_all_items(self):
      cache = Cache()
      cache.insert(self.sample_data)
      self.assertListEqual(list(self.ground_truth_cache.items()), list(cache.cache.items()))



if __name__ == "__main__":
   unittest.main()


   

