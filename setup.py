from setuptools import setup, find_packages

setup(
    name='snooker-ball-tracker-python',
    version='0.1.dev0',
    description='Demo app that tracks balls on a Snooker table',
    author='Daniel Black',
    author_email='danielcrblack@gmail.com',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=['numpy>=1.18.0', 'imutils>=0.5.3', 'requests', 'opencv-python==4.1.2.30', 'Pillow']
)
