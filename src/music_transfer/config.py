import tomllib
import os
from pathlib import Path
import sys

from platformdirs import user_config_path, user_music_path

from src.music_transfer.sources.source import Source
from src.music_transfer.sources.rhythmbox import RhythmBox
from src.music_transfer.errors import InvalidSource, ConfigNotExist


class Config:
    @staticmethod
    def sourceParser(source: str, source_file: str | None) -> Source:
        match source:
            case 'rhythmbox':
                return RhythmBox(source_file)
            case s:
                raise InvalidSource(s)

    def __init__(self, config_file: str = 'config.toml', source_file: str | None = None):
        
        p = user_config_path('music_transfer')
        
        if not p.exists():
            os.makedirs(p, exist_ok=True)
            
        conf = p / config_file
        
        if not conf.exists():
            createDefault(conf)
            
        with open(conf, "rb") as f:
            data = tomllib.load(f)
            
            self.parser: Source = self.sourceParser(data['local']['import_source'], source_file)
            self.local_music_dir: str = data['local']['local_music_dir']
            
            self.transfer_method: str = data['transfer']['method']
            self.va_dir: str = data['transfer']['va_dir']
            self.prompt_before_transfer: bool = data['transfer']['prompt_before_transfer']
            self.only_new: bool = data['transfer']['transfer_only_new']
            self.playlist_format: str = data['transfer']['playlist_format']
            self.device_music_dir: str = data['transfer']['device_music_dir']
            


def createDefault(p: Path):
    conf = f'''
[local]
import_source = "rhythmbox"
local_music_dir = "{user_music_path()}" # playlists will be created here to be transferred

[transfer]
method = "adb"
va_dir = "VA"                                    # directory to put files that are reside outside of the music library dir
transfer_only_new = false                        # set to false to disable checking if the files already exist
prompt_before_transfer = false                   # ask user if they want to transfer the specified number uf songs or not
playlist_format = "m3u"                          # set to "none" to not create playlists
device_music_dir = "/storage/self/primary/Music"

[adb]
command = "adb -d push --sync \\"<source_file>\\" \\"<base>/<dest_file>\\""

'''
    with open(p, 'xt') as f:
        f.write(conf)
    
    sys.tracebacklimit = 0
    raise ConfigNotExist(str(p))
    

