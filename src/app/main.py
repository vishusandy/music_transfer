from src.app.menu import showMenu
from src.collection import Collection
from src.app.config import Config


def main():
    config = Config()
    options = list(filter(lambda f: f != '', config.parser.listPlaylists()))
    
    choices = showMenu(options)
    
    if choices is None or len(choices) == 0:
        print('No playlists were selected.  Exiting..')
        return
    
    c = Collection(choices, config)
    c.createPlaylists(True)
    
    print(f'Transferred {c.transferSongs()} files')

    c.transferPlaylists()

if __name__ == '__main__':
    main()
