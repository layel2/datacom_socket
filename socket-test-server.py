# -*- coding: utf-8 -*-

# first of all import the socket library 
import socket		
import math	 
import hashlib
import time
from cryptography.fernet import Fernet

# next create a socket object 
s = socket.socket()
print ("Socket successfully created")

def load_key():
    """
    Loads the key named `secret.key` from the current directory.
    """
    return open("secret.key", "rb").read()

IS_ENCRYPT = True
CHECKSUM_SIZE = 16 #MD5
FRAGMENT_NUM = 2
FRAGMENT_HEADER_SIZE = 2 #bytes

port = 1234
s.bind(('192.168.1.50', port))		 
print ("socket binded to %s" %(port) )

# put the socket into listening mode 
s.listen(5)	 
print ("socket is listening")


#read_data = open('4thai.png','rb').read()
#encryption
#key = b'uwSs-EoXsrgAeZj9MVB_Rfm1kwlooP6Mwddm9iCmh5c='
key = load_key()
f = Fernet(key)

text = "Hello world my name is Pranpaveen Lay. เลย์ๆ"
data = text.encode('utf-8')
if(IS_ENCRYPT):
    data = f.encrypt(data)
checksum = hashlib.md5(data).digest()

combine_data = data+checksum
fragment_size = int(len(combine_data)/2 + 0.5)


while True: 

    c, addr = s.accept()	 
    print ('Got connection from', addr )
    for i in range(FRAGMENT_NUM):
        #print(i)
        frag_head = (str(i+1)+str(FRAGMENT_NUM)).encode('utf-8')
        frag_data = (combine_data[i*fragment_size:(i+1)*fragment_size])
        c.send(frag_head+frag_data)
        time.sleep(0.001)

    c.close() 
