#!/usr/bin/env python
"""
This file is for all the various static functions.  You should just normally leave this file alone unless you need to mod the way it connects to the servers.
"""

##########################
########functions#########
##########################
from email.mime.text import MIMEText               
from email.mime.image import MIMEImage                 #These are the MIME auto-formating thingys        
from email.mime.multipart import MIMEMultipart
import smtplib          #The libary for smtp.
import base64
import poplib
import config
import functs
import re
import gnupg
import threading
import Queue

# This below is just classes and seutuff for the threading stuff.  Not to import but i wouldnt advise messing around with it unless you know what your doing.
class emaildo( threading.Thread ):
   def run ( self ):
      print self.getName()+'  Is up'
      while True:
         data = clientPool.get()
         if data != None:
            print self.getName()+'  Is acting on an email'
            message = functs.respond(getSubject(data[1]), data, phraseSmtp(data))
            sendEmail(phraseSmtp(data), config.myemail, writeEmail(phraseSmtp(data), config.myemail, 'Re: '+getSubject(data[1]),  message).as_string())




#Here are some of the functions used.
def phraseSmtp( data ):
   userfrom = data[1][0].replace('<', '').replace('>', '').split()[1]         #->-- This function sorts the burst of data and returns the email address that sent the email.
   return userfrom
     
def sendEmail( fromadd, toadd, msg):   
   print "sending"
   if config.authmethod == 'saslplaintext':   
      server = smtplib.SMTP(config.smtp_server,  config.smtp_port)
      server.ehlo()  
      encoded = base64.b64encode('\0'+config.smtp_user+'\0'+config.smtp_userpass)   #Authenicating and sending email via smtp server.  
      server.docmd('AUTH PLAIN '+encoded)                                                         
   if config.authmethod ==  'smtplib':   
      server = smtplib.SMTP(config.smtp_server,  config.smtp_port)
      server.login(config.smtp_user, config.smtp_userpass) 
#   if config.authmethod == "gmail":
#     server = smtplib.SMTP("smtp.gmail.com")
#     server.ehlo("smtp.gmail.com")                              This doesnt work.
#     server.starttls()
#     server.ehlo("smtp.gmail.com")
#     encoded = base64.b64encode('\0'+config.smtp_user+'\0'+config.smtp_userpass)
#     server.putcmd("AUTH PLAIN "+encoded) 
   if config.authmethod == 'none': 
      server = smtplib.SMTP(config.smtp_server,  config.smtp_port)
      pass  
   server.sendmail(config.myemail, fromadd, msg) 
   server.quit()
   print "sent"

def writeEmail(to, fromuser, sub, msg1):   
   # Create the container (outer) email message. 
   msg = MIMEText(msg1+"\r\n\nFrom\r\nPyMail")   
   msg['Subject'] = sub       
   msg['From'] = fromuser
   msg['To'] = to
   msg.preamble = msg1  
   return msg

def getSubject(data):
   loop = 0
   for x in data:
      found = x.find('Subject')
      if found != -1:
         break
      loop = loop + 1
   return data[loop][8:]
   
def gethelp(withthis):
   try:
      f = open('help/'+withthis)
      tore = f.read()
      f.close()
   except:
      print "couldnt open help"
      tore = 'Sorry I dont know what your talking about.  Next time send me just \'help\' in the subject line to list all available commands'
      pass
   return tore
   
def normalPop(server, user, userpass):
   conn = poplib.POP3(config.pop_server)
   print "Connecting to POP3 server"
   conn.user(user)
   conn.pass_(userpass)
   status = conn.stat()
   status = str(status)
   print status
   new = status.replace( '(', '').replace( ')', '').split( ',' ) [ 0 ]
   print new
   newint = int(new)
   print newint
   if newint > 0:
      looper = 1
      while looper <= newint:
         print looper
         data = conn.retr(looper)
         conn.dele(looper)
         print ''
         print data
         print ''
         print phraseSmtp(data)
         clientPool.put ( data )
         print ''
         looper = looper + 1
   else:
      print "No new email"



   conn.quit()
   
def mk_nice_domain(domain):
   """
   convert domain into a nicer one (eg. www3.google.com into google.com)
   """
   domain = re.sub("^www(\d+)?\.", "", domain)
   # add more here
   return domain

def userAUTH(data, authaddr):
   failed = [-1,'']
   passed = [1,'','','', '']
   try:
      a = data[1].index('-----BEGIN PGP MESSAGE-----')
      b = data[1].index('-----END PGP MESSAGE-----')
   except:
      print 'Failed find encrypted message'
      return failed
   encrypted_msg = ''
   gpg = gnupg.GPG()
   message_sten = ''
   for i in range(a,b+1):
      encrypted_msg = encrypted_msg + data[1][i] + '\n'
   print encrypted_msg
   #decrypted_msg = decryptString(encrypted_msg)
   decrypted_msg = str(gpg.decrypt(encrypted_msg, passphrase=config.passphrase, always_trust = 'true')).split('\n')
   loop = 0
   for x in decrypted_msg:
      found = x.find('email')
      if found != -1:
         break
      loop = loop + 1
   print decrypted_msg
   if decrypted_msg[loop].find('email') != -1:
      enemail = decrypted_msg[loop].split(':')[1]
   else:
      print 'failed getting email'
      return failed
   if authaddr == enemail:
      passed[0] = 1 
      passed[2] = authaddr
   else:
      print 'failed matching emails'
      return failed
   for x in decrypted_msg:
      found = x.find('command')
      if found != -1:
         break
      loop = loop + 1
   if decrypted_msg[loop].find('command') != -1:
      passed[1] = decrypted_msg[loop].split(':')[1]
   else:
      print 'failed at getting command'
      return failed

   for x in decrypted_msg:
      found = x.find('user')
      if found != -1:
         print 'FOUND'
         break
      loop = loop + 1
   print decrypted_msg[loop]
   if decrypted_msg[loop].find('user') != -1:
      passed[2] = decrypted_msg[loop].split(':')[1]
   else:
      print'failed at getting user'
      return failed
   for x in decrypted_msg:
      found = x.find('password')
      if found != -1:
         break
      loop = loop + 1
   if decrypted_msg[loop].find('password') != -1:
      passed[3] = decrypted_msg[loop].split(':')[1]
   else:
      print 'failed at getting password.'
      return failed
   try:  #Checks if the user is registred.  If the user is it returns the access level.  This does not make it fail is it can't authenicate.  This is because some modules just need encryption but not auth.
      userdata = open('Database/users.log')
      userlines = userlines.readlines()
      userdata.close()
      for i in userlines:
         userdata_encrypted = userdata_encrypted + userlines[i] + '\n'
      userdata_decrypted = decryptString(userdata_encrypted)
      for x in userdata_decrypted:
         found = x.find(passed[2])
         if found != -1:
            break
         loop = loop + 1
      if decrypted_msg[loop].find(passed[2]) != -1:
         databaselineinfo = userdata_decrypted[loop].split()
         if databaselineinfo[0] == passed[2] and databaselineinfo[1] == passed[3]:
            passed[5] = 1
            passed[6] = databaselineinfo[2]
   except:
      passed[5] = -1
      passed[6] = 0
      

      
      
   try:
      print 'try'
      print decrypted_msg
      c = decrypted_msg.index('[start]')
      print c
      d = decrypted_msg.index('[end]') 
      messafe_sten = ''
      print d
      for i in range(c+1,d):
         message_sten = message_sten + decrypted_msg[i] + '\n'
         print message_sten  
      passed[5] = message_sten
      print passed
      return passed 
   except:
      print 'failed at trying to get the message'
      return failed

def decryptString(encrypted):
   gpg = gnupg.GPG()
   decrypted_msg = str(gpg.decrypt(encrypted, passphrase=config.passphrase, always_trust = 'true')).split('\n')
   return decrypted_msg


#Ignore this
clientPool = Queue.Queue ( 0 )
for x in xrange(config.threadnum):
   emaildo().start()
  
  
  
   """
def gmailPop(user, userpass):
   conn = poplib.POP3_SSL('pop.googlemail.com', '995')
   print "Connecting to Gmail's POP3 server"
   conn.user(user)
   conn.pass_(userpass)
   status = conn.stat()
   status = str(status)
   print status
   new = status.replace( '(', '').replace( ')', '').split( ',' ) [ 0 ]
   print new
   newint = int(new)                                                                #This gmailPop does work but the gmailSmtp doesn't.  Until me or someone can get smtp to work
   print newint                                                                       this and gmailSmtp will be commented out.
   if newint > 0:
      looper = 1
      while looper <= newint:
         print looper
         data = conn.retr(looper)
         conn.dele(looper)
         print ''
         print data
         print ''
         print phraseSmtp(data)
         message = functs.respond(getSubject(data[1]))
         sendEmail(phraseSmtp(data), config.myemail, writeEmail(phraseSmtp(data), config.myemail, 'Re: '+getSubject(data[1]),  message).as_string())
         print ''
         looper = looper + 1
   else:
      print "No new email"
      conn.quit()
      """
