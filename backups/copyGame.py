from GameElements import *
from random import randrange
from operator import itemgetter

class Game():
    def __init__(self, value = 0):
        self.running = True
        self.paused = False
        self.over = False
        self.playtime_value = value
        self.paused_time = 0
        self.clock = pygame.time.Clock()
        self.threshold = 500

    def move_piece(self, player):
        val, i = 0,0
        if player.key_bools[1]: i, val = 1, 1
        elif player.key_bools[2]: i, val = 0, 1
        elif player.key_bools[0]: i, val = 0, -1
        player.remove_piece_from_lines(BLACK)
        for n in range(4):
            player.cp_list[n][i] += val
        player.add_piece_to_lines()
        player.s_list = copy.deepcopy(player.cp_list)
        if player == single_player and i == 1: player.score_value += 1

    def hold_piece(self, player):
        if player.hold:
            player.remove_piece_from_lines(BLACK)
            if player.first_hold:
                player.first_hold = False
                player.held_piece = player.current_piece
                self.generate_new_current_piece(player)
            else:
                player.current_piece, player.held_piece = player.held_piece, player.current_piece
                player.cp_list = player.set_piece(player.current_piece)
                player.add_piece_to_lines()
                player.s_list = copy.deepcopy(player.cp_list)
                player.hold = False

    def drop_piece(self, player):
        player.remove_piece_from_lines(BLACK)
        player.key_bools[1]= True
        while (self.is_legal_move(player, player.cp_list)): self.move_piece(player)
        player.add_piece_to_lines()

    def rotate_piece(self, player, ls, ls2):
        player.remove_piece_from_lines(BLACK)
        for n in range(4):
            player.cp_list[n] = ls[n]
            player.cp_list[4][n] = ls2[n]
        player.add_piece_to_lines()
        player.s_list = copy.deepcopy(player.cp_list)

    def is_rotation_legal(self, player):
        ls = []
        ls2 = []
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
                if (player.lines[y2-player.ymin][x2-player.xmin] != BLACK and [x2,y2] not in player.cp_list[:4]): return
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

    def new_game_multiplayer(self, players):
        if self.over:
            player1.reset_values() ; player2.reset_values()
            self.over = False
            pygame.mixer.music.play()
            self.playtime_value = playtime_value
        for player in players:
            player.generate_random_current_piece()
            player.add_piece_to_lines()
            self.draw_lines(player) ; self.draw_right_side(player)
            self.draw_top()
            pygame.time.set_timer(player.event, player.time)

    def new_game_singleplayer(self, player):
        player.held_piece, player.first_hold, player.hold  =  "", True, True
        self.reset_lines(player) ; player.score_value = 0 ; player.speed_value = 1 ; player.time = start_time
        player.generate_random_current_piece()
        player.add_piece_to_lines()
        self.draw_right_side(player)
        self.draw_lines(player)
        pygame.time.set_timer(player.event, player.time)

    def game_is_over_multiplayer(self):
        draw = False
        self.over = True
        for player in players:
            pygame.time.set_timer(player.event, 0)
            self.clear_lines(player)
        if player1.times_KOed == player2.times_KOed: 
            if player1.score_value == player2.score_value:
                draw = True
                player1.text = player2.text = draw_text
            else: 
                winner = player1 if player1.score_value > player2.score_value else player2
                print(winner.score_value)
        else:
            winner = player1 if player1.times_KOed < player2.times_KOed else player2
        if draw: 
            for player in players:
                SCREEN.blit(draw_text, ((player.xmin)*block_size+70,500))
        else: 
            loser = winner.opponent
            SCREEN.blit(winner_text, ((winner.xmin)*block_size+30,500)) ; SCREEN.blit(loser_text, ((loser.xmin)*block_size+15,500))
            #  pygame.mixer.music.stop()

    def random_gray_line(self):
        ls = []
        n = randrange(10)
        for i in range(10): ls.append(BOMB) if i == n else ls.append(GRAY)
        return ls

    def show_score(self, player,x,y):
        text = "Score: " if player == single_player else "Lines sent: "
        score = medium_font.render(text + str(player.score_value), True, BLACK)
        SCREEN.fill(WHITE, score.get_rect(topleft=(x+5,y)))
        SCREEN.blit(score, (x,y))

    def show_speed(self, player, x,y):
        speed = xsmall_font.render("Speed: " + str(player.speed_value) + "/" + str(max_speed), True, BLACK)
        SCREEN.fill(WHITE, rect=speed.get_rect(topleft=(x,y)))
        SCREEN.blit(speed, (x,y))

    def show_paused(self, x,y):
        pause = huge_font.render("PAUSED", True, WHITE)
        #SCREEN.fill(BLACK, rect=pause.get_rect(topleft=(x,y)))
        SCREEN.blit(pause, (x,y))

    def show_combo(self, player, x,y):
        i = 0
        if player.combo_value < 0: i = 1
        combo = medium_font.render("Combo: " + str(player.combo_value+i), True, BLACK)
        SCREEN.fill(WHITE, rect=combo.get_rect(topleft=(x+5,y)))
        SCREEN.blit(combo,(x,y))

    def show_knockouts(self, player, x,y):
        knockouts = medium_font.render("KO's: " + str(player.opponent.times_KOed), True, BLACK)
        SCREEN.fill(WHITE, rect=knockouts.get_rect(topleft=(x+5,y)))
        SCREEN.blit(knockouts,(x,y))

    def show_playtime(self, x,y):
        playtime = huge_font.render("Time left: " + str(self.playtime_value) + " seconds", True, BLACK)
        self.draw_top()
        SCREEN.blit(playtime,(x,y))

    def show_highscore(self, x, y):
        score = xsmall_font.render("YOUR SCORE: ".rjust(20) + str(single_player.score_value), True, WHITE)
        highscore = xsmall_font.render("LEADER: " + leaderboard[0][0] + " with " + str(leaderboard[0][1]), True, WHITE)
        SCREEN.blit(score,(x,y))
        SCREEN.blit(highscore,(x,y+50))

    def show_new_highscore(self, x, y):
        index = leaderboard.index((single_player.name, single_player.score_value))
        score = xsmall_font.render("NEW HIGHSCORE!".rjust(20), True, WHITE)
        score2 = xsmall_font.render(" TOP " + str(index+1) + " WITH SCORE " + str(single_player.score_value), True, WHITE)
        highscore = xsmall_font.render("LEADER: ".rjust(10) + leaderboard[0][0] + " with " + str(leaderboard[0][1]), True, GREEN)
        SCREEN.blit(score,(x,y))
        SCREEN.blit(score2,(x,y+50))
        if index != 0: SCREEN.blit(highscore,(x,y+100))
        
    def setLineEmpty(self, player, y):
        for x in range(BOARD_WIDTH):
            player.lines[y-player.ymin][x] = BLACK

    def draw_lines(self, player):
        for y in range(player.ymin, player.ymax):
            for x in range(player.xmin, player.xmax):
                color = player.lines[y-player.ymin][x-player.xmin]
                rect = pygame.Rect(x*block_size, y*block_size, block_size, block_size)
                if color == BLACK: SCREEN.fill(color, rect)
                elif color == BOMB: SCREEN.blit(bomb_image, rect)
                else: SCREEN.fill(color,rect.inflate(-2,-2))

    def draw_right_side(self, player):
        for y in range (player.ymin, player.ymax):
            for x in range (player.xmax, player.xmax+7):
                rect = pygame.Rect(x*block_size, y*block_size, block_size, block_size)
                SCREEN.fill(WHITE, rect)

    def draw_top(self):
        rect = pygame.Rect(0,0,1360, (players[0].ymin*block_size))
        pygame.draw.rect(SCREEN, BLACK, rect, 5)
        SCREEN.fill(WHITE, rect.inflate(-6,-6))

    def reset_lines(self, player):
        for y in range(player.ymin, player.ymax):
            for x in range(player.xmin, player.xmax):
                player.lines[y-player.ymin][x-player.xmin] = BLACK

    def clear_lines(self, player):
        for y in range(player.ymin, player.ymax):
            for x in range(player.xmin, player.xmax):
                rect = pygame.Rect(x*block_size, y*block_size, block_size, block_size)
                SCREEN.fill(BLACK,rect)

    def is_legal_pos(self, player, ls):
            for [x2, y2] in ls:
                if (player.lines[y2-player.ymin][x2-player.xmin] != BLACK and [x2,y2] not in player.cp_list[:4]): return False
            return True

    def is_legal_move(self, player, ls):
        for x in range(0, 4):
            if player.key_bools[1]:
                if (ls[x][1] == player.ymax-1): return False
            elif player.key_bools[2]:
                if (ls[x][0] == player.xmax-1): return False
            elif player.key_bools[0]:
                if (ls[x][0] == player.xmin): return False
        boolean = player.is_line_free(ls)
        return boolean

    def get_silhouette(self, player):
        player.key_bools[1] = True
        while(self.is_legal_move(player, player.s_list)):
            for i in range(4): player.s_list[i][1] += 1
        player.key_bools[1] = False

    def draw_silhouette(self, player):
        color = player.cp_list[5]
        self.get_silhouette(player)
        for n in range (4):
            [x,y] = player.s_list[n]
            (fill_color, rect_color) = (color, BLACK) if [x,y] in player.cp_list[:4] else (BLACK, color)
            rect = pygame.Rect(x*block_size, y*block_size, block_size, block_size)
            SCREEN.fill(fill_color,rect)
            pygame.draw.rect(SCREEN, rect_color, rect, 1)

    def generate_new_current_piece(self, player):
        player.reset_lists()
        self.paused, player.hold = False, True
        player.current_piece = player.next_piece
        player.cp_list = player.set_piece(player.current_piece)
        if player.is_knocked_out():
            if player != single_player:
                player.times_KOed += 1
                knockout_sound.play()
                SCREEN.blit(knockout_image,((player.opponent.xmin)*block_size+550,180))
                self.clear_lines(player)
                self.reset_lines(player)
                pygame.time.set_timer(player.event, 0)
                self.new_game_multiplayer([player])
            else:
                self.clear_lines(player)
                text = huge_font.render("GAME", True, ZPIECE)
                text2 = huge_font.render("OVER", True, ZPIECE)
                text3 = small_font.render("PRESS N TO PLAY AGAIN!", True, ZPIECE)
                SCREEN.fill(BLACK, rect=pygame.Rect(0,300,400,100))
                SCREEN.blit(text, (80,100)) ; SCREEN.blit(text2, (90,200)) ; SCREEN.blit(text3, (20,600))
                if check_score(player.score_value): self.show_new_highscore(20, 400)
                else: self.show_highscore(20, 400)
                self.over = True
        else:
            player.s_list = copy.deepcopy(player.cp_list)
            player.next_piece = player.generate_random_piece()
            player.add_piece_to_lines()

    def line_bool(self, player):
        ls = []
        for y in range(20):
            if all(color not in [BLACK, GRAY] for color in player.lines[y]): ls.append(y)
            elif all(color in [GRAY, player.cp_list[5]] for color in player.lines[y]): ls.append(y)
        return ls

    def pop_line_multiplayer(self, player, n):
        if player.combo_value >= 0:
            comboNum = 6 if player.combo_value >= 7 else player.combo_value
            combo_sounds[comboNum].play()
        player.score_value += 1
        #setLineEmpty(player, n)
        for i in range(n, 0, -1):
            player.lines[i] = player.lines[i-1].copy()

    def pop_line_singleplayer(self, player, n):
        player.score_value += 50*(player.combo_value+1)
        for i in range(n, 0, -1):
            player.lines[i] = player.lines[i-1].copy()
        if player.score_value > 0 and player.score_value > self.threshold and player.speed_value < max_speed: 
            pygame.time.set_timer(player.event,0)
            player.speed_value += 1
            player.time -= 30
            self.threshold += 500
            pygame.time.set_timer(player.event, player.time)

    def add_lines(self, player, value):
        player.remove_piece_from_lines(BLACK)
        copy_lines = copy.deepcopy(player.lines)
        for i in range(19-value, 0, -1):
            player.lines[i] = copy_lines[i+value].copy()
        if all(12 > (player.cp_list[i][1] - value) >= 0 for i in range(4)): 
            for i in range(4): player.cp_list[i][1] -= value
        player.add_piece_to_lines()
        player.s_list = copy.deepcopy(player.cp_list)
        for i in range(0,value):
            player.lines[19-i] = self.random_gray_line()
       # self.draw_lines(player)

def check_score(score):
    global leaderboard
    leaderboard.append((single_player.name, score))
    leaderboard = sorted(leaderboard, key=itemgetter(1), reverse=True)[:20]
    with open('leaderboard.txt', 'wb') as f:
        pickle.dump(leaderboard, f)
    return True if (single_player.name, score) in leaderboard else False
