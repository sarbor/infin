import json
from typing import Any, Iterable
import jsonschema

class Validator:
   def __init__(self, schema_filename: str) -> None:
      """A class for validating whether given JSON data conforms to a given schema

      Args:
          schema_filename (str): path of file containing json schema
      """      
      self.schema = self.get_schema(schema_filename)

   def get_schema(self, schema_filename: str) -> Any:
      """Loads the JSON schema from a filename and returns it

      Args:
          schema_filename (str): path of file containing json schema

      Returns:
          Any: JSON schema from provided file
      """      
      with open(schema_filename, 'r') as file:
        schema = json.load(file)

      return schema

   def validate(self, all_json_data: Iterable[dict]) -> bool:
      """Returns whether an iterable of dicts conforms to the Validator's schema

      Args:
          all_json_data (Iterable[dict]): Iterable of dictionaries conforming to Validator's schema

      Returns:
          bool: True if all items in all_json_data conform to schema, False otherwise
      """      
      try:
         for data in all_json_data:
            jsonschema.validate(instance=data, schema=self.schema)
         return True
      except jsonschema.exceptions.ValidationError as err:
         return False

      

   

