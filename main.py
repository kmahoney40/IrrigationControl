import curses
import sys
import time
import datetime
import array
import json
import piplates.RELAYplate as RELAY

#import piplates.RELAYplate as RELAY



def main(scr):
    import time
    import datetime

    scr = curses.initscr()
    curses.cbreak()
    curses.noecho()
    scr.keypad(1)
    scr.nodelay(1)


    # Read conf file
    confFile = open("irragation.conf", "r")
    confData = confFile.read()
    confJson = json.loads(confData)
    
    pid = confJson["pid"]        
    runTimes = confJson["runTimes"]
    scr.addstr(1, 0, "startTime: " + str(confJson["startTime"]) + " pid:" + str(pid))
    

    # 24 hour loal time 600 = 6am, 1450 = 2:50 pm
    startTime = confJson["startTime"]
    manTime = 2.0

    # integar division in Python 2.x
    stHour = startTime / 100
    stMin  = startTime - stHour * 100
    stMin  = stMin + stHour * 60

    # Start with all valves off
    for v in range(len(runTimes)):
        RELAY.relayOFF(pid, v+1)

    scr.addstr(30, 0, "Press 'q' to quit or 'm'  to enter manual mode     ")
    keepGoing = True
    manualMode = 0
    manualStart = 0
    while keepGoing:
        dtn = datetime.datetime.now()

        scr.addstr(0, 0, "dtn: " + str(dtn))

        #dtNow is local 24hour time
        c = scr.getch()
        if c != curses.ERR:
            if chr(c) == 'q':
                keepGoing = False
            if chr(c) == 'm':
                manualMode = 1
                scr.addstr(30, 0, "Press 'Esc' to return to standard mode, 'q' to quit")
            if c == 27:
                manualMode = 0
                scr.addstr(30, 0, "Press 'q' to quit or 'm' to enter manual mode      ")
        
        dtNow = datetime.datetime.now()
        dtDay = datetime.datetime.today().weekday()
        dtNowHour = dtNow.hour
        dtNowMin  = dtNow.minute
        dtNowMin += dtNowHour * 60 - stMin
        # Clear extra characters for negative and 3 or 4 digit times
        scr.addstr(2, 0, "dtNowMin: " + str(dtNowMin) + "      ")

        scr.addstr(3, 0, "startTime: " + str(startTime))
        scr.addstr(4, 0, "stMins: " + str(stMin))
        scr.addstr(5, 0, "dtDay: " + str(dtDay))

        if manualMode:
            if manualMode == 1:
                manualMode += 1
                for v in range(14):
                    scr.addstr(6 + v, 0, "                                         ")
            if manualMode > 1:
                delta = time.time() - manualStart
                scr.addstr(6, 0, "delta: " + str(delta))
                scr.addstr(7, 0, "delta: " + str(round(delta, 4)) + "             ")
            
                #manTime = manTime * 60.0 - delta
                scr.addstr(9, 0, "manTime: " + str(manTime))

            manualStart = time.time()
            scr.addstr(8, 0, "manualStart: " + str(manualStart))
            
        else:
            gtMin = 0
            ltMin = 0
            if dtNowMin >= 0: 
                for v in range(len(runTimes)):
                    gtMin += runTimes[v][dtDay]
                    if v > 0:
                        ltMin += runTimes[v-1][dtDay]
                    scr.addstr(13 + v, 0, "ltMin: " + str(ltMin) + ", gtMin: " + str(gtMin))
                    if ltMin <= dtNowMin and dtNowMin < gtMin:
                        scr.addstr(6 + v, 0, "Valve" + str(v) + "  on")
                        RELAY.relayON(pid, v+1)
                    else:
                        scr.addstr(6 + v, 0, "Valve" + str(v) + " off")
                        RELAY.relayOFF(pid, v+1)
        # if manualModd: else:

        scr.refresh()
        time.sleep(1)


    # while keepGoing

    # Turn off all valves on exit
    for v in range(len(runTimes)):
        RELAY.relayOFF(pid, v+1)
    curses.endwin()

# def main(scr)


if __name__ == '__main__':
    try:
        curses.wrapper(main)
    finally:
        for v in range(7):
            RELAY.relayOFF(0, v+1)

# if __name__
