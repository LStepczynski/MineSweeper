import pygame as pg
import random
import time

pg.mixer.init(44100, -16,2,2048)

# CONSTANTS
MAP_SIZE = 10
TILE_SIZE = 50
WIDTH, HEIGHT = TILE_SIZE*MAP_SIZE, TILE_SIZE*MAP_SIZE
FPS = 30
NUM_OF_MINES = 10
# CONSTANTS

# COLORS
GRAY = (110, 110, 110)
LIGHT_GRAY = (171, 166, 166)
GREEN = (0,255,0)
RED = (255,0,0)
# COLORS

# SPRITES
GRASS_SPRITE = pg.image.load('Grass.png')
GRASS_SPRITE = pg.transform.scale(GRASS_SPRITE, (TILE_SIZE,TILE_SIZE))

FLOOR_SPRITE = pg.image.load('Floor.png')
FLOOR_SPRITE = pg.transform.scale(FLOOR_SPRITE, (TILE_SIZE,TILE_SIZE))

NUM_SPRITES = [pg.image.load('1.png'), pg.image.load('2.png'), pg.image.load('3.png'), pg.image.load('4.png'), pg.image.load('5.png')]
for i in range(len(NUM_SPRITES)):
    NUM_SPRITES[i] = pg.transform.scale(NUM_SPRITES[i], (TILE_SIZE/2,TILE_SIZE/2))
NUM_SPRITES.insert(0,0)
# SPRITES

# SOUNDS
DEATH_SOUND = pg.mixer.Sound('zgon_dzwiek.mp3')
FINISH_SOUND = pg.mixer.Sound('wygrana_dzwiek.mp3')
REVEAL_SOUND = pg.mixer.Sound('reveal.mp3')
FLAG_SOUND = pg.mixer.Sound('flag.mp3')
# SOUNDS


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

class Indicator:
    def __init__(self, xpos, ypos, sprite, width = TILE_SIZE, height = TILE_SIZE):
        self.xpos = xpos
        self.ypos = ypos
        self.sprite = sprite
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
        indicators[row].append(Indicator(row * TILE_SIZE + TILE_SIZE/4, col * TILE_SIZE + TILE_SIZE/4, 0))
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
        if dx + x >= 0 and dy + y >= 0:    
            try:
                if boxes[x+dx][y+dy].armed:
                    mines += 1
                if (dx, dy) != ((-1, -1), (1, 1), (-1, 1), (1, -1)):
                    if depth == 0 and bomb_count(x+dx,y+dy,1) == 0 and boxes[x+dx][y+dy].armed == False:
                        boxes[x+dx][y+dy].color = LIGHT_GRAY                    
            except IndexError:
                pass
    return mines

def reveal(x, y):
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (-1, -1), (1, 1), (-1, 1), (1, -1)):
        try:
            if dx + x >= 0 and dy + y >= 0:
                boxes[dx+x][dy+y].color = LIGHT_GRAY
        except: pass

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
                    REVEAL_SOUND.play()
                    if boxes[row][col].armed == False: # IF THE BLOCK WAS NOT A BOMB IT REVEALS THE BLOCK
                        boxes[row][col].color = LIGHT_GRAY
                        return
                    elif boxes[row][col].armed == True and boxes[row][col].color != RED: # IF THE BLOCK WAS A BOMB IT DISPLAYS THE LOSS MESSAGE
                        print('You lost')
                        DEATH_SOUND.play()

                elif side == 'right':
                    # FLAGS AND UNFLAGS THE BLOCK
                    FLAG_SOUND.play()
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
            if boxes[row][col].color == GRAY:
                WINDOW.blit(GRASS_SPRITE, (boxes[row][col].xpos, boxes[row][col].ypos))
            elif boxes[row][col].color == LIGHT_GRAY:
                WINDOW.blit(FLOOR_SPRITE, (boxes[row][col].xpos, boxes[row][col].ypos))
            else:
                pg.draw.rect(WINDOW, boxes[row][col].color, boxes[row][col].object) # DISPLAYES BOXES
            
            if indicators[row][col].sprite != 0:
                WINDOW.blit(indicators[row][col].sprite, (indicators[row][col].xpos, indicators[row][col].ypos))
            
    
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
        FINISH_SOUND.play()
        time.sleep(3)
        exit()

    # UPDATES INDICATORS AND REVEALS NEW BLOCKS
    for row in range(MAP_SIZE):
        for col in range(MAP_SIZE):
            if boxes[row][col].color == LIGHT_GRAY:
                indicators[row][col].sprite = NUM_SPRITES[bomb_count(row,col, 0)]
            if boxes[row][col].color == LIGHT_GRAY and bomb_count(row,col, 1) == 0:
                reveal(row,col)