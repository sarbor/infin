import click
from click_repl import register_repl

from typing import Any

from infin import DEFAULT_API_URL, DEFAULT_REFRESH_FREQ, API_JSON_SCHEMA_FILENAME

from infin.dispacher import Dispatcher
from infin.cache import Cache
from infin.validator import Validator


@click.group()
@click.option('--api_url', default=DEFAULT_API_URL, envvar='API_URL', help='url for endpoint')
@click.option('--refresh_freq', default=DEFAULT_REFRESH_FREQ, envvar='REFRESH_FREQ', help='num seconds needed to refresh cache')
@click.option('--category_color', default='blue',  help='color to print Category text in, choose from [BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE]')
@click.option('--enabled_feature_color', default='green',  help='color to print enabled feature text in, choose from [BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE]')
@click.option('--disabled_feature_color', default='red',  help='color to print disabled feature text in, choose from [BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE]')
@click.pass_context
def main(context: Any, api_url: str, refresh_freq: float, 
   category_color: str, enabled_feature_color: str, 
   disabled_feature_color: str) -> None:
   """
   Must be run from /infin/infin
   
   Commands:
      show-all-categories: prints out all categories from API endpoint
      show-all-items: prints out each category and every item inside each category.

   Optional Args:
       --api_url (str): url for API endpoint to query
       --refresh_freq (float): # seconds before API response is invalidated
       --category_color (string): color to print Category text in, choose from [BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE]
       --enabled_feature_color (string): color to print enabled feature text in, choose from [BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE]
       --disabled_feature_color (string): color to print disabled feature text in, choose from [BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE]

   Commands:
      repl: starts an interactive shell anf caches API response data
   """   
   cache = Cache()
   validator = Validator(API_JSON_SCHEMA_FILENAME)
   dispatcher = Dispatcher(DEFAULT_API_URL, DEFAULT_REFRESH_FREQ, validator, cache)
   
   #global context is initially None
   if context.obj is None:
      context.obj = {}
   
   context.obj['enabled_feature_color'] = enabled_feature_color
   context.obj['disabled_feature_color'] = disabled_feature_color
   context.obj['category_color'] = category_color
      
   #sets dispatcher to be shared 
   if 'dispatcher' not in context.obj:
      context.obj['dispatcher'] = dispatcher


@main.command()
@click.pass_obj
def show_all_items(obj: dict) -> None:
   """Prints out each category and every item inside each category. 

   Args:
       obj (dict): Global dict object shared by CLI commands
   """   
   dispatcher = obj['dispatcher']
   category_color = obj['category_color'].lower()
   enabled_feature_color = obj['enabled_feature_color'].lower()
   disabled_feature_color = obj['disabled_feature_color'].lower()
   all_data = dispatcher.query_data([])

   for category, capabilities in all_data:
      click.echo(click.style(category, fg=category_color))

      for capability in capabilities:
         if capability.enabled:
            click.echo(click.style('\t' + capability.title, fg=enabled_feature_color))
         else:
            click.echo(click.style('\t' + capability.title, fg=disabled_feature_color))


@main.command()
@click.pass_obj
def show_all_categories(obj: dict) -> None:
   """Prints out each category from cache 

   Args:
       obj ([dict]): Global dict object shared by CLI commands
   """   
   dispatcher = obj['dispatcher']
   category_color = obj['category_color'].lower()

   catgories = dispatcher.query_data([
      lambda all_data: map(lambda data: data[0], all_data)
   ])

   for category in catgories:
      click.echo(click.style(category, fg=category_color))


#add interactive repl as a command
register_repl(main)
