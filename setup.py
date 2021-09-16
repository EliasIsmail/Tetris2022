import cx_Freeze
from game_elements import bøffel_videos, list_of_songs

include_files = []
for i in range (1,8):
    include_files.append('sounds/gamesounds/combo' + str(i) + '.wav')
include_files.append('sounds/gamesounds/knockoutsound.wav')

for (name, artist) in list_of_songs:
    include_files.append('sounds/songs/' + name + '.mp3')

for i in range(1,15):
    include_files.append("bøflerne/images/" + str(i) + ".PNG")

for video in bøffel_videos:
    include_files.append(video)

include_files.append('images/alternate_singleplayer_controls.png')
include_files.append('images/bomb.png')
include_files.append('images/controls_multiplayer.png')
include_files.append('images/controls_singleplayer.png')
include_files.append('images/KO.png')
include_files.append('images/Tetris.png')
include_files.append('images/TetrisLogo.png')

executables = [cx_Freeze.Executable(
                script="Menu.py",
                base = "Win32GUI",
                icon = "images/Tetris.ico")]

cx_Freeze.setup(
    name="Tetris",
    version="1.0",
    options={"build_exe": {"packages":["pygame", "copy", "random", "os","sys","easygui", "pyglet", "cv2", "operator", "pickle", "numpy"],
                           "include_files": include_files}},
    description="Mit første spil. Tetris 06/10/2020",
    executables = executables

    )