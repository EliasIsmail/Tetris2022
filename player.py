from game_elements import *
# Player class
class Player():

    def __init__(self, xmin, xmax, ymin, ymax, startX, keys, cp_list, lines):
        self.name = ""
        self.xmin = xmin
        self.xmax = xmax 
        self.ymin = ymin
        self.ymax = ymax
        self.start_x = startX
        self.cp_list = cp_list
        self.s_list = cp_list
        self.lines = lines
        self.first_hold = True
        self.hold = True
        self.piece_dropped = False
        self.lines_added = False
        self.lines_to_be_added = 0
        self.keys = keys
        self.key_bools = [False, False, False]
        self.current_piece = ""
        self.held_piece = ""
        self.next_piece = ""
        self.text = ""
        self.score_value = 0
        self.combo_value = -1 if self.name == "" else 0
        self.opponent = None
        self.times_KOed = 0
        self.start_I = [[startX-1,ymin],[startX,ymin],[startX+1,ymin],[startX+2,ymin],rotation_list_I,IPIECE]
        self.start_O = [[startX,ymin],[startX,ymin+1],[startX+1,ymin],[startX+1,ymin+1],rotation_list_O,OPIECE]
        self.start_T = [[startX,ymin],[startX-1,ymin+1],[startX,ymin+1],[startX+1,ymin+1],rotation_list_T,TPIECE]
        self.start_L = [[startX-1,ymin+1],[startX,ymin+1],[startX+1,ymin+1],[startX+1,ymin],rotation_list_L,LPIECE]
        self.start_J = [[startX-1,ymin],[startX-1,ymin+1],[startX,ymin+1],[startX+1,ymin+1],rotation_list_J,JPIECE]
        self.start_S = [[startX-1,ymin+1],[startX,ymin],[startX,ymin+1],[startX+1,ymin],rotation_list_S,SPIECE]
        self.start_Z = [[startX,ymin],[startX-1,ymin],[startX,ymin+1],[startX+1,ymin+1],rotation_list_Z,ZPIECE]
    
    def reset_lists(self):
        global rotation_list_I, rotation_list_O, rotation_list_T, rotation_list_L, rotation_list_J, rotation_list_S, rotation_list_Z
        rotation_list_I = [[0,1],[1,1],[2,1],[3,1],4]
        rotation_list_O = [[0,0],[0,1],[1,0],[1,1],2]
        rotation_list_T = [[1,0],[0,1],[1,1],[2,1],3]
        rotation_list_L = [[0,1],[1,1],[2,1],[2,0],3]
        rotation_list_J = [[0,0],[0,1],[1,1],[2,1],3]
        rotation_list_S = [[0,1],[1,0],[1,1],[2,0],3]
        rotation_list_Z = [[1,0],[0,0],[1,1],[2,1],3]
        self.start_I = [[self.start_x-1,self.ymin],[self.start_x,self.ymin],[self.start_x+1,self.ymin],[self.start_x+2,self.ymin],rotation_list_I,IPIECE]
        self.start_O = [[self.start_x,self.ymin],[self.start_x,self.ymin+1],[self.start_x+1,self.ymin],[self.start_x+1,self.ymin+1],rotation_list_O,OPIECE]
        self.start_T = [[self.start_x,self.ymin],[self.start_x-1,self.ymin+1],[self.start_x,self.ymin+1],[self.start_x+1,self.ymin+1],rotation_list_T,TPIECE]
        self.start_L = [[self.start_x-1,self.ymin+1],[self.start_x,self.ymin+1],[self.start_x+1,self.ymin+1],[self.start_x+1,self.ymin],rotation_list_L,LPIECE]
        self.start_J = [[self.start_x-1,self.ymin],[self.start_x-1,self.ymin+1],[self.start_x,self.ymin+1],[self.start_x+1,self.ymin+1],rotation_list_J,JPIECE]
        self.start_S = [[self.start_x-1,self.ymin+1],[self.start_x,self.ymin],[self.start_x,self.ymin+1],[self.start_x+1,self.ymin],rotation_list_S,SPIECE]
        self.start_Z = [[self.start_x,self.ymin],[self.start_x-1,self.ymin],[self.start_x,self.ymin+1],[self.start_x+1,self.ymin+1],rotation_list_Z,ZPIECE]

    def reset_moves(self):
        self.key_bools = [False,False,False]

    def reset_values(self):
        self.first_hold = True
        self.hold = True
        self.score_value = 0
        self.combo_value = -1
        self.times_KOed = 0
        self.key_bools = [False, False, False]
        self.held_piece = ""

# Player elements
player1_lines = [[BLACK for x in range(BOARD_WIDTH)] for y in range(BOARD_HEIGHT)]
player2_lines = [[BLACK for x in range(17,27)] for y in range(BOARD_HEIGHT)]
single_player_lines = [[BLACK for x in range(BOARD_WIDTH)] for y in range(BOARD_HEIGHT)]

# Define player keys
player1_keys = [pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_w, pygame.K_LSHIFT, pygame.K_f]
player2_keys = [pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_UP, pygame.K_RSHIFT, pygame.K_RCTRL]
single_player_keys = [pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_UP, pygame.K_LSHIFT, pygame.K_SPACE]

# Create players
player1 = Player(0, BOARD_WIDTH, 3, 23, startX1, player1_keys, cpls, player1_lines)
player2 = Player(17, 27, 3, 23, startX2, player2_keys, cpls, player2_lines)
single_player = Player(0, BOARD_WIDTH, 0, 20, startX1, single_player_keys, cpls, single_player_lines)
player1.opponent, player2.opponent = player2, player1
players = [player1, player2]
