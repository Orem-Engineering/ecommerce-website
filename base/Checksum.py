# for security against hackers
# pip install pycryptodome
# suppost to be in paytme folder in the root directory
import base64
import string
import random
import hashlib

from Crypto.Cipher import AES

IV = "@@@@&&&&####$$$$"
BLOCK_SIZE = 16

# complete 
def generate_checksum(param_dict,merchant_key,salt=None):
    param_string = __get_param_string__(param_dict)
    salt = salt if salt else __id_generator__(4)
    final_string = '%s|%s'% (param_string,salt)
    
    hasher = hashlib.sha256(final_string.encode())
    hash_string = hasher.hexdigest()
    
    hash_string += salt
    
    return __encode__(hash_string,IV,merchant_key)

def generate_refund_checksum(param_dict,merchant_key,salt=None): 
    for i in param_dict:
        if("|" in param_dict[i]):
            param_dict = {}
            exit()
    params_string = __get_param_string__(param_dict)
    salt = salt if salt else __id_generator__(4)
    final_string = '%s|%s' % (params_string,salt)
    
    hasher = hashlib.sha256(final_string.encode())
    hash_string = hasher.hexdigest()
    hash_string += salt

# complete 
def verify_checksum(param_dict,merchant_key,checksum):
    # remove checksum
    if 'CHECKSUMHASH' in param_dict:
        param_dict.pop('CHECKSUMHASH')
        
    #get salt
    paytm_hash = __decode__(checksum,IV,merchant_key)
    salt = paytm_hash[-4:]
    calculated_checksum = generate_checksum(param_dict,merchant_key,salt=salt)
    return calculated_checksum == checksum

def verify_checksum_by_str(param_str,merchant_key,checksum):
    # geting salt
    paytm_hash = __decode__(checksum,IV,merchant_key)
    salt = paytm_hash[-4:]
    calculated_checksum = generate_checksum_by_str(param_str,merchant_key,salt=salt)
    return calculated_checksum == checksum
    
def __id_generator__(size=6,chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

def __get_param_string__(params):
    params_string = []
    for key in sorted(params.keys()):
        if("REFUND" in params[key] or "|" in params[key]):
            respons_dict = {}
            exit()
        value = params[key]
        params_string.append('' if value == 'null' else str(value))
    return '|'.join(params_string)
__pad__ =lambda s:s + (BLOCK_SIZE - len(s) % BLOCK_SIZE)* chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)

# complete 
def __decode__(to_decode,iv,key):
    # decode
    to_decode = base64.b64decode(to_decode)
    # decrypt
    c = AES.new(key.encode('utf-8'),AES.MODE_CBC,iv.encode('utf-8'))
    to_decode = c.decrypt(to_decode)
    if type(to_decode) == bytes:
        # convert bytes array to string
        to_decode = to_decode.decode()
    return _unpad__(to_decode)
# complete 
if __name__ == "__main__":
    params = {
        "MID":"mid",
        "ORDER_ID":"order_id",
        "CUST_ID":'cust_id',
        "TXN_AMOUNT":'1',
        "CHANNEL_ID":'WEB',
        "INDUSTRY_TYPE_ID":'Retail',
        "WEBSITE":'xxxxxxxxxx',
    }
    
    print(verify_checksum(params,'xxxxxxxxx,"CD5ndX8VVjWbbYoAtKQIlvtXPypQYOg0Fi2AUYKXZA5XSHiRF0FDj7vQu66S8MHx9NaDZ/uYm3WBOWHf+sDQAmTyxqUipA7i1nILlxrk="))