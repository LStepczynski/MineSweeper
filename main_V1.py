import pygame as pg
import random

# CONSTANTS
MAP_SIZE = 10
TILE_SIZE = 100
WIDTH, HEIGHT = TILE_SIZE*MAP_SIZE, TILE_SIZE*MAP_SIZE
FPS = 30
NUM_OF_MINES = 20
# CONSTANTS

# COLORS
GRAY = (110, 110, 110)
LIGHT_GRAY = (171, 166, 166)
GREEN = (0,255,0)
RED = (255,0,0)

MINE_COLOR = [(0,0,0),(255, 0, 106),(174, 0, 255),(47, 0, 255),(0, 162, 255),(0, 255, 153),(26, 255, 0),(255, 204, 0),(255, 115, 0)]
# COLORS


WINDOW = pg.display.set_mode((WIDTH,HEIGHT))
pg.display.set_caption("Saper")

class Box:
    def __init__(self, xpos, ypos, color, armed, detected = False, width = TILE_SIZE, height = TILE_SIZE):
        self.xpos = xpos
        self.ypos = ypos
        self.color = color
        self.armed = armed
        self.detected = detected
        self.width = width
        self.height = height
        self.object = pg.Rect(xpos,ypos,width,height)

# BUILDING BLOCKS OF THE MAP
boxes = [[] for _ in range(MAP_SIZE)]
for row in range(MAP_SIZE):
    for col in range(MAP_SIZE):
        boxes[row].append(Box(row * TILE_SIZE, col * TILE_SIZE, GRAY, False))
# BUILDING BLOCKS OF THE MAP

# SHOWS HOW MANY MINES ARE NEARBY
indicators = [[] for _ in range(MAP_SIZE)]
for row in range(MAP_SIZE):
    for col in range(MAP_SIZE):
        indicators[row].append(Box(row * TILE_SIZE + TILE_SIZE/3, col * TILE_SIZE + TILE_SIZE/3, GRAY, False, False, TILE_SIZE/3, TILE_SIZE/3))
# SHOWS HOW MANY MINES ARE NEARBY

# VISUALY SEPARATES BLOCKS
separators_horizontal = []
for row in range(1, MAP_SIZE):
    separators_horizontal.append(pg.Rect(0, (row*TILE_SIZE)-3, WIDTH, 6))

separators_vertical = []
for col in range(1, MAP_SIZE):
    separators_vertical.append(pg.Rect((col*TILE_SIZE)-3, 0, 6, HEIGHT))
# VISUALY SEPARATES BLOCKS

def bomb_count(x,y, depth):
    """ COUNTS HOW MANY MINES ARE NEARBY """
    mines = 0
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (-1, -1), (1, 1), (-1, 1), (1, -1)):
            try:
                if boxes[x+dx][y+dy].armed and (dx + x >= 0 and dy + y >= 0):
                    mines += 1
                if (dx, dy) != ((-1, -1), (1, 1), (-1, 1), (1, -1)):
                    if depth == 0 and bomb_count(x+dx,y+dy,1) == 0 and boxes[x+dx][y+dy].armed == False:
                        boxes[x+dx][y+dy].color = LIGHT_GRAY                    
            except IndexError:
                pass
    return mines

def finished():
    """ CHECKS IF THE PLAYER FINISHED THE GAME """
    for row in range(MAP_SIZE):
        for col in range(MAP_SIZE):
            if ((boxes[row][col].detected == False and boxes[row][col].armed == True) or (boxes[row][col].detected == True and boxes[row][col].armed == False)) or boxes[row][col].color == GRAY:
                return False
    return True

def on_click(side):
    """ ON LMB REVEALS NEW BLOCKS, ON RMB FLAGS A MINE """
    for row in range(MAP_SIZE):
        for col in range(MAP_SIZE):
            if mouse.colliderect(boxes[row][col].object):
                if side == 'left':
                    if boxes[row][col].armed == False: # IF THE BLOCK WAS NOT A BOMB IT REVEALS THE BLOCK
                        boxes[row][col].color = LIGHT_GRAY
                        return
                    elif boxes[row][col].armed == True and boxes[row][col].color != RED: # IF THE BLOCK WAS A BOMB IT DISPLAYS THE LOSS MESSAGE
                        print('You lost')

                elif side == 'right':
                    # FLAGS AND UNFLAGS THE BLOCK
                    if boxes[row][col].color == GRAY:
                        boxes[row][col].color = RED
                        boxes[row][col].detected = True
                    elif boxes[row][col].color == RED:
                        boxes[row][col].color = GRAY
                        boxes[row][col].detected = False

def place_mines():
    """ PLACES MINES ON THE MAP """
    i = 0
    while NUM_OF_MINES != i:
        x, y = random.randint(0,MAP_SIZE-1), random.randint(0,MAP_SIZE-1)
        if boxes[x][y].armed != True:
            boxes[x][y].armed = True
            i += 1

def visuals():
    """ DISPLAYS ALL THE ELEMENTS ON THE SCREEN """
    for row in range(MAP_SIZE):
        for col in range(MAP_SIZE):
            pg.draw.rect(WINDOW, boxes[row][col].color, boxes[row][col].object) # DISPLAYES BOXES
            pg.draw.rect(WINDOW, indicators[row][col].color, indicators[row][col].object) # DISPLAYS INDICATORS
    
    # DISPLAYES SEPARATORS
    for item in separators_vertical:
        pg.draw.rect(WINDOW, LIGHT_GRAY, item)
    for item in separators_horizontal:
        pg.draw.rect(WINDOW, LIGHT_GRAY, item)
    # DISPLAYES SEPARATORS

    pg.draw.rect(WINDOW, RED, mouse) # DISPLAYES THE MOUSE

    pg.display.update()

clock = pg.time.Clock()
run = True
place_mines()
while run:
    """ CONTAINS ALL THE NECESSARY PROCESSES IN A LOOP """
    mousex, mousey = pg.mouse.get_pos()
    mouse = pg.Rect(mousex,mousey,3,3) # CREATES THE MOUSE OBJECT

    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT: # CHECKS IF THE PLAYER EXITED THE GAME
            run = False
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1: # CHECKS IF THE PLAYER LEFT CLICKED
            on_click('left')
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 3: # CHECKS IF THE PLAYER RIGHT CLICKED
            on_click('right')
    

    visuals()

    if finished():
        print("You won")

    # UPDATES INDICATORS AND REVEALS NEW BLOCKS
    for row in range(MAP_SIZE):
        for col in range(MAP_SIZE):
            if boxes[row][col].color == LIGHT_GRAY:
                indicators[row][col].color = MINE_COLOR[bomb_count(row,col, 0)]