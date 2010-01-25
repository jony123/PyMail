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
   #userauth_DE[0] is failed status,  [1] = commands, [2] = username, [3] = user password, [4] = everything inbitween the [start] and [end] tags., [5] is if the user could be auth'd and [6] is user access level.
   print userauth_DE
   if userauth_DE[0] != -1:
      user_commands = userauth_DE[1].split()
      #This is where we call the auth functions now
      if user_commands[0] == 'sendback':
         returnstr = sendback(user_commands,userauth_DE[4])
      elif user_commands[0] == 'check':
         returnstr = check(userauth_DE[4])
      else:
         returnstr = failed
   try:
      return returnstr
   except:
      return failed
def sendback(commands, message):
   returnstr = 'You asked me to resend the email you sent to me but decrypted...\nhere it is\n\n'+message
   return returnstr

def check(decryptedstuff):
   passwordhash = 'x'*len(decryptedstuff[3])
   if decryptedstuff[5] != -1:
      authed = 'YES'
   else:
      authed = 'NO'
   if decryptedstuff[6] == 0:
      authvalue = 'NONE'
   elif decryptedstuff[6] == 1:
      authvalue = 'LEVEL 1'
   elif decryptedstuff[6] == 2:
      authvalue = 'LEVEL 2'
   elif decryptedstuff[6] == 3:
      authvalue = 'LEVEL 3'
   elif decryptedstuff[6] == 4:
      authvalue = 'LEVEl 4'  
   elif decryptedstuff[6] == 5:
      authvalue = 'LEVEL 5'
   else:
      authvalue = 'NONE'
   
   
   returnstr = 'Here is all the infomation about you i was sent.\n\nUserName = '+decryptedstuff[2]+'\nPassword = '+passwordhash+'\nAuthenicated = '+authed+'\nAuthenication Level = '+authvalue+'\n\nMESSAGE\n'+decryptedstuff[4]
   print returnstr
   return returnstr
   

