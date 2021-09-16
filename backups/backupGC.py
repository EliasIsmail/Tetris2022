from GameLogic import *

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
        play_next_song()
        if not (game.paused or game.over):
            # Update game time, and check if game is over
            game.playtime_value = playtime_value - int(time.time() - start) + int (game.paused_time)
            if game.playtime_value <= 0 or any(player.times_KOed > 2 for player in players):
                game.is_over_multiplayer()
                for player in players:
                    game.view.show_score(player, (player.xmax*block_size)+20, (player.ymin*block_size)+10)
                    game.view.show_combo(player, player.xmax*block_size+20, (player.ymin*block_size)+150)
                    game.view.show_knockouts(player, player.xmax*block_size+20, (player.ymin*block_size)+80)

                # if event.type == player.event or player.piece_dropped:
            if (time.time() - game.last_fall_time) > game.fall_frequency:

                for player in players:
                    if not player.piece_dropped:
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
                            if not (player.lines_added or game.over):
                                game.generate_new_current_piece(player)

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

                if game.paused: 
                    for player in players: game.view.show_paused(player.xmin*block_size+50, 350)
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

def start_game_singleplayer(mode=False):
    pygame.display.set_mode((680, 800))
    game = Game(bøffel_mode=mode)
    game.new_game_singleplayer(single_player)

    while game.running:
        # Makes sure songs are queued
        play_next_song() 
        # Check for event (piece drops every second)
        # if event.type == single_player.event or single_player.piece_dropped: 
        # print(str((time.time() - game.last_fall_time)) + " > " + str(game.fall_frequency))
        if game.over: game.view.show_game_over_singleplayer(single_player)
        
        for event in pygame.event.get():
            # If user quits game
            if event.type == pygame.QUIT:
                game.running = False

            # If game is paused or done
            elif game.paused or game.over:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p: game.paused = False

                # Start new game
                if game.over: 
                    game.view.show_game_over_singleplayer(single_player)

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                        game.over = False
                        game.new_game_singleplayer(single_player)


                # Quit game
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
                    return

            # If game is running
            elif event.type == pygame.KEYUP:
                    # if (event.key == pygame.K_p):
                    #     # Pausing the game
                    #     DISPLAYSURF.fill(BGCOLOR)
                    #     pygame.mixer.music.stop()
                    #     showTextScreen('Paused') # pause until a key press
                    #     pygame.mixer.music.play(-1, 0.0)
                    #     lastFallTime = time.time()
                    #     lastMoveDownTime = time.time()
                    #     lastMoveSidewaysTime = time.time()
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

                # Skip song on m key
                elif event.key == pygame.K_m:
                    skip_song()

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
            if game.bøffel_mode:
                show_bøffel = True
                next_y, held_y, score_y, speed_y, name_y, bøffel_y = 12,18,10,60,90,120
            else: 
                next_y, held_y, score_y, speed_y, name_y, bøffel_y = 10,16,10,100,150,200
                show_bøffel = False
            # Redraw game, reset necessary values and lists
            game.view.clear_lines(single_player) ; game.view.draw_lines(single_player) ;  game.view.draw_right_side(single_player) ; \
                game.view.draw_next_piece(single_player, 10, next_y) ; \
                game.view.draw_held_piece(single_player, 10, held_y) ; game.draw_silhouette(single_player) ; \
                    game.view.show_score(single_player, 465, score_y) ; game.view.show_speed(game.speed_value, 465,speed_y) ; \
                        game.view.show_name(single_player, 465, name_y) ; single_player.reset_lists() ; \
                            game.view.show_bøffel_mode(game.bøffel_mode, 445, bøffel_y)
            if show_bøffel: game.view.show_random_bøffel(game.bøffel_image_index)
        pygame.display.update()
        game.clock.tick(60) 

    # Quit game if main loop is exited
    pygame.quit()
