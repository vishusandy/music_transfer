import unittest

from music_transfer.sources.rhythmbox import RhythmBox
from ..config import genRbXml

# See https://docs.python.org/3/library/unittest.html


class RhythmBoxTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = RhythmBox(genRbXml())
        
    def testListPlaylist(self):
        playlists = [
            '70s',
            'all',
            'space',
        ]
        self.assertEqual(self.parser.listPlaylists(), playlists)
    
    def testPlaylistSongs(self):
        example_songs = [
            '/home/andrew/Music/song_a.mp3',
            '/home/andrew/Music/song_d.mp3',
            '/home/andrew/Music/song_e.mp3',
            '/home/andrew/Music/song_f.mp3'
        ]
        example_songs.sort()
        
        song_list = self.parser.playlistSongs(['70s', 'space'])
        song_list.sort()
        
        self.assertEqual(song_list, example_songs)

if __name__ == '__main__':
    unittest.main()
