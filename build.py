import os
import pathlib
import shutil

import PyInstaller.__main__
import pyinstaller_versionfile
import tomlkit

BASE_DIR = pathlib.Path(__file__).parent


os.environ["PYTHONOPTIMIZE"] = "1"


def _get_project_meta():
    with open('./pyproject.toml') as pyproject:
        file_contents = pyproject.read()

    return tomlkit.parse(file_contents)['tool']['poetry']


pkg_meta = _get_project_meta()
project = str(pkg_meta['name'])
version = str(pkg_meta['version'])


pyinstaller_versionfile.create_versionfile(
    output_file=str(BASE_DIR / "version_file.txt"),
    version=version + ".0",
    file_description="Snooker Ball Tracker",
    internal_name="Snooker Ball Tracker",
    original_filename=project + ".exe",
    product_name="Snooker Ball Tracker"
)


PyInstaller.__main__.run([
    str(BASE_DIR / "src" / project / "gui.py"),
    "--onefile",
    "--windowed",
    "-y",
    "--add-data", str(BASE_DIR / "src" / project / "resources" / "icon.ico") + ":icon.ico",
    "-i", str(BASE_DIR / "src" / project / "resources" / "icon.ico"),
    "-n", project + ".exe",
    "--clean",
    "--version-file", str(BASE_DIR / "version_file.txt")
])

shutil.copy(str(BASE_DIR / "src" / project / "resources" / "icon.ico"), str(BASE_DIR / "dist"))
shutil.copy(str(BASE_DIR / "src" / project / "resources" / "default_settings.json"), str(BASE_DIR / "dist"))
