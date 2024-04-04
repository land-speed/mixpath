import random
import numpy as np
from models import TrackNode, Key


def random_songs(count: int, min_bpm: int = 120, max_bpm: int = 140):
    """Generates a list of randomly generated TrackNodes

        Parameters:
            count: number of items in list
            min_bpm: minimum BPM to be used in generation
            max_bpm: maximum BPM to be used in generation

        Returns:
            nodes: List of randomly generated TrackNodes
    """
    keys = ["Cmaj", "Cmin", "C#maj", "C#min", "Dmaj", "Dmin", "D#maj", "D#min", "Emaj", "Emin", "Fmaj", "Fmin",
            "F#maj", "F#min", "Gmaj", "Gmin", "G#maj", "G#min", "Amaj", "Amin", "A#maj", "A#min", "Bmaj", "Bmin"]
    nodes = []
    i = 0
    while i < count:
        key = random.choice(keys)
        bpm = np.random.randint(low=min_bpm, high=max_bpm)
        node = TrackNode(f"{key}-{bpm}", bpm, Key(key))
        nodes.append(node)
        i += 1
    return nodes
