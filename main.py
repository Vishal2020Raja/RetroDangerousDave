'''
Demo Dangerous Dave -By Vishal Raja_20110230
Original By-John Romero

char sprites--https://github.com/techwithtim/pygame-tutorials/tree/master/Game
musics--music.mp3-https://github.com/techwithtim/pygame-tutorials/tree/master/Game
musics--background.wav-laser.wav-explosion.wav-https://github.com/attreyabhatt/Space-Invaders-Pygame
musics--trumpet.mp3-http://www.freesoundslibrary.com
'''

import pygame
# import the pygame library
import time
# for delay

pygame.init()
# syntax stuff, always written

# recurred music
pygame.mixer.music.load('background.wav')
pygame.mixer.music.play(-1)

# window size
# X and Y
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# score
score = 0
# go thru door--when char gets trophy--blue bubble
GO_THRU_DOOR = ''

global boxes
# global char
global door
gems = list()
# for the door check
gotTrophy = False
# draw gem and check burst in one function--in-short remove scored ones
firstDraw = True
# setting window variable
win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# title
pygame.display.set_caption('Dangerous Dave Like')

# thickness of bar
THICK = 70
velY = 10  # for fall
RADII = THICK // 2

# This goes outside the while loop, near the top of the program
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'),
             pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'),
             pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'),
            pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'),
            pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
# bg = pygame.image.load('bg.jpg')
charImg = pygame.image.load('standing.png')


class Bar(object):
    # constructor
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    # collision with char ONLY
    # axis aligned box collision ONLY considered
    def no_box_collision(self):
        global char
        if (self.x - (char.width - 10) < char.x) and (char.x + 10 < self.width + self.x):
            if self.y > char.y:
                if self.y - char.y < char.height:
                    char.y = -1 * (char.height - self.y)
                    return True
            if self.y < char.y:
                if char.y - self.y < self.height:
                    char.y = self.y + self.height
                    return True

        if self.y - char.height < char.y < self.y + self.height:
            if self.x > char.x:
                if self.x - char.x < char.width:
                    char.x = self.x - char.width
                    return True
            if char.x > self.x:
                if char.x - self.x < self.width:
                    char.x = self.x + self.width
                    return True
        return False


# each colored box is a class
# convenience, constructor draws box--no other reason
class red_bar(Bar):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))


# not of any use--under dev
class green_bar(Bar):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        pygame.draw.rect(win, (0, 255, 0), (x, y, width, height))


# for pipe
class grey_bar(Bar):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        pygame.draw.rect(win, (150, 150, 150), (x, y, width, height))


# for door
class brown_bar(Bar):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        pygame.draw.rect(win, (123, 67, 0), (x, y, width, height))


# bar surrounding the char
char = Bar(THICK * 2 + 20, WINDOW_HEIGHT - 2 * THICK + 2, 64, 64)
win.blit(charImg, (THICK * 2 + 20, WINDOW_HEIGHT - 2 * THICK + 2))
# twt-tutorial
vel = 10

isJump = False
# used to change char.y in jump
jumpCount = 10
left = False  # walking left
right = False  # walking right
walkCount = 0
# to stop jump, when in air
canJump = False
# apply changes
pygame.display.update()


# prints score in freesansbold.ttf after update
def show_score(x, y):
    font = pygame.font.Font('freesansbold.ttf', 25)  # set type, size of font
    txtScore = font.render('Score: ' + str(score) + '       '+GO_THRU_DOOR, True, (0, 255, 0))  # setting the string
    win.blit(txtScore, (x, y))  # printing set, at coordinates (x, y)


# the bubbles
class Gem(object):
    def __init__(self, x, y, radii):
        self.x = x
        self.y = y
        self.radii = radii
        self.isTaken = False
        self.color = (0, 255, 0)

    def gem_draw(self, r, g, b):
        pygame.draw.circle(win, (r, g, b), (self.x, self.y), self.radii)
        self.color = (r, g, b)
        pass

    # checks if gem is taken, if not prints it
    def taken_off(self):
        global char
        if char.y < self.y < char.y + char.height:
            if char.x > self.x:
                if abs(self.x - char.x) < RADII:
                    self.isTaken = True
                    self.x += WINDOW_WIDTH
                    return self.isTaken
            if char.x < self.x:
                if abs(self.x - char.x) < RADII + char.width:
                    self.isTaken = True
                    self.x += WINDOW_WIDTH
                    return self.isTaken

        if char.x < self.x < char.x + char.width:
            if char.y > self.y:
                if abs(char.y - self.y) < RADII + char.height:
                    self.isTaken = True
                    self.x += WINDOW_WIDTH
                    return self.isTaken
            if char.y < self.y:
                if abs(char.y - self.y) < RADII:
                    self.isTaken = True
                    self.x += WINDOW_WIDTH
                    return self.isTaken


def draw_bar():
    # pygame.draw.rect(win, (0, 0, 0), (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))
    global boxes
    boxes = \
        (
            red_bar(0, 40, WINDOW_WIDTH, THICK),  # 1
            red_bar(0, 40, THICK, WINDOW_HEIGHT),  # 2
            red_bar(WINDOW_WIDTH - THICK, 40, THICK, WINDOW_HEIGHT),  # 3
            red_bar(THICK, WINDOW_HEIGHT - THICK, WINDOW_WIDTH - 2 * THICK, THICK),  # 4
            grey_bar(THICK, WINDOW_HEIGHT - THICK * 2, THICK * 1.2, THICK),  # 5
            red_bar(258, WINDOW_HEIGHT - 3 * THICK, 258, THICK),  # 6
            red_bar(THICK, WINDOW_HEIGHT - 5 * THICK, THICK, THICK),  # 7
            red_bar(THICK * 5, WINDOW_HEIGHT - 5 * THICK, THICK, THICK),  # 8
            red_bar(THICK * 3, WINDOW_HEIGHT - 7 * THICK, THICK, THICK),  # 9
            red_bar(THICK * 7, WINDOW_HEIGHT - 7 * THICK, THICK, THICK),  # 10
            red_bar(THICK * 9, WINDOW_HEIGHT - 5 * THICK, THICK, THICK),  # 11
            red_bar(THICK * 11, WINDOW_HEIGHT - 7 * THICK, THICK, THICK),  # 12
            red_bar(THICK * 13, WINDOW_HEIGHT - 5 * THICK, THICK, THICK),  # 13
            red_bar(THICK * 15, WINDOW_HEIGHT - 7 * THICK, THICK, THICK),  # 14
            red_bar(WINDOW_WIDTH - 2 * THICK, WINDOW_HEIGHT - 5 * THICK, THICK, THICK),  # 15
            red_bar(THICK * 11, WINDOW_HEIGHT - 4 * THICK, THICK, THICK * 3),  # 16
            red_bar(THICK * 12, WINDOW_HEIGHT - 3 * THICK, THICK * 4, THICK))  # 17


def draw_gem():
    global boxes, gotTrophy
    global gems
    global firstDraw
    if firstDraw:
        # just to know the box, refer draw_box()
        # gem drawn above box
        for i in [6, 8, 7, 9, 10, 11, 12, 13, 14]:
            pass
            x = boxes[i].x + RADII
            y = boxes[i].y - RADII
            gem = Gem(x, y, RADII)
            if i != 11:
                gem.gem_draw(255, 255, 255)
            else:
                gem.gem_draw(0, 239, 213)
            if gem not in gems:
                gems.append(gem)
        firstDraw = False
    else:
        i = 0
        global score, GO_THRU_DOOR

        for gem in gems:
            r, g, b = gem.color
            if gem.taken_off():
                if i == 5: # i == 5, 11 the box-up-gem--trophy
                    gotTrophy = True
                    # sounds
                    pointSound = pygame.mixer.Sound('explosion.wav')
                    pointSound.play()
                    time.sleep(0.5)
                    pointSound.play()
                    pygame.mixer.music.load('music.mp3')
                    pygame.mixer.music.play(-1)
                    # does nothing for 6 sec
                    time.sleep(6)
                    pygame.mixer.music.load('background.wav')
                    pygame.mixer.music.play(-1)
                    GO_THRU_DOOR = "    GO THRU DOOR"
                    score += 300
                    # print(score)
                if i != 5:
                    score += 100
                    pointSound = pygame.mixer.Sound('explosion.wav')
                    pointSound.play()
                    # print(score)
                gems[i] = gem
                gems[i].x += WINDOW_WIDTH
                r, g, b = gem.color
            gems[i].gem_draw(r, g, b)
            i += 1


# represents Dave
class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velX = 20


def redraw_game_window():
    # We have 9 images for our walking animation, I want to show the same image for 3 frames
    # so I use the number 27 as an upper bound for walkCount because 27 / 3 = 9. 9 images shown
    # 3 times each animation.
    global walkCount, door

    # make screen black
    pygame.draw.rect(win, (0, 0, 0), (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))

    show_score(0, 0)
    draw_bar()
    draw_gem()
    # gem.gem_draw(0, 255, 0)
    door = brown_bar(THICK * 12, WINDOW_HEIGHT - 2 * THICK, THICK, THICK)

    if walkCount + 1 >= 27:
        walkCount = 0

    if left:  # If we are facing left
        win.blit(walkLeft[walkCount // 3], (char.x, char.y))
        walkCount += 1  # image is shown 3 times every animation
    elif right:
        win.blit(walkRight[walkCount // 3], (char.x, char.y))
        walkCount += 1
    else:
        win.blit(charImg, (char.x, char.y))  # If the character is standing still

    pygame.display.update()


def won_check():
    global gotTrophy, door, char

    if (door.x < char.x < door.x + door.width) and (door.y < char.y < door.width + door.y):
        if gotTrophy:
            # if the blue bubble is taken
            return True


up = False
run = True
while run:
    # win.blit(charImg, (char.x, char.y))--used in initial phases
    pygame.time.delay(50)  # frame rate controller

    if not isJump:
        char.y = char.y + velY

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # list of all keys pressed
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        # pygame.mixer.music.load('laser.wav')
        char.x -= vel
        left = True
        right = False

    elif keys[pygame.K_RIGHT]:
        # pygame.mixer.music.load('laser.wav')
        char.x += vel
        left = False
        right = True

    else:
        left = False
        right = False
        walkCount = 0

    if not isJump:
        if keys[pygame.K_UP] and canJump:
            moveSound = pygame.mixer.Sound('laser.wav')
            moveSound.play()
            isJump = True
            right = False
            left = False
            walkCount = 0
    else:
        if jumpCount >= -10:
            #  gives a parabolic effect
            char.y -= (jumpCount * abs(jumpCount)) * 0.5
            jumpCount -= 1
        else:
            isJump = False
            jumpCount = 10

    draw_bar()
    # gem = Gem(THICK + RADII, WINDOW_HEIGHT - 5 * THICK - RADII, RADII)
    # door drawn
    # all drawn in game_window...
    conditions = []
    for box in boxes:
        cond = box.no_box_collision()
        if cond:
            conditions.append(cond)
        if True in conditions:
            canJump = True
        else:
            canJump = False

    redraw_game_window()
    # if won, ends game
    # displays thing, upon win
    if won_check():
        pygame.mixer.music.load('trumpet.mp3')
        pygame.mixer.music.play(-1)
        time.sleep(3)
        font = pygame.font.Font('freesansbold.ttf', 50)
        txtVictory = font.render('YOU WIN!', True, (0, 0, 255))
        pygame.draw.rect(win, (0, 0, 0), (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))
        win.blit(txtVictory, (200, WINDOW_HEIGHT // 2))
        pygame.display.update()
        time.sleep(3)
        run = False

# eq to pressing stop[X] button
pygame.quit()
quit()
