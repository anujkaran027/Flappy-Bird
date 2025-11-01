import pygame
import sys
import random
from pygame.locals import *

class Button:
    def __init__(self, msg, x, y, image,textlength):
        self.x = x
        self.y = y
        self.msg = msg
        self.txtlen = int(textlength/2)*10
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.font = pygame.font.SysFont("comicsansms",30)
        
        self.clicked = False

    def draw(self,screen):
        action = False
        m_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(m_pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        screen.blit(self.image,(self.rect.x,self.rect.y))

        #text in button
        self.textrect = ((self.x+(self.width/2)-35-self.txtlen), (self.y + (self.height/2)-25))
        screen.blit(self.font.render(self.msg, True , (255,0,0)), self.textrect)

        return action

#variables
SCREENWIDTH = 500
SCREENHEIGHT = 692
SCREEN = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
CLOCK = pygame.time.Clock()
GAME_IMAGES = {}
GAME_SOUNDS = {}
GROUND = 495

def homescreen():

    playerx = int(SCREENWIDTH/5-70)
    playery = int((SCREENWIDTH -  GAME_IMAGES['player'].get_height())/2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif Play_button.draw(SCREEN) or (event.type==pygame.KEYDOWN and event.key==K_SPACE):
            gamestart()
        elif Quit_button.draw(SCREEN):
            pygame.quit()
            sys.exit()
        else:
            SCREEN.blit(GAME_IMAGES['background'],(0,0))
            SCREEN.blit(GAME_IMAGES['base'],(0,495))
            Play_button.draw(SCREEN)
            Quit_button.draw(SCREEN)
            SCREEN.blit(GAME_IMAGES['player'],(playerx,playery))
            pygame.display.flip()
            CLOCK.tick(60)


def pausemenu(player_x,player_y,upperpipes,lowerpipes,bgx):         
    while PAUSE:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type==pygame.KEYDOWN and event.key==K_ESCAPE:
                return
            
            elif Resume_button.draw(SCREEN) or (event.type==pygame.KEYDOWN and event.key==K_SPACE):
                return
            
            elif Restart_button.draw(SCREEN):
                restart = True
                return restart

            elif Exit_button.draw(SCREEN):
                pygame.quit()
                sys.exit()

            else:
                SCREEN.blit(GAME_IMAGES['background'],(bgx,0))
                for upperpipe , lowerpipe in zip(upperpipes,lowerpipes):
                    SCREEN.blit(GAME_IMAGES['pipe1'], (upperpipe['x'], upperpipe['y']))
                    SCREEN.blit(GAME_IMAGES['pipe2'], (lowerpipe['x'], lowerpipe['y']))
                SCREEN.blit(GAME_IMAGES['base'],(0,495))
                SCREEN.blit(GAME_IMAGES['player'],(player_x,player_y))
                Resume_button.draw(SCREEN)      
                Restart_button.draw(SCREEN)
                Exit_button.draw(SCREEN)
                pygame.display.flip()
                CLOCK.tick(60)

def gameover(score):
    font = pygame.font.SysFont("comicsansms", 40)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                return True

        SCREEN.blit(GAME_IMAGES['background'], (0, 0))
        SCREEN.blit(GAME_IMAGES['base'], (0, 495))

        # "Game Over"
        text = font.render("Game Over", True, (0, 0, 0))
        SCREEN.blit(text, (SCREENWIDTH//2 - text.get_width()//2, 70))

        # Score
        score_text = font.render(f"Score: {score}", True, (255, 255, 0))
        SCREEN.blit(score_text, (SCREENWIDTH//2 - score_text.get_width()//2, 230))

        # continue
        continue_text = font.render("Press Space To Continue", True, (0, 0, 0))
        SCREEN.blit(continue_text, (30, 430))
        
        pygame.display.update()
        CLOCK.tick(60)

def gamestart():
    global PAUSE
    global crashTest

    score = 0
    playerx = int(SCREENWIDTH/5-70)
    playery = int((SCREENWIDTH -  GAME_IMAGES['player'].get_height())/2)

    pipe1 = getpipe()
    pipe2 = getpipe()

    upperpipes = [
        {'x':SCREENWIDTH+200, 'y':pipe1[0]['y']},
        {'x':SCREENWIDTH+200+(SCREENWIDTH/2), 'y':pipe2[0]['y']},
    ]
    lowerpipes = [
        {'x':SCREENWIDTH+200, 'y':pipe1[1]['y']},
        {'x':SCREENWIDTH+200+(SCREENWIDTH/2), 'y':pipe2[1]['y']},
    ]

    pipemovingframe = -5                      
    playervely = -11
    playermaxvely = 10
    falldistance = 1
    jumpdistance = -8
    jump = False
    movebasespeed = -2
    movebase = 0
    movebg = 0
    movebgspeed = -2

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
                PAUSE = True
                go_home = pausemenu(playerx,playery,upperpipes,lowerpipes,bgx)
                if go_home:
                    return

            if event.type==pygame.KEYDOWN and event.key==K_SPACE:
                
                if playery > 0:
                    playervely = jumpdistance
                    jump =True
                    GAME_SOUNDS['fly'].play()

        crashTest = iscollide(playerx, playery, upperpipes, lowerpipes)
        if crashTest:
            if gameover(score):
                return
            
        playerpos = playerx + GAME_IMAGES['player'].get_width()/2
        for pipe in upperpipes:
            pipepos = pipe['x'] + GAME_IMAGES['pipe1'].get_width()/2
            if pipepos <= playerpos < pipepos+6:
                score += 1
                GAME_SOUNDS['point'].play()

        if playervely < playermaxvely and not jump:
            playervely += falldistance

        if jump:
            jump = False

        playerheight = GAME_IMAGES['player'].get_height()
        ground = 495
        playery= playery + min(playervely, ground - playery - playerheight)

        for upperpipe , lowerpipe in zip(upperpipes,lowerpipes):
            upperpipe['x'] += pipemovingframe
            lowerpipe['x'] += pipemovingframe

        if 0 <upperpipes[0]['x']<7 :
            newpipe = getpipe()
            upperpipes.append(newpipe[0])
            lowerpipes.append(newpipe[1])

        if upperpipes[0]['x'] < - GAME_IMAGES['pipe1'].get_width():
            upperpipes.pop(0)
            lowerpipes.pop(0)
        
        #move bg
        for i in range(0,3):
            movebg += movebgspeed

        bgwidth = GAME_IMAGES['background'].get_width()

        if abs(movebg) > bgwidth:
            movebg = 0

        #move base
        for i in range(0,3):
            movebase += movebasespeed   

        basewidth = GAME_IMAGES['base'].get_width()

        if abs(movebase) > basewidth+basewidth:
            movebase = 0

        #scoring
        score_list = [int(x) for x in list(str(score))]
        scorewidth = 0
        for num in score_list:
            scorewidth += GAME_IMAGES['scores'][num].get_width()
        scorex = (SCREENWIDTH - scorewidth)/2


        for i in range(0,3):
            bgx = i*(bgwidth) + movebg
            SCREEN.blit(GAME_IMAGES['background'],(i*(bgwidth) + movebg,0))
        for upperpipe , lowerpipe in zip(upperpipes,lowerpipes):
            SCREEN.blit(GAME_IMAGES['pipe1'], (upperpipe['x'], upperpipe['y']))
            SCREEN.blit(GAME_IMAGES['pipe2'], (lowerpipe['x'], lowerpipe['y']))
        for i in range(0,3):
            SCREEN.blit(GAME_IMAGES['base'], (i*(basewidth-(20*i)) + movebase, 495))
        for num in score_list:
            SCREEN.blit(GAME_IMAGES['scores'][num], (scorex , 100))
            scorex += GAME_IMAGES['scores'][num].get_width()
        SCREEN.blit(GAME_IMAGES['player'], (playerx,playery))
        pygame.display.flip()
        CLOCK.tick(30)
      


def getpipe():
    pipeheight = GAME_IMAGES['pipe1'].get_height()
    pipegap = 150
    pipey2 = pipegap + random.randrange(0,int(SCREENHEIGHT - GAME_IMAGES['base'].get_height() - 1.5*pipegap))
    pipex = SCREENWIDTH + 10
    pipey1 = int(pipeheight - pipey2 + pipegap)
    pipe = [
        {'x': pipex, 'y': -pipey1},
        {'x': pipex, 'y': pipey2}
    ]
    return pipe

def iscollide(playerx, playery, upperpipes, lowerpipes):
    if playery > GROUND-52 or playery<0:
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upperpipes:
        pipeh = GAME_IMAGES['pipe1'].get_height()
        if (playery < pipeh + pipe['y']) and abs(playerx - pipe['x']) < GAME_IMAGES['pipe1'].get_width():
            GAME_SOUNDS['hit'].play()
            return True
    
    for pipe in lowerpipes:
        if (playery + GAME_IMAGES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_IMAGES['pipe1'].get_width():
            GAME_SOUNDS['hit'].play()
            return True


pygame.init()

PAUSE = False

pygame.display.set_caption('Flappy Bird By Anuj Karan')

GAME_IMAGES['scores'] = (
    pygame.image.load('assets/images/0.png').convert_alpha(),
    pygame.image.load('assets/images/1.png').convert_alpha(),
    pygame.image.load('assets/images/2.png').convert_alpha(),
    pygame.image.load('assets/images/3.png').convert_alpha(),
    pygame.image.load('assets/images/4.png').convert_alpha(),
    pygame.image.load('assets/images/5.png').convert_alpha(),
    pygame.image.load('assets/images/6.png').convert_alpha(),
    pygame.image.load('assets/images/7.png').convert_alpha(),
    pygame.image.load('assets/images/8.png').convert_alpha(),
    pygame.image.load('assets/images/9.png').convert_alpha(),
)

GAME_IMAGES['player'] = pygame.image.load('assets/images/player.png').convert_alpha()
GAME_IMAGES['background'] = pygame.image.load('assets/images/bg.png').convert_alpha()
GAME_IMAGES['pipe1'] = pygame.transform.rotate(pygame.image.load('assets/images/pipe.png').convert_alpha(), 180)
GAME_IMAGES['pipe2'] = pygame.image.load('assets/images/pipe.png').convert_alpha()
GAME_IMAGES['base'] = pygame.image.load('assets/images/base.png').convert_alpha()
GAME_IMAGES['bluebutton'] = pygame.image.load('assets/images/bluebutton.png').convert_alpha()
GAME_IMAGES['yellowbutton'] = pygame.image.load('assets/images/yellowbutton.png').convert_alpha()
GAME_IMAGES['greenbutton'] = pygame.image.load('assets/images/greenbutton.png').convert_alpha()

GAME_SOUNDS['hit'] = pygame.mixer.Sound('assets/sounds/hit.mp3')
GAME_SOUNDS['fly'] = pygame.mixer.Sound('assets/sounds/fly.mp3')
GAME_SOUNDS['bgm'] = pygame.mixer.Sound('assets/sounds/bgm.mp3')
GAME_SOUNDS['point'] = pygame.mixer.Sound('assets/sounds/point.mp3')

buttonx = int((SCREENWIDTH - GAME_IMAGES['bluebutton'].get_width())/2)

#main menu button
Play_button = Button('PLAY',buttonx,120,GAME_IMAGES['greenbutton'],0)
# Help_button = Button('HELP',buttonx,220,GAME_IMAGES['yellowbutton'],0)
Quit_button = Button('QUIT',buttonx,320,GAME_IMAGES['bluebutton'],0)

#pause buttons
Resume_button = Button('RESUME',buttonx,150,GAME_IMAGES['bluebutton'],6)
Restart_button = Button('RESTART',buttonx,250,GAME_IMAGES['yellowbutton'],7)
Exit_button = Button('QUIT',buttonx,350,GAME_IMAGES['greenbutton'],0)

while True:
    homescreen()
