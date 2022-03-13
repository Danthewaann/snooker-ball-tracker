import sys

# This variable is set by pyinstaller if running from a frozen
# build. See http://pyinstaller.readthedocs.io/en/stable/runtime-information.html
IS_FROZEN = getattr(sys, "frozen", False)
