from dataclasses import dataclass
import os
from pathlib import Path
import tomlkit
import tomllib

from platformdirs import user_config_path, user_music_dir

from src.music_transfer.sources.source import Source
from src.music_transfer.sources.rhythmbox import RhythmBox
from src.music_transfer.errors import InvalidSource

@dataclass
class Config:
    quiet: bool
    list_songs: bool
    source: str
    parser: Source
    local_music_dir: str
    transfer_method: str
    va_dir: str
    prompt_before_transfer: bool
    only_new: bool
    playlist_format: str
    device_music_dir: str
    
    def print(self, s: str):
        if not self.quiet:
            print(s)
    
    @classmethod
    def default(cls, source_file: Path | str | None = None):
        quiet: bool = False
        list_songs: bool = False
        
        source = "rhythmbox"
        parser = getSource(source, source_file)
        local_music_dir = user_music_dir()
        
        transfer_method = "adb"
        va_dir = "VA"
        prompt_before_transfer = True
        only_new = False
        playlist_format = "m3u"
        device_music_dir = "/storage/self/primary/Music"
        
        return cls(quiet, list_songs, source, parser, local_music_dir, transfer_method, va_dir, prompt_before_transfer, only_new, playlist_format, device_music_dir)
    
    @classmethod
    def userConfigFile(cls, create_path: bool = False, create_config: bool = False) -> Path:
        p = user_config_path('music_transfer')
        
        if create_path and not p.exists():
            os.makedirs(p, exist_ok=True)
            
        conf = p / "config.toml"
        
        if create_config and not conf.exists():
            with open(conf, "xt") as f:
                f.write(cls.default().toToml())
                print(f'Wrote default config to "{conf}"')
        
        return conf


    @classmethod
    def fromToml(cls, file: Path | str | None = None, source_file: Path | str | None = None):
        if file is None:
            file = cls.userConfigFile(False)
        
        with open(file, "rb") as f:
            data = tomllib.load(f)
            
            quiet = False
            list_songs = False
            
            source = data['local']['import_source']
            parser = getSource(source, source_file)
            local_music_dir: str = data['local']['local_music_dir']
            
            transfer_method: str = data['transfer']['method']
            va_dir: str = data['transfer']['va_dir']
            prompt_before_transfer: bool = data['transfer']['prompt_before_transfer']
            only_new: bool = data['transfer']['transfer_only_new']
            playlist_format: str = data['transfer']['playlist_format']
            device_music_dir: str = data['transfer']['device_music_dir']
            
            return cls(quiet, list_songs, source, parser, local_music_dir, transfer_method, va_dir, prompt_before_transfer, only_new, playlist_format, device_music_dir)


    def toToml(self) -> str:
        doc = tomlkit.document()
        
        local = tomlkit.table()
        local.add("import_source", self.source)
        local.add("local_music_dir", self.local_music_dir)
        doc.add("local", local)
        
        transfer = tomlkit.table()
        transfer.add("method", self.transfer_method)
        transfer.add("va_dir", self.va_dir)
        transfer.add("transfer_only_new", self.only_new)
        transfer.add("prompt_before_transfer", self.prompt_before_transfer)
        transfer.add("playlist_format", self.playlist_format)
        transfer.add("device_music_dir", self.device_music_dir)
        doc.add("transfer", transfer)
        
        return tomlkit.dumps(doc)


def getSource(source: str, source_file: Path | str | None = None) -> Source:
    match source.lower():
        case 'rhythmbox':
                return RhythmBox(source_file)
        case s:
            raise InvalidSource(s)
