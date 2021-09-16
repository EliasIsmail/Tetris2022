from collections import OrderedDict
import pygame
import os, sys, json
from github import Github, InputGitTreeElement, GithubException
from easygui import textbox
from firebase import *


# Relative path

def relative_path(file_name):
    return os.path.join(getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))), file_name)


token = 'd469b0bf4c8196b2c8d57ad3e20657ddfa6d8854'
g = Github(token)
repo = g.get_user().get_repo('TetrisNew')
file = repo.get_contents("leaderboard.txt")

# Initialize pygame modules
pygame.mixer.pre_init(48000, -16, 2, 2096)
pygame.init()
pygame.mixer.music.set_volume(0.1)

# Set size of screen and menu elements 
MENU_WIDTH, MENU_HEIGHT = 1000, 800
BOARD_WIDTH, BOARD_HEIGHT = 10, 20
SCREEN = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
RECT_WIDTH = round(MENU_WIDTH/2.4)
RECT_HEIGHT = round(MENU_HEIGHT/10)

# Menu font and colors
menu_font = pygame.font.SysFont ("Times New Norman", round((MENU_HEIGHT+MENU_WIDTH)/20))
WHITE, GREEN, HOVER_COLOR, BLACK = (255, 255, 255), (58, 155, 11), (58, 65, 11), (0,0,0)

# Text for buttons
txt1, txt2, txt3, txt4, txt5, txt6, txt7 = "NEW GAME", "LEADERBOARD", "ABOUT", "EXIT", "MULTIPLAYER",\
     "BACK", "SINGLEPLAYER"

text1, text2, text3, text4, text5, text6, text7 = menu_font.render(txt1, True, GREEN), \
        menu_font.render(txt2, True, GREEN), menu_font.render(txt3, True, GREEN), menu_font.render(txt4, True, GREEN), \
            menu_font.render(txt5, True, GREEN), menu_font.render(txt6, True, GREEN),menu_font.render(txt7, True, GREEN)

# Text rectangles for buttons
text1_rect = text1.get_rect(center=(MENU_WIDTH/2, MENU_HEIGHT/2.5))
text2_rect = text2.get_rect(center=(MENU_WIDTH/2, MENU_HEIGHT/1.8))
text3_rect = text3.get_rect(center=(MENU_WIDTH/2, MENU_HEIGHT/1.4))
text4_rect = text4.get_rect(center=(MENU_WIDTH/2, MENU_HEIGHT/1.15))
text5_rect = text5.get_rect(center=(MENU_WIDTH/2, MENU_HEIGHT/2))
text6_rect = text6.get_rect(center=(MENU_WIDTH/2, MENU_HEIGHT/1.6))
text7_rect = text7.get_rect(center=(MENU_WIDTH/2, MENU_HEIGHT/1.6))
back_rect = text6.get_rect(center=(MENU_WIDTH/2, MENU_HEIGHT/1.2))

# EasyGui text strings
first_box_text = "Welcome to Eli's version of Tetris. This game is my first project in Python.\nClick Next for further info"
second_box_text = "To start a game of Tetris, you click the \"New Game\"-button on the Main Menu. " + \
    "From here, you can choose to play alone in single_player, or play against a friend in multiplayer!"
third_box_text = "The controls are as follows:\nPlayer 1:"

# Images
logo = pygame.image.load(relative_path("images/TetrisLogo.png"))
logo = pygame.transform.scale(logo, (round(MENU_WIDTH/2), round(MENU_HEIGHT/5)))
spc_path = relative_path("images/controls_singleplayer.png")
single_player_controls = pygame.image.load(spc_path)
mpc_path = relative_path("images/controls_multiplayer.png")
multi_player_controls = pygame.image.load(mpc_path)

# Show music
music_font = pygame.font.SysFont("microsoftsansserif",18)

class MenuElements:
    def __init__(self):
        self.song_index = 0
        self.current_song = ()
        self.next_song = ()
        self.music_paused = False
        self.main_color = WHITE
        self.music_color = BLACK
        #self.leaderboard = []
        self.leaderboard = OrderedDict()
    
    def show_music(self, title, artist, x, y, font, text_color, panel_color):
        music_text = font.render("Now playing: " + title + " by " + artist, True, text_color)
        SCREEN.fill(panel_color, music_text.get_rect(topleft=(x,y)))
        SCREEN.blit(music_text, (x,y))

    def download_leaderboard(self):
        return sorted(ref.order_by_child('Score').get(), key=lambda x:x['Score'], reverse=True)[:20]

    def upload_leaderboard(self):
        # with open("data.json", "r") as f:
	    #     file_contents = json.load(f)
        ref.set(self.leaderboard)

    def show_leaderboard(self):
        self.leaderboard = self.download_leaderboard()
        i = 1
        score_box_text = "Rank        Name                 Score         Date\n"
        for tuple in self.leaderboard:
            score_box_text += str(i) + ":" + tuple['Name'].rjust(16-len(str(i)) + len(tuple['Name'])-5) + \
                str(tuple['Score']).rjust(26-len(tuple['Name'])) + str(tuple['Date'].rjust(16)) + "\n"
            i += 1
        textbox("                    LEADERBOARD - TOP 20          ", "Tetris Leaderboard", score_box_text, False, None, True)



# Create instance of menu elements for further use
menu = MenuElements()
menu.download_leaderboard()