# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 19:45:03 2018

@author: dmarg
"""

from spotipy import Spotify
from spotipy.client import SpotifyException
from spotipy.oauth2 import SpotifyOAuth, SpotifyOauthError
from ..models.doument_models import (SpotifyTrackDoc,
                                     SpotifyAlbumDoc, SpotifyArtistDoc)
from ..helper.settings import logger


class SpotifyManager(object):
    developer_categories_uri: str =\
        "https://developer.spotify.com/documentation/web-api/reference/browse/get-list-categories/"

    def __init__(self, sp_client_id: str, sp_client_secret: str, sp_username: str, sp_redirect_uri: str,
                 sp_scope: str):
        self.client_id: str = sp_client_id
        self.secret: str = sp_client_secret
        self.username: str = sp_username
        self.redirect_uri: str = sp_redirect_uri
        self.scope: str = sp_scope
        self.sp_oauth: SpotifyOAuth = SpotifyOAuth(
            username=sp_username,
            client_id=sp_client_id,
            client_secret=sp_client_secret,
            redirect_uri=sp_redirect_uri,
            scope=sp_scope)
        self.token: str = str()
        self.token_info: dict = dict()
        self.sp_api: Spotify = Spotify()

    def set_up_authentication_via_token(self):
        try:
            self.token_info: dict = self.sp_oauth.get_access_token()
            if not self.token_info:
                auth_url: str = self.sp_oauth.get_authorize_url()
                logger.info(auth_url)
                response = input('Paste the above link into your browser, then paste the redirect url here: ')

                code = self.sp_oauth.parse_response_code(response)
                self.token_info = self.sp_oauth.get_access_token(code)

            self.token: str = self.token_info.get('access_token')
        except SpotifyException as e:
            logger.error(e)
        except SpotifyOauthError as oauthErr:
            logger.error(oauthErr)

    def init_spotify_connector(self):
        try:
            self.set_up_authentication_via_token()
            self.sp_api: Spotify = Spotify(auth=self.token)
            logger.info('Connected to Spotify API')
        except Exception as e:
            logger.error(e)

    def refresh_access_token(self):
        try:
            self.token_info: dict = self.sp_oauth.refresh_access_token(self.token_info.get('refresh_token'))
            self.token: dict = self.token_info.get('access_token')
            self.sp_api: Spotify = Spotify(auth=self.token)
        except Exception as e:
            logger.error(e)

    @staticmethod
    def get_categories_items_by_country(sp_api: Spotify, country: str = 'ES', locale: str = "en_EN",
                                        limit: int = 50):
        categories_items: list = []
        try:
            offset = 0
            done = -limit
            while done <= 0:
                try:
                    res: dict = sp_api.categories(limit=limit, offset=offset, country=country, locale=locale)
                    categories_raw = res.get("categories").get("items")
                    categories_items += categories_raw

                    # Check if finish
                    if len(categories_raw) < limit:
                        done = 1
                    else:
                        done = -1
                    offset += limit
                except SpotifyException as e:
                    logger.warning(e)
                    continue
        except Exception as e:
            logger.error(e)
        return categories_items

    @staticmethod
    def get_categories_by_name(sp_api: Spotify, categories: list, country: str = 'ES',
                               locale: str = "en_EN", limit: int = 50):
        categories_items: list = []
        try:
            # 1. Get all categories associated to a country
            all_category_items: list = __class__.get_categories_items_by_country(
                sp_api=sp_api, country=country, locale=locale, limit=limit)
            categories_items = [category for category in all_category_items if category.get("name") in categories]
        except Exception as e:
            logger.error(e)
        return categories_items

    def get_all_countries_playlists_ids(self, sp_api: Spotify, countries: list, locale: str = "en_EN",
                                        limit: int = 50):
        country_playlists_data: dict = {}
        try:
            if not self.sp_oauth.is_token_expired(self.token_info):
                for idx, country in enumerate(countries):

                    logger.info("Collecting Playlists from %s, %s/%s", country, idx + 1, len(countries))

                    # Get Category ID
                    category_items: list = self.get_categories_items_by_country(
                        sp_api=sp_api, country=country, locale=locale, limit=limit)

                    # Get Playlists
                    country_playlists: list = []
                    category_ids: list = []
                    for ii, category in enumerate(category_items):
                        done = True
                        offset = 0
                        try:
                            while done:
                                res: dict = self.sp_api.category_playlists(
                                    category_id=category.get('id', -1),
                                    country=country,
                                    limit=limit,
                                    offset=offset)
                                cat_playlists: list = res.get('playlists').get('items')
                                country_playlists += cat_playlists
                                # Update categories
                                category_ids += [category.get('id', -1) for ct in range(
                                    len(cat_playlists))]

                                if len(cat_playlists) < limit:
                                    done = False
                                else:
                                    offset += limit
                        except SpotifyException as e:
                            logger.warning(e)
                            self.refresh_access_token()
                            continue

                    # Save partial data into dictionary
                    playlists_ids = [i.get('id', -1) for i in country_playlists if i is not None]
                    current_country = [country for k in range(
                        len(playlists_ids))]
                    current_categories = category_ids

                    playlist_data_dct: dict = dict(zip(playlists_ids,
                                                       zip(current_country,
                                                           current_categories)))
                    country_playlists_data.update(playlist_data_dct)

            else:
                self.refresh_access_token()
                self.get_all_countries_playlists_ids(
                    sp_api=sp_api, countries=countries, limit=limit)
        except Exception as e:
            logger.error(e)
        return country_playlists_data

    def get_countries_playlists_ids_by_categories(self, sp_api: Spotify,
                                                  categories: list,
                                                  countries: list,
                                                  locale: str = "en_EN",
                                                  limit: int = 50):
        country_playlists_data: dict = {}
        try:
            if not self.sp_oauth.is_token_expired(self.token_info):
                for idx, country in enumerate(countries):

                    logger.info("Collecting Playlists from %s, %s/%s", country, idx + 1, len(countries))

                    # Get Category ID
                    category_items: list = self.get_categories_by_name(
                        categories=categories,
                        sp_api=sp_api, country=country,
                        locale=locale)

                    if len(category_items) > 0:
                        # Get Playlists
                        country_playlists: list = []
                        category_ids: list = []
                        for ii, category in enumerate(category_items):
                            done = True
                            offset = 0
                            try:
                                while done:
                                    res: dict = self.sp_api.category_playlists(
                                        category_id=category.get('id', -1),
                                        country=country,
                                        limit=limit,
                                        offset=offset)
                                    cat_playlists = res.get('playlists').get('items')
                                    country_playlists += cat_playlists
                                    category_ids += [category.get('id', -1) for ct in range(
                                        len(cat_playlists))]
                                    if len(cat_playlists) < limit:
                                        done = False
                                    else:
                                        offset += limit

                            except Exception as e:
                                logger.warning(e)
                                continue

                            # Save partial data into dictionary
                            playlists_ids = [i.get('id', -1) for i in country_playlists if i is not None]
                            current_country = [country for ct in range(
                                len(playlists_ids))]
                            current_categories = category_ids

                            playlist_data_dct: dict = dict(zip(playlists_ids,
                                                               zip(current_country,
                                                                   current_categories)))
                            country_playlists_data.update(playlist_data_dct)
                    else:
                        logger.warning("No categories found at country %s by querying %s.\n"
                                       "Please check Spotify categories at %s",
                                       country, ",".join(categories), self.developer_categories_uri)
            else:
                self.refresh_access_token()
                self.get_countries_playlists_ids_by_categories(
                    sp_api=sp_api, categories=categories, countries=countries, limit=limit)
        except SpotifyException as oauthErr:
            logger.warning(str(oauthErr))
            self.get_countries_playlists_ids_by_categories(
                sp_api=sp_api, categories=categories, countries=countries, limit=limit)
        except Exception as e:
            logger.error(e)
        return country_playlists_data

    @staticmethod
    def get_track_information(sp_api: Spotify, base_track: dict, playlist_name: str, market: str,
                              category: str):
        track_data: SpotifyTrackDoc = object.__new__(SpotifyTrackDoc)
        try:
            audio_features: dict = __class__.get_track_audio_features(
                sp_api=sp_api, base_track=base_track)

            if audio_features:
                track: dict = sp_api.track(track_id=base_track.get("id"))
                track_data: SpotifyTrackDoc = SpotifyTrackDoc(
                    track=track,
                    playlist_name=playlist_name,
                    country=market,
                    category=category,
                    audio_features=audio_features)

        except Exception as e:
            logger.error(e)
            return None
        return track_data

    @staticmethod
    def get_track_audio_features(sp_api: Spotify, base_track: dict):
        audio_features: dict = dict()
        try:
            track_id: str = base_track.get('id')
            res: list = sp_api.audio_features([track_id])
            audio_features: dict = res[0]
            audio_features.pop('duration_ms', None)
            audio_features.pop('track_href', None)
        except Exception as e:
            logger.error(e)
        return audio_features

    @staticmethod
    def get_album_information_from_track(sp_api: Spotify, base_track: dict):
        album_data: SpotifyAlbumDoc = object.__new__(SpotifyAlbumDoc)
        try:
            base_album: dict = base_track.get("album")
            album: dict = sp_api.album(album_id=base_album.get("id"))
            album_data: SpotifyAlbumDoc = SpotifyAlbumDoc(album=album)

        except Exception as e:
            logger.error(e)
        return album_data

    @staticmethod
    def get_artist_information(sp_api: Spotify, base_track: dict):
        artist_data: list = []
        try:
            artists: list = base_track['artists']
            artists_obj: list = [sp_api.artist(artist.get('id')) for artist in artists]
            artist_data += [SpotifyArtistDoc(artist=artist) for artist in artists_obj]
        except Exception as e:
            logger.error(e)
        return artist_data