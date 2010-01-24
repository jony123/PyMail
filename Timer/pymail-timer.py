# Written By JustGage for the pymail.py script made by jony123

import time
import datetime

def getNowSecs():
    # get's all the dates numbers
    today = datetime.date.today()
    day = today.day
    month = today.month
    year = today.year
    # get's all the time's numbers
    now = time.localtime()
    hours = now.tm_hour
    mins = now.tm_min
    secs = now.tm_sec

    #this combines the current date and time into seconds
    totalSecs = (year * 360 * 12.0 * 24.0 * 60.0 * 60.0) + (month * 12.0 * 24.0 * 60.0 * 60.0)  + (day * 24.0 * 60.0 * 60.0) + (mins * 60.0) + secs

    return totalSecs

# Returns the number of seconds till the timer goes off
def newTimer(email, minsToAlarm):
    #get now's time in seconds
    nowSecs = getNowSecs()
    alarmSecs = nowSecs + minsToAlarm * 60.0
    #saves a new timer to the end of the file
    dbfile = open('Database/timers.log' , 'a')
    toWrite = email + " " + str(alarmSecs) + " \n"
    print "writing: " + toWrite
    dbfile.write(toWrite)
    dbfile.close()
    return alarmSecs #this should probably store the timer somhow

def logClean():
    print "---Logclean---"
    nowSecs = getNowSecs()
    dbfile = open('Database/timers.log')
    linesAray = dbfile.readlines()
    i = 0
    linesCleaned = 0
    cleanLines = ['']#range(0, len(linesAray)) # This makes sure the array is big enough for the whole file if we need it
    for line in linesAray:
        aTimer = line.split(' ')
        if (len(aTimer) > 1): # Supposed to get rid of annoying 0's and 1's
            if (float(aTimer[1]) > nowSecs):
                cleanLines.append(line)
                i += 1
            else:
                linesCleaned += 1
    dbfile.close()
    dbfile = open('Database/timers.log' , 'w')
    for line in cleanLines:
        print "writing: " 
        print line
        print line.__class__
        dbfile.write(str(line))

    dbfile.close()
    print "cleaned out " + str(linesCleaned) + " timers"
    print "---Logclean END---"

def checkTimers():

    here = getNowSecs()
    dbfile = open('Database/timers.log')
    linesAray = dbfile.readlines()
    dbfile.close()
    i = 0
    for line in linesAray:
        aTimer = line.split(' ')
        if (len(aTimer) == 3): #This makes sure this line is in proper format
            minsLeft = (float(aTimer[1]) - here) / 60.0
            if (float(aTimer[1]) < here):
                print str(i) + ") better send an Email!"
            else:
                print str(i) + ") " + str(aTimer[0]) + " still has " + str(minsLeft) + " mins left"
            i += 1
    logClean()


#---this will add a new timer for testing----
print "welcome to my timer! do you want to add a new entry?"
if (raw_input("[y/n]").lower() == "y"):
    newTimer(raw_input("Email: ") , float(raw_input("how many mins to time:"))) #this sets the timer for 15 seconds
    print "Timers going:\n-----------------------"
#---this will check all the existing timers---
checkTimers()

