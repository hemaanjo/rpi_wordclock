import logging
import datetime
import os
import time
import time_joda
import time_german
import wordclock_tools.wordclock_colors as wcc

class plugin:
    '''
    A class to display the current time (default mode).
    This default mode needs to be adapted to the hardware
    layout of the wordclock (the choosen stencil) and is
    the most essential time display mode of the wordclock.
    '''

    def __init__(self, config):
        '''
        Initializations for the startup of the current wordclock plugin
        '''
        # Get plugin name (according to the folder, it is contained in)
        self.name = os.path.dirname(__file__).split('/')[-1]
        self.pretty_name = "Clock 2"
        self.description = "Alles was die Wort-UHR braucht"

        # log anlegen
        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.INFO)
        loghandle = logging.FileHandler('wordclock.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        loghandle.setFormatter(formatter)
        # add the handlers to the logger
        self.log.addHandler(loghandle)
        self.log.info('INIT')

	# ambilight
	self.ambilight = False

        # Choose language
        language = config.get('plugin_' + self.name, 'language')
        if language == 'joda':
	    self.taw = time_joda.time_joda()
        else:
            print(self.name + ' Could not detect language: ' + language + '.')
            print(self.name + 'Choosing default: german')
            self.taw = time_german.time_german()

        # typewriter effect
        try:
            self.typewriter = config.getboolean('plugin_' + self.name, 'typewriter')
        except:
            print(
            '  No typewriter-flag set for default plugin within the config-file. Typewriter animation will be used.')
            self.typewriter = True

        try:
            self.typewriter_speed = config.getint('plugin_' + self.name, 'typewriter_speed')
        except:
            self.typewriter_speed = 5
            print('  No typewriter_speed set for default plugin within the config-file. Defaulting to ' + str(
                self.typewriter_speed) + '.')

	try:
            self.purist = config.getboolean('plugin_time_default', 'purist')
        except:
            print('  No purist-flag set for default plugin within the config-file. Prefix will be displayed.')
            self.purist = False

        # sleep mode
        try:
            self.sleep_begin = datetime.time(config.getint('plugin_' + self.name, 'sleep_begin_hour'),config.getint('plugin_' + self.name, 'sleep_begin_minute'),0)
        except:
            self.sleep_begin = datetime.time(0,0,0)
            self.sleep_end = datetime.time(0,0,0)
            print('  No sleeping time set, display will stay bright 24/7.')

        try:
            self.sleep_end = datetime.time(config.getint('plugin_' + self.name, 'sleep_end_hour'),config.getint('plugin_' + self.name, 'sleep_end_minute'),0)
        except:
            self.sleep_begin = datetime.time(0,0,0)
            self.sleep_end = datetime.time(0,0,0)
            print('  No sleeping time set, display will stay bright 24/7.')

        try:
            self.sleep_brightness = config.getint('plugin_' + self.name, 'sleep_brightness')
        except:
            self.sleep_brightness = 5
            print('  No sleep brightness set within the config-file. Defaulting to ' + str(
                self.sleep_brightness) + '.')

        # if left/right button is pressed during sleep cycle, the current sleep cycle is skipped for the rest of the night
        # to allow manual override
        self.skip_sleep = False
        self.is_sleep = False

        # monitor sleep mode changes to apply brightness
        self.sleep_switch = False


#        try:
#            self.typewriter = config.getboolean('plugin_' + self.name, 'typewriter')
#        except:
#            print('  No typewriter-flag set for default plugin within the config-file. Typewriter animation will be used.')
#            self.typewriter = True
#
#        try:
#            self.typewriter_speed = config.getint('plugin_' + self.name, 'typewriter_speed')
#        except:
#            self.typewriter_speed = 5
#            print('  No typewriter_speed set for default plugin within the config-file. Defaulting to ' + str(self.typewriter_speed) + '.')

        self.bg_color     = wcc.BLACK  # default background color
        self.word_color   = wcc.WWHITE # default word color
        self.minute_color = wcc.WWHITE # default minute color

        # Other color modes...
        self.color_modes = \
               [[wcc.BLACK, wcc.WWHITE, wcc.WWHITE],
                [wcc.BLACK, wcc.WHITE, wcc.WHITE],
                [wcc.BLACK, wcc.ORANGE, wcc.ORANGE],
                [wcc.BLACK, wcc.ORANGE, wcc.WWHITE],
                [wcc.BLACK, wcc.PINK, wcc.GREEN],
                [wcc.BLACK, wcc.RED, wcc.YELLOW],
                [wcc.BLACK, wcc.BLUE, wcc.RED],
                [wcc.BLACK, wcc.RED, wcc.BLUE],
                [wcc.YELLOW, wcc.RED, wcc.BLUE],
                [wcc.RED, wcc.BLUE, wcc.BLUE],
                [wcc.RED, wcc.WHITE, wcc.WHITE],
                [wcc.GREEN, wcc.YELLOW, wcc.PINK],
                [wcc.WWHITE, wcc.BLACK, wcc.BLACK],
                [wcc.BLACK, wcc.Color(30,30,30), wcc.Color(30,30,30)]]
        self.color_mode_pos = 0
        self.rb_pos = 0 # index position for "rainbow"-mode
        try:
            self.brightness_mode_pos = config.getint('wordclock_display', 'brightness')
        except:
            print('WARNING: Brightness value not set in config-file: To do so, add a "brightness" between 1..255 to the [wordclock_display]-section.')
            self.brightness_mode_pos = 255
        self.brightness_change = 8

    def run(self, wcd, wci):
        '''
        Displays time until aborted by user interaction on pin button_return
        '''
        # Some initializations of the "previous" minute
        prev_min = -1
	prev_seconds = -1
	ac = wcd.AmbiCount()

	if self.ambilight = True:
		print('acounter = ' + str(ac))
        	deltaSecond = 60 / ac
	else
		print('acounter = 0')

	while True:
            # Get current time
            now = datetime.datetime.now()
            # Check, if a minute has passed (to render the new time)
	    ###self.log.info(str(now))
            if prev_min < now.minute:
                # Set background color
                self.show_time(wcd, wci)
                prev_min = -1 if now.minute == 59 else now.minute
            ###event = wci.waitForEvent(1)
        self.log.INFO("ambilight=" & self.ambilight)
	    if self.ambilight = True:
            	if prev_seconds < now.second:
			if deltaSecond >= 1:
            			if now.second % deltaSecond == 0:
            				self.show_second(wcd, wci, now.second)
					prev_seconds = -1 if now.second == 59 else now.second
				else:
					#print(str(now.second))
					self.show_second(wcd, wci, now.second, ac)
		        		prev_seconds = -1 if now.second == 59 else now.second
            #print('sec=' +  str(prev_seconds))
	    event = wci.waitForEvent(1) # original 1 - 0.9 ok
	    #else:
	    #	event = wci.waitForEven(1)
            # Switch display color, if button_left is pressed
            if (event == wci.EVENT_BUTTON_LEFT):
                #self.color_mode_pos += 1
                #if self.color_mode_pos == len(self.color_modes):
                #    self.color_mode_pos = 0
                #self.bg_color     = self.color_modes[self.color_mode_pos][0]
                #self.word_color   = self.color_modes[self.color_mode_pos][1]
                #self.minute_color = self.color_modes[self.color_mode_pos][2]
                #self.show_time(wcd, wci)
                #time.sleep(0.2) # original 0.2
		self.setBrightness(event, wcd, wci)
		  
            if (event == wci.EVENT_BUTTON_RETURN) or (event == wci.EVENT_EXIT_PLUGIN):
                return # Return to main menu, if button_return is pressed
            if (event == wci.EVENT_BUTTON_RIGHT):
                #time.sleep(wci.lock_time)
                #self.color_selection(wcd, wci)
		self.setBrightness(event, wcd, wci)

    def setBrightness(self, event, wcd, wci):
	addThis = 0
	# self.brightness_mode_pos += self.brightness_change
	if (event == wci.EVENT_BUTTON_RIGHT):
		addThis = self.brightness_change * 1 
	if (event == wci.EVENT_BUTTON_LEFT):
		addThis = ((0-1) * self.brightness_change)
	if (addThis <> 0):
		print(' asasa ' + str(addThis))
		cb = self.brightness_mode_pos + addThis
		if(cb <= 0):
			cb = 255
		if(cb >= 256):
			cb = 1
		self.brightness_mode_pos = cb
		wcd.setBrightness(self.brightness_mode_pos)
                wcd.show()
                wcd.showText(str(self.brightness_mode_pos) + ' ')
                time.sleep(1)
                self.show_time(wcd, wci)


    def show_second(self, wcd, wci, second, aCounter=1):
        now = datetime.datetime.now()
	if aCounter <= 60:
        	for i in range(0, aCounter+1):
			if aCounter <= 60:
				sec = second / (60 / aCounter)
            			if i == sec:
                			wcd.AmbiLED(i, wcc.Color(  254,  0,  0))
            			else:
                			wcd.AmbiLED(i, self.bg_color)
	else:
		#print('Sekunde = ' + str(second))
		for i in range(0, aCounter+1):
			wcd.AmbiLED(i, self.bg_color)
		if second <= 29:
			ambiIDX = 29 - second
		else:
			ambiIDX = 59 - (second - 30)
		wcd.AmbiLED(ambiIDX * 2, wcc.Color( 254, 254, 0))
		wcd.AmbiLED((ambiIDX * 2) + 1, wcc.Color( 254, 254, 0))
	wcd.show()


    def show_time(self, wcd, wci):
        now = datetime.datetime.now()
        # Set background color
        wcd.setColorToAll(self.bg_color, includeMinutes=True)
        # Returns indices, which represent the current time, when beeing illuminated
        taw_indices = self.taw.get_time(now)
	#print('typewriter=' + str(self.typewriter))
        if self.typewriter and now.minute%5 == 0:
            for i in range(len(taw_indices)):
                wcd.setColorBy1DCoordinates(wcd.strip, taw_indices[0:i+1], self.word_color)
                wcd.show()
                time.sleep(1.0/self.typewriter_speed)
            wcd.setMinutes(now, self.minute_color)
            wcd.show()
        else:
            wcd.setColorBy1DCoordinates(wcd.strip, taw_indices, self.word_color)
            wcd.setMinutes(now, self.minute_color)
	    wcd.show()

    def color_selection(self, wcd, wci):
        while True:
            # BEGIN: Rainbow generation as done in rpi_ws281x strandtest example! Thanks to Tony DiCola for providing :)
            if self.rb_pos < 85:
                self.word_color = self.minute_color = wcc.Color(3*self.rb_pos, 255-3*self.rb_pos, 0)
            elif self.rb_pos < 170:
                self.word_color = self.minute_color = wcc.Color(255-3*(self.rb_pos-85), 0, 3*(self.rb_pos-85))
            else:
                self.word_color = self.minute_color = wcc.Color(0, 3*(self.rb_pos-170), 255-3*(self.rb_pos-170))
            # END: Rainbow generation as done in rpi_ws281x strandtest example! Thanks to Tony DiCola for providing :)
            #TODO: Evaluate taw_indices only every n-th loop (saving ressources)
            now = datetime.datetime.now() # Set current time
            taw_indices = self.taw.get_time(now)
            wcd.setColorToAll(self.bg_color, includeMinutes=True)
            wcd.setColorBy1DCoordinates(wcd.strip, taw_indices, self.word_color)
            wcd.setMinutes(now, self.minute_color)
            wcd.show()
            self.rb_pos += 1
            if self.rb_pos == 256: self.rb_pos = 0
            event = wci.waitForEvent(0.1)
            if event != wci.EVENT_INVALID:
                time.sleep(wci.lock_time)
                break
        while True:
            self.brightness_mode_pos += self.brightness_change
            #TODO: Evaluate taw_indices only every n-th loop (saving ressources)
            now = datetime.datetime.now() # Set current time
            taw_indices = self.taw.get_time(now)
            wcd.setColorToAll(self.bg_color, includeMinutes=True)
            wcd.setColorBy1DCoordinates(wcd.strip, taw_indices, self.word_color)
            wcd.setMinutes(now, self.minute_color)
            wcd.setBrightness(self.brightness_mode_pos)
            wcd.show()
            if self.brightness_mode_pos < abs(self.brightness_change) or self.brightness_mode_pos > 255 - abs(self.brightness_change):
                self.brightness_change *= -1
            event = wci.waitForEvent(0.1)
            if event != wci.EVENT_INVALID:
                time.sleep(wci.lock_time)
                return

