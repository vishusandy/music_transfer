from pathlib import Path
from abc import ABC, abstractmethod

from src.app.config import Config
from src.app.song import Song

class Playlist(ABC):
    def __init__(self, playlist: str, config: Config):
        self.config = config
        self.playlist = playlist
        self.songs = self.songList()
    
    @abstractmethod
    def createPlaylist(self) -> str:
        raise NotImplementedError("Method not implemented")
    
    @abstractmethod
    def ext() -> str:
        raise NotImplementedError("Method not implemented")
    
    def devicePlaylistPath(self) -> str:
        name = Path(self.playlist).stem
        return f'{name}.{self.ext()}'
    
    def localPlaylistPath(self) -> str:
        name = Path(self.playlist).stem
        return str(Path(self.config.music_dir) / f'{name}.{self.ext()}')
    
    def songList(self) -> dict[str, Song]:
        songs = dict()
        for s in self.config.parser.playlistSongs([self.playlist]):
            songs[s] = Song(s, self.config)
        
        return songs
    
    

