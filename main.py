import curses
import sys
import time
import datetime
import array

#import piplates.RELAYplate as RELAY


if __name__ == '__main__':

    import time
    import datetime

    scr = curses.initscr()
    curses.cbreak()
    curses.noecho()
    scr.keypad(1)
    scr.nodelay(1)

    keepGoing = True

    # 24 hour loal time 600 = 6am, 1450 = 2:50 pm
    startTime = 1359
    # Rows are valves, columns are days 0 - 6 for Mon - Sun, valve run times
    runTimes = [  [10, 0, 2, 2,   2, 0, 10],
                    [0, 30, 0, 0, 1, 0, 0],
                    [5, 5, 2, 2,  0, 0, 5],
                    [0, 0, 0, 0,  1, 1, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0]]


    # integar division in Python 2.x
    stHour = startTime / 100
    stMin  = startTime - stHour * 100
    stMin  = stMin + stHour * 60

    while keepGoing:
        dtn = datetime.datetime.now()

        scr.addstr(0, 0, "dtn: " + str(dtn))

        #dtNow is local 24hour time
        dtNow = datetime.datetime.now()
        dtDay = datetime.datetime.today().weekday()
        dtNowHour = dtNow.hour
        dtNowMin  = dtNow.minute
        dtNowMin += dtNowHour * 60 - stMin
        # Clear extra characters for negative and 3 or 4 digit times
        scr.addstr(6, 0, "dtNowMin: " + str(dtNowMin) + "      ")



        scr.addstr(7, 0, "startTime: " + str(startTime))
        scr.addstr(10, 0, "stMins: " + str(stMin))
        scr.addstr(11, 0, "dtDay: " + str(dtDay))

        gtMin = 0
        ltMin = 0
        if dtNowMin >= 0: 
            for v in range(len(runTimes)):
                gtMin += runTimes[v][dtDay]
                if v > 0:
                    ltMin += runTimes[v-1][dtDay]
                scr.addstr(21 + v, 0, "ltMin: " + str(ltMin) + " - gtMin: " + str(gtMin))
                if ltMin <= dtNowMin and dtNowMin < gtMin:
                    scr.addstr(14 + v, 0, "Valve" + str(v) + "  on")
                else:
                    scr.addstr(14 + v, 0, "Valve" + str(v) + " off")

        scr.refresh()
    
        c = scr.getch()
        if c != curses.ERR:
            keepGoing = False
    
        time.sleep(1)

    # while keepGoing

    curses.endwin()


# if __name__
