# Authored by Josef D.

import os
import wordclock_tools.wordclock_colors as wcc
import time
import datetime

class plugin:
    '''
    Lichtzeitpegel a la Rheinturm ;-)
    '''

    def __init__(self, config):
        '''
        Initializations for the startup of the current wordclock plugin
        '''
        # Get plugin name (according to the folder, it is contained in)
        self.name = os.path.dirname(__file__).split('/')[-1]
        self.bg_color = wcc.BLACK
        self.word_color = wcc.ORANGE
	self.color = wcc.Color(212, 165, 25)

	self.threshold = 0.9

        self.pretty_name = "Lichtzeitpegel"
        self.description = "Wie Rheinturm nur nebeneinander"

    def run(self, wcd, wci):
        '''
	Indices for RANGE
        1.   0- 11   Zeile frei
	2.  12- 22  Zeile Stunden Zehner  1 2
	3.  23- 33  Zeile Stunden Einer  1 2 3 4 5 6 7 8 9
	4.  34- 44  Zeile frei
	5.  45- 55  Zeile Minuten Zehner  1 2 3 4 5
	6.  56- 66  Zeile Minuten Einer 1 2 3 4 5 6 7 8 9
	7.  67- 77  Zeile frei
	8.  78- 89  Zeile Sekunden Zehner 1 2 3 4 5
	9.  90-101  Zeile Sekunden Einer  1 2 3 4 5 6 7 8 9
	10. Zeile frei
        '''
	mysecond=-1
	myminute=-1
	myhour=-1
	# Set background color
        wcd.setColorToAll(self.bg_color, includeMinutes=True)
	wcd.show()
        while True:
		now = datetime.datetime.now()
                if myhour <> now.hour:
                        self.show_second(wcd, wci, now.hour, 12)
                        myhour = int(now.hour)

		if myminute <> now.minute:
			self.show_second(wcd, wci, now.minute, 45)
                        myminute = int(now.minute)

		if mysecond <> now.second:
			self.show_second(wcd, wci, now.second, 78)
			mysecond = int(now.second)

		event = wci.waitForEvent(0.4)
            	if (event == wci.EVENT_BUTTON_RETURN) or (event == wci.EVENT_EXIT_PLUGIN):
                	return # Return to main menu, if button_return is pressed


    def show_second(self, wcd, wci, second, startindex):
	stz = startindex
	ste = stz + 11
	se = second%10 
	if (se == 0):
		wcd.setColorBy1DCoordinates(wcd.strip, range(ste, (ste+11)), self.bg_color)
	else:
		wcd.setColorBy1DCoordinates(wcd.strip, range(ste, (ste+se)), self.color)
	sz = second // 10
	if (sz == 0):
		wcd.setColorBy1DCoordinates(wcd.strip, range(stz, (stz+11)), self.bg_color)
        else:
                wcd.setColorBy1DCoordinates(wcd.strip, range(stz, (stz+sz)), self.color)
	wcd.show()
	print(str(second) + ' se=' + str(se) + ' sz=' + str(sz))


    def show_time(self, wcd, wci):
	now = datetime.datetime.now()
	print(str(now))
