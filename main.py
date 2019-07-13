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

    startTime = 2032


    # integar division in Python 2.x
    stHour = startTime / 100
    stMin  = startTime - stHour * 100
    stMins = stMin + stHour * 60

    runTimes = [  [10, 0, 2, 2,   2, 0, 10],
                    [0, 30, 0, 0, 1, 0, 0],
                    [5, 5, 2, 2,  0, 0, 5],
                    [0, 0, 0, 0,  1, 1, 0],
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
        dtNowMinute += dtNowHour * 60 - stMins
        scr.addstr(6, 0, "dtNowMinute-tot: " + str(dtNowMinute) + " ")



        scr.addstr(7, 0, "startTime: " + str(startTime))
        scr.addstr(8, 0, "stHour: " + str(stHour))
        scr.addstr(9, 0, "stMin: " + str(stMin))
        scr.addstr(10, 0, "stMins: " + str(stMins))
        scr.addstr(11, 0, "dtDay: " + str(dtDay))

        scr.addstr(12, 0, str(runTimes[0][dtDay]))
        scr.addstr(13, 0, str(runTimes[1][dtDay]))

        minsLt = 0
        minsGt = 0
        counter = [0, 0, 0, 0, 0, 0, 0]
        if dtNowMinute >= 0: 
            for v in range(7):
                minsGt += runTimes[v][dtDay]
                if v > 0:
                    minsLt += runTimes[v-1][dtDay]
                scr.addstr(21 + v, 0, "minsLt: " + str(minsLt) + " - minsGt: " + str(minsGt))
                #minsLt  = minsGt
                #minsGt += runTimes[v][dtDay]
                counter[v] += 1
                if minsLt <= dtNowMinute and dtNowMinute < minsGt:
                    scr.addstr(14 + v, 0, "Valve" + str(v) + "  on")
                else:
                    scr.addstr(14 + v, 0, "Valve" + str(v) + " off")
                    

#                scr.addstr(22, 0, "minsLt: " + str(minsLt) +  " minsGt: " + str(minsGt) + " dtNowMinute: " + str(dtNowMinute))
#                scr.addstr(23, 0, "v: " + str(v) + " dtDay: " + str(dtDay))
#                while minsLt <= dtNowMinute and dtNowMinute < minsGt:
#            minsLt += minsGt
#            minsGt += runTimes[v][dtDay]

                # update dtNowMinute here KMDB
#                    dtNow = datetime.datetime.now()
#                    dtDay = datetime.datetime.today().weekday()
#                    dtNowHour = dtNow.hour
#                    dtNowMinute  = dtNow.minute
#                    if minsLt < dtNowMinute and dtNowMinute < minsGt:
#                        scr.addstr(14 + v, 0, "Valve " + str(v) + " on")
#                    else:
#                        scr.addstr(14 + v, 0, "Valve " + str(v) + " off")
#                    time.sleep(1)


        scr.refresh()
    
        c = scr.getch()
        if c != curses.ERR:
            keepGoing = False
    
        time.sleep(1)
        count += 1
        #if count > 100:
        #`    keepGoing = False
    # while keepGoing

    curses.endwin()


# if __name__
