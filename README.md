# Snooker Ball Tracker

This project is a prototype that I developed in Python to demo an idea I had for an app that could automatically detect and track Snooker balls on a Snooker table.

The app would therefore be able to automatically score points based upon which ball was potted.

## Python version
Python => 3.6.9 

## Setup and Run
- Run `python setup.py install` to install all required modules and dependencies
- Run `python -m snooker_ball_tracker` to run the GUI app or;
- Run `python -m snooker_ball_tracker.ball_tracker_cli` to run the older CLI

## GUI Examples
The GUI provides an interface to allow you to configure the ball tracker in real-time as the app
is processing video. Currently only supports pre-recorded video.

When running the app click on the `Select File` button at the bottom, and use one of the provided video files located under `resources/videos/`.

### Interface screenshot

<img src="examples/gui-screenshot.png" width=100%></img>


## CLI Examples
The CLI was the original tool used to demonstrate the ball tracker.

### Image 1
`python ball_tracker_cli.py -i ../../resources/images/image-1.jpg --settings image-1`

<img src="examples/image-1-frame-1.jpg" width=100%></img>

### Image 2
`python ball_tracker_cli.py -i ../../resources/images/image-2.jpg --settings image-2 --crop`

<img src="examples/image-2-frame-1.jpg" width=100%></img>

### Video 1
`python ball_tracker_cli.py -v ../../resources/videos/pre-recorded-1.mp4 --settings pre_recorded_footage --crop`

<img src="examples/video-example.gif" width=100%></img>
