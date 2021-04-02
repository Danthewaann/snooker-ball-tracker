from setuptools import setup, find_packages

setup(
    name='snooker_ball_tracker',
    version='0.1.dev0',
    description='Demo app that tracks balls on a Snooker table',
    author='Daniel Black',
    author_email='danielcrblack@gmail.com',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=['numpy', 'imutils', 'opencv-python', 'Pillow', 'pyqt5']
)
