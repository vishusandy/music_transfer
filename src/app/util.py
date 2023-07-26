
# prompt user until they answer with a correct yes/no response
def askYesNo(question: str) -> bool:
    ans = input(question + ':')

    yes_choices = ['yes', 'y']
    no_choices = ['no', 'n']
    
    while True:
        if ans.lower() in yes_choices:
            return True
        if ans.lower() in no_choices:
            return False

# prompt user for a yes/no response.  If the answer in not a yes answer assume a no answer regardless of whether it conforms to a no answer or not
def askYes(question: str) -> bool:
    ans = input(question + ':')

    yes_choices = ['yes', 'y']
    
    if ans.lower() in yes_choices:
        return True
    
    return False
