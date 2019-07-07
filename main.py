import curses
import sys
import time
import datetime

import piplates.RELAYplate as RELAY


if __name__ == '__main__':

    src = curses.iniscr()
    src.noecho()
    src.nodelay(1)

    keepGoing = True
    
    while keepGoing:
        dtm = datetime.datetime.now()
        tm = time.time()

        src.addstr(0, 0, "dtm: " + str(dtm))
        src.addstr(1, 0, "tm:  " + str(tm))
    # while keepGoing

# if __name__