from abc import ABC, abstractmethod

from src.music_transfer.song import Song

class Device(ABC):
    @abstractmethod
    def fileSize(self, file: str) -> int | None:
        raise NotImplementedError("Method not implemented")
    
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


