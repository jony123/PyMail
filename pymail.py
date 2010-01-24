#!/usr/bin/env python

#A simple test program for recieving and sending emails via python
#For others reading this please keep in mind i had to use AUTH PLAIN because i have saslauth
#on my server and no combinations of normal methods via smtplib would allow me to send mail.
#Contact  jony123@jonys.info
#Verson 1
"""
I wrote the simple script for checking the status of the inbox

Verson 1.1
I added the part that connects checks the status and if there emails  
it fetchs them displays them and delets them.

Version 1.2
Added support to email user back.  Added options for differnt auth  
methods not supported by smtplib (i may be wrong)

Version 1.3
Emails back with proper MIME stuff.

Version 1.4
Phrases for subject and now can act upon it

Verson 1.5
Added help command which returns the conents of any file in help/

Verson 1.6
Added test command

Verson 1.7
Completely revamped the whole script with imports of differnt files.  Also added some example functions.

Verson 1.8
attemped to add gmail support but couldn't get email to send,  If anyone could fix this and send the infomation to me it would be greatly appreasiated.  Added another test function 'this' to check math.
"""
import threading
import commands #This is our custom libary.
import functs #This is where all our custom functions and commands that 
import config
import time   #Time libarary
from time import strftime
message = ''#Leave this                     
####################################
############End Functions###########
####################################

#We are threading
class normalstuff ( threading.Thread ):
   def run ( self ):
      while True:
         if config.popmethod == "gmail":
            commands.gmailPop(config.pop_user, config.pop_userpass)
         else:
            commands.normalPop(config.pop_server, config.pop_user, config.pop_userpass)
         print "COnnection closed"
         print 'Sleeping for 3 minutes'
         print ' '
         print ' '
         time.sleep(config.poprefresh)

#We create an instance of the normal stuff thread here.

normalstuff().start()
