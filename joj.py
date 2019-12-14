import math
import random

import pygame
from pygame import mixer

# inicialização
pygame.init ()

# tela
screen = pygame.display.set_mode ( (800 , 600) )

# background
background = pygame.image.load ( 'RiodeJaneiro2076.png' ).convert ()
background = pygame.transform.scale ( background , (800 , 600) )

#BGM
mixer.music.load('potencial.mp3')
mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

# titulo e icone
pygame.display.set_caption ( "Potência" )
icon = pygame.image.load ( 'icon.png' )
pygame.display.set_icon ( icon )

# Player
playerIMG = pygame.image.load ( 'spaceship.png' )
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyIMG = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 7

for i in range(num_of_enemies):
    enemyIMG.append(pygame.image.load ( 'inimigo.png' ))
    enemyX.append(random.randint ( 0 , 800 ))
    enemyY.append(random.randint ( 50 , 150 ))
    enemyX_change.append(1.5)
    enemyY_change.append(40)

# Bullet
bulletIMG = pygame.image.load ( 'Pytiro.png' )
bulletIMG = pygame.transform.scale ( bulletIMG , (32 , 32) )
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 5
bullet_state = "ready"

#pontuação

score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)


textX = 10
textY = 10

#game over text
over_font = pygame.font.Font('freesansbold.ttf',70)


def show_score(x,y):
    score = font.render("Score:"+ str(score_value),True, (255,255,255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("FALTOU POTÊNCIA", True, (255,255,255))
    screen.blit(over_text, (60,250))


def player(x , y) :
    screen.blit ( playerIMG , (x , y) )


def enemy(x , y, i) :
    screen.blit ( enemyIMG[i] , (x , y) )


def fire_bullet(x , y) :
    global bullet_state
    bullet_state = "fire"
    screen.blit ( bulletIMG , (x + 16 , y + 10) )


def isCollision(enemyX , enemyY , bulletX , bulletY) :
    distance = math.sqrt ( math.pow ( enemyX - bulletX , 2 ) + (math.pow ( enemyY - bulletY , 2 )) )
    if distance <= 27 :
        return True
    else :
        return False


# Game Loop

running = True
while running :
    screen.fill ( (0 , 0 , 0) )

    # background
    screen.blit ( background , (0 , 0) )

    for event in pygame.event.get () :
        if event.type == pygame.QUIT :
            running = False

        # Direita e esquerda
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_LEFT :
                playerX_change = -0.8
            if event.key == pygame.K_RIGHT :
                playerX_change = 0.8
        if event.type == pygame.KEYUP :
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT :
                playerX_change = 0
            if event.key == pygame.K_SPACE :
                if bullet_state == "ready" :
                    bullet_Sound = mixer.Sound('pew.wav')
                    bullet_Sound.play()
                    bulletX = playerX
                    fire_bullet ( bulletX , bulletY )

    playerX += playerX_change

    # Barreiras

    if playerX <= 0 :
        playerX = 0
    elif playerX >= 736 :
        playerX = 736

    # movimento do inimigo
    for i in range(num_of_enemies):

        #game over
        if enemyY[i] > 360:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            FERROU_sound = mixer.Sound('FERROU.wav')
            FERROU_sound.play()
            pygame.mixer_music.stop()
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0 :
            enemyX_change[i] = 0.65
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 730 :
             enemyX_change[i] = -0.65
             enemyY[i] += enemyY_change[i]

        # colisão
        collision = isCollision( enemyX[i] , enemyY[i] , bulletX , bulletY )
        if collision :
            bulletY = 480
            bullet_state = "ready"
            score_value += 10
            enemyX[i] = random.randint ( 0 , 735 )
            enemyY[i] = random.randint ( 50 , 150 )

        enemy ( enemyX[i] , enemyY[i], i )

    # movimento do tiro
    if bulletY <= 0 :
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire" :
        fire_bullet ( bulletX , bulletY )
        bulletY -= bulletY_change

    player ( playerX , playerY )
    show_score(textX,textY)
    pygame.display.update ()
