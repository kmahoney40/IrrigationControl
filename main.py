import curses
import sys
import time
import datetime
import array

#import piplates.RELAYplate as RELAY


if __name__ == '__main__':`

    import time
    import datetime

    scr = curses.initscr()
    curses.cbreak()
    curses.noecho()
    scr.keypad(1)
    scr.nodelay(1)

    keepGoing = True
    count = 0

    startTime = 615
    runTimes = array('i',[10,15,10,0])
    # integar division in Python 2.x
    stHour = startTime / 100
    stMin  = startTime - stHour * 100
    stMins = stMin + stHour * 60  

    while keepGoing:
        dtn = datetime.datetime.now()
        tm = time.time()

        scr.addstr(0, 0, "dtn: " + str(dtn))
        scr.addstr(1, 0, "tm:  " + str(tm))

        #dtNow is local 24hour time
        dtNow = datetime.datetime.now()
        dtNowHour = dtNow.hour
        dtNowMinute  = dtNow.minute
        scr.addstr(3, 0, "dtNow: " + str(dtNow))
        scr.addstr(4, 0, "dtNowHour: " + str(dtNowHour))
        scr.addstr(5, 0, "dtNowMinute: " + str(dtNowMinute))
        dtNowMinute += dtNowHour * 60
        scr.addstr(6, 0, "dtNowMinute-tot: " + str(dtNowMinute))
        

    
        scr.addstr(7, 0, "startTime: " + str(startTime))
        scr.addstr(8, 0, "stHour: " + str(stHour))
        scr.addstr(9, 0, "stMin: " + str(stMin))
        scr.addstr(10, 0, "stMins: " + str(stMins))
       
        if dtNowMinute > stMins:
            if dtNowMinute < stMins + runTimes[0] + runTimes[1] + runTimes[2] + runTimes[3]:
                scr.addstr(11, 0, "v4 ON")
            if dtNowMinute < stMins + runTimes[0] + runTimes[1] + runTimes[2]:
                scr.addstr(12, 0, "v3 ON")
            if dtNowMinute < stMins + runTimes[0] + runTimes[1]:
                scr.addstr(13, 0, "v2 ON")
            if dtNowMinute < stMins + runTimes[0]:
                scr.addstr(14, 0, "v1 ON")



 
        scr.refresh()
        time.sleep(1)
        count += 1
        if count > 10:
            keepGoing = False
    # while keepGoing

    curses.endwin()

# if __name__
