from hfilesize import FileSize

from src.music_transfer.menu import showMenu
from music_transfer.collection import Collection
from src.music_transfer.config import Config
from src.music_transfer.errors import InvalidPlaylistFormat, InvalidTransferMethod
from src.music_transfer.playlists.playlist import Playlist
from src.music_transfer.playlists.m3u import M3u
from src.music_transfer.devices.device import Device
from src.music_transfer.devices.adb import Adb


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
    c.transfer()
    
    
def playlistFormat(config: Config) -> Playlist | None:
    match config.playlist_format.lower():
        case 'm3u':
            return M3u
        case 'none':
            return None
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
