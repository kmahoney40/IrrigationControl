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
    count = 0

    startTime = 1289
    # integar division in Python 2.x
    stHour = startTime / 100
    stMin  = startTime - stHour * 100
    stMins = stMin + stHour * 60

    runTimes = [  [10, 0, 2, 0, 10, 0, 10],
                    [0, 30, 0, 0, 30, 0, 0],
                    [5, 5, 2, 5, 5, 5, 5],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0]]
    valvePos = ["Off", "Off", "Off", "Off", "Off", "Off", "Off"]

    while keepGoing:
        dtn = datetime.datetime.now()
        tm = time.time()

        scr.addstr(0, 0, "dtn: " + str(dtn))
        scr.addstr(1, 0, "tm:  " + str(tm))


               #dtNow is local 24hour time
        dtNow = datetime.datetime.now()
        dtDay = datetime.datetime.today().weekday()
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
        scr.addstr(11, 0, "dtDay: " + str(dtDay))

        scr.addstr(12, 0, str(runTimes[1][1]))
        scr.addstr(13, 0, str(runTimes[2][6]))

        minsLt = 0
        minsGt = stMins
        for v in range(7):
          minsLt += minsGt
            minsGt += runTimes[v][dtDay]
            if minsLt < dtNowMinute and dtNowMinute < minsGt:
                scr.addstr(14 + v, 0, "Valve " + str(v) + " on")
            else:
                scr.addstr(14 + v, 0, "Valve " + str(v) + " off")


        scr.refresh()
        time.sleep(1)
        count += 1
        if count > 100:
            keepGoing = False
    # while keepGoing

    curses.endwin()


# if __name__
