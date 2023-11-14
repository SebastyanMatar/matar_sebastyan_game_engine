# content from kids can code: http://kidscancode.org/blog/
# Goals:Make someone interact with player
# Rule:Jump and run
#Freedom runs side to side
#Feedback: Score, health, points, mobs

# In the form of a sprite
#Have platforms scroll left like super mario
# While self x+1 platforms x - 1

#Have obstacles bounce the player backwards like a collision
#Double Jump

#CREDITS 
#Thanks to Jaden, Antonio, and Alejandro for helping me out and giving me tips when I get stuck
#Thanks to Mr. Cozort for helping out too and giving helpful coding tips and telling us how to code certain things when we are stuck



# import libraries and modules
import pygame as pg
from pygame.sprite import Sprite
import random
from random import randint
import os
from settings import *
from sprites import *

vec = pg.math.Vector2

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

class Game:
    def __init__(self):
        # init pygame and create a window
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("My Game...")
        self.clock = pg.time.Clock()
        self.running = True

    def new(self):
        # create a group for all sprites
        self.score = 0
        self.bgimage = pg.image.load(os.path.join(img_folder, "cool.png")).convert()
        self.all_sprites = pg.sprite.Group()
        self.all_platforms = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.all_mob2 = pg.sprite.Group()
        self.all_mob3 = pg.sprite.Group()
        self.all_mob4 = pg.sprite.Group()
        # instantiate classes
        self.player = Player(self)
        # add instances to groups
        self.all_sprites.add(self.player)

        for p in PLATFORM_LIST:
            # instantiation of the Platform class
            plat = Platform(*p)
            self.all_sprites.add(plat)
            self.all_platforms.add(plat)

        #Spawns in good mobs
        for m in range(0,20):
            m = Mob(self, randint(0, WIDTH), randint(0, HEIGHT/2), 20, 20, "normal")
            self.all_sprites.add(m)
            self.all_mobs.add(m)
        #Spawns in bad dragon mobs
        for s in range(0,40):
            s = Mob2(self, randint(0, WIDTH), randint(0, HEIGHT/2), 20, 20, "normal")
            self.all_sprites.add(s)
            self.all_mob2.add(s)
        
        
        #Spawns in a powerup/trap coin (One gives you points and one takes it away)
        for l in range(0,1):
            l = Mob3(self, randint(0, WIDTH), randint(0, HEIGHT/2), 20, 40, "normal")
            self.all_sprites.add(l)
            self.all_mob3.add(l)
        
        for f in range(0,1):
            f = Mob3(self, randint(0, WIDTH), randint(0, HEIGHT/2), 20, 20, "normal")
            self.all_sprites.add(f)
            self.all_mob4.add(f)
        


        self.run()
    
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            if not self.paused:
                self.update()
            self.draw()


        self.run()

    
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.all_sprites.update()

        # this is what prevents the player from falling through the platform when falling down...
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.all_platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
                self.player.vel.x = hits[0].speed*1.5

                    
         # this prevents the player from jumping up through a platform
        if self.player.vel.y < 0:
            hits = pg.sprite.spritecollide(self.player, self.all_platforms, False)
            if hits:
                print("ouch")
                self.score -= 1
                if self.player.rect.bottom >= hits[0].rect.top - 1:
                    self.player.rect.top = hits[0].rect.bottom
                    self.player.acc.y = 5
                    self.player.vel.y = 0


            

    def events(self):
        for event in pg.event.get():
        # check for closed window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
                
    def draw(self):
        ############ Draw ################
        # draw the background screen
        self.screen.fill(BLACK)
        self.screen.blit(self.bgimage, (0,0))
        # draw all sprites
        self.all_sprites.draw(self.screen)
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH/2, HEIGHT/10)
        # buffer - after drawing everything, flip display
        pg.display.flip()
    
    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

    def show_start_screen(self):
        pass
    def show_go_screen(self):
        pass



g = Game()
while g.running:
    g.new()


pg.quit()

