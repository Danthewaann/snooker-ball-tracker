try:
    __version__ = (
        __import__("pkg_resources").get_distribution("snooker_ball_tracker").version
    )
except Exception:
    __version__ = "unknown"
