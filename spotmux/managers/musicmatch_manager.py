from musixmatch import Musixmatch
from ..helper.settings import logger


class MusixmatchManager:
    def __init__(self, api_key: str):
        self.musixmatch: Musixmatch = Musixmatch(
            api_key)

    @staticmethod
    def get_lyric_by_track_id(musixmatch_api: Musixmatch, track_id: int):
        response: dict = {}
        try:
            response: dict = musixmatch_api.track_lyrics_get(track_id)
            response = response.get("message")
        except Exception as e:
            logger.error(e)
        return response

    @staticmethod
    def search_track_by_query(musixmatch_api: Musixmatch, q_track: str, q_artist: str,
                              page_size: int = 10, page: int = 1):
        response: dict = {}
        try:
            response: dict = musixmatch_api.track_search(
                q_track=q_track,
                q_artist=q_artist,
                page_size=page_size,
                page=page,
                s_track_rating="desc")
            response = response.get("message")
        except Exception as e:
            logger.error(e)
        return response

    @staticmethod
    def get_lyrics_by_match_query(musixmatch_api: Musixmatch, q_track: str, q_artist: str):
        response: dict = {}
        try:
            response: dict = musixmatch_api.matcher_lyrics_get(
                q_track=q_track, q_artist=q_artist)
            response = response.get("message")
        except Exception as e:
            logger.error(e)
        return response

    @staticmethod
    def extract_lyrics_from_matching(musixmatch_api: Musixmatch, q_track: str, q_artist: str):
        lyrics: str = ""
        try:
            response_matching: dict = __class__.get_lyrics_by_match_query(
                musixmatch_api=musixmatch_api,
                q_track=q_track,
                q_artist=q_artist)
            if isinstance(response_matching.get("body"), dict):
                lyrics: str = response_matching.get("body").get("lyrics", {}).get("lyrics_body", "")
        except Exception as e:
            logger.error(e)
        return lyrics