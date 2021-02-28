# Infin Design Document

# Background:

 Infin is a CLI for displaying the capabilties of an AI system via the https://us-central1-infinitus-interviews.cloudfunctions.net/take-home-b API endpoint
 

#  Installation:
    $ git clone https://github.com/sarbor/infin.git
    $ cd infin
    $ pip3 install .
    $ cd infin #very important!!!
    $ infin --help


**Important: Must be within Infin/infin in order for commands to work**


# Example Usage
****![](https://paper-attachments.dropbox.com/s_D8BCB78957EDFA4D411B34A9B88F82D40454B23D240466C7E2278098725EE2F0_1614550491012_Screen+Shot+2021-02-28+at+2.14.47+PM.png)

![](https://paper-attachments.dropbox.com/s_D8BCB78957EDFA4D411B34A9B88F82D40454B23D240466C7E2278098725EE2F0_1614550635603_Screen+Shot+2021-02-28+at+2.17.12+PM.png)



# CLI Commands
- show-all-categories
    -  *prints out all categories from API endpoint*
    - Optional Args
        - *--api_url (str): url for API endpoint to query*
        - *--refresh_freq (float): # seconds before API response is invalidated*
        - *--category_color (string): color to print Category text in, choose from [BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE]*
        - *--enabled_feature_color (string): color to print enabled feature text in, choose from [BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE]*
        - *--disabled_feature_color (string): color to print disabled feature text in, choose from [BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE]*
- *show-all-items*
    - *prints out each category and every item inside each category.*
    - Optional Args
        - *--api_url (str): url for API endpoint to query*
        - *--refresh_freq (float): # seconds before API response is invalidated*
        - *--category_color (string): color to print Category text in, choose from [BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE]*
        - *--enabled_feature_color (string): color to print enabled feature text in, choose from [BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE]*
        - *--disabled_feature_color (string): color to print disabled feature text in, choose from [BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE]*
- repl
    - *starts an interactive shell anf caches API response data*

  **

# Design Tenets
## Fast Iteration Speed
    - Creating the fully functioning Infin CLI should take <= 8 hours
    - Should leverage stable abstractions to decrease development time
    - Architecture should be modular and easy to update/add features
## Intuitive Interface
    - Interacting with Infin out of the box should be dead simple and should require minimal documentation glancing
    - The CLI should make use of rich elements such as color customization
## Self Explanatory Code
    - Reading the Infin source code should be easily digestible and self explanatory even for novice programmers
# Technical Assumptions
- Small Scale
    - Total API response should easily fit within the RAM of a Macbook Air
- Duplicates Provide No Value
    - duplicate (title, category) pairs should not be displayed
- Not Real Time Data
    - API response can be cached for at least 1 minute without consequences


# Infin Architecture
![](https://paper-attachments.dropbox.com/s_D8BCB78957EDFA4D411B34A9B88F82D40454B23D240466C7E2278098725EE2F0_1614548120649_Blank+diagram.png)



## CLI
- Customizes CLI colors, cache invalidation length, etc
- Queries relevant information from Dispatcher and displays in the terminal 
- Leverages [click](https://click.palletsprojects.com/en/7.x/) library for a flexible, fast, clean CLI design


## Cache
- Stores API endpoint response
- Uses a hashtable to map categories to sets containing all AI Capabilities within the category


## Validator
- Validates whether API response conforms to given JSON schema


## Dispatcher
- Provides an API to query contents of the cache
- Updates Cache if invalidated
    - cache is invalidate if more than “refresh_freq” seconds elapses since the last time the cache is fetched
- Retrieves response from API endpoint



## Further Improvements
- Asynchronous callbacks
    - switch from synchronous requests to asynchronous requests
- Logging
    - log request and response status codes as well as CLI commands and errors
    - verbose and debug modes to display different levels of events 
- UI Improvements
    - Loading Bars 
    - Response Times
    


