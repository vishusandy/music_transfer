from pathlib import Path
import shlex, subprocess

from src.app.config import Config
from src.app.playlists.playlist import Playlist
from src.app.playlists.m3u import M3u
from src.app.song import Song
from src.app.errors import InvalidPlaylistFormat

class Collection:
    def __init__(self, playlists: list[str], config: Config):
        self.config: Config = config
        self.selected_playlists: list[str] = playlists
        self.playlists: list[Playlist] = []
        self.songs: dict[str, Song] = {}

        match self.config.format.lower():
            case 'm3u':
                self.pl_class: Playlist = M3u
            case f:
                raise InvalidPlaylistFormat(f)

        for p in self.selected_playlists:
            c = self.pl_class(p, self.config)
            self.playlists.append(c)
            self.songs |= c.songs

    def createPlaylists(self, output: bool = False):
        for p in self.playlists:
            f = p.createPlaylist()
            if output:
                print(f'created "{f}"')

    def transferSongs(self) -> int:
        base = self.config.command.replace('<base>', self.config.base_device_dir)
        
        i = 0
        for s in self.songs.values():
            cmd = base.replace('<source_file>', s.file) \
                      .replace('<dest_file>', s.dest)
            
            subprocess.run(shlex.split(cmd), stdout=None, stderr=subprocess.PIPE, check=True)
            
            i += 1
            
        return i
    
    def transferPlaylists(self):
        base = self.config.command.replace('<base>', self.config.base_device_dir)
        
        for p in self.playlists:
            cmd = base.replace('<source_file>', p.localPlaylistPath()) \
                      .replace('<dest_file>', p.devicePlaylistPath())
            
            subprocess.run(shlex.split(cmd), stdout=None, stderr=subprocess.PIPE, check=True)
            

