import xml.etree.ElementTree as ET
import urllib.parse
from pathlib import Path

from platformdirs import user_data_path

from .source import Source

class RhythmBox(Source):
    def __init__(self, file: Path | str | None = None):
        if file is None:
            file = user_data_path('rhythmbox') / 'playlists.xml'
        
        self.file = file
        self.xml = ET.parse(file)
        
    def listPlaylists(self) -> list[str]:
        p = []
        root = self.xml.getroot()
        
        for playlist in root.iter('playlist'):
            t = playlist.get('type')
            
            if t is None or t != 'static':
                continue
            
            p.append(playlist.get('name'))
        
        return p

    def playlistSongs(self, playlist_names: list[str]) -> list[str]:
        songs = set()
        root = self.xml.getroot()
        
        for playlist in root.iter('playlist'):
            t = playlist.get('type')
            name = playlist.get('name')
            
            if t == 'static' and name in playlist_names:
                for song in playlist.iter('location'):
                    f = urllib.parse.unquote(song.text[7:])
                    songs.add(f)

        return list(songs)


