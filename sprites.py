import pygame as pg
from pygame.sprite import Sprite

from pygame.math import Vector2 as vec
import os
from settings import *
import math
from math import floor
import random 
from random import randint

# setup asset folders here - images sounds etc.
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
snd_folder = os.path.join(game_folder, 'sounds')




class Cooldown():
    def __init__(self):
        self.current_time = 0
        self.event_time = 0
        self.delta = 0
        # ticking ensures the timer is counting...
    def ticking(self):
        self.current_time = floor((pg.time.get_ticks())/1000)
        self.delta = self.current_time - self.event_time
    def timer(self):
        self.current_time = floor((pg.time.get_ticks())/1000)

class Player(Sprite):
    def __init__(self, game):
        Sprite.__init__(self)
        # self.image = pg.Surface((50, 50))
        # self.image.fill(GREEN)
        # use an image for player sprite...
        self.game = game
        self.image = pg.image.load(os.path.join(img_folder, 'thebell.png')).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (0, 0)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0) 
    def controls(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -5
        if keys[pg.K_d]:
            self.acc.x = 5
        if keys[pg.K_SPACE]:
            self.jump()
    def jump(self):
            hits = pg.sprite.spritecollide(self, self.game.all_platforms, False)
            if hits:
                print("i can jump")
            self.vel.y = -PLAYER_JUMP
    def update(self):
        # CHECK FOR COLLISION MOBS HERE
        #Checks for collisions for good mobs and adds 2 points
        mhits = pg.sprite.spritecollide(self, self.game.all_mobs, True)
        if mhits:
                print("nice!")
                self.game.score +=2
        #Checks if player collided with dragon mob to take away 5 points
        shits = pg.sprite.spritecollide(self, self.game.all_mob2, True)
        if shits:
                print("No!")
                self.game.score +=-5
        #Checks if player collided with good coin to add 15 points
        lhits = pg.sprite.spritecollide(self, self.game.all_mob3, True)
        if lhits:
            print("Go!")
            self.game.score +=15

#Checks if player collided with trap coin to take away 15 points
        fhits = pg.sprite.spritecollide(self, self.game.all_mob4, True)
        if fhits:
            print("Tough!")
            self.game.score +=-15
        
        self.acc = vec(0,PLAYER_GRAV)
        self.controls()
        # if friction - apply here
        self.acc.x += self.vel.x * -PLAYER_FRIC
        # self.acc.y += self.vel.y * -0.3
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos
        mhits = pg.sprite.spritecollide(self, self.game.all_mobs, False)
        
        #Checks if player collided with good mobs to cause an explosion effect
        if mhits:
            mhits[0].tagged = True
            mhits[0].cd.event_time = floor((pg.time.get_ticks())/1000)
            mhits[0].image = pg.image.load(os.path.join(img_folder, "explode.png")).convert()
            mhits[0].image.set_colorkey(BLACK)


# platforms

class Platform(Sprite):
    def __init__(self, x, y, w, h, category):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.category = category
        self.speed = 0
        if self.category == "moving":
            self.speed = 5
    def update(self):
        if self.category == "moving":
            self.rect.x += self.speed
            if self.rect.x + self.rect.w > WIDTH or self.rect.x < 0:
                self.speed = -self.speed


#New enemy class for bad mobs
class Mob2(Sprite):
    def __init__(self, game, x, y, w, h, kind):
        Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((w, h))
        self.image.fill(BLUE)
        self.image = pg.image.load(os.path.join(img_folder, "enemy.png")).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.kind = kind
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.cd = Cooldown()
        self.tagged = False
    '''def seeking(self):
        if self.rect.x < self.game.player.rect.x:
            self.rect.x +=1
        if self.rect.x > self.game.player.rect.x:
            self.rect.x -=1
        if self.rect.y < self.game.player.rect.y:
            self.rect.y +=1
        if self.rect.y > self.game.player.rect.y:
            self.rect.y -=1
    def update(self):
        self.seeking()
        self.cd.ticking()
        # print("mob tick " + str(self.cd.delta))
        if self.tagged:
            pg.transform.scale(self.image, (self.rect.w + 30, self.rect.h + 30))

        if self.cd.delta > 0.5 and self.tagged:
            self.kill()
            '''


#Another class for evil mobs
class Mob(Sprite):
    def __init__(self, game, x, y, w, h, kind):
        Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((w, h))
        self.image.fill(RED)
        self.image = pg.image.load(os.path.join(img_folder, "enemy.png")).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.kind = kind
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.cd = Cooldown()
        self.tagged = False
    #Seeking effect for bad mobs to hunt player
    def seeking(self):
        if self.rect.x < self.game.player.rect.x:
            self.rect.x +=1
        if self.rect.x > self.game.player.rect.x:
            self.rect.x -=1
        if self.rect.y < self.game.player.rect.y:
            self.rect.y +=1
        if self.rect.y > self.game.player.rect.y:
            self.rect.y -=1
    def update(self):
        #self.seeking()
        #self.cd.ticking()
        # print("mob tick " + str(self.cd.delta))'''
        if self.tagged:
            pg.transform.scale(self.image, (self.rect.w + 30, self.rect.h + 30))
#Kills mobs if made contact with player
        if self.cd.delta > 0.5 and self.tagged:
            self.kill()
#Another class for dragon mob 
class Mob2(Sprite):
    def __init__(self, game, x, y, w, h, kind):
        Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((w, h))
        self.image.fill(RED)
        self.image = pg.image.load(os.path.join(img_folder, "dragon2.png")).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.kind = kind
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.cd = Cooldown()
        self.tagged = False
    #Seeking effect to hunt player down
    def seeking(self):
        if self.rect.x < self.game.player.rect.x:
            self.rect.x +=1
        if self.rect.x > self.game.player.rect.x:
            self.rect.x -=1
        if self.rect.y < self.game.player.rect.y:
            self.rect.y +=1
        if self.rect.y > self.game.player.rect.y:
            self.rect.y -=1
    def update(self):
        self.seeking()
        self.cd.ticking()
        # print("mob tick " + str(self.cd.delta))
        if self.tagged:
            pg.transform.scale(self.image, (self.rect.w + 30, self.rect.h + 30))

        if self.cd.delta > 0.5 and self.tagged:
            self.kill()
#Class for powerup mob
class Mob3(Sprite):
    def __init__(self, game, x, y, w, h, kind):
        Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((w, h))
        self.image.fill(RED)
        self.image = pg.image.load(os.path.join(img_folder, "powerup2.png")).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.kind = kind
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.cd = Cooldown()
        self.tagged = False
#Class for trap powerup mob (Takes away points)
class Mob4(Sprite):
    def __init__(self, game, x, y, w, h, kind):
        Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((w, h))
        self.image.fill(RED)
        self.image = pg.image.load(os.path.join(img_folder, "powerup3.png")).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.kind = kind
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.cd = Cooldown()
        self.tagged = False
    def init(self):
#Groups all sprites
        self.sprites = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()
        self.mob2 = pg.sprite.Group()
        self.mob3 = pg.sprite.Group()


def update(self):
        pass 