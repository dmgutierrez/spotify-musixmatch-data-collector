from setuptools import setup, find_packages

name: str = "SpotMux"
version: str = "1.0.3"
license: str = "MIT"
author: str = "David Martin-Gutierrez"
author_email: str = "dmargutierrez@gmail.com"

setup(name=name,
      version=version,
      packages=find_packages(),
      license=license,
      author=author,
      author_email=author_email,
      python_requires='>=3.6',
      install_requires=['spotipy', 'coloredlogs',
                        'pycountry_convert',
                        'pandas', 'numpy',
                        'pymongo', 'pymusixmatch'])
