import re

GREEN = '\033[32m'
ENDC = '\033[0m'

def getFormattedResponseText(response):    
    formattedResponse = ''
    substrings = re.split('(```.*?```)', response, flags=re.DOTALL)

    for substring in substrings:
        substr = substring
        if substr.startswith('```'):
            substr = GREEN + substring + ENDC
        
        formattedResponse = formattedResponse + substr

    return formattedResponse