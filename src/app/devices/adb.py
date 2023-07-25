import sys
import shlex, subprocess

from src.app.config import Config
from .device import Device
from src.app.song import Song


class Adb(Device):
    def __init__(self, config: Config):
        self.config = config
    
    def fileExists(self, file: str, size: int | None = None) -> bool:
        rst = subprocess.run(["adb", "-d", "shell", "stat", "-c", "%s", f'"{file}"'], capture_output=True, encoding="utf8")
        return rst.returncode == 0 and (size is None or size == int(rst.stdout))
    
    def songExists(self, song: Song) -> bool:
        dest = f'{self.config.device_music_dir}/{song.dest}'
        # rst = subprocess.run(["adb", "-d", "shell", "stat", "-c", "%s", f'"{dest}"'], capture_output=True, encoding="utf8")
        # return rst.returncode == 0 and int(rst.stdout) == int(song.tags.filesize)
        return self.fileExists(song.dest, int(song.tags.filesize))
    
    def transferSong(self, song: Song) -> int:
        dest = f'{self.config.device_music_dir}/{song.dest}'
        rst = subprocess.run(["adb", "-d", "push", "--sync", song.file, dest], capture_output=False, stdout=subprocess.DEVNULL)
        return song.tags.filesize if rst.returncode == 0 else 0
    
    def transferFile(self, file: str, dest: str) -> bool:
        rst = subprocess.run(["adb", "-d", "push", "--sync", file, dest], capture_output=False, stdout=subprocess.DEVNULL)
        return rst.returncode == 0
