from pathlib import Path

from progress1bar import ProgressBar
from halo import Halo
from hfilesize import FileSize

from src.music_transfer.config import Config
from src.music_transfer.song import Song
from src.music_transfer.playlists.playlist import Playlist
from src.music_transfer.devices.device import Device
from src.music_transfer.util import askYes


class Collection:
    def __init__(self, playlists: list[str], config: Config, pl_format: Playlist | None, device: Device):
        self.config: Config = config
        self.playlist_names: list[str] = playlists
        self.playlists: list[Playlist] = []
        self.songs: dict[str, Song] = {}
        self.transfer_songs: dict[str, Song] = {}
        self.device: Device = device

        self.getSongs(pl_format)
        self.checkNewFiles()

    def getSongs(self, pl_format: Playlist | None):
        if pl_format is not None:
            for p in self.playlist_names:
                c: Playlist = pl_format(p, self.config)
                self.playlists.append(c)
                self.songs |= c.songs
        else:
            for p in self.playlist_names:
                for f in self.config.parser.playlistSongs([p]):
                    if f not in self.songs:
                        self.songs[f] = Song(f, self.config)

    def checkNewFiles(self):
        if self.config.only_new:
            spinner = Halo(text='Checking for new files', spinner='point', color='')
            spinner.start()
            for f, s in self.songs.items():
                if not self.device.songExists(s):
                    print(f'file {f} does not exist')
                    self.transfer_songs[f] = s
            spinner.stop()
        else:
            self.transfer_songs = self.songs

    def createPlaylists(self, output: bool = False):
        for p in self.playlists:
            f = p.createPlaylist()
            if output:
                print(f'created "{f}"')

    def transfer(self):
        new = len(self.transfer_songs)
        old = len(self.songs) - new
        
        if new == 0 and self.config.only_new == True:
            print(f'No new songs to transfer')
        elif new == 0:
            print(f'No songs to transfer')
        else:
            total_size = sum(map(lambda s: s.tags.filesize, self.transfer_songs.values()))
            total = FileSize(total_size).format()
            
            if old > 0:
                print(f'Found {new} new songs ({total}) to transfer ({old} songs already exist on device)')
            else:
                print(f'Found {new} songs ({total}) to transfer')
            
            if self.config.prompt_before_transfer == True:
                if askYes("Continue? [Y/n]") == False:
                    print('Aborting...')
                    return
            
            # num_bytes = FileSize(self.transferSongs()).format()
            # print(f'Transferred {num_bytes}')
            self.transferSongs()
            print(f'{new} songs transferred')
            
        self.createPlaylists(False)
        self.transferPlaylists()

    def transferSongs(self) -> int:
        i = 0
        with ProgressBar(total=len(self.transfer_songs), completed_message='Songs transferred', clear_alias=True, show_duration=True, show_prefix=False) as p:
            for s in self.transfer_songs.values():
                p.alias = Path(s.file).stem
                i += self.device.transferSong(s)
                p.count += 1
            
        return i
    
    def transferPlaylists(self):
        if len(self.playlists) != 0:
            spinner = Halo(text='Transferring playlists', spinner='point', color='')
            spinner.start()
            for p in self.playlists:
                src = p.localPlaylistPath()
                dest = self.config.device_music_dir + '/' + p.devicePlaylistPath()
                size = Path(src).stat().st_size
                
                if not self.device.fileExists(dest, size):
                    self.device.transferFile(src, dest)
            spinner.stop()
