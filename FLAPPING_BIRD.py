import random
import sys
import pygame
import time
from pygame.locals import *


FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = 408
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'bluebird-midflap.png'
BACKGROUND = 'background-day.png'
PIPE = 'pipe-green.png'
GAMEOVER = 'gameover.png'
pygame.mixer.init()
backgrmusic = pygame.mixer.music.load('flappybackgrmusic.mp3')
pygame.mixer.music.play(-1)

def welcomeScreen():
    playerX = int(SCREENWIDTH / 5)
    playerY = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height()) / 2)
    messageX = int((SCREENWIDTH - GAME_SPRITES['message'].get_width()) / 2)
    messageY = int(SCREENHEIGHT * 0.13)
    baseX = 0
    while True:
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        SCREEN.blit(GAME_SPRITES['player'], (playerX, playerY))
        SCREEN.blit(GAME_SPRITES['message'], (messageX, messageY))
        SCREEN.blit(GAME_SPRITES['base'], (baseX, GROUNDY))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN and (event.key == K_UP or event.key == K_SPACE):
                return
            # else:
            #     SCREEN.blit(GAME_SPRITES['background'], (0, 0))
            #     SCREEN.blit(GAME_SPRITES['player'], (playerX, playerY))
            #     SCREEN.blit(GAME_SPRITES['message'], (messageX, messageY))
            #     SCREEN.blit(GAME_SPRITES['base'], (baseX, GROUNDY))
            #     pygame.display.update()
            FPSCLOCK.tick(FPS)


def mainGame():
    score = 0

    class bird:
        def __init__(self):
            self.x = SCREENWIDTH/5
            self.y = SCREENHEIGHT/2
            self.virtual_spd = 0
            self.jump_spd = 8
            self.gravity_spd = 0.6
        def jump(self):
            self.virtual_spd = -self.jump_spd
        def move(self):
            self.virtual_spd += self.gravity_spd
            self.y += self.virtual_spd

        def collision(self):
            pipeheight0 = GAME_SPRITES['pipe'][0].get_height()
            self.width = GAME_SPRITES['player'].get_width()
            self.height = GAME_SPRITES['player'].get_height()
            if self.y >= (GROUNDY - 24):
                GAME_SOUNDS['die'].play()
                return True
            for pipe in upperPipes:
                if (self.y < pipeheight0 + pipe['y'] and abs(self.x - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
                    GAME_SOUNDS['hit'].play()
                    return True
            for pipe in lowerPipes:
                # if (self.y +  self.height > pipe['y'] ) and (self.x + self.width > pipe['x']):
                if (self.y +  self.height > pipe['y'] ) and abs(self.x - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
                    GAME_SOUNDS['hit'].play()
                    return True

            return False

    #first set of pipes
    newpipe1 = getRandomPipe() #1st upper and lower pipe both
    newpipe2 = getRandomPipe() #2nd upper and lower pipe both


    upperPipes = [
        {'x': SCREENWIDTH + 200 , 'y': newpipe1[0]['y']}, #for 1st pipe
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH/2), 'y': newpipe2[0]['y']}, #for 2nd pipe

    ]
    lowerPipes = [
        {'x': SCREENWIDTH + 200 , 'y': newpipe1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH/2), 'y': newpipe2[1]['y']},

    ]

    pipe_x_change = -4
    bird = bird()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                # if playery > 0:
                if bird.y > 0:
                    bird.jump()
                    GAME_SOUNDS['wing'].play()

        #move pipes to the left
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipe_x_change
            lowerPipe['x'] += pipe_x_change

        # if upperPipes[0]['x'] < 15:
        if 0 < upperPipes[0]['x'] < 5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        #if pipes are out of the screen, then remove them
        # if upperPipes[0]['x'] < 10:
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        bird.move()

        birdheight = GAME_SPRITES['player'].get_height()
        if bird.y > (GROUNDY - birdheight):
            bird.y = GROUNDY - birdheight

        if upperPipes[0]['x'] < bird.x < upperPipes[0]['x']+4:
            score += 1
            GAME_SOUNDS['point'].play()
        if bird.collision() == True:
            over_rect = GAME_SPRITES['over'].get_rect(center = (int(SCREENWIDTH/2),int(SCREENHEIGHT/2.5)))
            SCREEN.blit(GAME_SPRITES['over'], over_rect)
            pygame.display.update()
            time.sleep(2)
            return

        SCREEN.blit(GAME_SPRITES['background'], (0,0))

        for upperPipe,lowerPipe in zip(upperPipes,lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (int(upperPipe['x']), int(upperPipe['y'])))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (int(lowerPipe['x']), int(lowerPipe['y'])))

        SCREEN.blit(GAME_SPRITES['base'], (0,408))
        SCREEN.blit(GAME_SPRITES['player'], (int(bird.x), int(bird.y)))
        font = pygame.font.Font('ARCADECLASSIC.TTF', 30)
        score_text = font.render(f"SCORE {score}",  True, (0,0,0))
        text_rect = score_text.get_rect(center = (int(SCREENWIDTH/2), int(SCREENHEIGHT/5)))
        SCREEN.blit(score_text, text_rect)



        pygame.display.update()
        FPSCLOCK.tick(30)

def getRandomPipe():

    upperPipeX = SCREENWIDTH + 10
    upperPipeY = -(random.randrange(100, (GROUNDY - 100)))
    lowerPipeX = SCREENWIDTH + 10
    upper_pipe_in_the_screen = (320 +upperPipeY)
    lowerPipeY = (200 + upper_pipe_in_the_screen)
    pipe_object = [
        {'x': upperPipeX, 'y': upperPipeY},
        {'x': lowerPipeX, 'y': lowerPipeY}
    ]
    return pipe_object

if __name__ == '__main__':
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption("Flappy Bird Game")
    GAME_SPRITES['message'] = pygame.image.load('message.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
        pygame.image.load(PIPE).convert_alpha()
    )

    GAME_SOUNDS['die'] = pygame.mixer.Sound('die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('point.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('wing.wav')

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert_alpha()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()
    GAME_SPRITES['over'] = pygame.image.load(GAMEOVER).convert_alpha()

    while True:
        welcomeScreen()
        mainGame()
