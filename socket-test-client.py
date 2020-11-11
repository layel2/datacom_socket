# -*- coding: utf-8 -*-

# Import socket module 
import socket
import hashlib	
from cryptography.fernet import Fernet		 

# Create a socket object 
s = socket.socket()				

PACKGATE_LEN = 2048 #bytes
FRAGMENT_HEADER_SIZE = 2 #bytes
CHECKSUM_SIZE = 16 
DATA_SIZE = PACKGATE_LEN - FRAGMENT_HEADER_SIZE - CHECKSUM_SIZE

key = b'uwSs-EoXsrgAeZj9MVB_Rfm1kwlooP6Mwddm9iCmh5c='
f = Fernet(key)

# connect to the server on local computer 
port = 12345
s.connect(('127.0.0.1', port)) 
get_data = bytes()
# receive data from the server 
frag_num = int(s.recv(8))
print(frag_num,type(frag_num))
for i in range(frag_num):
    rev_pkg = s.recv(PACKGATE_LEN)
    num_frag = rev_pkg[:FRAGMENT_HEADER_SIZE]
    rev_md5 = rev_pkg[FRAGMENT_HEADER_SIZE:FRAGMENT_HEADER_SIZE+CHECKSUM_SIZE]
    rev_data = rev_pkg[FRAGMENT_HEADER_SIZE+CHECKSUM_SIZE : ]
    md5 = hashlib.md5(rev_data).digest()
    if(rev_md5 != md5):
        print('loss pkg')
    get_data += rev_data

decryp_data = f.decrypt(get_data)
#print(s.recv(2048))
# close the connection 
s.close()	 
out = open('rec.png','wb')
out.write(decryp_data)
out.close()