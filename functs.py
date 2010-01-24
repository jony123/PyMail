#!/usr/bin/python
"""
This file will be where we put all our custom functions.  Its up to you to pass the correct arguments.
"""
import commands
import config
import authfuncts
from xgoogle.search import GoogleSearch
from urlparse import urlparse
import gnupg

def respond(subject, data, useraddr):
   phrase = subject.split()
   print phrase
   
   ################################################### This is where we call our custom functions. The list 'phrase' contains the words in the subject line
   ################################################### e.g. If sent in the subject line was this 'mail user pass' phrase[0] would be 'mail', phrase[1] would be 'user' 
   ################################################### and phrase[2] would be 'pass'. As you can see phrase just contains the subject line split()
   if phrase [0] == 'help':
      try:
         tore = commands.gethelp(phrase[1])
      except:
         tore = commands.gethelp(phrase[0])

   elif phrase[0] == 'google':
      tore = google(phrase)
   elif phrase[0] == 'test':    #This hear fetches the first word of the subject line and asks if it is identicle to the function identifyer 'test'. 
      tore = test(phrase)       # We then say if phrase[0] does = 'test' run the function test giving it the whole subject line and store the results in tore  
   elif phrase[0] == 'this':                     #This checks if phrase[0] = this.  if it does it calls this passing phrase[1] and phrase[2] and then storing the results in tore
      tore = this(phrase[1], phrase[2])
   elif phrase[0] == 'public_key':
      print "Called public_key"
      tore = pubkey(data)
      
   elif phrase[0] == 'GPG':          #This is where the auth functions are called
      gpg = gnupg.GPG()
      tore = authfuncts.respond(data ,useraddr)

      
  
      
      
      
   ################################################### Just marking the end of the function calling part.
   ###################################################
   else:                  
      tore = 'Sorry I\'m not sure what you want.  Next time email me a single \'help\' in the subject line to list alll available commands'
      pass
   return tore






################################################################################################
#                    These are all the functions that come with PyMail                         #
################################################################################################


"""
Example of how to write the function
"""
def test(text):              #We define the function 'test' and tell it that the argument text will be pased to it.  When writing functions you can pass the whole subject line or 
   print "test"
   tore = ''                     #specfic parts of it.  For simplicatly we passed the whole subject line.
   for x in text:              #We give tore a value and then return it.                                     
      tore = tore+' '+x
   return tore
   #----------------------------------------------
   # Example of how to write a function with specific argus

def this(a, b):            #We define the function 'this' and tell it that the arguments a and b will be passed to it.  We assign tore the value of a plus b to the power of b and then we 
   a = int(a)
   b = int(b)
   rsults = a+b+a*b
   rs1 = a*b
   a = str(a)
   b = str(b)
   rs1 = str(rs1)
   rsults = str(rsults)             #   return the value of tore.
   tore = "a = "+a+"\nb = "+b+"\nc = a + b + ab\nc = "+a+" + "+b+" + "+a+" * "+b+"\nc = "+a+" + "+b+" + "+rs1+"\nc = "+rsults+"\n"
   return tore
   
def google(data):  #In this fuction we will do the phrasing of the subject line ourselfs.
   print "Called google"
   tore = ''
   search_string = ''

   if data[1] == 'search':
      for i in range(2,len(data)):
         search_string = search_string + data[i] + ' '
      try:
         
         tore = "Here are the first 25 results from google when \'"+search_string+"\' is queried\n\n"
         gs = GoogleSearch(search_string)
         gs.results_per_page = 25
         results = gs.get_results()
         
         for res in results:
            #print res.title.encode('utf8')
            tore = tore+res.title.encode('utf8')+"\n"
            #print res.desc.encode('utf8')
            tore = tore+res.desc.encode('utf8')+"\n"
            #print res.url.encode('utf8')
            tore = tore+res.url.encode('utf8')+"\n\n--------------------------------------\n"
            print
      except:
         print "Search failed: %s" % e
         tore = "Search failed: %s" % e

   return tore

def pubkey(data):
   gpg = gnupg.GPG()
   tore = 'Here is my public key.  Use it to encrypt the infomation you send to me. \nP.s if you don\' know whats this is for you probally don\' need it\n\n'+gpg.export_keys('jonathon')
   return tore
   
