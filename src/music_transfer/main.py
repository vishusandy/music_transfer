import argparse
from random import choices
import sys
from typing import Type

from src.music_transfer.menu import showMenu
from music_transfer.collection import Collection
from src.music_transfer.config import Config, getSource
from src.music_transfer.errors import InvalidPlaylistFormat, InvalidTransferMethod
from src.music_transfer.playlists.playlist import Playlist
from src.music_transfer.playlists.m3u import M3u
from src.music_transfer.devices.device import Device
from src.music_transfer.devices.adb import Adb



def main():
    config = configSetup()
    
    run(config)


def configSetup():
    if Config.userConfigFile().exists():
        config = Config.fromToml()
    else:
        config = Config.default()
    
    epilog = '''
Configuration File\n
    If exists, a user config file will be loaded from ~/.config/music_transfer/config.toml

    Commandline options will override the corresponding config file values.
    
    
Transferring Songs
    Music files will be transferred from LOCAL_MUNIC_DIR to DEVICE_MUSIC_DIR.
    
    Example:
        Using the following options
            --local      ~/Music
            --device-dir /storage/self/primary/Music
            --va         VA
        will copy ~/Music/Beastie Boys/Ill Communication/Sabotage.mp3
        to /storage/self/primary/Music/Beastie Boys/Ill Communication/Sabotage.mp3
        
        However, files outside of the local music directory will be handled differently.
        These files will be transferred into the va directory.
        The resulting filename will be based on the song's metadada with a format
        similar to <artist>_<album>_<title>
        
        For example, ~/songs/sabotage.mp3 will be transferred to
        /storage/self/primary/Music/VA/Beastie Boys_Ill Communication_


'''
    
    parser = argparse.ArgumentParser(
        description='Transfer music playlists from a local music library to a phone or device',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=epilog
    )
    
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='suppress stdout output',
                        dest='quiet')
    
    parser.add_argument('--list', action='store_true',
                        help='list songs to transfer',
                        dest='list_songs')
    
    parser.add_argument('--new-only', action=argparse.BooleanOptionalAction, 
                        help='only transfer files that do not already exist',
                        dest='transfer_only_new')
    
    parser.add_argument('--prompt', action=argparse.BooleanOptionalAction, 
                        help='Do not prompt before transferring files',
                        dest='prompt_before_transfer')
    
    parser.add_argument('-l', '--local', 
                        help='local directory containing music files',
                        dest='local_music_dir')
    
    parser.add_argument('-v', '--va', 
                        help='folder to put music files that did not originate in LOCAL_MUSIC_DIR',
                        dest='va_dir')
    
    parser.add_argument('-s', '--source', choices=['rhythmbox'], 
                        help='where to find playlists',
                        dest='import_source')
    
    parser.add_argument('-m', '--method', choices=['adb'], 
                        help='how to transfer the files',
                        dest='method')
    
    parser.add_argument('-f', '--playlist', choices=['m3u', 'none'], 
                        help='format to create playlist files in',
                        dest='playlist_format')
    
    parser.add_argument('-d', '--device-dir', 
                        help='directory to transfer files to.  Ex: /storage/self/primary/Music',
                        dest='device_music_dir')
    
    parser.add_argument('--create-config', action='store_true', dest='create_config')
    
    args = parser.parse_args()
    
    if args.create_config == True:
        Config.userConfigFile(True, True)
        sys.exit()
    
    config.quiet = args.quiet
    config.list_songs = args.list_songs
    
    if args.device_music_dir is not None:
        config.device_music_dir = args.device_music_dir
    if args.playlist_format is not None:
        config.playlist_format = args.playlist_format
    if args.prompt_before_transfer is not None:
        config.prompt_before_transfer = args.prompt_before_transfer
    if args.transfer_only_new is not None:
        config.only_new = args.transfer_only_new
    if args.va_dir is not None:
        config.va_dir = args.va_dir
    if args.method is not None:
        config.transfer_method = args.method
    if args.local_music_dir is not None:
        config.local_music_dir = args.local_music_dir
    if args.import_source is not None:
        config.source = args.import_source
        config.parser = getSource(config.source)
    
    return config


def run(config: Config):
    options = list(filter(lambda f: f != '', config.parser.listPlaylists()))
    
    choices = showMenu(options)
    
    if choices is None or len(choices) == 0:
        print('No playlists were selected.  Exiting..', file=sys.stderr)
        return
    
    dev = transferMethod(config)
    pl = playlistFormat(config)
    
    c = Collection(choices, config, pl, dev)
    c.transfer()


# T = TypeVar('T', bound=Playlist)
def playlistFormat(config: Config) -> Type[Playlist] | None:
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
