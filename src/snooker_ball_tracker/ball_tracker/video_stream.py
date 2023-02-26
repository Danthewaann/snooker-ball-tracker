from __future__ import annotations

from abc import ABC, abstractmethod
from queue import Queue
from typing import TYPE_CHECKING

import imutils

if TYPE_CHECKING:
    from . import ColourDetectionSettings, VideoPlayer
    from .types import Frame


class VideoStream(ABC):

    Q: Queue[Frame]
    _video_player: VideoPlayer
    _colour_settings: ColourDetectionSettings

    def transform_frame(self, frame: Frame | None) -> Frame | None:
        """Performs initial operations on `frame` before it is properly processed

        :param frame: frame to process
        :return: processed frame
        """
        if frame is not None:
            # resize the frame if width is provided
            resized_frame: Frame = imutils.resize(frame, width=self._video_player.width)
            # set video player height to height of resized frame
            self._video_player.height = resized_frame.shape[0]
            return resized_frame
        return None

    @abstractmethod
    def start(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def read(self) -> Frame:
        raise NotImplementedError

    @abstractmethod
    def running(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def more(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def stop(self) -> None:
        raise NotImplementedError
