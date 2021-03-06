from game import *

def start_game_multiplayer():
    pygame.display.set_mode((1360, 920))
    pause_start, pause_end = 0,0
    game = Game(True,playtime_value)
    for player in players:
        player.reset_values()
        game.view.clear_lines(player)
        game.view.reset_lines(player)
    game.new_game_multiplayer(players)
    start = time.time()

    while game.running:
        if not game.view.menu.music_paused: play_next_song() 

        if not (game.paused or game.over):
                # if event.type == player.event or player.piece_dropped:
            if (time.time() - game.last_fall_time) > game.fall_frequency:

                for player in players:
                        player.key_bools[1] = True
                        if game.is_legal_move(player, player.cp_list): 
                            game.move_piece(player)
                            game.last_fall_time = time.time()
                        else: 
                            if game.line_bool(player) != []:
                                lines_to_pop = game.line_bool(player)
                                for line in lines_to_pop: game.pop_line_multiplayer(player, line)
                                player.combo_value += 1
                                if player.combo_value > 0: player.opponent.lines_to_be_added += 1
                            else:
                                player.combo_value = -1
                            if not (player.lines_added):
                                game.generate_new_current_piece(player)
                                    
                # Update game time, and check if game is over
                game.playtime_value = playtime_value - int(time.time() - start) + int (game.paused_time)
                if game.playtime_value <= 0 or any(player.times_KOed > 2 for player in players):
                    game.is_over_multiplayer()
                    for player in players:
                        game.view.show_score(player, (player.xmax*block_size)+20, (player.ymin*block_size)+10)
                        game.view.show_combo(player, player.xmax*block_size+20, (player.ymin*block_size)+150)
                        game.view.show_knockouts(player, player.xmax*block_size+20, (player.ymin*block_size)+80)

        # Check events, keys, lines to pop, and so on for both players. Go to the single-player loop below for comments on the functions.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
                    return
                elif game.paused:
                    if event.key == pygame.K_p:
                        pause_end = time.time()
                        game.paused_time += pause_end - pause_start
                        game.paused = False
                elif game.over:
                    if event.key == pygame.K_n:
                        start_game_multiplayer()

                elif event.key == pygame.K_m:
                    game.view.menu.music_paused = False
                    skip_song()

                elif event.key == pygame.K_c:
                    game.view.board_color, game.view.panel_color = game.view.panel_color,  game.view.board_color
                    for player in players:
                        for y in range(BOARD_HEIGHT):
                            for x in range(BOARD_WIDTH):
                                if player.lines[y][x] in [game.view.panel_color,  game.view.board_color]:
                                    player.lines[y][x] = game.view.board_color
                elif event.key == pygame.K_p:
                    pause_start = time.time()
                    game.paused = True
                    for player in players: game.view.show_paused(player.xmin*block_size+50, 350)

                elif event.key == pygame.K_b:
                    game.view.menu.music_paused = not game.view.menu.music_paused
                    pygame.mixer.music.pause() if game.view.menu.music_paused else pygame.mixer.music.unpause()
                else:
                    for player in players:
                        if event.key in player.keys[:3]:
                            for i in range(3):
                                if event.key == player.keys[i]: player.key_bools[i] = True
                            if game.is_legal_move(player, player.cp_list): game.move_piece(player)
                        elif event.key == player.keys[3]: game.is_rotation_legal(player)
                        elif event.key == player.keys[4]: game.hold_piece(player)
                        elif event.key == player.keys[5]: game.drop_piece(player)
        if not (game.paused or game.over):
            keys = pygame.key.get_pressed()
            for player in players:
                if keys[player.keys[1]]:
                    player.key_bools[1] = True
                    if game.is_legal_move(player, player.cp_list): 
                        game.move_piece(player)
                else: player.key_bools[1] = False

            game.update_multiplayer(players)
        game.view.show_playtime(game.playtime_value, int(MENU_WIDTH/4),10)
        pygame.display.update()
        game.clock.tick(60)
    pygame.quit()





### SINGLEPLAYER ###
index = 1
def start_game_singleplayer(mode=False):
    global index
    pygame.display.set_mode((680, 800))
    game = Game(b??ffel_mode=mode)
    game.new_game_singleplayer(single_player)

    update = True
    write_and_upload = True

    while game.running:

        # Makes sure songs are queued
        if not game.view.menu.music_paused: play_next_song() 

        if game.over: 
            game.view.show_game_over_singleplayer(single_player)
            if not game.has_checked_score:
                game.new_highscore = game.check_score(single_player.score_value)
            if game.new_highscore: 
                game.view.show_new_highscore(single_player, 20, 400)
                game.has_checked_score = True
                if update: 
                    pygame.display.update()
                    update = False
                if write_and_upload:
                    # game.write_leaderboard()
                    game.view.menu.upload_leaderboard()
                    write_and_upload = False
            else: 
                game.view.show_highscore(single_player, 20, 400)
                if update: 
                    pygame.display.update()
                    update = False

        for event in pygame.event.get():
            # If user quits game
            if event.type == pygame.QUIT:
                game.running = False

            # If game is paused or done
            elif game.paused or game.over:

                if game.paused:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                        game.paused = False
                        game.last_fall_time = time.time()
                        game.last_move_down_time = time.time()
                        game.last_move_side_time = time.time()

                # Start new game
                elif game.over:

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                        update, write_and_upload = True, True
                        game = Game(b??ffel_mode=mode)
                        game.new_game_singleplayer(single_player)

                # Quit game
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
                    return

            # If game is running
            elif event.type == pygame.KEYUP:
                if (event.key == single_player_keys[0]):
                    single_player.key_bools[0] = False
                elif (event.key == single_player_keys[1]):
                    single_player.key_bools[1] = False
                elif (event.key == single_player_keys[2]):
                    single_player.key_bools[2] = False
            
            # Key pressed
            elif event.type == pygame.KEYDOWN:

                # If the key is left, up or down, move the piece if possible
                if event.key in [single_player.keys[0], single_player.keys[2]]:
                    index_true = single_player.keys.index(event.key)
                    index_false = 0 if index_true == 2 else 2
                    single_player.key_bools[index_false] = False
                    single_player.key_bools[index_true] = True
                    if game.is_legal_move(single_player, single_player.cp_list): 
                        game.move_piece(single_player)
                        game.last_move_side_time = time.time()

                elif event.key == single_player.keys[1]:
                    single_player.key_bools[1] = True
                    if game.is_legal_move(single_player, single_player.cp_list): 
                        game.move_piece(single_player)
                        game.last_move_down_time = time.time()
                # Rotate piece on up key
                elif event.key == single_player.keys[3]: game.is_rotation_legal(single_player)

                # Hold piece on hold key
                elif event.key == single_player.keys[4]: game.hold_piece(single_player)

                # Drop piece on drop key
                elif event.key == single_player.keys[5]:
                    # pygame.time.set_timer(single_player.event,0)
                    game.drop_piece(single_player)

                # Pause game on pause key
                elif event.key == pygame.K_p:
                    game.view.show_paused(single_player.xmin*block_size+50, 350)
                    game.paused = True
                    for i in range (3):
                        single_player.key_bools[i] = False

                # Skip song on m key
                elif event.key == pygame.K_m:
                    game.view.menu.music_paused = False
                    skip_song()

                elif event.key == pygame.K_COMMA:
                    game.b??ffel_image_index = (game.b??ffel_image_index + 1) % (len(b??ffel_images)-1)
                # Pause song
                elif event.key == pygame.K_b:
                    game.view.menu.music_paused = not game.view.menu.music_paused
                    pygame.mixer.music.pause() if game.view.menu.music_paused else pygame.mixer.music.unpause()

                elif event.key == pygame.K_c:
                    game.view.board_color, game.view.panel_color = game.view.panel_color,  game.view.board_color
                    for y in range(BOARD_HEIGHT):
                        for x in range(BOARD_WIDTH):
                            if single_player.lines[y][x] in [game.view.panel_color,  game.view.board_color]:
                                single_player.lines[y][x] = game.view.board_color

        # If the game is not paused or over, check if down key is held for soft drop, and move piece if legal
        if not (game.over or game.paused):

            if single_player.piece_dropped or (time.time() - game.last_fall_time) > game.fall_frequency:

                # Move piece down if possible
                single_player.key_bools[1] = True
                if game.is_legal_move(single_player, single_player.cp_list): 
                    game.move_piece(single_player)
                    game.last_fall_time = time.time()
                # If not possible, find out why
                else:
                    # Check if there are lines to pop, after piece was added - pop lines if so, and increment combo value accordingly
                    if game.line_bool(single_player) != []:
                        lines_to_pop = game.line_bool(single_player)
                        single_player.combo_value = len(lines_to_pop)
                        for line in lines_to_pop: game.pop_line_singleplayer(single_player, line)
                    else: single_player.combo_value = 0

                    # If player dropped the piece, start time again for next piece
                    if single_player.piece_dropped:
                        # pygame.time.set_timer(single_player.event,single_player.time)
                        single_player.piece_dropped = False    

                        # Generate next piece
                    game.generate_new_current_piece(single_player)

            if (single_player.keys[0] or single_player.keys[2]) and time.time() - game.last_move_side_time > game.move_side_frequency:
                if game.is_legal_move(single_player, single_player.cp_list): 
                    game.move_piece(single_player)
                    game.last_move_side_time = time.time()
            
            # if single_player.keys[1] and time.time() - game.last_move_side_time > game.move_down_frequency:
            #     if game.is_legal_move(single_player, single_player.cp_list): 
            #         game.move_piece(single_player)
            #         game.last_move_down_time = time.time()
            keys = pygame.key.get_pressed()
            if keys[single_player.keys[1]]:
                    single_player.key_bools[1] = True
                    if game.is_legal_move(single_player, single_player.cp_list): game.move_piece(single_player)
            else: single_player.key_bools[1] = False
            if game.b??ffel_mode:
                show_b??ffel = True
                next_y, held_y, score_y, speed_y, name_y, b??ffel_y = 11.5,17,10,50,80,115
            else: 
                next_y, held_y, score_y, speed_y, name_y, b??ffel_y = 10,16,10,80,120,200
                show_b??ffel = False
            # Redraw game, reset necessary values and lists
            game.update_singleplayer(next_y, held_y, score_y, speed_y, name_y, b??ffel_y, show_b??ffel)
        pygame.display.update()
        game.clock.tick(60) 

    # Quit game if main loop is exited
    pygame.quit()
