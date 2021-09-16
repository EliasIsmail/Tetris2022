import pyglet
import copy
import cv2
from menu_elements import *
from random import choice, shuffle, randint
from easygui import textbox
import ast

# Starting values
playtime_value = 200
max_speed = 32

# Current piece list and x values at start
cpls = [[0,0],[0,0],[0,0],[0,0]]
startX1 = (int) (BOARD_WIDTH/2)-1
startX2 = 17 + startX1

# Size of each block in board
block_size = 40

# Rotation lists for each piece
rotation_list_I = [[0,1],[1,1],[2,1],[3,1],4]
rotation_list_O = [[0,0],[0,1],[1,0],[1,1],2]
rotation_list_T = [[1,0],[0,1],[1,1],[2,1],3]
rotation_list_L = [[0,1],[1,1],[2,1],[2,0],3]
rotation_list_J = [[0,0],[0,1],[1,1],[2,1],3]
rotation_list_S = [[0,1],[1,0],[1,1],[2,0],3]
rotation_list_Z = [[1,0],[0,0],[1,1],[2,1],3]

# General game element colors
GRAY, BOMB = (168,168,168), (69, 69, 69)

# Colors of each piece 
OPIECE, IPIECE, TPIECE, LPIECE, JPIECE, SPIECE, ZPIECE = (255, 213, 0),\
    (51,223,255), (255,0,144), (255, 151, 28), (3, 65, 174), (114, 203, 59), (255, 50, 19)

# Fonts
game_music_font = pygame.font.SysFont("microsoftsansserif",13)
xxsmall_font = pygame.font.SysFont("microsoftsansserif",22)
xsmall_font = pygame.font.SysFont("microsoftsansserif", 26)
small_font = pygame.font.SysFont("microsoftsansserif", 28)
medium_font = pygame.font.SysFont("microsoftsansserif", 32)
large_font = pygame.font.SysFont("microsoftsansserif", 40)
huge_font = pygame.font.SysFont("microsoftsansserif",72)

# Text elements
draw_text = huge_font.render("DRAW!", True, OPIECE)
winner_text = huge_font.render("YOU WIN!", True, SPIECE)
loser_text = huge_font.render("YOU LOSE!", True, ZPIECE)
game_text = huge_font.render("GAME", True, ZPIECE)
over_text = huge_font.render("OVER", True, ZPIECE)
play_again_text = small_font.render("PRESS N TO PLAY AGAIN!", True, ZPIECE)

# Paddings
text_pad_y = 3.2
box_pad_y = 2
text_pad_x = 2.5
box_pad_x = 1.5

# Image elements 
knockout_image = pygame.image.load(relative_path('images/KO.png'))
bomb_image = pygame.image.load(relative_path('images/bomb.png'))

# Sound elements #
combo_sounds = []
for i in range(1, 8):
    combo_sounds.append(pygame.mixer.Sound(relative_path('sounds/gamesounds/combo' + str(i) + ".wav")))
knockout_sound = pygame.mixer.Sound(relative_path('sounds/gamesounds/knockoutsound.wav'))

# Song elements
list_of_songs = [('Dejlig', 'Jimilian ft. Fouli'), ('Wellerman', 'Nathan Evans'), ('Tetris 99', 'Tetris Inc'), \
                ('Tetris', '2PM'), ('SMS', 'Barcode Brothers'), ('Breaking Free (Remix)', 'HSM'), \
                ('Barbie Girl (Remix)', 'Aqua'), ('Come Get Your Love', 'Redbone'), ('Hot', 'Nik & Jay'), \
                ('Lets Groove Tonight', 'EW&F'), ('No Problem', 'Chase & Status'), ('Bet On It', 'Troy'), \
                ('Ievan Polkka', 'Miku Hatsune'), ('Wake Me Up', 'Avicii'), ('Toxic', 'Britney Spears'), \
                ('Rasputin', 'Boney M'), ('Filur', 'Larry 44 ft. Gilli'), ('Kickflipper', 'Razz'), \
                ('Se Venedig og Dø', 'Lone K'), ('Salami', 'Gustav Winckler'), ('In Your Eyes', 'The Weeknd'),\
                ('Dynamite', 'BTS'), ('Lordly', 'Feder ft. Alex Aiono'), ('Old Town Road', 'Lil Nas X'), \
                ('Arne', 'Fætr'), ('Lækker', 'Nik & Jay'), ('Mufasa', 'Timmy Trumpet'), ('Rock With U', 'Michael Jackson'), \
                ('Toss A Coin (Remix)', 'Jaskier'), ('Wild Eyes', 'Broiler'), ('Without You', 'Avicii'),
                ('Red Lights', 'Tiesto'), ('Kig Forbi', 'Johnson')]
shuffle(list_of_songs)

def play_next_song():
    if not pygame.mixer.music.get_busy():
        if menu.song_index == len(list_of_songs)-1: menu.song_index = 0
        if menu.current_song != (): menu.current_song = copy.deepcopy(menu.next_song)
        else: menu.current_song = list_of_songs[menu.song_index]
        pygame.mixer.music.load(relative_path('sounds/songs/' + list_of_songs[menu.song_index][0] + '.mp3'))
        pygame.mixer.music.play()
        pygame.event.wait()
        menu.song_index += 1
        menu.next_song = list_of_songs[menu.song_index]
        
def skip_song():
    menu.current_song = copy.deepcopy(menu.next_song)
    pygame.mixer.music.stop()
    pygame.mixer.music.load(relative_path('sounds/songs/' + list_of_songs[menu.song_index][0] + '.mp3'))
    pygame.mixer.music.play()
    pygame.event.wait()
    if menu.song_index == len(list_of_songs)-1: menu.song_index = 0
    else: menu.song_index += 1
    menu.next_song = list_of_songs[menu.song_index]

# Bøflerne elements
bøffel_names = ["Hoff", "Jacq", "Samson", "Brylling", "Eli", "Heber", "Freddy", "Bene",\
                "Svende", "Louis", "Gnibe", "Moar", "Trøffe", "Dits"]
bøffel_images = []
bøffel_videos = []
for i in range(1,169):
    image = pygame.image.load(relative_path('bøflerne/images/' + str(i) + '.PNG'))
    image = pygame.transform.scale(image, (180, 180))
    bøffel_images.append(image)

for i in range(1,33):
    bøffel_videos.append(relative_path('bøflerne/videos/' + str(i) + '.mp4'))

### PLAY VIDEO WITHOUT SOUND ###
# def play_video(i):
#     cap = cv2.VideoCapture(bøffel_videos[i])
#     cv2.namedWindow('Bøffelvideo' + str(i),cv2.WINDOW_AUTOSIZE)
#     while cap.isOpened():
#         ret,frame = cap.read()
#         if ret == True:
#             cv2.imshow('frame', frame)
#             cv2.waitKey(50)
#             if cv2.waitKey(1) == 27:
#                 break  # esc to quit
#         else: break
#     cap.release()
#     cv2.destroyAllWindows()

### PLAY VIDEO WITH SOUND ###
def play_video(i):
    player = pyglet.media.Player()
    # source = pyglet.media.StreamingSource()
    video = pyglet.media.load(bøffel_videos[i])
    vid = cv2.VideoCapture(bøffel_videos[i])
    height = int  (vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int (vid.get(cv2.CAP_PROP_FRAME_WIDTH))

    window=pyglet.window.Window(width, height ,caption="Bøffel video")
    player = pyglet.media.Player()
    player.queue(video)
    player.play()

    @window.event
    def on_draw():
        if player.source and player.source.video_format:
            player.get_texture().blit(0,0)

    @window.event 
    def on_key_press(symbol, modifier): 
        if symbol == pyglet.window.key.ESCAPE:
            player.volume = 0
            window.close()
            return True

    @window.event   
    def on_close():
        window.close()
        player.volume = 0
        return True
        
    pyglet.app.run()
