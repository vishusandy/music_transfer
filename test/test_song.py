import unittest
from pathlib import Path
from copy import copy

from src.music_transfer.song import Song
from .config import rbConfig

# See https://docs.python.org/3/library/unittest.html


class SongTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path.absolute(Path(__file__)).parent
        cls.root = root
        cls.song_a = root / 'assets' / 'music' / 'song_a.mp3'
        cls.config = rbConfig()
        
    def testOutsideDest(self):
        config = copy(self.config)
        music = Path().home() / 'Music'
        config.local_music_dir = str(music)
        
        self.assertNotEqual(music, str(self.root))
        
        song = Song(str(self.song_a), config)
        
        self.assertEqual(song.dest, 'VA/Aerosmith_Toys in the Attic_Walk This Way.mp3')
    
    
    def testInsideDest(self):
        song = Song(str(self.song_a), self.config)
        
        self.assertEqual(remove_prefix(song.file, str(Path.cwd()))[1:], 'test/assets/music/song_a.mp3')
        self.assertEqual(song.dest, 'song_a.mp3')


def remove_prefix(text, prefix):
    return text[text.startswith(prefix) and len(prefix):]

if __name__ == '__main__':
    unittest.main()
