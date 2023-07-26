import tomllib

from src.app.sources.source import Source
from src.app.sources.rhythmbox import RhythmBox
from src.app.errors import InvalidSource


class Config:
    @staticmethod
    def sourceParser(source: str, source_file: str | None) -> Source:
        match source:
            case 'rhythmbox':
                return RhythmBox(source_file)
            case s:
                raise InvalidSource(s)

    def __init__(self, config_file: str = 'config.toml', source_file: str | None = None):
        with open(config_file, "rb") as f:
            data = tomllib.load(f)
            
            self.parser: Source = self.sourceParser(data['local']['import_source'], source_file)
            self.local_music_dir: str = data['local']['local_music_dir']
            
            self.transfer_method: str = data['transfer']['method']
            self.va_dir: str = data['transfer']['va_dir']
            self.prompt_before_transfer: bool = data['transfer']['prompt_before_transfer']
            self.only_new: bool = data['transfer']['transfer_only_new']
            self.playlist_format: str = data['transfer']['playlist_format']
            self.device_music_dir: str = data['transfer']['device_music_dir']
            





