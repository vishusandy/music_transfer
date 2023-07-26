from typing import Optional, Tuple
import xml.etree.ElementTree as ET

from simple_term_menu import TerminalMenu

def showMenu(options: list[str]) -> Optional[list[str]]:
    menu = TerminalMenu(options, multi_select=True, show_multi_select_hint=True)
    
    choices = menu.show()
    
    if choices is not None:
        return list(map(lambda c: options[c], choices))
    else:
        return None

