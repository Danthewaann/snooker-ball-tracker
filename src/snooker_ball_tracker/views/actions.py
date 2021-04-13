def select_video_file_action(parent=None, ):
    """Select video file event handler.

    Gets a video file provided by the user and attempts to validate
    that it is in fact a valid video file.

    Passes the video file to the VideoProcessor thread for processing
    and display.

    :raises TypeError: If the video file is not valid will display an error box
    """
    video_file, _ = QtWidgets.QFileDialog().getOpenFileName(parent, "Select Video File", "")

    if not video_file:
        return

    try:
        video_file_stream = cv2.VideoCapture(video_file)
        if not video_file_stream.isOpened():
            raise TypeError
    except:
        error = QtWidgets.QMessageBox(parent)
        error.setWindowTitle("Invalid Video File!")
        error.setText('Invalid file, please select a video file!')
        error.exec_()
        return

    return video_file

    # self.video_player.play = False
    # self.start_video_player()