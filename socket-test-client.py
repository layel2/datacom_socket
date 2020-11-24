# -*- coding: utf-8 -*-

# Import socket module 
import socket
import hashlib	
from cryptography.fernet import Fernet	 

def load_key():
    """
    Loads the key named `secret.key` from the current directory.
    """
    return open("secret.key", "rb").read()

# Create a socket object 
s = socket.socket()				

IS_ENCRYPT = True
PACKGATE_LEN = 2048 #bytes
FRAGMENT_HEADER_SIZE = 2 #bytes
CHECKSUM_SIZE = 16 
DATA_SIZE = PACKGATE_LEN - FRAGMENT_HEADER_SIZE - CHECKSUM_SIZE


# connect to the server
port = 1234
s.connect(('', port)) 
get_data = []
rev_pkg = s.recv(PACKGATE_LEN)
get_data.append(rev_pkg)
print(rev_pkg)
while(rev_pkg!=bytes()):
    rev_pkg = s.recv(PACKGATE_LEN)
    if(rev_pkg==bytes()):
        break
    print(rev_pkg)
    get_data.append(rev_pkg)

print("\n")
num_frag = len(get_data)
frag_dict = {}
for i,pkg in enumerate(get_data):
    pkg_frag = pkg[0]-48
    frag_dict[pkg_frag] = i

combine_data = bytes()

for frag in sorted(frag_dict.values()):
    combine_data += get_data[frag][2:]

rev_msg = combine_data[:-16]
rev_checksum = combine_data[-16:]

print("Recive message is ",rev_msg.decode('utf-8'))
print("Recive md5 is ",rev_checksum)
msg_checksum = hashlib.md5(rev_msg).digest()
print("Checksum match :",msg_checksum==rev_checksum)

#key = b'uwSs-EoXsrgAeZj9MVB_Rfm1kwlooP6Mwddm9iCmh5c='
key = load_key()
f = Fernet(key)
if(IS_ENCRYPT):
    decrypt_data = f.decrypt(rev_msg)
print("Decrypt message is ",decrypt_data.decode('utf-8'))



s.close()	 
