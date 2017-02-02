import pygame
import random
import pdb
import numpy
import math
import os, sys
import datetime, time
import json
import platform


from twisted.internet import reactor
from twisted.internet.task import LoopingCall

#try:
    ##from pyfixation import VelocityFP
    ##print("Pyfixation success.")
    #from pyviewx.client import iViewXClient, Dispatcher
    #print("Pyview client success")
    #from pyviewx.pygame import Calibrator
    #print("Pyview pygame support success.")
    #from pyviewx.pygame import Validator
    #print("Pyview validator support success.")
    #import numpy as np
    #print("numpy success")
    #eyetrackerSupport = True
#except ImportError:
    #print("Warning: Eyetracker not supported on this machine.")
    #eyetrackerSupport = False

#Game world class
class World():
    
        #gaze_buffer = []
        #d = Dispatcher()    
    
        stop = False
## World constants
#set of colors
        colors = {
                'turquoise': (26, 188, 156),
                'green sea': (22, 160, 133),
                'emerald': (46, 204, 113),
                'nephritis': (39, 174, 96),
                'peter river': (52, 152, 219),
                'belize hole': (41, 128, 185),
                'amethyst': (155, 89, 182),
                'wisteria': (142, 68, 173),
                'wet asphalt': (52, 73, 94),
                'midnight blue': (44, 62, 80),
                'sun flower': (241, 196, 15),
                'orange': (243, 156, 18),
                'carrot': (230, 126, 34),
                'pumpkin': (211, 84, 0),
                'alizarin': (231, 76, 60),
                'pomegranate': (192, 57, 43),
                'clouds': (236, 240, 241),
                'silver': (189, 195, 199),
                'concrete': (149, 165, 166),
                'asbestos': (127, 140, 141),
                'brown':(165, 110, 110),
                'hot pink':(255, 105, 180)
                }
                
        class Hole():
                def __init__(self, left, top, width, height):
                        self.left= left
                        self.top= top
                        self.width= width
                        self.height= height
                        self.rect= pygame.Rect(left, top, width, height)
                        
        class Mole():
                def __init__(self, x, y, timer, counter=0, color='brown' , size= 36, is_there= False, hit= False):
                        self.x= x
                        self.y= y
                        self.timer= timer
                        self.counter= counter
                        self.min_x= x-35
                        self.max_x= x+35
                        self.min_y= y-35
                        self.max_y= y+35
                        self.color= color
                        self.size= size
                        self.is_there= False
                        self.hit= False
                        
                           
                def get_xy(self):
                        return [self.x, self.y]
                def within_mole(self, x, y):
                        if x > self.min_x and x < self.max_x:
                                if y > self.min_y and y < self.max_y: 
                                        return True
                        return False
                def get_size(self):
                        return self.size
                def get_eye1(self):
                        return self.x-9, self.y-3
                def get_eye2(self):
                        return self.x+9, self.y-3
                def get_mouth(self):
                        return pygame.Rect(self.x-10, self.y+15, 20, 6)
                def isit_there(self):
                        return self.is_there
                def set_is_there(self, val):
                        self.is_there= val
                def set_color(self, color):
                        self.color= color
                def get_color(self):
                        return self.color
                def incr_counter(self):
                        self.counter+=1
                def set_counter(self, val):
                        self.counter= val
                def get_timer(self):
                        return self.timer
                def get_counter(self):
                        return self.counter
                def is_hit(self):
                        return self.hit
                def set_hit(self, val):
                        self.hit= val
                def draw_me(self, screen):
                        pygame.draw.circle(screen, World.colors[self.get_color()], self.get_xy(), self.size, 0)
                        pygame.draw.circle(screen, World.colors["clouds"], self.get_eye1(), 9, 0)
                        pygame.draw.circle(screen, World.colors["clouds"], self.get_eye2(), 9, 0)
                        pygame.draw.circle(screen, World.colors["wet asphalt"], self.get_eye1(), 5, 0)
                        pygame.draw.circle(screen, World.colors["wet asphalt"], self.get_eye2(), 5, 0)
                        pygame.draw.rect(screen, World.colors["pomegranate"], self.get_mouth(), 0)
                def step_up(self):
                        self.y-=1
                def step_down(self):
                        self.y+=1
                
        
        #Initializes the world object
        def __init__(self, path = None):
                
                self.resolution = [800,600]
                self.margin = 0
                pygame.font.init()
                self.font = pygame.font.SysFont("comic sans", 60, True, False)
                
                self.board_wh = [self.resolution[0]-(2*self.margin), self.resolution[1]-(2*self.margin)]        
                self.center = [self.board_wh[0]//2, self.board_wh[1]//2]                
                self.bottomleft = [self.board_wh[0]//4, 7*(self.board_wh[1])//8]
                self.screen = pygame.display.set_mode(self.resolution) # returns a Surface
                
                self.clock = pygame.time.Clock()
                
                self.timer = 0
                self.score = 0
                                
                self.hole_field= []
                self.hole_covers= []
                
                self.hole_field.append(self.Hole(155,105,90,45))
                self.hole_field.append(self.Hole(355,105,90,45))
                self.hole_field.append(self.Hole(555,105,90,45))
                self.hole_field.append(self.Hole(155,405,90,45))
                self.hole_field.append(self.Hole(355,405,90,45))
                self.hole_field.append(self.Hole(555,405,90,45))
                
                self.hole_covers.append(self.Hole(155,115,90,30))
                self.hole_covers.append(self.Hole(355,115,90,30))
                self.hole_covers.append(self.Hole(555,115,90,30))
                self.hole_covers.append(self.Hole(155,415,90,30))
                self.hole_covers.append(self.Hole(355,415,90,30))
                self.hole_covers.append(self.Hole(555,415,90,30))                
                
                self.moles= []
                self.mole1= self.Mole(0,0,0,0)
                self.mole2= self.Mole(0,0,0,0)
                
                self.moles.append(self.Mole(200,100, 45))
                self.moles.append(self.Mole(400,100, 60))
                self.moles.append(self.Mole(600,100, 75))
                self.moles.append(self.Mole(200,400, 45))
                self.moles.append(self.Mole(400,400, 60))
                self.moles.append(self.Mole(600,400, 75))
                
                
        def input(self):
                for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                                (mx,my)= pygame.mouse.get_pos()
                                for m in self.moles:
                                        if m.within_mole(mx, my):
                                                if m.isit_there() and not m.is_hit():
                                                        self.score += 1
                                                        m.set_color('pomegranate')
                                                        m.set_hit(True)
                                                        pygame.mixer.init()
                                                        pygame.mixer.music.load('doh.mp3')
                                                        pygame.mixer.music.play()
                                                                
                        #key was pressed
                        if event.type == pygame.KEYDOWN:
                                k = event.key
                                if k == pygame.K_ESCAPE:
                                        #self.stop = True
                                        self.lc.stop()
                                        
                
                
        def logic(self):
                (self.mole1).incr_counter()
                (self.mole2).incr_counter()
        
                if (self.mole1).get_counter() == (self.mole1).get_timer():
                        (self.mole1).set_is_there(False)
                        (self.mole1).set_counter(0)
                if (self.mole2).get_counter() == (self.mole2).get_timer():
                        (self.mole2).set_is_there(False)
                        (self.mole2).set_counter(0)       
                        
                if self.mole1== self.Mole(0,0,0,0) or (self.mole1).isit_there() == False:
                        mole= random.choice(self.moles)
                        while mole == self.mole2 or mole == self.mole1:
                                mole= random.choice(self.moles)
                        mole.set_color('brown')
                        mole.set_hit(False)
                        self.mole1= mole
                        (self.mole1).set_is_there(True)        
                       
                if self.mole2== self.Mole(0,0,0,0) or (self.mole2).isit_there() == False:
                        mole= random.choice(self.moles)
                        while mole == self.mole1 or mole == self.mole2:
                                mole= random.choice(self.moles)
                        mole.set_color('brown')
                        mole.set_hit(False)
                        self.mole2 = mole
                        (self.mole2).set_is_there(True)                
                
                if self.mole1.get_counter() < 20:
                        self.mole1.step_up()
                if self.mole2.get_counter() < 20:
                        self.mole2.step_up()
                        
                if (self.mole1.get_timer()-self.mole1.get_counter()) < 21:
                        self.mole1.step_down()
                if (self.mole2.get_timer()-self.mole2.get_counter()) < 21:
                        self.mole2.step_down()                
                
        
        #text-drawing helper function; simplifies text
        def draw_text( self, text, color, loc, surf, justify = "center" ):
                t = self.font.render( str(text), True, color )
                tr = t.get_rect()
                setattr( tr, justify, loc )
                surf.blit( t, tr )
                return tr        
        
        def draw(self):

                        ###Layer 0: Screen Background
                        self.screen.fill(World.colors['emerald']) 
                        
                        textcolor = World.colors["clouds"]
                        self.draw_text("WHACK-A-MOLE", textcolor,self.center, self.screen)
                        score_str= str(self.score)
                        self.draw_text("Score: "+score_str, textcolor,self.bottomleft, self.screen)                
                        
                        for i in self.hole_field:
                                pygame.draw.ellipse(self.screen, World.colors["wet asphalt"], i, 0)

                        self.mole1.draw_me(self.screen)
                                
                        self.mole2.draw_me(self.screen)
                        
                        for i in self.hole_covers:
                                pygame.draw.ellipse(self.screen, World.colors["wet asphalt"], i, 0)
                        
                        pygame.display.update()
                                               
                        
        def run(self):
                #while not self.stop:
                        #self.input()
                        #self.logic()
                        #self.draw()
                        #self.clock.tick(60)
                        
                        ##time
                        #self.timer += 1
            
                self.start( None )
                reactor.run()      
                
                
        def start(self, lc):
                self.lc = LoopingCall( self.refresh )
                cleanupD = self.lc.start( 1.0/60 )
                cleanupD.addCallbacks( self.quit )                
            
            
        def quit( self, lc ):
                reactor.stop()      
                
        def refresh(self):
                self.input()
                self.logic()
                self.draw()                
            
if __name__ == "__main__":
        if len(sys.argv) > 1:
                W = World(path = sys.argv[1].upper())
        else:
                W = World()
                
        W.run()    