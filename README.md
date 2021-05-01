# Snooker Ball Tracker

This project is a prototype that I developed in Python to demo an idea I had for a program that could automatically detect and track Snooker balls on a Snooker table. The program would therefore be able to automatically score points based upon which ball was potted.

The program allows you to configure all the settings that are used by the ball tracker, from how it detects colours to how it detects balls. It also provides features that allows you to see what the ball trackers sees. 

## Python version
Python => 3.8.5

## Setup and Run
- Run `python setup.py install` to install all required modules and dependencies
- Run `python -m snooker_ball_tracker.gui` to run the Video GUI or;
- Run `python -m snooker_ball_tracker.cli` to run the Image CLI

## Video GUI Examples
The Video GUI provides an interface to allow you to configure the ball tracker in real-time as the app
is processing video. Currently only supports pre-recorded video.

### Interface screenshot

<img src="examples/gui-screenshot.png" width=100%></img>

### Video Example

<img src="examples/video-example.gif" width=100%></img>

## Image CLI Examples
The Image CLI supports processing images.

### Image 1
    python src/snooker_ball_tracker/cli.py \
        resources/images/image-1.jpg --settings resources/config/image_1.json

<img src="examples/image-1-frame-1.jpg" width=100%></img>

### Image 2
    python src/snooker_ball_tracker/cli.py \
        resources/images/image-2.jpg --settings resources/config/image_2.json

<img src="examples/image-2-frame-1.jpg" width=100%></img>
