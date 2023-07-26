from abc import ABC, abstractmethod

class Source(ABC):
    @abstractmethod
    def listPlaylists(self) -> list[str]:
        raise NotImplementedError("Method not implemented")
    
    @abstractmethod
    def playlistSongs(self, playlist_names: list[str]) -> list[str]:
        raise NotImplementedError("Method not implemented")
