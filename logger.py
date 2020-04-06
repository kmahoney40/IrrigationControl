import logging
import datetime

class logger:
    def __init__(self):
        self.today = datetime.date.today()
        log_file = "water_" + str(self.today) + ".log"
        logging.basicConfig(filename=log_file, level=logging.DEBUG)
    #def __init__

    def log(self, msg, lvl="i"):
        new_day = datetime.date.today()
        dtnow = str(datetime.datetime.now()) + " "
        if new_day != self.today:
            self.today = new_day
            log_file = "water_" + str(self.today) + ".log"
            loggind.basicConfig(filename=log_file)
        if lvl.lower() == "i":
            logging.info(dtnow + msg)
        if lvl.lower() == "d":
            logging.info(dtnow + msg)
        if lvl.lower() == "w":
            logging.info(dtnow + msg)

    # def log()
# class Log
