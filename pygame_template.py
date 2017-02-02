"""
pygame template v0.1
John K. Lindstedt

"""


import pygame
import random
import pdb
import numpy
import math
import os, sys
import datetime, time
import json








#Game world class
class World():
    
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
            'asbestos': (127, 140, 141)
            }
    
    colors_sorted = ['alizarin','pomegranate',
                     'carrot','pumpkin',
                     'sun flower', 'orange',
                     'turquoise', 'green sea',
                     'emerald', 'nephritis', 
                     'peter river', 'belize hole',
                     'amethyst', 'wisteria',
                     'wet asphalt', 'midnight blue',
                     'concrete', 'asbestos',
                     'clouds', 'silver']
    
    #window title
    title = "pygame_template"
    
    #game states
    STATE_1 = 1
    STATE_2 = 2
    STATE_3 = 3
    
    ##Simple helper functions
    
    #mathematical distance function; 
    #generally useful for geometric collisions
    def dist(self,p1, p2):
        d = (abs((p1[0]-p2[0])**2) + abs((p1[1]-p2[1])**2))**.5
        return d   
    
    #date-time formatting function; great for logging information
    def getDateTimeStamp(self):
        d = datetime.datetime.now().timetuple()
        return "%d-%02.d-%02.d_%02.d-%02.d-%02.d" % (d[0], d[1], d[2], d[3], d[4], d[5])
    
    
    ##Support classes
    
    #Simple Subject class, as provided by Mike Schoelles
    class Subject():
        id = None
        age = None
        gender = None
    
        def __init__(self,cnd):
            self.cnd = cnd
            self.id = raw_input('Enter Subject ID: ')
            self.age = raw_input('Enter Subject Age: ')
            self.gender = raw_input('Enter Subject Gender: ')

    #Logger class, as provided by Mike Schoelles
    class Logger():
        def __init__(self,header,dl = '\t', nl = '\n', fl = 'NA', logtype="main"):
            self.header = header
            self.delim = dl
            self.newline = nl
            self.filler = fl
            self.file = None
            self.logtype = logtype
            return
        
        def open_log(self,fn,subdir=True, ext = ".tsv"):
            dir = os.path.splitext(os.path.basename(__file__))[0] + "_data"
            dir = dir + "/" + fn
            if not os.path.exists(dir):
                os.makedirs(dir)
            self.file = open(dir+"/"+self.logtype+"_"+fn+ext,'w')
            self.file.write(self.delim.join(self.header))
            self.file.write(self.newline)
            return
        
        def log(self,  **kwargs):
            line = [self.filler] * len(self.header) #list with filler entries
            for k, v in kwargs.iteritems(): #if keyword in header, replace filler with value
                if k in self.header:
                    line[self.header.index(k)] = str(v)
            self.file.write(self.delim.join(line)) #convert list to delimited string
            self.file.write(self.newline)
            return
        
        def close_log(self):
            self.file.close()
    
    
    #Initializes the world object
    def __init__(self, path = None):
        
        self.STATE = self.STATE_1
        
        self.stop = False
        
        #pygame setup
        pygame.init()
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.st = time.time() #start time of the game
        
        ## Input elements
        self.keys_held = []
        
        
        ## Display elements
        
        #screen
        pygame.display.set_caption(self.title)
        #resolution options: [1400, 750], [800,600]
        self.resolution = [800,600]
        self.screen = pygame.display.set_mode(self.resolution) # returns a Surface
        
        self.font = pygame.font.Font(None, 30)
        
        #defining the game space (on screen)
        self.margin = 0
        
        self.board_wh = [self.resolution[0]-(2*self.margin), self.resolution[1]-(2*self.margin)]
        self.board_lt = [self.margin,self.margin]
        
        self.center = [self.board_wh[0]//2, self.board_wh[1]//2]
        
        self.board_rect = pygame.Rect(self.board_lt,self.board_wh)
        self.board_rect.center = self.center
        
        #HUD display variables (on screen)
        self.hud_offset = self.board_wh[1]//10
        
        self.main_logger = World.Logger(["ts","event","item"])
        self.input_logger = World.Logger(["ts","event","item"], logtype="input")
        
        filename = self.getDateTimeStamp()
        self.main_logger.open_log(filename)
        self.input_logger.open_log(filename)
        
        self.timer = 0
    
        
        
        #game objects
        
        self.objs = []
        
        
        
        
    
    def reset(self):
        
        self.clear_screen()
                    
    
    
    #process all input (occurs once per frame)
    def input(self):
        for event in pygame.event.get():
            t = event.type
            
            ## Respond to keypresses
            
            if t == pygame.QUIT:
                self.stop = True
            
            #key was pressed
            if t == pygame.KEYDOWN:
                k = event.key
                
                if k == pygame.K_ESCAPE:
                    self.stop = True
            
            elif t == pygame.KEYUP:
                k = event.key
                
            
            
            #mouse buttons
            elif t == pygame.MOUSEBUTTONDOWN:
                p = event.pos
                
            
            elif t == pygame.MOUSEBUTTONUP:
                p = event.pos
                
            
            elif t == pygame.MOUSEMOTION:
                p = event.pos
                
            
            
            ## Log or print input events
            type_name = pygame.event.event_name(t)
            
            if 'key' in event.__dict__:
                event.__dict__["keyname"] = pygame.key.name(event.key)
            
            self.input_logger.log(ts = time.time() - self.st, event = type_name, item = json.dumps(event.__dict__))
            #print "\t".join([type_name, str(event.__dict__)])
            
            
        ##find pressed keys
        self.keys_held = pygame.key.get_pressed()
        if self.keys_held[pygame.K_SPACE]:
            self.hud_offset += 4
        else:
            self.hud_offset = max(self.hud_offset-1,0)
            
            
            
            
            
    
    
    #the core update of the game logic (happens once per frame)
    def logic(self):
        
        
        #event handling
        
        
        
        #physics updates
        
        
        
        
        
        return None
    
    def draw(self):
        
        ###Layer 0: Screen Background
        self.screen.fill(World.colors['clouds'])
        
        
        ###Layer 1: Game objects
        
        
        ###Layer 2: test pattern
        
        #circles! move with self.timer
        for ix, it in enumerate(World.colors_sorted):
            off = (ix - (len(World.colors)//2)) * 20
            #change height of each based on a harmonic
            pos = (self.center[0] + off, self.center[1] + off//9 + 90 + abs(self.timer%(10*(ix+1))-5*(ix+1)))
            pygame.draw.circle(self.screen, World.colors[it], pos, 20, 0)
        
                
        #snowbox
        sb_x = (self.center[0]-75,self.center[0]+75)
        sb_y = (self.center[1]-40,self.center[1]+40)
        for i in range(sb_x[0],sb_x[1]):
            for j in range(sb_y[0],sb_y[1]):
                self.screen.set_at((i,j), World.colors[random.choice(World.colors.keys())])
        
        #hello world
        textcolor = World.colors[World.colors_sorted[self.timer//4%len(World.colors_sorted)]] if 1 in self.keys_held else World.colors["clouds"]
        self.draw_text("Hello world!", textcolor, self.center, self.screen)
                
        
        ###Layer 3: Hud background
        
        #hud
        #fill hud background
        pygame.draw.rect(self.screen,World.colors["asbestos"],pygame.Rect(0,0,self.board_wh[0],self.hud_offset))
        
        ###Layer 4: Hud items
        ##draw hud items
        
        
        pygame.display.update()
    
    #text-drawing helper function; simplifies text
    def draw_text( self, text, color, loc, surf, justify = "center" ):
        t = self.font.render( str(text), True, color )
        tr = t.get_rect()
        setattr( tr, justify, loc )
        surf.blit( t, tr )
        return tr
    ###
    
    
    
    
    
    #Core run-loop. Take input, process logic, draw, refresh.
    def run(self):
        while not self.stop:
            self.input()
            self.logic()
            self.draw()
            
            #time
            self.clock.tick(self.fps)
            self.timer += 1
            
            

    
    
    
if __name__ == "__main__":
    if len(sys.argv) > 1:
        W = World(path = sys.argv[1].upper())
    else:
        W = World()
    
    W.run()
            
            
        

