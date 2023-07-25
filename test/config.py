from src.app.config import Config
from pathlib import Path
import urllib.parse

from src.app.sources.rhythmbox import RhythmBox


def genRbXml() -> str:
    test = Path.absolute(Path(__file__)).parent
    example_file = test / 'assets' / 'rhythmbox' / 'playlists.xml'
    
    with open(example_file, "r") as example:
        tmp = test / 'tmp'
        
        if not tmp.exists():
            tmp.mkdir()
            
        rbdir = tmp / 'rhythmbox'
        if not rbdir.exists():
            rbdir.mkdir()
            
        xml_file = rbdir / 'playlists.xml'
        if xml_file.exists():
            return xml_file
        
        with open(xml_file, "w") as rb:
            example_contents = example.read()
            music_dir = urllib.parse.quote('file://' + str(test / 'assets' / 'music'))
            example_contents.replace('file:///home/andrew/Music', music_dir)
        
            rb.write(example_contents)
        
            return xml_file


def rbConfig():
    test = Path.absolute(Path(__file__)).parent
    cfg = Config(source_file=genRbXml())
    cfg.local_music_dir = str(test / 'assets' / 'music')
    
    return cfg

