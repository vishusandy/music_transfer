from hfilesize import FileSize

from src.app.menu import showMenu
from src.collection import Collection
from src.app.config import Config
from src.app.errors import InvalidPlaylistFormat, InvalidTransferMethod
from src.app.playlists.playlist import Playlist
from src.app.playlists.m3u import M3u
from src.app.devices.device import Device
from src.app.devices.adb import Adb


def main():
    config = Config()
    options = list(filter(lambda f: f != '', config.parser.listPlaylists()))
    
    choices = showMenu(options)
    
    if choices is None or len(choices) == 0:
        print('No playlists were selected.  Exiting..')
        return
    
    dev = transferMethod(config)
    pl = playlistFormat(config)
    c = Collection(choices, config, pl, dev)
    
    new = len(c.new_songs)
    old = len(c.songs) - new
    
    if old > 0:
        print(f'About to transfer {new} new songs ({old} songs already exist on device)')
    else:
        print(f'About to transfer {new} new songs')
    
    c.createPlaylists(True)
    
    num_bytes = FileSize(c.transferSongs()).format()
    
    
    print(f'Transferred {num_bytes}')

    c.transferPlaylists()
    
    
def playlistFormat(config: Config) -> Playlist:
    match config.playlist_format.lower():
        case 'm3u':
            return M3u
        case f:
            raise InvalidPlaylistFormat(f)
        
def transferMethod(config: Config) -> Device:
    match config.transfer_method.lower():
        case 'adb':
            return Adb(config)
        case t:
            raise InvalidTransferMethod(t)

if __name__ == '__main__':
    main()
