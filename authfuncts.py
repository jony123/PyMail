#!/usr/bin/env python
import functs
import commands
import config
import gnupg

"""
This file will be where we put all our custom functions that require auth.  Its up to you to pass the correct arguments.
"""
def respond(data, useraddr):
   failed = 'Sorry i could not authenicate you.  This is how to properly format for auth.\n\nemail:(Email you sent the auth from\ncommand:(authenication required command that you wanted to run\nuser:(username that you registred with.  In most cases it will be the email you registered with)\n(anything past this is command dependant)\n\nIf you have anymore troblues please email root@jonys.info for help.  Include everything you did.'
   userauth_DE = commands.userAUTH(data, useraddr) 
   #userauth_DE[0] is failed status,  [1] = commands, [2] = useremail, [3] = user password, [4] = everything inbitween the [start] and [end] tags.
   if userauth_DE[0] != -1:
      user_commands = userauth_DE[1].split()
      #This is where we call the auth functions now
      if user_commands[0] == 'sendback':
         returnstr = sendback(user_commands,userauth_DE[4])
            
      #This is where we stop calling authenicated function
   else:
      returnstr = failed
   return returnstr

def sendback(commands, message):
   returnstr = 'You asked me to resend the email you sent to me but decrypted...\nhere it is\n\n'+message
   return returnstr
   

