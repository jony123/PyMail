#!/usr/bin/python
"""
In this file we set some config varibles such as pop,smtp servers and ports.
There isn't much settings yet but to create this file was needed after i redid the 
functions
"""
smtp_server = 'example.tld'      # Pop and Smtp server.
smtp_port = 25
smtp_user = 'user'
smtp_userpass = 'pass'
authmethod = "saslplaintext"                 #Authenication method See below.
"""
Support is for smtplib, saslplaintext and none. smtplib uses the normal way to authenicate saslplaintext encodes the username and pass with base64.  Normally it willl probaly be smtplib for most.  none is for if you where sending from localhost and didn't need to authenicate anyway.
"""

pop_server = 'example.tld'            
pop_port = 110
pop_user = 'user'
pop_userpass = 'pass'             
popmethod = "normal"
poprefresh = 60

myemail = 'user@example.tld'        #Email address you want to give the bot.

##Setting for gpg.
passphrase = 'passphrase here'

##Thread settings
threadnum = 2  #I would advive only changing this if you plan on having *VERY* large amounts of incomming mail.  Otherwise just leave it
