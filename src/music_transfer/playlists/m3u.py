from pathlib import Path

from .playlist import Playlist
from src.music_transfer.config import Config

class M3u(Playlist):
    def __init__(self, playlist: str, config: Config):
        super().__init__(playlist, config)

    @staticmethod
    def ext() -> str:
        return 'm3u'

    def playlistEntry(self, file: str):
        s = self.songs[file]
        
        title = ""
        if s.tags.artist and s.tags.title:
            # title = f'{s.tags.artist} - {s.tags.title}'
            title = f'{s.tags.title}'
        elif s.tags.title:
            title = str(s.tags.title)
        else:
            title = Path(s.file).stem
        
        # return f'#EXTINF:{s.tags.duration}, {title}\n{s.dest}\n'
        return f'#EXTINF:,{title}\n{s.dest}\n'

    def createPlaylist(self) -> str:
        p = self.localPlaylistPath()
        with open(p, 'w', encoding="utf-8") as f:
            f.write("#EXTM3U\n")
        
            for s in self.songs:
                f.write(self.playlistEntry(s))
            
            return p
