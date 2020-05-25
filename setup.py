from setuptools import setup, find_packages

setup(
    name='PlayerClientMPD',
    version='1.0.0',
    url='https://github.com/JimmyAdams/GMPC_Extended_Manipulation',
    author='Jakub Adamec',
    author_email='xadame41@stud.fit.vutbr.cz',
    description='Player MPD',
    package_data = {"PlayerClientMPD" : ["playlists", "icons/*"]},
    packages=find_packages(),
    install_requires=['numpy >= 1.11.1',
     'PyQt5',
     'python-vlc',
     'mutagen',
     'musicbrainzngs',
     'audio_metadata',
     'eyed3',
     'objectpath',
     'scipy',
     'pydub',
     'soundfile',
     'wave']
)
