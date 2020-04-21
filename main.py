import curses
import sys
import time
import datetime
import array
import json
import piplates.RELAYplate as RELAY
import logger
import smtplib
import mail
from pathlib2 import Path

def adjManTime(inCh):
    
    dt = 1
    retVal = (0,0)

    lst = ['a','s','d','f','g','h','j','A','S','D','F','G','H','J','z','x','c','v','b','n','m','Z','X','C','V','B','N','M']
    if inCh in lst:
        idx = lst.index(inCh)
        if inCh.isupper():
            dt = 5
        if idx > 13:
            dt *= -1
        idx = idx % 7
        retVal = (idx,dt)

    return retVal

def getRunTimes(day, times):
 strTimes = "Today's run times: "
    for idx in range(len(times)):
        strTimes += str(times[idx][day]) + ", "
    strTimes = strTimes[:len(strTimes) - 2]
    return strTimes

def main(scr):
    import time
    import datetime

    scr = curses.initscr()
    curses.cbreak()
    curses.noecho()
    scr.keypad(1)
    scr.nodelay(1)

    log = logger.logger()
    log.log("main started")

    # Read conf file
    confFile = open("irragation.conf", "r")
    confData = confFile.read()
    confJson = json.loads(confData)
    
    pid = confJson["pid"]        
    runTimes = confJson["runTimes"]
    scr.addstr(1, 0, "startTime: " + str(confJson["startTime"]) + " pid:" + str(pid))
   
    # show run times on the right side of display, runTimes is only read at startup
    for v in range(len(runTimes)):
        scr.addstr(3+v, 32, "Valve " + str(v) + ":")
        for d in range(len(runTimes[0])):
            scr.addstr(3+v, 40+d*3, str(runTimes[v][d]).rjust(3))

    # 24 hour loal time 600 = 6am, 1450 = 2:50 pm
    startTime = confJson["startTime"]
    manTimes = [0, 0, 0, 0, 0, 0, 0]
    manStart =  0

    # integar division in Python 2.x
    stHour = startTime / 100
    stMin  = startTime - stHour * 100
    stMin  = stMin + stHour * 60

    # Start with all valves off
    for v in range(len(runTimes)):
        RELAY.relayOFF(pid, v+1)

    scr.addstr(29, 0, "Press 'q' to quit or 'm' to enter manual mode")
    keepGoing = True
    manualMode = 0
    runManMode = False
    manualStart = 0
    sendMail = True

    while keepGoing:
        #log.log("keepGoing")
        dtn = datetime.datetime.now()

        scr.addstr(0, 0, "dtn: " + str(dtn))

        
        dtNow = datetime.datetime.now()
        dtDay = datetime.datetime.today().weekday()
        dtNowHour = dtNow.hour
        dtNowMin  = dtNow.minute
        dtNowMin += dtNowHour * 60 - stMin
       
        if dtNow.minute == 0 and dtNow.second < 10:
            Path('./TouchFile.txt').touch()

        c = scr.getch()
        if c != curses.ERR:
            if chr(c) == 'q':
                keepGoing = False
            # m is overloaded in manual mode - decrease valve 7 runtime
            if chr(c) == 'm':
                if manualMode == 0:
                    manualMode = 1
                    manStart = 0
                    scr.addstr(29, 0, "Press 'Esc' to return to standard mode, 'r' to run manual mode, 'q' to quit")
                    scr.clrtoeol()
            if chr(c) == 'r':
                if manualMode:
                    runManMode = True
            if c == 27:
                manualMode = 0
                runManMode = False
                for v in range(len(manTimes)):
                    RELAY.relayOFF(pid, v+1)       
                scr.addstr(29, 0, "Press 'q' to quit or 'm' to enter manual mode")
                scr.clrtoeol()

            if chr(c) == 'k':
                rt = getRunTimes(dtDay, runTimes)
                
                scr.addstr(30, 0, "trTimes: " + rt)
                m = mail.mail()
                m.send_mail(None, rt)
                Path('./TouchFile.txt').touch()

            if chr(c) == 'K':
                m = mail.mail()
                m.send_mail("Special Mail", "WOOT")
            
            if manualMode > 1:
                idx,delta = adjManTime(chr(c))
                manTimes[idx] += delta
                if manTimes[idx] > 99:
                    manTimes[idx] = 99
                if manTimes[idx] < 0:
                    manTimes[idx] = 0

        
        # Clear extra characters for negative and 3 or 4 digit times
        scr.addstr(2, 0, "dtNowMin: " + str(dtNowMin) + "      ")

        scr.addstr(3, 0, "startTime: " + str(startTime))
        scr.addstr(4, 0, "stMins: " + str(stMin))
        scr.addstr(5, 0, "dtDay: " + str(dtDay))

        if manualMode:
            if manualMode == 1:
                manualMode += 1
                manStart = dtNowMin
            
            scr.addstr(8, 0, "Up: 'a' 's' 'd' 'f' 'g' 'h' 'j'")
            for v in range(len(manTimes)):
                scr.addstr(9, 3 + v*4, str(manTimes[v]).rjust(3)) 
            scr.addstr(10, 0, "Dn: 'z' 'x' 'c' 'v' 'b' 'n' 'm'")
            scr.addstr(28, 0, "runManMode: " + str(runManMode) + "  ")

            if runManMode:
                sumManTimes = 0
                lastSumManTimes = 0
                for v in range(len(manTimes)):
                    sumManTimes += manTimes[v]
                    ltMin = manStart + lastSumManTimes
                    gtMin = manStart + sumManTimes
                    if manStart + lastSumManTimes <= dtNowMin and dtNowMin < manStart + sumManTimes:     
                        scr.addstr(11+v, 0, "Valve "+str(v) + ": ON - Time: " + str(gtMin-dtNowMin))
                        RELAY.relayON(pid, v+1)
                    else:
                        scr.addstr(11+v, 0, "Valve " + str(v) + ": OFF")
                        scr.clrtoeol()
                        RELAY.relayOFF(pid, v+1)
                    lastSumManTimes = sumManTimes
                if dtNowMin >= manStart + sumManTimes:
                    runManMode = False
            else:
                for v in range(len(manTimes)):
                    scr.addstr(11+v, 0, "Valve " + str(v) + ": OFF")
                    scr.clrtoeol()
                    RELAY.relayOFF(pid, v+1)       
            # if runManMode            
        else:
            
            scr.addstr(8, 0, "                               ")
            scr.addstr(9, 0, "                               ")
            scr.addstr(10, 0, "                               ")
            scr.addstr(27, 0, "                                  ")
            scr.move(28,0)
            scr.clrtoeol()
            gtMin = 0
            ltMin = 0
            if dtNowMin >= 0: 

                if(sendMail):
                    rt = getRunTimes(dtDay, runTimes)
                    m = mail.mail()
                    m.send_mail(None, rt)
                    sendMail = False

                for v in range(len(runTimes)):
                    gtMin += runTimes[v][dtDay]
                    if v > 0:
                        ltMin += runTimes[v-1][dtDay]
                    if ltMin <= dtNowMin and dtNowMin < gtMin:
                        scr.addstr(11+v, 0, "Valve " + str(v) + ": ON - Time: "+ str(gtMin-dtNowMin))
                        RELAY.relayON(pid, v+1)
                    else:
                        scr.addstr(11+v, 0, "Valve " + str(v) + ": OFF")
                        scr.clrtoeol()
                        RELAY.relayOFF(pid, v+1)
            else:
                sendMail = True
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
