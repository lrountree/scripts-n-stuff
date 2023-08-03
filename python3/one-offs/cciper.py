# Final Capstone Project

# Caesar Cipher:
## Key: 1 - 25
## Rotate each letter in a string up using key
## Wrap Z to A
## Encrypt and Decrypt a provided message

# Import Modules
import string
from random import seed, shuffle

#import pdb

# Set up classes and functions
class Cipher():
    def __init__(self, CHAR, KEY):
        self.char = CHAR
        self.key = KEY
        self.list = list(string.printable)
        seed(KEY)
        shuffle(self.list)
        self.char_index = self.list.index(CHAR)
    def Encrypt(self):
        encrypted_char = self.char_index + self.key
        if encrypted_char > 99:
            encrypted_char = encrypted_char + -100
        return self.list[encrypted_char]
    def Decrypt(self):
        decrypted_char = self.char_index - self.key
        if decrypted_char < 0:
            decrypted_char = decrypted_char + 100
        return self.list[decrypted_char]

def encrypt_message(KEY):
    message = input('Please enter a message to encrypt: ')
    object_list = list(string.printable)
    seed(KEY)
    shuffle(object_list)
    return ''.join([Cipher(X, KEY).Encrypt() for X in message])

def decrypt_message(KEY, message):
    if not message:
        message = input('Please enter a message to be decrypted: ')
    object_list = list(string.printable)
    seed(KEY)
    shuffle(object_list)
    return ''.join([Cipher(X, KEY).Decrypt() for X in message])

def YORN():
    get_yorn = input('[y]es or [n]o?: ')
    valid_yorn = False
    while not valid_yorn:
        if get_yorn not in ['y','Y','n','N']:
            get_yorn = input('Sorry, please choose [y] for yes or [n] for no: ')
        else:
            valid_yorn = True
    return get_yorn.lower()


# Set Variables
object_list = list(string.printable)

print('** Welcome to Caeser Cipher **')
# Get Key
key = int(input('Please enter an integer between 1 and 100: '))
valid_key = False
while not valid_key:
    if key not in range(1,101):
        key = int(input('Sorry, you must enter an integer between 1 and 100: '))
    else:
        valid_key = True

# Get Message
run_prompt = True
while run_prompt:
    e_or_d = input('Would you like to [e]ncrypt or [d]ecrypt?: ')
    valid_answer = True
    while not valid_answer:
        if e_or_d not in ['e','E','d','D']:
            e_or_d = input('Sorry, please choose [e] for encrypt or [d] for decrypt: ')
        else:
            valid_answer = True
    e_or_d = e_or_d.lower()
    if e_or_d == 'e':
        message = encrypt_message(key)
        print(f'Encrypted Message: {message}')
    elif e_or_d == 'd':
        try:
            message
        except:
            message = False
        message = decrypt_message(key, message)
        print(f'Decrypted Message: {message}')
    print('Would you like to decrypt the last message/encrypt a new message?')
    get_yorn = YORN()
    if get_yorn == 'n':
        run_prompt = False
