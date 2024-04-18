from src.models.song_status import SongStatus


class ChartRow:
    def __init__(self, pos, artist_photo_url, song_status: SongStatus, song_name, artist_name, last_week, peak_pos,
                 weeks_on_chart, page_url):
        self.pos = pos
        self.artist_photo_url = artist_photo_url
        self.song_status = song_status.value
        self.song_name = song_name
        self.artist_name = artist_name
        self.last_week = last_week
        self.peak_pos = peak_pos
        self.weeks_on_chart = weeks_on_chart
        self.page_url = page_url

    def to_dict(self):
        return {
            'pos': self.pos,
            'artist_photo_url': self.artist_photo_url,
            'song_status': self.song_status,
            'song_name': self.song_name,
            'artist_name': self.artist_name,
            'last_week': self.last_week,
            'peak_pos': self.peak_pos,
            'weeks_on_chart': self.weeks_on_chart,
            'page_url': self.page_url,
        }
