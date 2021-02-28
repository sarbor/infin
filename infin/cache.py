from collections import defaultdict, namedtuple
from typing import Iterable, Tuple

class Cache:
   def __init__(self) -> None:
      """
      Class for generating map from category to all items within category
      """      
      self.cache = defaultdict(set)
      self.named_tuple_from_dict = None

   def insert(self, data: Iterable[dict]) -> None:
      """Creates map from category to all items within categories from iterable of JSON data

      Args:
          data (Iterable[dict]): Iterable of JSON data conforming to us-central1-infinitus-interviews.cloudfunctions.net/take-home-b response
      """
      if not len(data):
         return

      #Converts JSON data from dict to named tuple so data is hashable.
      self.named_tuple_from_dict = namedtuple('Capability', data[0].keys())

      for item in data:
         category = item['category']
         item = self.named_tuple_from_dict(**item)
         self.cache[category].add(item)

   def get_all_items(self) -> Iterable[Tuple[str, set]]:
      """Returns an iterab;e of tuples with a category and a set of all items within that category. Items are named tuples instead of dicts.

      Returns:
          Iterable[Tuple[str, set]]: Iterable of tuples in the form of (category, set([all items within category]))
      """      
      return self.cache.items()

   
