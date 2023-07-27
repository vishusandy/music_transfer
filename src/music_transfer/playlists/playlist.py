from pathlib import Path
from abc import ABC, abstractmethod

from src.music_transfer.config import Config
from src.music_transfer.song import Song

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
    
    def devicePlaylistPath(self, device_dir: str | None = None) -> str:
        name = Path(self.playlist).stem
        
        if device_dir is not None:
            return f'{device_dir}/{name}.{self.ext()}'
        else:
            return f'{name}.{self.ext()}'
    
    def localPlaylistPath(self) -> str:
        name = Path(self.playlist).stem
        
        return str(Path(self.config.local_music_dir) / f'{name}.{self.ext()}')
    
    def songList(self) -> dict[str, Song]:
        songs = dict()
        
        for s in self.config.parser.playlistSongs([self.playlist]):
            # songs.add(Song(s, self.config))
            songs[s] = Song(s, self.config)
            
        
        return songs
    
    

