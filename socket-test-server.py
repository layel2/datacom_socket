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

IS_ENCRYPT = False
CHECKSUM_SIZE = 16 #MD5
FRAGMENT_NUM = 3
FRAGMENT_HEADER_SIZE = 2 #bytes

IPREV_1 = '192.168.1.1'
IPREV_2 = '192.168.1.2'


port = 1234
s.bind(('192.168.1.3', port))		 
print ("socket binded to %s" %(port) )

# put the socket into listening mode 
s.listen(5)	 
print ("socket is listening")


#read_data = open('4thai.png','rb').read()
#encryption
key = b'uwSs-EoXsrgAeZj9MVB_Rfm1kwlooP6Mwddm9iCmh5c='
#key = load_key()
f = Fernet(key)

text = "Pranpaveen Laykaviriyakul Lay Hello world eiei wow za1234567890"
data = text.encode('utf-8')
if(IS_ENCRYPT):
    data = f.encrypt(data)
checksum = hashlib.md5(data).digest()

combine_data = data+checksum
fragment_size = int(len(combine_data)/FRAGMENT_NUM + 0.5)

data_frag = []
for i in range(FRAGMENT_NUM):
    #print(i)
    frag_head = (str(i+1)+str(FRAGMENT_NUM)).encode('utf-8')
    frag_data = (combine_data[i*fragment_size:(i+1)*fragment_size])
    data_frag.append(frag_head+frag_data)
    #time.sleep(0.001)

while True: 

    c, addr = s.accept()	 
    print ('Got connection from', addr )
    '''
    if addr[0] == IPREV_1 :
        c.send(data_frag[0])
    if addr[0] == IPREV_2 :
        c.send(data_frag[1])
    '''
    for i in range(FRAGMENT_NUM):
        #print(i)
        frag_head = (str(i+1)+str(FRAGMENT_NUM)).encode('utf-8')
        frag_data = (combine_data[i*fragment_size:(i+1)*fragment_size])
        c.send(frag_head+frag_data)
        time.sleep(0.1)
    

    c.close() 
