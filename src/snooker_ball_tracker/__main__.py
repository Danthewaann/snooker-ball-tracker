import tkinter as tk
import cv2
import imutils
import snooker_ball_tracker.settings as s
import numpy as np
import time
from snooker_ball_tracker.views.gui import GUI

# class SplashScreen:
#     def __init__(self, root):
#         self.root = root
#         self.a = tk.Toplevel()
#         self.percentage = 0
#         tk.Label(self.a,text="I am loading screen").pack()
#         self.load = tk.Label(self.a,text=f"Loading...{self.percentage}%")
#         self.load.pack()
#         self.load_bar()

#     def load_bar(self):
#         self.percentage +=5
#         self.load.config(text=f"Loading...{self.percentage}%")
#         if self.percentage == 100:
#             self.a.destroy()
#             self.root.deiconify()
#             return
#         else:
#             self.root.after(100,self.load_bar)


if __name__ == "__main__":
    app = GUI()
    # root.withdraw()
    # SplashScreen(app)
    app.mainloop()