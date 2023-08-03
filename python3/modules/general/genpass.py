# Python modules to generate passwords
# password types: alpha numeric, random characters, xkcd

# import common modules
import string, secrets, requests
from cryptography.fernet import Fernet as crypt

# alpha numeric
def alpha_numeric(LEN):
    '''
    Outputs password LEN characters long composed of lowercase, uppercase, and numbers.
    genpass.alpha_numeric(LEN)
    LEN: Integer, how many characters long you want your password to be.
    Output: String, or False on failure.
    '''
    if type(LEN) is not int or LEN <= 0:
        return False
    pool = string.ascii_letters + string.digits
    while True:
        result = ''.join(secrets.choice(pool) for X in range(LEN))
        if (any(X.islower() for X in result)
                and any(X.isupper() for X in result)
                and sum(X.isdigit() for X in result) >= 3):
            break
    return result

# random characters
def random_characters(LEN):
    '''
    Outputs LEN characters composed of lowercase, uppercase, numbers, and symbols.
    genpass.random_characters(LEN)
    LEN: Integer, how many characters you want.
    Output: String, or False on failure.
    '''
    if type(LEN) is not int or LEN <= 0:
        return False
    pool = string.ascii_letters + string.digits + string.punctuation
    while True:
        result = ''.join(secrets.choice(pool) for X in range(LEN))
        if (any(X.islower() for X in result)
                and any(X.isupper() for X in result)
                and sum(X.isdigit() for X in result) >= 3
                and [X in string.punctuation for X in result].count(True) <= 5):
            break
    return result

def generate_password(LEN):
    '''
    Outputs password LEN characters long composed of lowercase, uppercase, numbers, and symbols.
    Follows character compatibility for passwords.
    genpass.generate_password(LEN)
    LEN: Integer, how many characters long you want your password to be.
    Output: STring, or False on failure.
    '''
    if type(LEN) is not int or LEN <= 0:
        return False
    pool = string.ascii_letters + string.digits + string.punctuation.replace('=', '').replace('\'', '').replace('\"', '').replace('`', '').replace('@', '')
    while True:
        result = ''.join(secrets.choice(pool) for X in range(LEN))
        if (any(X.islower() for X in result)
                and any(X.isupper() for X in result)
                and sum(X.isdigit() for X in result) >= 3
                and [X in string.punctuation for X in result].count(True) > 1
                and [X in string.punctuation for X in result].count(True) <= 5):
            break
    if result[0] in string.punctuation:
        result = result[:0] + secrets.choice(string.ascii_letters) + result[1:]
    return result

# xkcd
def xkcd(LEN):
    '''
    Outputs XKCD style password composed of LEN amount of words, seperated by spaces.
    Requires internet access.
    genpass.xkcd(LEN)
    LEN: Integer, how many random words you want in your password.
    Output: String, or False on failure.
    '''
    if type(LEN) is not int:
        return False
    get_words = 'https://www.mit.edu/~ecprice/wordlist.10000'
    response = requests.get(get_words)
    word_list = [X.decode('utf-8') for X in response.content.splitlines()]
    return ' '.join(secrets.choice(word_list) for X in range(LEN))

# encrypt password string
def encrypt_password(IN, KEY=None):
    '''
    Encrypt a password string using fernet for local storage etc.
    genpass.encrypt_password(IN)
    IN: Password string to encrypt
    KEY: Optional fernet encryption key to include
    Output: tuple, first object is the encrypted password bytes and the \
            second is the encryption key bytes, or False on failure
    '''
    if not KEY:
        key = crypt.generate_key()
    else:
        key = KEY
    if type(IN) is not str:
        return False
    IN = IN.encode()
    try:
        result = crypt(key).encrypt(IN)
    except:
        return False
    return result, key

# decrypt password bytes
def decrypt_password(IN, KEY):
    '''
    Decrypt a password using a provided fernet generated key.
    gnepass.decrypt_password(IN, KEY)
    IN: Fernet encrypted password bytes to decrypt
    KEY: Key to decrypt password
    Output: Decrypted password in string format, False on failure
    '''
    try:
        result = crypt(KEY).decrypt(IN).decode()
    except:
        return False
    return result
