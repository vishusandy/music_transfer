from pathlib import Path
import shlex
import re

from tinytag import TinyTag

from src.music_transfer.config import Config

path_sanitize = re.compile("[\"'\\…|><*+\[\]:?]")

class Song:
    
    @staticmethod
    def sanitize(s: str) -> str:
        # return s.replace('\\', '\\\\').replace('\'', '\\\'')
        # return s.replace('\'', '').replace(':', '')
        return re.sub(path_sanitize, '', s)
    
    def __init__(self, file: str, config: Config):
        tags = TinyTag.get(file)
        self.file = file
        self.tags = tags
        self.dest = self.sanitize(self.findDest(config))
    
    def __hash__(self):
        return hash(self.file)
    
    def __eq__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return self.file == other.file
    
    def findDest(self, config: Config) -> str:
        if self.file.startswith(config.local_music_dir):
            return self.file[len(config.local_music_dir)+1:]
        else:
            p = Path(self.file)
            out = Path(config.va_dir)
            
            parts = []
            if self.tags.artist is not None:
                parts.append(self.tags.artist)
            
            if self.tags.album is not None:
                parts.append(self.tags.album)
            
            if self.tags.title is not None and len(parts) > 0:
                parts.append(self.tags.title)
                name = '_'.join(parts) + p.suffix
                out = out / name
            else:
                out = out / p.name
            
            s = str(out)
            
            if s.startswith('/'):
                return s[1:]
            else:
                return s
    