from game_elements import *

# GameView class - used for showing text and images
class GameView():
    def __init__(self):
        self.game = None
        self.menu = menu
        self.board_color = BLACK
        self.panel_color = WHITE

    def show_random_bøffel(self):
        SCREEN.fill(self.panel_color, bøffel_images[self.game.bøffel_image_index].get_rect(topleft=(450, 150)))
        SCREEN.blit(bøffel_images[self.game.bøffel_image_index],(450, 150))

    def show_bøffel_mode(self, bool, x, y):
        if bool: text = xxsmall_font.render("Bøffel mode: ON", True, GREEN)
        else: text = xxsmall_font.render("Bøffel mode: OFF", True, ZPIECE)
        SCREEN.fill(self.panel_color, text.get_rect(topleft=(x,y)))
        SCREEN.blit(text, (x,y))

    def show_name(self, player, x, y):
        name = xxsmall_font.render("Name: " + player.name, True, self.board_color)
        SCREEN.fill(self.panel_color, name.get_rect(topleft=(x,y)))
        SCREEN.blit(name, (x,y))

    def show_score(self, player,x,y):
        text = "Score: " if not self.game.multiplayer else "Lines sent: "
        score = medium_font.render(text + str(player.score_value), True, self.board_color)
        SCREEN.fill(self.panel_color, score.get_rect(topleft=(x,y)))
        SCREEN.blit(score, (x,y))

    def show_speed(self, speed, x,y):
        speed = xxsmall_font.render("Speed: " + str(speed) + "/" + str(max_speed), True, self.board_color)
        SCREEN.fill(self.panel_color, rect=speed.get_rect(topleft=(x,y)))
        SCREEN.blit(speed, (x,y))

    def show_paused(self, x,y):
        pause = huge_font.render("PAUSED", True, self.panel_color)
        #SCREEN.fill(BLACK, rect=pause.get_rect(topleft=(x,y)))
        SCREEN.blit(pause, (x,y))

    def show_combo(self, player, x,y):
        i = 0
        if player.combo_value < 0: i = 1
        combo = medium_font.render("Combo: " + str(player.combo_value+i), True, self.board_color)
        SCREEN.fill(self.panel_color, rect=combo.get_rect(topleft=(x,y)))
        SCREEN.blit(combo,(x,y))

    def show_knockouts(self, player, x,y):
        knockouts = medium_font.render("KO's: " + str(player.opponent.times_KOed), True, self.board_color)
        SCREEN.fill(self.panel_color, rect=knockouts.get_rect(topleft=(x,y)))
        SCREEN.blit(knockouts,(x,y))

    def show_playtime(self, playtime_value, x,y):
        playtime = huge_font.render("Time left: " + str(playtime_value) + " seconds", True, self.board_color)
        self.draw_top()
        SCREEN.blit(playtime,(x,y))

    def show_highscore(self, player, x, y):
        top_name, top_score = self.menu.leaderboard[0]['Name'], self.menu.leaderboard[0]['Score']
        score = xsmall_font.render("YOUR SCORE: ".rjust(20) + str(player.score_value), True, self.panel_color)
        highscore = xsmall_font.render("LEADER: ".rjust(15-len(top_name)) + top_name + " with " + str(top_score), True, self.panel_color)
        SCREEN.blit(score,(x,y))
        SCREEN.blit(highscore,(x,y+50))

    def show_new_highscore(self, player, x, y):
        top_name, top_score = self.menu.leaderboard[0]['Name'], self.menu.leaderboard[0]['Score']
        #index = [x[1] for x in self.menu.leaderboard].index(player.score_value)
        index = next((index for (index, d) in enumerate(self.menu.leaderboard) if d['Name'] == player.name and d['Score'] == player.score_value), None)
        score = xsmall_font.render("NEW HIGHSCORE!".rjust(22), True, self.panel_color)
        score2 = xsmall_font.render(" TOP " + str(index+1) + " WITH SCORE " + str(player.score_value), True, self.panel_color)
        highscore = xsmall_font.render("LEADER: ".rjust(15-len(top_name)) + top_name + " with " + str(top_score), True, self.panel_color)
        SCREEN.blit(score,(x,y))
        SCREEN.blit(score2,(x,y+50))
        SCREEN.blit(highscore,(x,y+100))

    def show_game_over_singleplayer(self, player):
        self.clear_lines(player)
        SCREEN.fill(self.board_color, rect=pygame.Rect(0,300,400,100))
        SCREEN.blit(game_text, (80,100)) ; SCREEN.blit(over_text, (90,200)) ; SCREEN.blit(play_again_text, (20,600))
    
    def show_game_over_multiplayer(self, players):
        for player in players:
            self.clear_lines(player)
        draw, winner, loser = False, None, None
        if players[0].times_KOed == players[1].times_KOed: 
            if players[0].score_value == players[1].score_value:
                draw = True
                players[0].text = players[1].text = draw_text
            else: 
                winner = players[0] if players[0].score_value > players[1].score_value else players[1]
        else:
                winner = players[0] if players[0].times_KOed < players[1].score_value else players[1]
        if draw: 
            for player in players:
                SCREEN.blit(draw_text, ((player.xmin)*block_size+70,500))
        else: 
            loser = winner.opponent
            SCREEN.blit(winner_text, ((winner.xmin)*block_size+30,500)) ; SCREEN.blit(loser_text, ((loser.xmin)*block_size+5,500))
            #  pygame.mixer.music.stop()


    def draw_top(self):
        rect = pygame.Rect(0,0,1360, (3*block_size))
        pygame.draw.rect(SCREEN, self.board_color, rect, 5)
        SCREEN.fill(self.panel_color, rect.inflate(-6,-6))

    def draw_lines(self, player):
        for y in range(player.ymin, player.ymax):
            for x in range(player.xmin, player.xmax):
                color = player.lines[y-player.ymin][x-player.xmin]
                rect = pygame.Rect(x*block_size, y*block_size, block_size, block_size)
                if color == self.board_color: SCREEN.fill(color, rect)
                elif color == BOMB: SCREEN.blit(bomb_image, rect)
                else: SCREEN.fill(color,rect.inflate(-2,-2))

    def reset_lines(self, player):
        for y in range(player.ymin, player.ymax):
            for x in range(player.xmin, player.xmax):
                player.lines[y-player.ymin][x-player.xmin] = self.board_color

    def clear_lines(self, player):
        for y in range(player.ymin, player.ymax):
            for x in range(player.xmin, player.xmax):
                rect = pygame.Rect(x*block_size, y*block_size, block_size, block_size)
                SCREEN.fill(self.board_color,rect)

    def draw_right_side(self, player):
        for y in range (player.ymin, player.ymax):
            for x in range (player.xmax, player.xmax+7):
                rect = pygame.Rect(x*block_size, y*block_size, block_size, block_size)
                SCREEN.fill(self.panel_color, rect)

    def draw_held_piece(self, player, pos_x, pos_y):
        pad = 0.5 if player.held_piece in ["O","I"] else 0
        if not self.game.multiplayer:
            pad += 1
            rect_pad = 1
        else: 
            rect_pad = 4
        held_x, held_y = (player.xmax + text_pad_x) * block_size, (pos_y - text_pad_y) * block_size
        held_text = large_font.render("Held", True, self.board_color)
        SCREEN.fill(self.panel_color, rect=held_text.get_rect(topleft=(held_x, held_y)))
        SCREEN.blit(held_text, (held_x, held_y))
        if player.held_piece != "":
            self.clear_held_piece(player, pos_y, box_pad_x, box_pad_y)
            piece_list = self.game.set_piece(player, player.held_piece)
            for n in range(4):
                [x,y] = piece_list[n]
                color = piece_list[5]
                rect = pygame.Rect((x + pos_x - pad) * block_size, (y + pos_y - rect_pad)*block_size, block_size, block_size)
                SCREEN.fill(color,rect.inflate(-2,-2))
                pygame.draw.rect(SCREEN, self.board_color, rect, 1)
        box_rect = pygame.Rect((player.xmax + box_pad_x)*block_size, (pos_y - box_pad_y)*block_size, 4*block_size, 4*block_size)
        pygame.draw.rect(SCREEN, self.board_color, box_rect, 4)

    def clear_held_piece(self, player, pos_y, box_pad_x, box_pad_y):
        player.reset_lists()
        box_rect = pygame.Rect((player.xmax + box_pad_x)*block_size, (pos_y - box_pad_y)*block_size, 4*block_size, 4*block_size)
        SCREEN.fill(self.panel_color,box_rect.inflate(-6,-6))

    def draw_next_piece(self, player, pos_x, pos_y):
        pad = 0.5 if player.next_piece in ["O","I"] else 0
        if not self.game.multiplayer:
            pad += 1
            rect_pad = 1
        else:
            rect_pad = 4
        next_x, next_y = (player.xmax + text_pad_x)*block_size, (pos_y - text_pad_y)*block_size
        next_text = large_font.render("Next", True, self.board_color)
        SCREEN.fill(self.panel_color, rect=next_text.get_rect(topleft=(next_x, next_y)))
        SCREEN.blit(next_text, (next_x, next_y))
        piece_list = self.game.set_piece(player, player.next_piece)
        self.clear_next_piece(player, pos_y, box_pad_x, box_pad_y)
        for n in range(4):
            [x,y] = piece_list[n]
            color = piece_list[5]
            piece_rect = pygame.Rect((x + pos_x - pad)*block_size, (y + pos_y - rect_pad)*block_size, block_size, block_size)
            SCREEN.fill(color,piece_rect.inflate(-2,-2))
            pygame.draw.rect(SCREEN, self.board_color, piece_rect, 1)
        box_rect = pygame.Rect((player.xmax + box_pad_x)*block_size, (pos_y - box_pad_y)*block_size, 4*block_size, 4*block_size)
        pygame.draw.rect(SCREEN, self.board_color, box_rect, 4)

    def clear_next_piece(self, player, pos_y, box_pad_x, box_pad_y):
        player.reset_lists()
        box_rect = pygame.Rect((player.xmax + box_pad_x)*block_size, (pos_y - box_pad_y)*block_size, 4*block_size, 4*block_size)
        SCREEN.fill(self.panel_color,box_rect.inflate(-6,-6))

    def get_silhouette(self, player):
        player.key_bools[1] = True
        while(self.game.is_legal_move(player, player.s_list)):
            for i in range(4): player.s_list[i][1] += 1
        player.key_bools[1] = False

    def draw_silhouette(self, player):
        color = player.cp_list[5]
        self.get_silhouette(player)
        for n in range (4):
            [x,y] = player.s_list[n]
            (fill_color, rect_color) = (color, self.board_color) if [x,y] in player.cp_list[:4] else (self.board_color, color)
            rect = pygame.Rect(x*block_size, y*block_size, block_size, block_size)
            SCREEN.fill(fill_color,rect)
            pygame.draw.rect(SCREEN, rect_color, rect, 1)