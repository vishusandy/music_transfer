from pathlib import Path

from src.app.config import Config
from src.app.song import Song
from src.app.playlists.playlist import Playlist
from src.app.devices.device import Device


class Collection:
    def __init__(self, playlists: list[str], config: Config, pl_format: Playlist, device: Device):
        self.config: Config = config
        self.playlist_names: list[str] = playlists
        self.playlists: list[Playlist] = []
        self.songs: dict[str, Song] = {}
        self.new_songs: dict[str, Song] = {}
        self.transfer: Device = device

        for p in self.playlist_names:
            c: Playlist = pl_format(p, self.config)
            self.playlists.append(c)
            self.songs |= c.songs
            
        for f, s in self.songs.items():
            if not self.transfer.songExists(s):
                self.new_songs[f] = s

    def createPlaylists(self, output: bool = False):
        for p in self.playlists:
            f = p.createPlaylist()
            if output:
                print(f'created "{f}"')

    def transferSongs(self) -> int:
        i = 0
        for s in self.new_songs.values():
            i += self.transfer.transferSong(s)
            
        return i
    
    def transferPlaylists(self):
        for p in self.playlists:
            src = p.localPlaylistPath()
            dest = self.config.device_music_dir + '/' + p.devicePlaylistPath()
            size = Path(src).stat().st_size
            
            if not self.transfer.fileExists(dest, size):
                self.transfer.transferFile(src, dest)

