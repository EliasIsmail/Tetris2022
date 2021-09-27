from game_view import *
from player import *
from random import randrange
from operator import itemgetter
from datetime import date
import time

class Game():
    def __init__(self, multiplayer=False, bøffel_mode = False):
        self.running = True
        self.paused = False
        self.over = False
        self.playtime_value = playtime_value
        self.paused_time = 0
        self.clock = pygame.time.Clock()
        self.multiplayer = multiplayer
        self.last_fall_time = time.time()
        self.fall_frequency = 0.72
        self.last_move_side_time = time.time()
        self.move_side_frequency = 0.15
        self.move_down_frequency = 0.10
        self.last_move_down_time = time.time()
        self.speed_value = 1
        self.score_threshold = 1000
        self.image_threshold = 1000
        self.video_threshold = 5000
        self.bøffel_mode = bøffel_mode
        self.bøffel_image_index = randint(0,len(bøffel_images)-1)
        self.bøffel_video_index = randint(0,len(bøffel_videos)-1)
        self.view = GameView()
        self.new_highscore = False
        self.has_checked_score = False
        self.set_game()

    def set_game(self):
        self.view.game = self

### NEW GAMES ###

    def new_game_multiplayer(self, players):
        if self.over:
            player1.reset_values() ; player2.reset_values()
            self.over = False
            pygame.mixer.music.play()
            self.playtime_value = playtime_value
        for player in players:
            self.view.clear_lines(player)
            self.view.reset_lines(player)
            player.lines_to_be_added = 0
            self.generate_random_current_piece(player)
            self.add_piece_to_lines(player)
            self.view.draw_lines(player) ; self.view.draw_right_side(player)
            self.view.draw_top()

    def new_game_singleplayer(self, player):
        self.view.reset_lines(player)
        player.reset_values() ; player.reset_moves()
        self.generate_random_current_piece(player)
        self.add_piece_to_lines(player)
        self.view.draw_right_side(player)
        self.view.draw_lines(player)

### IS GAME OVER / IS PLAYER KNOCKED OUT ? ###

    def is_over_multiplayer(self):
        self.over = True
        self.view.show_game_over_multiplayer(players)

    def is_player_knocked_out(self, player):
        for i in range(4):
            [x,y] = player.cp_list[i] 
            if player.lines[y-player.ymin][x-player.xmin] != self.view.board_color: return True
        return False

### UPDATE LINES ###

    def add_lines(self, player, value):
        copy_lines = copy.deepcopy(player.lines)
        for i in range(19-value, 0, -1):
            player.lines[i] = copy_lines[i+value].copy()
        for i in range(0,value):
            player.lines[19-i] = self.generate_random_gray_line()

    def add_piece_to_lines(self, player):
        for n in range(4):
            [x,y] = player.cp_list[n]
            color = player.cp_list[5]
            player.lines[y-player.ymin][x-player.xmin] = color

    def remove_piece_from_lines(self, player):
        for n in range(4):
            [x,y] = player.cp_list[n]
            player.lines[y-player.ymin][x-player.xmin] = self.view.board_color

### KEY EVENTS ###

    def move_piece(self, player):
        val, i = 0,0
        if player.key_bools[1]: i, val = 1, 1
        elif player.key_bools[2]: i, val = 0, 1
        elif player.key_bools[0]: i, val = 0, -1
        self.remove_piece_from_lines(player)
        for n in range(4):
            player.cp_list[n][i] += val
        self.add_piece_to_lines(player)
        player.s_list = copy.deepcopy(player.cp_list)
        if player == single_player and i == 1:
            player.score_value += 2 if player.piece_dropped else 1
            self.check_level(player)


    def hold_piece(self, player):
        if player.hold:
            self.remove_piece_from_lines(player)
            if player.first_hold:
                player.first_hold = False
                player.held_piece = player.current_piece
                self.generate_new_current_piece(player)
            else:
                player.current_piece, player.held_piece = player.held_piece, player.current_piece
                player.cp_list = self.set_piece(player, player.current_piece)
                self.add_piece_to_lines(player)
                player.s_list = copy.deepcopy(player.cp_list)
                player.hold = False

    def drop_piece(self, player):
        self.remove_piece_from_lines(player)
        player.key_bools[1]= True
        player.piece_dropped = True
        while (self.is_legal_move(player, player.cp_list)): self.move_piece(player)
        if not self.over:
            self.add_piece_to_lines(player)
            if self.multiplayer:
                if self.line_bool(player) != []:
                    lines_to_pop = self.line_bool(player)
                    for line in lines_to_pop: self.pop_line_multiplayer(player, line)
                    player.combo_value += 1
                    if player.combo_value > 0: player.opponent.lines_to_be_added += 1
                else:
                    player.combo_value = -1
                self.update_multiplayer([player])
                self.generate_new_current_piece(player)
                player.key_bools[1]= False
                player.piece_dropped = False

    def rotate_piece(self, player, ls, ls2):
        self.remove_piece_from_lines(player)
        for n in range(4):
            player.cp_list[n] = ls[n]
            player.cp_list[4][n] = ls2[n]
        self.add_piece_to_lines(player)
        player.s_list = copy.deepcopy(player.cp_list)

### GENERATE METHODS ###

    def generate_random_piece(self):
        return choice(["L","I","T","O","S","J","Z"])

    def generate_random_current_piece(self, player):
        player.current_piece = self.generate_random_piece()
        player.next_piece = self.generate_random_piece()
        player.cp_list = self.set_piece(player, player.current_piece)
        player.s_list = copy.deepcopy(player.cp_list)

    def generate_new_current_piece(self, player):
        player.reset_lists()
        self.paused, player.hold = False, True
        player.current_piece = player.next_piece
        player.cp_list = self.set_piece(player, player.current_piece)
        if self.is_player_knocked_out(player):
            if self.multiplayer:
                player.times_KOed += 1
                knockout_sound.play()
                SCREEN.blit(knockout_image,((player.opponent.xmin)*block_size+550,180))
                self.new_game_multiplayer([player])
            else:
                self.over = True
        else:
            if player.lines_to_be_added > 0:
                self.add_lines(player, player.lines_to_be_added)
                player.lines_added = True
                player.lines_to_be_added = 0
            player.s_list = copy.deepcopy(player.cp_list)
            player.next_piece = self.generate_random_piece()
            self.add_piece_to_lines(player)
            if not self.multiplayer: self.last_fall_time = time.time()
    
    def generate_random_gray_line(self):
        ls = []
        n = randrange(10)
        for i in range(10): ls.append(BOMB) if i == n else ls.append(GRAY)
        return ls
        
    def set_piece(self, player, piece):
        player.reset_lists()
        if piece == "I": return player.start_I
        elif piece == "O": return player.start_O
        elif piece == "T": return player.start_T
        elif piece == "L": return player.start_L
        elif piece == "J": return player.start_J
        elif piece == "S": return player.start_S
        elif piece == "Z": return player.start_Z

### VARIOUS BOOLS AND CHECKS ###

    def is_rotation_legal(self, player):
        ls, ls2 = [], []
        xval, yval = 0,0
        xBool, yBool = False, False
        for n in range(4):
            [x1,y1] = player.cp_list[n]
            rotation_list = player.cp_list[4]
            [x_old, y_old] = rotation_list[n]
            size = rotation_list[4]
            x_new, y_new = 1-(y_old - (size - 2)), x_old
            x_dif, y_dif = x_new - x_old, y_new - y_old
            x2, y2 = x1+x_dif, y1+y_dif
            ls.append([x2,y2])
            ls2.append([x_new, y_new])
            if (player.xmin <= x2 <= player.xmax-1 and player.ymin <= y2 <= player.ymax-1):
                if (player.lines[y2-player.ymin][x2-player.xmin] != self.view.board_color and [x2,y2] not in player.cp_list[:4]): return
        for n in range(4):
            [x2, y2] = ls[n]
            if x2 < player.xmin and (x2-player.xmin) < xval:
                xval = x2-player.xmin
                xBool = True
            elif x2 > player.xmax-1 and x2-(player.xmax-1) > xval:
                xval = x2-(player.xmax-1)
                xBool = True
            if y2 < player.ymin and (y2-player.ymin) < yval:
                yval = y2-player.ymin
                yBool = True
            elif y2 > player.ymax-1 and y2-(player.ymax-1) > yval:
                yval = y2-(player.ymax-1)
                yBool = True
        for n in range(4):
            if xBool: ls[n][0] -= xval
            if yBool: ls[n][1] -= yval
        if self.is_legal_pos(player, ls): self.rotate_piece(player, ls, ls2)

    def line_bool(self, player):
        ls = []
        for y in range(20):
            if all(color not in [self.view.board_color, GRAY] for color in player.lines[y]): ls.append(y)
            elif all(color in [GRAY, player.cp_list[5]] for color in player.lines[y]): ls.append(y)
        return ls

    def is_line_free(self, player, ls):
        for i in range(0,4):
            [x,y] = ls[i]
            if player.key_bools[1]:
                if (player.lines[y+1-player.ymin][x-player.xmin] not in [self.view.board_color, BOMB] and [x,y+1] not in ls): return False
            elif player.key_bools[2]:
                if (player.lines[y-player.ymin][x+1-player.xmin] not in [self.view.board_color, BOMB]  and [x+1,y] not in ls): return False
            elif player.key_bools[0]:
                if (player.lines[y-player.ymin][x-1-player.xmin] not in [self.view.board_color, BOMB]  and [x-1,y] not in ls): return False
        return True

    def is_legal_pos(self, player, ls):
        for [x2, y2] in ls:
            if (player.lines[y2-player.ymin][x2-player.xmin] != self.view.board_color and [x2,y2] not in player.cp_list[:4]): return False
        return True

    def is_legal_move(self, player, ls):
        for x in range(0, 4):
            if player.key_bools[1]:
                if (ls[x][1] == player.ymax-1): return False
            elif player.key_bools[2]:
                if (ls[x][0] == player.xmax-1): return False
            elif player.key_bools[0]:
                if (ls[x][0] == player.xmin): return False
        boolean = self.is_line_free(player, ls)
        return boolean

    def check_level(self, player):
        if player.score_value > 0 and self.speed_value < max_speed:
            if player.score_value > self.score_threshold:
                self.score_threshold += 500 + (100 * (self.speed_value - 1))
                self.speed_value += 1
                self.fall_frequency -= 0.02
            if self.bøffel_mode:
                if player.score_value > self.image_threshold:
                    self.bøffel_image_index = (self.bøffel_image_index + randint(1,len(bøffel_videos))) % (len(bøffel_images)-1)
                    self.image_threshold += 1000
                if player.score_value > self.video_threshold:
                    self.video_threshold += 5000
                    pygame.mixer.music.pause()
                    self.paused = True
                    self.view.show_paused(single_player.xmin*block_size+50, 350)
                    response = play_video(self.bøffel_video_index)
                    self.bøffel_video_index = (self.bøffel_video_index + randint(1,len(bøffel_videos))) % (len(bøffel_videos)-1)
                    pygame.mixer.music.unpause()
                    if response == True: self.paused = False

    def check_score(self, score):
        self.view.menu.download_leaderboard()
        self.view.menu.leaderboard.append({
            'Date': date.today().strftime("%d/%m/%Y"),
            'Name': single_player.name,
            'Score': score
        })
        self.view.menu.leaderboard = sorted(self.view.menu.leaderboard, key=lambda x:x['Score'], reverse=True)[:20]
        for entry in self.view.menu.leaderboard:
            if single_player.name in entry.values() and score in entry.values(): return True
        else: return False

    # def write_leaderboard(self):
    #     with open(relative_path('data.json'), 'w') as outfile:
    #         json.dump(self.view.menu.leaderboard, outfile, indent=4)
    #     print("SUCCES IN WRITING!")

### POP LINE METHODS ###

    def pop_line_multiplayer(self, player, n):
        if player.combo_value >= 0:
            comboNum = 6 if player.combo_value >= 7 else player.combo_value
            combo_sounds[comboNum].play()
        player.score_value += 1
        for i in range(n, 0, -1):
            player.lines[i] = player.lines[i-1].copy()

    def pop_line_singleplayer(self, player, n):
        self.check_level(player)
        line_bonus = 100 if player.combo_value == 1 else 300 if player.combo_value == 2 else 500
        player.score_value += int (line_bonus * self.speed_value * 0.1)
        for i in range(n, 0, -1):
            player.lines[i] = player.lines[i-1].copy()
        self.check_level(player)


### UPDATE GAMEVIEW ###

    def update_multiplayer(self, players):
        for player in players:
            self.view.clear_lines(player) ; self.view.draw_lines(player) ; self.view.draw_right_side(player) ; \
            self.view.draw_silhouette(player) ; \
            self.view.draw_held_piece(player, 9, 19) ; self.view.draw_next_piece(player, 9, 12) ; \
            player.reset_lists() ; player.reset_moves() ; player.lines_added = False ; \
            self.view.show_score(player, (player.xmax*block_size)+20, (player.ymin*block_size)+10) ; \
            self.view.show_combo(player, player.xmax*block_size+20, (player.ymin*block_size)+150) ; \
            self.view.show_knockouts(player, player.xmax*block_size+20, (player.ymin*block_size)+80)

    def update_singleplayer(self, next_y, held_y, score_y, speed_y, name_y, bøffel_y, show_bøffel):
        self.view.clear_lines(single_player) ; self.view.draw_lines(single_player) ;  self.view.draw_right_side(single_player) ; \
        self.view.draw_next_piece(single_player, 10, next_y) ; \
        self.view.draw_held_piece(single_player, 10, held_y)
        if not self.over: self.view.draw_silhouette(single_player)
        self.view.show_score(single_player, 465, score_y) ; self.view.show_speed(self.speed_value, 465,speed_y) ; \
        self.view.show_name(single_player, 465, name_y) ; single_player.reset_lists() ; \
            self.view.menu.show_music(menu.current_song[0], menu.current_song[1], 410,780, game_music_font, self.view.board_color, self.view.panel_color)
        if show_bøffel: 
            self.view.show_bøffel_mode(self.bøffel_mode, 445, bøffel_y)
            self.view.show_random_bøffel()