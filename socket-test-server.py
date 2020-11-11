# -*- coding: utf-8 -*-

# first of all import the socket library 
import socket		
import math	 
import hashlib
from cryptography.fernet import Fernet

# next create a socket object 
s = socket.socket()
print ("Socket successfully created")

port = 12345		
s.bind(('', port))		 
print ("socket binded to %s" %(port) )

# put the socket into listening mode 
s.listen(5)	 
print ("socket is listening")


read_data = open('4thai.png','rb').read()
key = b'uwSs-EoXsrgAeZj9MVB_Rfm1kwlooP6Mwddm9iCmh5c='
f = Fernet(key)
data = f.encrypt(read_data)

PACKGATE_LEN = 2048 #bytes
FRAGMENT_HEADER_SIZE = 2 #bytes
CHECKSUM_SIZE = 16 
DATA_SIZE = PACKGATE_LEN - FRAGMENT_HEADER_SIZE - CHECKSUM_SIZE#bytes
#DATA_LENGTH = FRAGMENT_SIZE + PACKGATE_SIZE + CHECKSUM_SIZE
fragmnet_num = int(math.ceil(len(data)/DATA_SIZE))



while True: 

    c, addr = s.accept()	 
    print ('Got connection from', addr )
    c.send(str(fragmnet_num).encode('utf-8').ljust(8))
    for i in range(fragmnet_num):
        #print(i)
        frag_head = str(i).encode('utf-8').ljust(FRAGMENT_HEADER_SIZE)
        frag_data = data[i*DATA_SIZE:(i+1)*DATA_SIZE]
        frag_md5 = hashlib.md5(frag_data).digest()
        c.send(frag_head+frag_md5+frag_data) 
    #c.send(b'aaasd') 
    c.close() 
