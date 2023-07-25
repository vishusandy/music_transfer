from abc import ABC, abstractmethod

from src.app.song import Song

class Device(ABC):
    @abstractmethod
    def fileExists(self, file: str, size: int | None = None) -> bool:
        raise NotImplementedError("Method not implemented")
    
    @abstractmethod
    def songExists(self, f: Song) -> bool:
        raise NotImplementedError("Method not implemented")
    
    @abstractmethod
    def transferSong(self, song: Song) -> int:
        raise NotImplementedError("Method not implemented")
    
    @abstractmethod
    def transferFile(self, file: str, dest: str) -> bool:
        raise NotImplementedError("Method not implemented")


