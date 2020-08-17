from setuptools import setup, find_packages

name: str = "spotmux"
version: str = "1.0.0"
license: str = "MIT"
author: str = "David Martin-Gutierrez"
author_email: str = "dmargutierrez@gmail.com"

setup(name=name,
      version=version,
      packages=find_packages(),
      license=license,
      author=author,
      author_email=author_email,
      python_requires='>=3.6'
      )
