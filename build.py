import os
import pathlib
import shutil
import sys

import PyInstaller.__main__
import pyinstaller_versionfile
from setuptools.config import read_configuration

from src.snooker_ball_tracker import __version__

BASE_DIR = pathlib.Path(__file__).parent
CONF = read_configuration(BASE_DIR / "setup.cfg")


os.environ["PYTHONOPTIMIZE"] = "1"


pyinstaller_versionfile.create_versionfile(
    output_file=str(BASE_DIR / "version_file.txt"),
    version=__version__+".0",
    file_description="Snooker Ball Tracker",
    internal_name="Snooker Ball Tracker",
    original_filename=CONF["metadata"]["name"]+".exe",
    product_name="Snooker Ball Tracker"
)


PyInstaller.__main__.run([
    str(BASE_DIR / "src" / CONF["metadata"]["name"] / "gui.py"),
    "--onefile",
    "--windowed",
    "-y",
    "--add-data", str(BASE_DIR / "src" / CONF["metadata"]["name"] / "icon.ico") + ":icon.ico",
    "-i", str(BASE_DIR / "src" / CONF["metadata"]["name"] / "icon.ico"),
    "-n", CONF["metadata"]["name"]+".exe",
    "--clean",
    "--version-file", str(BASE_DIR / "version_file.txt")
])
