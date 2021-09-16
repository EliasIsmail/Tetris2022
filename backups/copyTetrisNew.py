
from Game import *
import time

def start_game_multiplayer():
    pygame.display.set_mode((1360, 920))
    pause_start, pause_end = 0,0
    game = Game(playtime_value)
    player1.reset_values() ; player2.reset_values()
    game.new_game_multiplayer(players)
    start = time.time()

    while game.running:
        game.clock.tick(60)
        play_next_song()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            elif game.paused or game.over:  
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p: 
                    pause_end = time.time()
                    game.paused_time += pause_end - pause_start
                    game.paused = False
                if not game.paused:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                        for player in players:
                            game.clear_lines(player)
                            game.reset_lines(player)
                        game.running = False
                        start_game_multiplayer()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    game.running = False
                    return
            else:
                game.playtime_value = playtime_value - int(time.time() - start) + int (game.paused_time)
                if game.playtime_value <= 0 or any(player.times_KOed > 2 for player in players):
                    game.game_is_over_multiplayer()
                for player in players:
                    if event.type == player.event or player.piece_dropped:
                        player.key_bools[1] = True
                        if game.is_legal_move(player, player.cp_list): game.move_piece(player)
                        else: 
                            if game.line_bool(player) != []:
                                lines_to_pop = game.line_bool(player)
                                for line in lines_to_pop: game.pop_line_multiplayer(player, line)
                                player.combo_value += 1
                            else:
                                if player.combo_value > 0:
                                    game.add_lines(player.opponent, player.combo_value)
                                    player.opponent.lines_added = True
                                player.combo_value = -1
                            if player.piece_dropped:
                                pygame.time.set_timer(player.event, 0)
                                pygame.time.set_timer(player.event, player.time)
                                player.piece_dropped = False
                            if not player.lines_added:
                                game.generate_new_current_piece(player)
                    if event.type == pygame.KEYDOWN:
                        if event.key in player.keys[:3]:
                            for i in range(3):
                                if event.key == player.keys[i]: player.key_bools[i] = True
                            if game.is_legal_move(player, player.cp_list): game.move_piece(player)
                        elif event.key == player.keys[3]: game.is_rotation_legal(player)
                        elif event.key == player.keys[4]: game.hold_piece(player)
                        elif event.key == player.keys[5]: 
                            pygame.time.set_timer(player.event,0)
                            game.drop_piece(player)
                            player.piece_dropped = True
                        elif event.key == pygame.K_p:
                            pause_start = time.time()
                            game.show_paused(player.xmin*block_size+50, 350)
                            game.paused = True
                        elif event.key == pygame.K_m:
                            skip_song()
        if not (game.paused or game.over):
            keys = pygame.key.get_pressed()
            for player in players:
                if keys[player.keys[1]]:
                    player.key_bools[1] = True
                    if game.is_legal_move(player, player.cp_list): game.move_piece(player)
                else: player.key_bools[1] = False
                game.clear_lines(player) ; player.draw_held_piece(9, 19) ; player.reset_moves() ; \
                    player.draw_next_piece(9, 12) ; game.draw_lines(player) ; game.show_score(player, (player.xmax*block_size)+20, (player.ymin*block_size)+10) ; \
                        game.show_combo(player, player.xmax*block_size+20, (player.ymin*block_size)+150) ; \
                            game.show_knockouts(player, player.xmax*block_size+20, (player.ymin*block_size)+80) ; player.reset_lists()
                if not player.lines_added:
                    game.draw_silhouette(player)
                player.lines_added = False
        game.show_playtime(int(MENU_WIDTH/4),10)
        pygame.display.update()
    pygame.quit()


### SINGLEPLAYER ###

def start_game_singleplayer():
    pygame.display.set_mode((680, 800))
    game = Game()
    game.new_game_singleplayer(single_player)

    while game.running:
        play_next_song()
        game.clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            elif game.paused or game.over:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p: game.paused = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                    game.over = False
                    game.new_game_singleplayer(single_player)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    game.running = False
                    return
            else:
                if event.type == single_player.event or single_player.piece_dropped:
                    single_player.key_bools[1] = True
                    if game.is_legal_move(single_player, single_player.cp_list): game.move_piece(single_player)
                    else: 
                        if game.line_bool(single_player) != []: 
                            lines_to_pop = game.line_bool(single_player)
                            for line in lines_to_pop: game.pop_line_singleplayer(single_player, line)
                            single_player.combo_value += 1
                        else:
                            single_player.combo_value = 0
                        if single_player.piece_dropped: 
                            pygame.time.set_timer(single_player.event,single_player.time)
                            single_player.piece_dropped = False    
                        game.generate_new_current_piece(single_player)
                elif event.type == pygame.KEYDOWN:
                    if event.type == pygame.KEYDOWN:
                        if event.key in single_player.keys[:3]:
                            for i in range(3):
                                if event.key == single_player.keys[i]: single_player.key_bools[i] = True
                            if game.is_legal_move(single_player, single_player.cp_list): game.move_piece(single_player)
                        elif event.key == single_player.keys[3]: game.is_rotation_legal(single_player)
                        elif event.key == single_player.keys[4]: game.hold_piece(single_player)
                        elif event.key == single_player.keys[5]: 
                            pygame.time.set_timer(single_player.event,0)
                            game.drop_piece(single_player)
                            single_player.piece_dropped = True
                        elif event.key == pygame.K_p:
                            game.show_paused(single_player.xmin*block_size+50, 350)
                            game.paused = True
                        elif event.key == pygame.K_m:
                            skip_song()
        if not (game.paused or game.over):
            keys = pygame.key.get_pressed()
            if keys[single_player.keys[1]]:
                    single_player.key_bools[1] = True
                    if game.is_legal_move(single_player, single_player.cp_list): game.move_piece(single_player)
            else: single_player.key_bools[1] = False
            game.clear_lines(single_player) ; game.draw_lines(single_player) ; single_player.draw_next_piece(10,9) ; \
                single_player.draw_held_piece(10,16) ; single_player.reset_moves() ; game.draw_silhouette(single_player) ; \
                    game.show_score(single_player, 470,10) ; game.show_speed(single_player, 465,100) ; game.show_combo(single_player, 465, 150) ; \
                        single_player.reset_lists() 
        pygame.display.update()
    pygame.quit()

                    # elif event.key == pygame.K_s:
                    #     if musicOn: 
                    #         pygame.mixer.music.pause()
                    #         musicOn = False
                    #     else: 
                    #         pygame.mixer.music.unpause()
                    #         musicOn = True
        # if keys[pygame.K_DOWN]:
        #     single_player.key_bools[1] = True
        #     if is_legal_move(single_player, single_player.cp_list): move_piece(single_player)
        # # if keys[pygame.K_LEFT]:
        # #     left = True
        # #     if isLegalMove(currentPieceList): movePiece()
        # # if keys[pygame.K_RIGHT]:
        # #     right = True
        # #     if isLegalMove(currentPieceList): movePiece()
        # if not (paused or game_over):

