import requests
import time 
from typing import Any, Callable, Iterable

from infin.validator import Validator
from infin.cache import Cache

class Dispatcher:
   def __init__(self, api_url: str, refresh_freq: float, 
                  validator: Validator, cache: Cache) -> None:
      """Class for validating, caching, and querying the response from an API endpoint 

      Args:
          api_url (str): url of API endpoint to request data from
          refresh_freq (float): Max amount of secs before cache is invalidated
          validator (Validator): Validator for API endpoint response
          cache (Cache): Cache for storing API endpoint response
      """                  
      self.cache = cache
      self.api_url = api_url
      self.refresh_freq = refresh_freq
      self.validator = validator
      self.cache_last_updated = None

   def update_cache(self) -> None:
      """
      updates the cache if cache is invalidated by fetching response from API endpoint
      """      
      response = requests.get(self.api_url) 
      if response.status_code == 200:
         data = response.json()
         if self.validator.validate(data):
            self.cache.insert(data)

      self.cache_last_updated = time.perf_counter()

   def should_update_cache(self) -> bool:
      """Returns whether cache is invalidated

      Returns:
          bool: True if cache is invalidated, False otherwise
      """      
      if self.cache_last_updated is not None:
         return(time.perf_counter() - self.cache_last_updated > self.refresh_freq)

      return True

   def query_data(self, transformation_funcs: Iterable[Callable]) -> Any:
      """Provides an API for querying data from the cache by chaining the results of given functions

      Args:
          transformation_funcs (Iterable[Callable]): Iterable of chained functions that ultimately return a dersire query

      Returns:
          Any: Up to the caller to decide what to return
      """
      
      if self.should_update_cache():
         self.update_cache()

      data = self.cache.get_all_items()

      for func in transformation_funcs:
         data = func(data)

      return data

      
      

     



