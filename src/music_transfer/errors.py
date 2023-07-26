

class InvalidPlaylistFormat(Exception):
    def __init__(self, format: str):
        self.format = format
 
    def __str__(self):
        return f'Invalid playlist format "{self.format}"'

class InvalidTransferMethod(Exception):
    def __init__(self, method: str):
        self.method = method
 
    def __str__(self):
        return f'Invalid transfer method "{self.method}"'

class InvalidSource(Exception):
    def __init__(self, source: str):
        self.source = source
 
    def __str__(self):
        return f'Invalid source "{self.source}"'

