import pycountry_convert as pc
from helper.settings import logger
import os


def get_regions_by_markets(markets: list):
    regions: list = []
    try:
        regions = list(set([
            pc.country_alpha2_to_continent_code(country_code)
            for country_code in markets]))
    except Exception as e:
        logger.error(e)
    return regions


def prepare_directory(dir_path_to_check: str):
    try:
        if not os.path.exists(dir_path_to_check):
            os.makedirs(dir_path_to_check)
    except Exception as e:
        logger.error(e)


def convert_country_to_continent(country_alpha2: str):
    country_continent_name: str = ""
    try:
        country_continent_code: str = pc.country_alpha2_to_continent_code(
            country_alpha2)
        country_continent_name: str = pc.convert_continent_code_to_continent_name(
            country_continent_code)
    except Exception as e:
        logger.error(e)
    return country_continent_name


def get_continents():
    continents: dict = {
        'NA': 'North America',
        'SA': 'South America',
        'AS': 'Asia',
        'OC': 'Australia',
        'AF': 'Africa',
        'EU': 'Europe'
    }
    return continents