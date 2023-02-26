from copy import deepcopy

import PyQt5.QtWidgets as QtWidgets

from snooker_ball_tracker.ball_tracker import (
    BallDetectionSettings,
    ColourDetectionSettings,
)
from snooker_ball_tracker.settings import settings as s


def select_video_file_action(*args) -> str:
    """Select video file action handler.

    Gets a video file provided by the user and attempts to validate
    that it is in fact a valid video file.

    :raises TypeError: If the video file is not valid will display an error box
    :return: video file path or None
    """
    video_file, _ = QtWidgets.QFileDialog().getOpenFileName(
        None, "Select Video File", ""
    )
    return video_file


def load_settings_action(*args) -> tuple:
    """Load settings from user provided file

    :return: path of loaded settings file, loaded colour settings
    and loaded ball settings
    """
    colours_settings = {}
    ball_settings = {}
    settings_file, _ = QtWidgets.QFileDialog().getOpenFileName(
        None, "Load Settings", ""
    )

    if not settings_file:
        return

    success, error = s.load(settings_file)

    if success:
        colours_settings = deepcopy(s.COLOUR_DETECTION_SETTINGS)
        ball_settings = deepcopy(s.BALL_DETECTION_SETTINGS)
    else:
        error = QtWidgets.QMessageBox(None)
        error.setWindowTitle("Invalid Settings File!")
        error.setText("Invalid file, please select a valid json file!")
        error.exec_()

    return settings_file, colours_settings, ball_settings


def save_settings_action(
    colour_settings: ColourDetectionSettings,
    ball_settings: BallDetectionSettings,
    settings_file: str,
) -> str:
    """Save settings to user provided file

    :param colour_settings: colour settings to save
    :param ball_settings: ball settings to save
    :param settings_file: settings file path to write to
    :return: settings file we saved to
    """
    settings_file, _ = QtWidgets.QFileDialog().getSaveFileName(
        None, "Save Settings", settings_file
    )

    if not settings_file:
        return

    success, error = s.save(
        settings_file,
        settings={
            "COLOUR_DETECTION_SETTINGS": colour_settings.settings,
            "BALL_DETECTION_SETTINGS": ball_settings.settings,
        },
    )

    if success:
        s.COLOUR_DETECTION_SETTINGS = deepcopy(colour_settings.settings)
        s.BALL_DETECTION_SETTINGS = deepcopy(ball_settings.settings)
    else:
        error = QtWidgets.QMessageBox(None)
        error.setWindowTitle("Failed to Save Settings!")
        error.setText(f"Failed to save settings to '{settings_file}'\nReason: {error}")
        error.exec_()

    return settings_file
