import unittest
from copy import copy

from src.music_transfer.config import Config
from src.music_transfer.main import transferMethod, playlistFormat
from .config import rbConfig
from src.collection import Collection

# See https://docs.python.org/3/library/unittest.html


class PlaylistTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = rbConfig()
    
    def testValidFormat(self):
        cfg = copy(self.config)
        
        cfg.playlist_format = 'm3u'
        
        Collection([], cfg, playlistFormat(cfg), transferMethod(cfg))
    
    @unittest.expectedFailure
    def testInvalidFormat(self):
        cfg = copy(self.config)
        cfg.playlist_format = 'jpg'
        
        Collection([], cfg, playlistFormat(cfg), transferMethod(cfg))

    @unittest.expectedFailure
    def testInvalidTransfer(self):
        cfg = copy(self.config)
        cfg.transfer_method = 'potatoes'
        
        Collection([], cfg, playlistFormat(cfg), transferMethod(cfg))
        
    
    def testCollectionSongs(self):
        Collection([], self.config, playlistFormat(self.config), transferMethod(self.config))

if __name__ == '__main__':
    unittest.main()
