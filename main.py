#! /usr/bin/env python

import os, sys
import math
import pygame
from pygame.locals import *
from helpers import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

X = 0
Y = 1

def worldToScreen(pt, ptCenter):
    """Converts absolute coordinates in a world larger than the displayed screen to distance on-screen
pt is the point being converted
ptCenter is the viewpoint's world coordinates"""
    return (CENTER[X]+pt[X]-ptCenter[X], CENTER[Y]+pt[Y]-ptCenter[Y])

PLAYER_SIZE = 64
CENTER = [320, 240]
class PyManMain:
    """The Main PyMan Class - This class handles the main 
    initialization and creating of the Game."""
    
    def __init__(self, width=640,height=480):
        """Initialize"""
        """Initialize PyGame"""
        pygame.init()
        """Set the window Size"""
        self.width = width
        self.height = height
        """Create the Screen"""
        self.screen = pygame.display.set_mode((self.width
                                               , self.height))
                                                          
    def MainLoop(self):
        """This is the Main Loop of the Game"""
        
        """Load All of our Sprites"""
        self.LoadSprites();
        """tell pygame to keep sending up keystrokes when they are
        held down"""
        pygame.key.set_repeat(500, 30)
        
        """Create the background"""
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0,0,0))

        CENTER = (self.screen.get_size()[0]/2, self.screen.get_size()[1]/2)

        self.player = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.mobs = pygame.Surface(self.screen.get_size())
        
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    sys.exit()
                elif event.type == KEYDOWN:
                    if ((event.key == K_d)
                    or (event.key == K_a)
                    or (event.key == K_w)
                    or (event.key == K_s)):
                        self.snake.steer(event.key)

            self.snake.move()
                        
            """Check for collision"""
            lstCols = pygame.sprite.spritecollide(self.snake
                                                 , self.pellet_sprites
                                                 , True)
            """Update the amount of pellets eaten"""
            self.snake.pellets = self.snake.pellets + len(lstCols)
                        
            """Do the Drawing"""               
            self.screen.blit(self.background, (0, 0))     
            if pygame.font:
                font = pygame.font.Font(None, 36)
                text = font.render("Pellets %s" % self.snake.pellets
                                    , 1, (255, 0, 0))
                textpos = text.get_rect(centerx=self.background.get_width()/2)
                self.screen.blit(text, textpos)

            # Draw the player in the center point
            # changing dimensions to make up for varying sprite size.
            CENTER_CURR = (CENTER[0]-self.snake.image.get_size()[0]/2,
                           CENTER[1]-self.snake.image.get_size()[1]/2)
            self.player.fill((0,0,0))
            self.snake_sprites.draw(self.player)

            self.pellet_sprites.draw(self.mobs)
            self.screen.blit(self.mobs, worldToScreen((0, 0), self.snake.pos()))
            
            self.screen.blit(self.player, CENTER_CURR)

            
            
            
            pygame.display.flip()
                    
    def LoadSprites(self):
        """Load the sprites that we need"""
        self.snake = Mob()
        self.snake_sprites_original = pygame.sprite.RenderPlain((self.snake))
        self.snake_sprites = pygame.sprite.RenderPlain((self.snake))
        
        """figure out how many pellets we can display"""
        nNumHorizontal = int(self.width/64)
        nNumVertical = int(self.height/64)       
        """Create the Pellet group"""
        self.pellet_sprites = pygame.sprite.Group()
        """Create all of the pellets and add them to the 
        pellet_sprites group"""
        for x in range(nNumHorizontal):
            for y in range(nNumVertical):
                self.pellet_sprites.add(Pellet(pygame.Rect(x*64, y*64, 64, 64)))        

TURN_RATE = 5
SPEED_MAX = 10

SPEED_DIVISOR = 200.0

class Mob(pygame.sprite.Sprite):
    """This is our mob that will move around the screen"""

    heading = 0
    speed = 0
    # accumulated fractional distance.
    x = 0
    y = 0
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) 
        self.image, self.rect = load_image('mob.png',-1)
        self.image_orig = self.image
        self.pellets = 0
        """Set the number of Pixels to move each time"""
        self.x_dist = 5
        self.y_dist = 5
        self.x_pos = CENTER[0]
        self.y_pos = CENTER[1]

    def pos(self):
        return (self.x_pos, self.y_pos)
        
    def steer(self, key):
        """Move your self in one of the 4 directions according to key"""
        """Key is the pyGame define for either up, down, left, or right key
        we will adjust ourselfs in that direction"""
        if (key == K_d):
            self.heading = (self.heading + TURN_RATE)%360
            self.image = pygame.transform.rotate(self.image_orig, -1*self.heading)
        elif (key == K_a):
            self.heading = (self.heading - TURN_RATE)%360
            self.image = pygame.transform.rotate(self.image_orig, -1*self.heading)
        elif (key == K_w):
            self.speed = min(self.speed+1, SPEED_MAX) 
        elif (key == K_s):
            self.speed = max(self.speed-1, -1*SPEED_MAX)
        print "Speed", self.speed, "Heading", self.heading

    def move(self):
        xMove = math.cos(math.radians(self.heading))*self.speed/SPEED_DIVISOR
        yMove = math.sin(math.radians(self.heading))*self.speed/SPEED_DIVISOR
        self.x += xMove
        self.y += yMove
        if abs(self.x) > 1 or abs(self.y) > 1:
            self.x_pos += int(self.x)
            self.y_pos += int(self.y)
            #self.rect.move_ip(self.x, self.y);
            pass
        if self.x > 1:
            self.x -= 1
        if self.x < -1:
            self.x += 1
        if self.y > 1:
            self.y -= 1
        if self.y < -1:
            self.y += 1
        #print self.x, self.y
        
class Pellet(pygame.sprite.Sprite):
        
    def __init__(self, rect=None):
        pygame.sprite.Sprite.__init__(self) 
        self.image, self.rect = load_image('pellet.png',-1)
        if rect != None:
            self.rect = rect        

if __name__ == "__main__":
    MainWindow = PyManMain()
    MainWindow.MainLoop()
       
