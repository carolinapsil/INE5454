from src.models.award import Award
from src.models.song_status import SongStatus


def parse_song_status(raw_text: str) -> str:
    enum_map = {
        'Group 7170': SongStatus.UP.value,
        'Group 7171': SongStatus.DOWN.value,
        'Group 3': SongStatus.KEEP.value,
        'NEW': SongStatus.NEW.value,
        'RE- ENTRY': SongStatus.RE_ENTRY.value,
    }

    return enum_map[raw_text]


def parse_song_status_uk(raw_text: str) -> str:
    enum_map = {
        'movement-icon': SongStatus.KEEP.value,
        'movement-up': SongStatus.UP.value,
        'movement-down': SongStatus.DOWN.value,
        'NEW': SongStatus.NEW.value,
        'RE': SongStatus.RE_ENTRY.value,
    }

    return enum_map[raw_text]


def parse_song_award(raw_text: str) -> str:
    enum_map = {
        '': Award.NOTHING.value,
        'Path 3055': Award.PERFORMANCE_GAIN_ONLY.value,
        'Group 7175': Award.PERFORMANCE_GAIN_AND_ADDITIONAL_AWARD.value
    }

    return enum_map[raw_text]
