from menu_elements import *
from easygui import buttonbox, enterbox
from game import *
from game_controller import start_game_multiplayer, start_game_singleplayer

# #  Necessary for exportion to .exe file
# if getattr(sys, 'frozen', False):
#     current_path = os.path.dirname(sys.executable) # frozen
# else: 
#     current_path = os.path.dirname(os.path.realpath(__file__)) # unfrozen

def main():
    play_next_song()
    # Set icon and various
    pygame.display.set_caption("Tetris")
    icon = pygame.image.load(relative_path('images/Tetris.png'))
    pygame.display.set_icon(icon)

    # Booleans to control main menu loop
    menu_running = True
    main_menu = True
    new_game_screen = False
    leaderboard_screen = False
    about_screen = False
    # Buttons of main menu
    buttons = [
    [txt1, text1, text1_rect, False],
    [txt2, text2, text2_rect, False],
    [txt3, text3, text3_rect, False],
    [txt4, text4, text4_rect, False]
    ]
    main_menu_buttons = buttons
    # main loop
    while menu_running:
        if not menu.music_paused: play_next_song()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu_running = False
                elif event.key == pygame.K_m:
                    menu.music_paused = False
                    skip_song()
                elif event.key == pygame.K_c:
                    menu.main_color = BLACK if menu.main_color == WHITE else WHITE
                    menu.music_color = WHITE if menu.main_color == BLACK else BLACK
                elif event.key == pygame.K_b:
                    menu.music_paused = not menu.music_paused
                    pygame.mixer.music.pause() if menu.music_paused else pygame.mixer.music.unpause()
            elif event.type == pygame.MOUSEMOTION:
                for button in buttons:
                    if button[2].collidepoint(event.pos):
                        # Set the button's color to the hover color.
                        button[1] = menu_font.render(button[0], True, HOVER_COLOR)
                    else:
                        button[3] = False # Mouse is not hovering over button anymore
                        button[1] = menu_font.render(button[0], True, GREEN) # Otherwise reset the color to GREEN
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if main_menu:
                    if buttons[0][2].collidepoint(event.pos):
                        buttons = [[txt5, text5, text5_rect, False],[txt7, text7, text7_rect, False]]
                        main_menu = False
                        new_game_screen = True
                        buttons.append([txt6, text6, back_rect, False])
                    elif buttons[1][2].collidepoint(event.pos):
                        main_menu = False
                        leaderboard_screen = True
                    elif buttons[2][2].collidepoint(event.pos):
                        main_menu = False
                        about_screen = True
                    elif buttons[3][2].collidepoint(event.pos):
                        menu_running = False
                elif leaderboard_screen:
                    menu.show_leaderboard()
                    leaderboard_screen = False
                    main_menu = True
                elif about_screen:
                    name = buttonbox(title="Singleplayer controls", msg="", image=spc_path, choices=["Next", "Cancel"])
                    if name == "Next": 
                        buttonbox(title="Multiplayer controls", msg="", image=mpc_path, choices=["Alright!", "Cancel"])
                    # print(easygui.indexbox(msg=first_box_text, title="Welcome to Sprouts!", choices=("Exit", "Back", "Next"), image=None, default_choice="Yes", cancel_choice="Exit"))
                    # print(easygui.indexbox(msg=second_box_text, title="Welcome to Sprouts!", choices=("Exit", "Next"), image=None, default_choice="Yes", cancel_choice="Exit"))
                    about_screen = False
                    main_menu = True
                elif new_game_screen:
                    if buttons[0][2].collidepoint(event.pos) or buttons[1][2].collidepoint(event.pos):
                        if buttons[0][2].collidepoint(event.pos):
                            # START MULTIPLAYER
                            start_game_multiplayer()
                        if buttons[1][2].collidepoint(event.pos):
                            # START SINGLEPLAYER
                            name = enterbox(msg='Enter your name', title='Name input', default='', strip=True)
                            if name: 
                                single_player.name = name
                                if name in bøffel_names: start_game_singleplayer(mode=True)
                                else: start_game_singleplayer()
                            pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
                    if buttons[2][2].collidepoint(event.pos): # if BACK button is cicked
                        buttons = main_menu_buttons
                        main_menu = True
                        new_game_screen = False
        if (menu_running):      
            SCREEN.fill(menu.main_color)
            SCREEN.blit(logo,((MENU_WIDTH-1.25*RECT_WIDTH)/2,MENU_HEIGHT/6 - RECT_HEIGHT))
            for _, text, rect, _  in buttons:
                pygame.draw.rect(SCREEN, menu.main_color, rect)
                SCREEN.blit(text, rect)
            menu.show_music(menu.current_song[0], menu.current_song[1], 10, 770, music_font, menu.music_color, menu.main_color)
            pygame.display.flip()
        pygame.display.update()
    pygame.quit()