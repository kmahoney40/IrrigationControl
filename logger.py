import logging

class Log:
    def __init__(self):
        new_day = datetime.date.today()
        today = datetime.date.today()
        log_file = "irrigation_" + str(today) + ".log"
        loggind.basicConfig(filename=log_file)
    #def __init__

    def log(msg, lvl="INFO"):
        new_day = datetime.date.today()
        if new_day != today:
            today = new_day
            log_file = "irrigation_" + str(today) + ".log"
            loggind.basicConfig(filename=log_file)
        if lvl == "INFO":
            logging.info(
        if lvl == "DEBUG":

        if lvl == "WARNING":

    # def log()
# class Log
