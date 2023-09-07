from abc import ABC, abstractmethod

from src.music_transfer.song import Song

class Device(ABC):
    @abstractmethod
    def fileSize(self, file: str) -> int | None:
        ...
    
    @abstractmethod
    def fileExists(self, file: str, size: int | None = None) -> bool:
        ...
    
    @abstractmethod
    def songExists(self, f: Song) -> bool:
        ...
    
    @abstractmethod
    def transferSong(self, song: Song) -> int:
        ...

    @abstractmethod
    def downloadFile(self, remote: str, local: str) -> bool:
        ...

    @abstractmethod
    def transferFile(self, file: str, dest: str) -> bool:
        ...


