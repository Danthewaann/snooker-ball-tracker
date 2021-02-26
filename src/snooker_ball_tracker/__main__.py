import argparse
from snooker_ball_tracker.views.gui import GUI


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--settings", dest="settings_file", default=None)

    args = parser.parse_args()
    app = GUI(args)
    app.mainloop()
