import pygame
import sys
import random
import os
from pygame.locals import *
import time
pygame.init()
screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()
font = pygame.font.Font('assets/ElectronPulseItalic-6YJX1.ttf',40)
score = 0
player_name_input = ""
background = pygame.image.load('assets/darkPurple.png')
background = pygame.transform.scale(background,(800,800))
laser_sound = pygame.mixer.Sound('assets/sfx_laser1.ogg')
pygame.display.set_caption("Space Shooter")
passed_aliens = 0
typingName = False
high_score = {'high score': 0, 'name': 'Player'}
class player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('assets/BAOyZX.png')
        self.image = pygame.transform.scale(self.image,(60,60))
        self.rect = self.image.get_rect(center=(400,500))
        self.speed = 6

    def update(self,keys):
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed
        self.rect.x = max(0,min(self.rect.x,800-self.rect.width))
        self.rect.y = max(0,min(self.rect.y,600-self.rect.height))


class alien(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image1 = pygame.image.load('assets/matt-smith-boss.gif')
        self.image1 = pygame.transform.scale(self.image1,(68,68))
        self.image2 = pygame.image.load('assets/matt-smith-enemy.gif')
        self.image2 = pygame.transform.scale(self.image2,(60,60))
        if random.randint(0,1)==0:
            self.image = self.image1
        else:
            self.image = self.image2
        self.rect = self.image.get_rect(center=(random.randint(50,750),random.randint(-200,100)))
        self.speed = random.randint(2,4)

    def update(self):
        global passed_aliens
        self.rect.y += self.speed
        if self.rect.top >600:
            self.kill()
            passed_aliens += 1
    
class laser(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load('assets/laserBlue07.png')
        self.rect = self.image.get_rect(center=(x,y))
        self.speed = -15
    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom <0:
            self.kill()

player1 = player()
playerGroup = pygame.sprite.GroupSingle(player1)
laser_bullets = pygame.sprite.Group()
aliens =pygame.sprite.Group()
alienTimer = 0
game_over = False
running = True
can_restart = True

while running:
    keys = pygame.key.get_pressed()
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if typingName:
            if event.type==KEYDOWN:
                if event.key == K_RETURN:
                    high_score["high score"]=int(highScore)
                    high_score["name"]= player_name_input
                    typingName= False
                elif event.key == K_BACKSPACE:
                    player_name_input = player_name_input[:-1]
                else:
                    if len(player_name_input) < 11:
                        player_name_input += event.unicode
        if event.type == KEYDOWN and event.key == K_SPACE and not game_over:
            laser_sound.play()
            laser_shoot = laser(player1.rect.centerx,player1.rect.top)
            laser_bullets.add(laser_shoot)
        if event.type == KEYUP and event.key == K_r:
            can_restart = True 
        

    if not game_over and not typingName:
        playerGroup.update(keys)
        laser_bullets.update()
        aliens.update()

        alienTimer += 1
        if alienTimer > 30:
            aliens.add(alien())
            alienTimer = 0

        hits = pygame.sprite.groupcollide(aliens,laser_bullets,True,True)
        for i in hits:
            score +=1

        if pygame.sprite.spritecollide(player1,aliens,False):
            game_over = True
        
        playerGroup.draw(screen)
        laser_bullets.draw(screen)
        aliens.draw(screen)
        scoreText = font.render(f'Score:{score}',True,(255,255,255))
        screen.blit(scoreText,(15,15))
    else:
        gameOverT = font.render('Game Over press R to restart',True,(255,0,0))
        screen.blit(gameOverT,(70,250))

        scoreText = font.render(f'Score:{score}',True,(255,255,255))
        screen.blit(scoreText,(70,300))

        alienText = font.render(f'Passed Aliens:{passed_aliens}',True,(255,255,255))
        screen.blit(alienText,(70,350))

        highScore = (score/(max(passed_aliens/2,1)))
        highScoreText = font.render(f'High Score: {high_score["high score"]} by {high_score["name"]}',True,(255,255,0))
        screen.blit(highScoreText,(70,400))

        if highScore > high_score["high score"] and not typingName:
            typingName = True
            player_name_input = ""

        if typingName:
            inputText = font.render(f'Enter your name: {player_name_input}_',True,(255,255,255))
            screen.blit(inputText,(70,450))

        if keys[pygame.K_r] and can_restart and not typingName:
            passed_aliens = 0
            can_restart = False
            game_over = False
            score = 0
            aliens.empty()
            laser_bullets.empty()
            player1.rect.center=(400,500)
            can_restart= False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

