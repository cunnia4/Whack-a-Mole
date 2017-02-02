
#Importing the necessary packages and setting
#a defensive flag to make sure we don't
#try to use them when they fail to load.

try:
    #from pyfixation import VelocityFP
    #print("Pyfixation success.")
    from pyviewx.client import iViewXClient, Dispatcher
    print("Pyview client success")
    from pyviewx.pygame import Calibrator
    print("Pyview pygame support success.")
    from pyviewx.pygame import Validator
    print("Pyview validator support success.")
    import numpy as np
    print("numpy success")
    eyetrackerSupport = True
except ImportError:
    print("Warning: Eyetracker not supported on this machine.")
    eyetrackerSupport = False 



#Defined just inside of game world object-- sets up place to 
#store eyetracker x-y pairs, and the dispatcher needed for 
#twisted's threading.

    if eyetrackerSupport:
        gaze_buffer = []
        d = Dispatcher()




# setup 
    self.fix = None
    self.samp = None
    if self.args.eyetracker and eyetrackerSupport:
        self.client = iViewXClient( "128.113.89.143" , 4444 )
        self.client.addDispatcher( self.d )
        self.calibrator = Calibrator( self.client, self.screen, reactor = reactor ) #escape = True?

    self.eye_x = None
    self.eye_y = None


#input handling for eyes

        if self.args.eyetracker and eyetrackerSupport and len( World.gaze_buffer ) > 1:
            #get avg position
            xs = []
            ys = []
            for i in World.gaze_buffer:
                xs += [i[0]]
                ys += [i[1]]

            self.prev_x_avg = self.i_x_avg
            self.prev_y_avg = self.i_y_avg
            self.i_x_avg = int( sum(xs) / len( World.gaze_buffer ) )
            self.i_y_avg = int( sum(ys) / len( World.gaze_buffer ) )



            #handle eye-based events
            if self.eye_mask:
                prev = self.mask_toggle
                if self.i_x_avg > int((self.gamesurf_rect.width + self.gamesurf_rect.left + self.nextsurf_rect.left) / 2) and self.i_y_avg < int((self.nextsurf_rect.top + self.nextsurf_rect.height + self.score_lab_left[1]) / 2):
                    self.mask_toggle = True
                else:
                    self.mask_toggle = False
                if self.mask_toggle != prev:
                    self.log_game_event("MASK_TOGGLE", self.mask_toggle)


            #HOOK FOR MISDIRECTION / LOOKAWAY EVENTS
            # when in board, normal. when leave board, subtly alter accumulation.
            ## will need crossover detection for event onset
            ## will need board mutator function
            ## could use some helper "in-bounds" or collision functions.

            self.i_x_conf = 0 if int(self.i_x_avg)<=0 else sum(map((lambda a, b: pow(a + b, 2)), xs, [-self.i_x_avg] * len(xs))) / int(self.i_x_avg)#len(xs)
            self.i_y_conf = 0 if int(self.i_y_avg)<=0 else sum(map((lambda a, b: pow(a + b, 2)), ys, [-self.i_y_avg] * len(ys))) / int(self.i_y_avg)#len(ys)



# reactor start function (with calibrator)

    #Begin the reactor
    def run( self ):
        #coop.coiterate(self.process_pygame_events()).addErrback(error_handler)
        if self.args.eyetracker and eyetrackerSupport:
            self.state = self.STATE_CALIBRATE
            reactor.listenUDP( 5555, self.client )
            self.log_game_event("CALIBRATION", "Start")
            self.calibrator.start( self.start , points = self.calibration_points, auto = int(self.calibration_auto))
        else:
            self.start( None )
        reactor.run()
    ###




#setting up the dispatcher to ALSO listen for 
# eyetracking events (on top of the main loop call)
#-- done WITHIN the game world object definition (just as above)

    if eyetrackerSupport:
        @d.listen( 'ET_SPL' )
        def iViewXEvent( self, inResponse ):
            self.inResponse = inResponse
            global x, y
            if self.state < 0:
                return
            
            try:
                x = float( inResponse[2] )
                y = float( inResponse[4] )

                #if good sample, add
                if x != 0 and y != 0:
                    World.gaze_buffer.insert( 0, ( x, y ) )
                    if len( World.gaze_buffer ) > self.gaze_window:
                        World.gaze_buffer.pop()
            
            except(IndexError):
                print("IndexError caught-- AOI error on eyetracking machine?")
                self.log_game_event("ERROR", "AOI INDEX")
