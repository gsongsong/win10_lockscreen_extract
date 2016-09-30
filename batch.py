import extract
import arrange
import publish
import func
import datetime

if __name__ == "__main__":
    LOG = 'log'
    logfile = open(LOG, 'a')
    func.logwrite(logfile, datetime.datetime.now().isoformat(' ') + '\n')
    logfile.close()
    extract.main(LOG)
    arrange.main(LOG)
    publish.main(LOG)
