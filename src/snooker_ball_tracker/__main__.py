import tkinter as tk
import cv2
import imutils
import snooker_ball_tracker.settings as s
import numpy as np
import time
from snooker_ball_tracker.views.gui import GUI


if __name__ == "__main__":
    app = GUI()
    app.mainloop()