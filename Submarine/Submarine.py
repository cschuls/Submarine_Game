#+ - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#+
#+     Simple Submarine Game Written in Python
#+
#+     Copyright (C) 2018, 2019, 2020, 2021, 2022 by Craig Schulstad
#+
#+ This program is free software; you can redistribute it and/or modify
#+ it under the terms of the GNU General Public License as published by
#+ the Free Software Foundation; either version 2 of the License, or
#+ (at your option) any later version.
#+
#+ This program is distributed in the hope that it will be useful,
#+ but WITHOUT ANY WARRANTY; without even the implied warranty of
#+ MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#+ GNU General Public License for more details.
#+
#+ You should have received a copy of the GNU General Public License
#+ along with this program; if not, write to the Free Software
#+ Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#+
#+ - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

#+ - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#+ Note this program runs using "python3"
#+ - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

import pygame
import time
import pygame.mixer
import random
import math

pygame.init()
pygame.mixer.init()

smallfont = pygame.font.SysFont(None, 25)
mediumfont = pygame.font.SysFont(None, 40)
largefont = pygame.font.SysFont(None, 80)
display_width  = 800
display_height = 600
FPS = 60

# Colours

WHITE = (255, 255, 255)
LIGHTBLUE = (179, 231, 255)
GREEN = (0, 200, 0)
SAND = (194,178,128)
AQUA = (160, 240, 240)
GRAY = (128,128,128)
BLACK = (0,0,0)

# Boundaries for the submarine

SUBMIN = 80
SUBMAX = 500
SUBLEFT = 30
SUBRIGHT = 670

# Images used in this game

subimage = pygame.image.load('Sub.png')
bottom = pygame.image.load('Bottom.png')
sky = pygame.image.load('Sky.png')
torpedo = pygame.image.load('Torpedo.png')
mineimage = pygame.image.load('Mine.png')
kaboom = pygame.image.load('Boom.png')
gameicon = pygame.image.load('Periscope.png')

# Sound files used in this game

sonar_ping = pygame.mixer.Sound('Sonar.wav')
torpedo_launch = pygame.mixer.Sound('Torpedo.wav')
explosion = pygame.mixer.Sound('Explosion.wav')

pygame.display.set_icon(gameicon)
gameDisplay  = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Submarine')
clock = pygame.time.Clock()



# Check for a collision between the subamarine and a mine

def collision(object_x, object_y, object_width, object_height, mlist, minecount):
    for eachMine in mlist:
        if object_x < eachMine[0]+ minecount and object_x + object_width > eachMine[0]+minecount and object_y < eachMine[1] and object_y + object_height> eachMine[1]:
            return eachMine
        if object_x < eachMine[0]+ minecount and object_x + object_width > eachMine[0]+minecount and object_y < eachMine[1] + 20 and object_y > eachMine[1]:
            return eachMine
    return -1, -1

# Display the current level - the level is incremented every time the submarine gets through a group of mines

def displayLevel(level):
    text = smallfont.render("Level: " + str(level), True, BLACK)
    gameDisplay.blit(text, [0,20])

#Display the current score - the score is incremented for every mine destroyed

def displayScore(score):
    text = smallfont.render("Mines: " + str(score), True, BLACK)
    gameDisplay.blit(text, [0,0])

# Draw the bottom of the ocean - the bottom image file is moved one pixel for every frame

def drawBottom(bottomLoc):
    gameDisplay.blit(bottom, (bottomLoc, 540))
    gameDisplay.blit(bottom, ((bottomLoc + display_width), 540))
    return

# Draw the group of mines - the mine locations actually start off the right side of the display window and are moved one pixel for every frame

def drawMines(mlist, minecount, lvl, override):
    for eachMine in mlist:
        if lvl < 3 or override == True:
            gameDisplay.blit(mineimage, (eachMine[0]+minecount,eachMine[1]))

# Draw the sky - the sky image is moved at a slower rate across the top of the display

def drawSky(skyLoc):
    x = int(skyLoc/60)
    gameDisplay.blit(sky, (x, 0))
    gameDisplay.blit(sky, ((x + display_width), 0))
    return

# An introduction screen denoting how the game is played.

def game_intro():

    intro = True

    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    intro = False
                if event.key == pygame.K_q and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    pygame.quit()
                    quit()

        gameDisplay.fill(AQUA)
        drawSky(0)
        drawBottom(0)
        welcome = largefont.render("Welcome to Submarine", True, BLACK)
        gameDisplay.blit(welcome, [80,40])
        welcome = smallfont.render("The goal of the game is to pass through as many mine fields as possible.", True, WHITE)
        gameDisplay.blit(welcome, [80,120])
        welcome = smallfont.render("Every mine field passed through increments the level, and every mine", True, WHITE)
        gameDisplay.blit(welcome, [80,140])
        welcome = smallfont.render("destroyed by a torpedo increments the score.  The mines are visible for", True, WHITE)
        gameDisplay.blit(welcome, [80,160])
        welcome = smallfont.render("the first two levels.  After that, the mines are invisible and can only", True, WHITE)
        gameDisplay.blit(welcome, [80,180])
        welcome = smallfont.render("be detected if in sonar range when using the submarine's sonar system.", True, WHITE)
        gameDisplay.blit(welcome, [80,200])
        welcome = smallfont.render("The game continues until the submarine hits an underwater mine.  Good Luck!", True, WHITE)
        gameDisplay.blit(welcome, [80,220])
        welcome = mediumfont.render("Controls", True, WHITE)
        gameDisplay.blit(welcome, [80,260])
        welcome = smallfont.render("Up Arrow", True, WHITE)
        gameDisplay.blit(welcome, [100,300])
        welcome = smallfont.render("Move the submarine up towards the surface", True, WHITE)
        gameDisplay.blit(welcome, [240,300])
        welcome = smallfont.render("Down Arrow", True, WHITE)
        gameDisplay.blit(welcome, [100,320])
        welcome = smallfont.render("Move the submarine down towards the ocean floor", True, WHITE)
        gameDisplay.blit(welcome, [240,320])
        welcome = smallfont.render("Left Arrow", True, WHITE)
        gameDisplay.blit(welcome, [100,340])
        welcome = smallfont.render("Move the submarine to the left on the screen", True, WHITE)
        gameDisplay.blit(welcome, [240,340])
        welcome = smallfont.render("Right Arrow", True, WHITE)
        gameDisplay.blit(welcome, [100,360])
        welcome = smallfont.render("Move the submarine to the right on the screen", True, WHITE)
        gameDisplay.blit(welcome, [240,360])
        welcome = smallfont.render("Spacebar", True, WHITE)
        gameDisplay.blit(welcome, [100,380])
        welcome = smallfont.render("Launch a torpedo - only one torpedo at a time", True, WHITE)
        gameDisplay.blit(welcome, [240,380])
        welcome = smallfont.render("The 'S' key", True, WHITE)
        gameDisplay.blit(welcome, [100,400])
        welcome = smallfont.render("Send out a sonar signal", True, WHITE)
        gameDisplay.blit(welcome, [240,400])
        welcome = smallfont.render("CTRL+'Q'", True, WHITE)
        gameDisplay.blit(welcome, [100,420])
        welcome = smallfont.render("Quit", True, WHITE)
        gameDisplay.blit(welcome, [240,420])
        welcome = smallfont.render("CTRL+'R'", True, WHITE)
        gameDisplay.blit(welcome, [100,440])
        welcome = smallfont.render("Start a new game.", True, WHITE)
        gameDisplay.blit(welcome, [240,440])
        gameDisplay.blit(subimage, (10, display_height - 80))
        gameDisplay.blit(mineimage, (180,display_height - 74))
        pygame.display.update()
        clock.tick(10)

# Display an expanding circle to simulate a sonar wave travelling through the water

def ping(cycles, cx, cy):
    circle_size = int(cycles*4) + 2
    pygame.draw.circle(gameDisplay, GRAY, (cx, cy), circle_size, 2)
    if circle_size >= 300:
        return False
    else:
        return True

# Determine if a torpedo has hit a mine - if so, this will trigger an explosion display, remove the mine from the screen, and increment the score

def torpedo_collision(torp_x, torp_y, torp_width, torp_height, mlist, minecount):
    for eachMine in mlist:
        if torp_x + torp_width > eachMine[0] + minecount - 5 and torp_x + torp_width < eachMine[0] + minecount + 25 and torp_y > eachMine[1] and torp_y < eachMine[1] + 30:
            return eachMine
    return -1, -1

# The start of the game loop
# Current controls:
#       Arrow up        Move the submarine up
#       Arrow down      Move the submarine down
#       Arrow left      Move the submarine to the left
#       Arrow right     Move the submarine to the right
#       S               Send out a sonar ping
#       T or Space      Shoot a torpedo - note only one torpedo can be in the water at a time
#       Ctrl-R          Restart the game
#       Ctrl-Q          Quit - clicking the "X" on the top of the window will also quit the game
def gameLoop():

    gameExit = False
    blink = 0
    toggle = True
    bottomLoc = 1
    skyLoc = 1
    sub_x = 220
    sub_y = 220
    subChange = 0
    subMove = 0
    sonar = False
    torpedoVisible = False
    playSonar = False
    playTorpedo = False
    counter = 0
    torpedo_x = 0
    torpedo_y = 0
    showBoom = 0
    gameOver = False
    subHit = False
    xx = 0
    yy = 0
    override = False
    score = 0
    level = 1
    minecounter = 0
    minelist = []
    for xx in range(0,11):
        yy = int(random.randrange(SUBMIN+20, SUBMAX-20))
        tup = ((display_width + xx * 60),yy)
        minelist.append(tup)

    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    gameExit = True
                if event.key == pygame.K_r and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    gameOver = False
                    bottomLoc = 1
                    skyLoc = 1
                    sub_x = 220
                    sub_y = 220
                    subChange = 0
                    subMove = 0
                    sonar = False
                    torpedoVisible = False
                    playSonar = False
                    playTorpedo = False
                    counter = 0
                    torpedo_x = 0
                    torpedo_y = 0
                    showBoom = 0
                    gameOver = False
                    subHit = False
                    xx = 0
                    yy = 0
                    score = 0
                    level = 1
                    minecounter = 0
                    minelist = []
                    for xx in range(0,11):
                        yy = int(random.randrange(SUBMIN+20, SUBMAX-20))
                        tup = ((display_width + xx * 60),yy)
                        minelist.append(tup)
                if event.key == pygame.K_DOWN:
                    subChange = 1
                if event.key == pygame.K_UP:
                    subChange = -1
                if event.key == pygame.K_RIGHT:
                    subMove = 1
                if event.key == pygame.K_LEFT:
                    subMove = -1
                if event.key == pygame.K_s and gameOver == False:
                    if playSonar == False:
                        sonar_ping.play()
                    sonar = True
                if event.key == pygame.K_t or event.key == pygame.K_SPACE:
                    if playTorpedo == False:
                        torpedo_launch.play()
                        torpedoVisible = True
                        torpedo_x = sub_x + 110
                        torpedo_y = sub_y +24
                        playTorpedo = True
            if event.type == pygame.KEYUP:
                subChange = 0
                subMove = 0

        sub_x += subMove
        sub_y += subChange

        if sub_y < SUBMIN:
            sub_y = SUBMIN

        if sub_y > SUBMAX:
            sub_y = SUBMAX

        if sub_x < SUBLEFT:
            sub_x = SUBLEFT

        if sub_x > SUBRIGHT:
            sub_x = SUBRIGHT

        bottomLoc -= 1
        if bottomLoc < ((display_width - 1) * -1):
            bottomLoc = 0

        skyLoc -= 1
        if skyLoc < ((display_width * 60 - 1) * -1):
            skyLoc = 0

        gameDisplay.fill(AQUA)

        if sonar == True:
            counter += 1
            sonar = ping(counter,sub_x + 110,sub_y+24)
        else:
            counter = 0
            sonarsize = 0

        if torpedoVisible == True:
            torpedo_x += 2
            gameDisplay.blit(torpedo, (torpedo_x, torpedo_y))
            if torpedo_x > display_width:
                torpedoVisible = False
                playTorpedo = False

        if gameOver == False:
            minecounter -= 1

        if minecounter < (display_width * 2 * -1):
            level += 1
            minecounter = 0
            minelist = []
            for xx in range(0,11):
                yy = int(random.randrange(SUBMIN+20, SUBMAX-20))
                tup = ((display_width + xx * 60),yy)
                minelist.append(tup)

        for theMine in minelist:
            distance = int(math.sqrt((theMine[0] + minecounter - sub_x)**2 + (theMine[1] - sub_y)**2))
            if distance <= counter * 4:
                override = True
                break

        drawMines(minelist,minecounter,level,override)
        override = False

        hit = collision(sub_x, sub_y, 102,36 , minelist,minecounter)

        if hit[0] != -1:
            subHit = True

        if hit[0] == -1 and playTorpedo == True:
            hit = torpedo_collision(torpedo_x, torpedo_y, 25, 3, minelist, minecounter)
        
        if hit[0] != -1:
            score +=1
            for idx in range(0, len(minelist)):
                cc = idx
                if cc == len(minelist):
                    break
                if hit == minelist[idx]:
                    del minelist[idx]
                    xx = hit[0]
                    yy = hit[1]
                    showBoom = 15
                    explosion.play()
                    #pygame.mixer.music.load('Explosion.wav')
                    #pygame.mixer.music.play()
                    playTorpedo = False
                    torpedo_x = 2000
                    break

        if showBoom > 0:
            gameDisplay.blit(kaboom, (xx + minecounter - 10,yy))
            showBoom -= 1

        if showBoom <= 0 and subHit == True:
            gameOver = True

        if gameOver == False:
            drawBottom(bottomLoc)
            drawSky(skyLoc)
            gameDisplay.blit(subimage, (sub_x, sub_y))
        else:
            drawBottom(1)
            drawSky(1)
            text = largefont.render("Game Over", True, WHITE)
            gameDisplay.blit(text, [240,300])
            blink += 1
            if blink%90 == 0:
                if toggle == True:
                    toggle = False
                else:
                    toggle = True
            if toggle == True:
                text = mediumfont.render("Press CTRL+'R' to play again or CTRL+'Q' to quit.", True, WHITE)
                gameDisplay.blit(text, [80,380])
            gameDisplay.blit(subimage, (10, display_height - 80))
        
        displayScore(score)
        displayLevel(level)
        pygame.display.update()
        clock.tick(FPS)
        
    pygame.quit()
    quit()

game_intro()
gameLoop()
