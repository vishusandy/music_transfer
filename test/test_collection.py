import unittest
from copy import copy

from src.app.config import Config
from .config import rbConfig
from src.collection import Collection

# See https://docs.python.org/3/library/unittest.html


class PlaylistTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = rbConfig()
    
    def testValidFormat(self):
        cfg = copy(self.config)
        cfg.format = 'm3u'
        Collection([], cfg)
    
    @unittest.expectedFailure
    def testInvalidFormat(self):
        cfg = copy(self.config)
        cfg.format = 'jpg'
        Collection([], cfg)
        
    
    def testCollectionSongs(self):
        Collection([], self.config)

if __name__ == '__main__':
    unittest.main()
