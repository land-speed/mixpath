class Key:
    def __init__(self, trad_key: str):
        self.trad_key = trad_key
        self.camelot_note, self.camelot_m = self.toCamelot()
        self.camelot_full = str(self.camelot_note)+self.camelot_m

    def toCamelot(self):
        match self.trad_key:
            case "G#min":
                return [1, "A"]
            case "Bmaj":
                return [1, "B"]
            case "D#min":
                return [2, "A"]
            case "F#maj":
                return [2, "B"]
            case "A#min":
                return [3, "A"]
            case "C#maj":
                return [3, "B"]
            case "Fmin":
                return [4, "A"]
            case "G#maj":
                return [4, "B"]
            case "Cmin":
                return [5, "A"]
            case "D#maj":
                return [5, "B"]
            case "Gmin":
                return [6, "A"]
            case "A#maj":
                return [6, "B"]
            case "Dmin":
                return [7, "A"]
            case "Fmaj":
                return [7, "B"]
            case "Amin":
                return [8, "A"]
            case 'Cmaj':
                return [8, "B"]
            case 'Emin':
                return [9, "A"]
            case "Gmaj":
                return [9, "B"]
            case "Bmin":
                return [10, "A"]
            case "Dmaj":
                return [10, "B"]
            case "F#min":
                return [11, "A"]
            case "Amaj":
                return [11, "B"]
            case "C#min":
                return [12, "A"]
            case "Emaj":
                return [12, "B"]
            case _:
                print(f"Unknown key {_}")


class TrackNode:
    def __init__(self, title: str, bpm, key: Key):
        self.uuid = None
        self.title = title
        self.bpm = bpm
        self.camelot_note = key.camelot_note
        self.camelot_m = key.camelot_m
        self.camelot_full = key.camelot_full
    
    def add_uuid(self, uuid: str):
        """Adds id param to TrackNode object

            Parameters:
                id: UUID of node
        """
        self.uuid = uuid

    def __eq__(self, other):
        if isinstance(other, TrackNode):
            return self.uuid == other.uuid
        return False
