from typing import Dict, List, NamedTuple, TypeVar

import cv2
import numpy as np
import numpy.typing as npt

Shape = TypeVar("Shape")
DType = TypeVar("DType")
Keypoints = Dict[str, List[cv2.KeyPoint]]
Frame = npt.NDArray[np.float64]


class Image(NamedTuple):
    frame: Frame
    binary_frame: Frame
    hsv_frame: Frame
