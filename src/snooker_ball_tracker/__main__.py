import argparse
from snooker_ball_tracker.views.gui import GUI


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--settings", dest="settings_file", default=None, 
                        help="Use settings from JSON file")
    parser.add_argument("--no-splash", dest="splash", action="store_false", default=True, 
                        help="Lanuch GUI without splash screen")

    args = parser.parse_args()
    GUI(args).mainloop()
