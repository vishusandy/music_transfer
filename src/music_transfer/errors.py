

class InvalidPlaylistFormat(Exception):
    def __init__(self, format: str):
        self.format = format
 
    def __str__(self):
        return f'Error: invalid playlist format "{self.format}"'

class InvalidTransferMethod(Exception):
    def __init__(self, method: str):
        self.method = method
 
    def __str__(self):
        return f'Error: invalid transfer method "{self.method}"'

class InvalidSource(Exception):
    def __init__(self, source: str):
        self.source = source
 
    def __str__(self):
        return f'Error: invalid source "{self.source}"'

