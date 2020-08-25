from ..helper.utils import get_regions_by_markets


class PlaylistDataDoc(object):
    def __init__(self, tracks: list, artists: list, albums: list):
        self.tracks: list = tracks
        self.artists: list = artists
        self.albums: list = albums


class SpotifyTrackDoc(object):
    def __init__(self, track: dict, playlist_name: str, country: str,
                 category: str, audio_features: dict, lyrics: str = None):
        self.id: str = track.get('id')
        self.name: str = track.get('name')
        self.popularity: int = track.get('popularity')
        self.preview_url: str = track.get('preview_url')
        self.available_markets: list = track.get('available_markets', [])
        self.continents: list = get_regions_by_markets(markets=self.available_markets)
        self.total_markets: int = len(self.available_markets) if self.available_markets else [country]
        self.disc_number: int = track.get('disc_number')
        self.duration_ms: int = track.get('duration_ms')
        self.href: str = track.get('href')
        self.track_number: int = track.get('track_number')
        self.artists_spotify_id: list = [art.get('id') for art in track.get('artists')]
        self.album_spotify_id: str = track.get('album').get('id')
        self.playlist_name: str = playlist_name
        self.category: str = category
        self.audio_features: dict = audio_features
        self.lyrics: str = lyrics if lyrics is not None else ""


class SpotifyAlbumDoc(object):
    def __init__(self, album: dict):
        self.album_type: str = album.get("album_type")
        self.artists_ids: list = [i.get('id') for i in album.get('artists')]
        self.available_markets: list = album.get("available_markets")
        self.continents: list = get_regions_by_markets(markets=self.available_markets)
        self.total_markets: int = len(self.available_markets)
        self.copyrights: list = album.get("copyrights")
        self.external_urls: list = album.get("external_urls")
        self.genres: list = album.get("genres")
        self.href: str = album.get("href")
        self.id: str = album.get('id')
        self.images: list = album.get('images')
        self.label: str = album.get("label")
        self.name: str = album.get("name")
        self.popularity: int = album.get("popularity")
        self.release_date: str = album.get("release_date")
        self.tracks_ids: list = [i.get('id') for i in album.get('tracks').get("items")]
        self.uri: str = album.get("uri")


class SpotifyArtistDoc(object):
    def __init__(self, artist: dict):
        self.followers: int = artist.get("followers").get("total")
        self.genres: list = artist.get("genres")
        self.href: str = artist.get("href")
        self.id: str = artist.get("id")
        self.images: list = artist.get("images")
        self.name: str = artist.get("name")
        self.popularity: int = artist.get("popularity")
        self.uri: str = artist.get("uri")


