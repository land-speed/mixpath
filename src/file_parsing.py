from pathlib import Path
from mutagen.mp3 import MP3
from models import *


def to_node(path: str):
    nodes = []
    for file in Path(path).rglob("*"):
        parsed = MP3(file)
        title = str(parsed.tags["TIT2"])
        bpm = float(str(parsed.tags["TBPM"]))
        key = Key(str(parsed.tags["TKEY"]))
        nodes.append(TrackNode(title, bpm, key))
    return nodes
