from ..managers.spotify_manager import SpotifyManager
from ..managers.musicmatch_manager import MusixmatchManager
from ..helper.settings import logger
from ..models.doument_models import (PlaylistDataDoc, SpotifyTrackDoc,
                                     SpotifyAlbumDoc)
from spotipy.oauth2 import SpotifyOauthError
from collections import defaultdict


class MusicManager(object):
    def __init__(self, music_manager_params: dict):
        self.spotify_manager: SpotifyManager = SpotifyManager(
            sp_client_id=music_manager_params.get("sp_client_id"),
            sp_client_secret=music_manager_params.get("sp_client_secret"),
            sp_redirect_uri=music_manager_params.get("sp_redirect_uri"),
            sp_username=music_manager_params.get("sp_username"),
            sp_scope=music_manager_params.get("sp_scope"))

        self.musixmatch_manager: MusixmatchManager = MusixmatchManager(
            api_key=music_manager_params.get("musixmatch_api_key"))

    def set_up_spotify_connection(self):
        self.spotify_manager.init_spotify_connector()

    def extract_data_from_spotify_playlist(self, playlist_id: str, market: str, category: str):
        playlist_data_doc: PlaylistDataDoc = object.__new__(PlaylistDataDoc)
        try:
            if not self.spotify_manager.sp_oauth.is_token_expired(self.spotify_manager.token_info):
                playlist: dict = self.spotify_manager.sp_api.playlist(
                    playlist_id=playlist_id,
                    market=market)
                tracks: list = playlist.get("tracks").get("items")
                playlist_name: str = playlist.get("name")
                PlaylistDataDoc.__init__(playlist_data_doc,
                                         tracks=[], albums=[],
                                         artists=[])
                for j, track_item in enumerate(tracks):
                    try:
                        logger.info("Processing Track ... %s/%s", j + 1, len(tracks))
                        items: dict = self.process_track_item(
                            spotify_manager=self.spotify_manager,
                            musixmatch_manager=self.musixmatch_manager,
                            track_item=track_item,
                            playlist_name=playlist_name,
                            market=market,
                            category=category)

                        # If there is data, update the list
                        if items.get("track") and items.get("album") and items.get("artists"):
                            playlist_data_doc.tracks += [items.get("track")]
                            playlist_data_doc.albums += [items.get("album")]
                            playlist_data_doc.artists += items.get("artists")

                    except SpotifyOauthError as oauthErr:
                        logger.warning(str(oauthErr))
                        self.spotify_manager.refresh_access_token()
                        continue

                    except Exception:
                        logger.warning('It was not possible to extract the information of the Track!')
                        continue
            else:
                self.spotify_manager.refresh_access_token()
                playlist_data_doc: PlaylistDataDoc = self.extract_data_from_spotify_playlist(
                    playlist_id=playlist_id,
                    market=market,
                    category=category)
        except SpotifyOauthError as oauthErr:
            logger.warning(str(oauthErr))
            self.spotify_manager.refresh_access_token()
            playlist_data_doc: PlaylistDataDoc = self.extract_data_from_spotify_playlist(
                playlist_id=playlist_id,
                market=market,
                category=category)
        except Exception as e:
            logger.error(e)
        return playlist_data_doc

    @staticmethod
    def process_track_item(spotify_manager: SpotifyManager, musixmatch_manager: MusixmatchManager,
                           track_item: dict, playlist_name: str, market: str, category: str):
        items: dict = defaultdict()
        try:
            base_track: dict = track_item.get("track")
            track_id: int = base_track.get("id")
            preview: str = base_track.get("preview_url")

            if base_track is not None and track_id is not None and preview is not None:
                # 1. Album
                spot_album_doc: SpotifyAlbumDoc = spotify_manager.get_album_information_from_track(
                    sp_api=spotify_manager.sp_api, base_track=base_track)
                items["album"]: SpotifyAlbumDoc = spot_album_doc if \
                    getattr(spot_album_doc, 'id', -1) != -1 else {}

                # 2. Artists
                spot_art_docs: list = spotify_manager.get_artist_information(
                    sp_api=spotify_manager.sp_api, base_track=base_track)
                items["artists"]: list = spot_art_docs

                # 3. Track + lyrics
                spot_track_doc: SpotifyTrackDoc = spotify_manager.get_track_information(
                    sp_api=spotify_manager.sp_api,
                    base_track=base_track,
                    playlist_name=playlist_name,
                    market=market,
                    category=category)
                lyrics: str = musixmatch_manager.extract_lyrics_from_matching(
                    musixmatch_api=musixmatch_manager.musixmatch,
                    q_track=spot_track_doc.name, q_artist=spot_art_docs[0].name)
                spot_track_doc.lyrics: str = lyrics
                items["track"]: SpotifyTrackDoc = spot_track_doc if \
                    getattr(spot_track_doc, 'id', -1) != -1 else []

        except SpotifyOauthError as oauthErr:
            logger.warning(str(oauthErr))
            spotify_manager.refresh_access_token()
            items: dict = __class__.process_track_item(
                spotify_manager=spotify_manager,
                musixmatch_manager=musixmatch_manager,
                track_item=track_item,
                playlist_name=playlist_name,
                market=market,
                category=category)
        except Exception as e:
            logger.warning('It was not possible to extract the information of the current track!')
        return items
