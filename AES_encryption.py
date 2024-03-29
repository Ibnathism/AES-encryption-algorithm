from BitVector import *
from bitstring import ConstBitStream
import base64 
Sbox = [
    [0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76],
    [0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0],
    [0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15],
    [0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75],
    [0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84],
    [0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF],
    [0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8],
    [0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2],
    [0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73],
    [0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB],
    [0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79],
    [0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08],
    [0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A],
    [0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E],
    [0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF],
    [0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16],
]

InvSbox = (
    [0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB],
    [0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB],
    [0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E],
    [0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25],
    [0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92],
    [0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84],
    [0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06],
    [0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B],
    [0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73],
    [0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E],
    [0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B],
    [0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4],
    [0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F],
    [0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF],
    [0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61],
    [0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D],
)

def read_sbox(index_string: str, is_inverse: bool):
    
    row = int(index_string[0], 16)
    col = int(index_string[1], 16)
    #print(Sbox[row][col])
    
    if is_inverse:
        temp = InvSbox[row][col]
    else:
        temp = Sbox[row][col]
    
    temp_bv = BitVector(intVal=temp, size=16)
    s_box_data = temp_bv.get_bitvector_in_hex()
    #print(s_box_data+" when index string "+index_string)
    
    return str(s_box_data)[2:4]

def generate_sub_bytes(word: str, is_inverse: bool):
    
    length = len(word)
    sub_bytes = ""
    
    for i in range(0, length-1, 2):
        temp = read_sbox(index_string=word[i:i+2], is_inverse=is_inverse)
        sub_bytes = sub_bytes + temp
    
    return sub_bytes

def add_round_key(str1: str, str2: str):
    
    added_val = BitVector(hexstring=str1) ^ BitVector(hexstring=str2)
    
    return added_val.get_bitvector_in_hex()

def shift_row(word: str):
    
    return word[2:8]+word[0:2]

def cyclic_shift_row(state_mat: str):
    
    w0 = state_mat[0:2] + state_mat[10:12] + state_mat[20:22] + state_mat[30:32]
    w1 = state_mat[8:10] + state_mat[18:20] + state_mat[28:30] + state_mat[6:8]
    w2 = state_mat[16:18] + state_mat[26:28] + state_mat[4:6] + state_mat[14:16]
    w3 = state_mat[24:26] + state_mat[2:4] + state_mat[12:14] + state_mat[22:24]

    return w0 + w1 + w2 + w3 

def inverse_cyclic_shift_row(state_mat: str):
    
    w0 = state_mat[0:2] + state_mat[26:28] + state_mat[20:22] + state_mat[14:16]
    w1 = state_mat[8:10] + state_mat[2:4] + state_mat[28:30] + state_mat[22:24]
    w2 = state_mat[16:18] + state_mat[10:12] + state_mat[4:6] + state_mat[30:32]
    w3 = state_mat[24:26] + state_mat[18:20] + state_mat[12:14] + state_mat[6:8]

    return w0 + w1 + w2 + w3 

def g(word: str, round_constant: str):
    
    row_shifted_word = shift_row(word=word)
    sub_bytes = generate_sub_bytes(word=row_shifted_word, is_inverse=False)
    result = add_round_key(str1=sub_bytes, str2=round_constant)
    
    return result

def generate_round_keys(word0: str, word1: str, word2: str, word3: str, round_constant:str):
    
    round_key = ''
    temp = g(word=word3, round_constant=round_constant)
    
    word4 = add_round_key(str1=word0, str2=temp)
    word5 = add_round_key(str1=word4, str2=word1)
    word6 = add_round_key(str1=word5, str2=word2)
    word7 = add_round_key(str1=word6, str2=word3)
    
    round_key = word4+word5+word6+word7
    
    return round_key

def multiply(str1: str, str2: str):
    
    AES_modulus = BitVector(bitstring='100011011')
    bv1 = BitVector(hexstring=str1)
    bv2 = BitVector(hexstring=str2)
    temp = bv1.gf_multiply_modular(b=bv2, mod=AES_modulus, n=8)
    
    return temp.get_bitvector_in_hex()

def get_linear_val(row: int, col: int, str: str):
    
    idx = row*2 + col*8
    
    return str[idx:idx+2]

def get_mix_column_value(row: int, col: int, state_mat: str, is_inverse: bool):
    
    if is_inverse:
        mix_con = "0E090D0B0B0E090D0D0B0E09090D0B0E"
    else:
        mix_con = "02010103030201010103020101010302"
    
    m0 = multiply(str1=get_linear_val(row=row, col=0, str=mix_con), str2=get_linear_val(row=0, col=col, str=state_mat))
    m1 = multiply(str1=get_linear_val(row=row, col=1, str=mix_con), str2=get_linear_val(row=1, col=col, str=state_mat))
    m2 = multiply(str1=get_linear_val(row=row, col=2, str=mix_con), str2=get_linear_val(row=2, col=col, str=state_mat))
    m3 = multiply(str1=get_linear_val(row=row, col=3, str=mix_con), str2=get_linear_val(row=3, col=col, str=state_mat))
    
    temp = add_round_key(str1=m0, str2=m1)
    temp = add_round_key(str1=temp, str2=m2)
    temp = add_round_key(str1=temp, str2=m3)
    
    return temp

def apply_mix_column(state_mat: str, is_inverse: bool):
    
    temp = ''
    
    for col in range(0,4):
        for row in range(0,4):
            temp = temp + get_mix_column_value(row=row, col=col, state_mat=state_mat, is_inverse=is_inverse)
    
    return temp

def get_rk_list(keyInHex: str):
    
    round_constants = ['01000000','02000000', '04000000' , '08000000', '10000000', '20000000', '40000000',  '80000000', '1b000000', '36000000']
    
    rk_list = []
    rk_list.append(keyInHex)

    word0 = keyInHex[0:8]
    word1 = keyInHex[8:16]
    word2 = keyInHex[16:24]
    word3 = keyInHex[24:32]

    for i in range(1, 11):
        round_key = generate_round_keys(word0=word0, word1=word1, word2=word2, word3=word3, round_constant=round_constants[i-1])
        #print(round_key)
        rk_list.append(round_key)
        word0 = round_key[0:8]
        word1 = round_key[8:16]
        word2 = round_key[16:24]
        word3 = round_key[24:32]

    return rk_list


def encrypt_text(rkList: list, text: str):

    textInHex = BitVector(textstring=text).get_bitvector_in_hex()
    
    state_mat = add_round_key(str1=rkList[0], str2=textInHex)

    for r in range(1, 11):
        state_mat = generate_sub_bytes(word=state_mat, is_inverse=False)
        state_mat = cyclic_shift_row(state_mat=state_mat)
        
        if r != 10:
            state_mat = apply_mix_column(state_mat=state_mat, is_inverse=False)
        
        state_mat = add_round_key(str1=state_mat, str2=rkList[r])
        
        #print(r, ': ', state_mat)
    
    return state_mat

def decrypt_text(rkList: list, cipherText: str):
    
    state_mat = add_round_key(str1=rkList[10], str2=cipherText)

    for r in range(1, 11):
        state_mat = inverse_cyclic_shift_row(state_mat=state_mat)
        state_mat = generate_sub_bytes(word=state_mat, is_inverse=True)
        state_mat = add_round_key(str1=state_mat, str2=rkList[10-r])
        
        if r != 10:
            state_mat = apply_mix_column(state_mat=state_mat, is_inverse=True)
        
        #print(r, ': ', state_mat)

    print("Decipher", state_mat)
    state_mat = BitVector(hexstring=state_mat).get_bitvector_in_ascii()
    
    return state_mat
    

def init(key: str):
    if len(key) > 16:
        key = key[0:16]
    elif len(key) < 16:
        key.ljust(16, '0')
    
    keyInHex = BitVector(textstring=key).get_bitvector_in_hex()

    rk_list = get_rk_list(keyInHex=keyInHex)

    return rk_list

def encrypt(f_name: str, rks: list):
    s = ConstBitStream(filename=f_name)
    text = BitVector(bitstring=s).get_bitvector_in_ascii()

    l = len(text)
    encrypted_text = ''
    for i in range(0, l-1, 16):
        t = text[i:i+16]
        if i+16 > l:
            t = t.ljust(16)
        temp = encrypt_text(rkList=rks, text=t)
        print('Cipher', temp)
        encrypted_text = encrypted_text + temp

    return encrypted_text

def decrypt(encrypted_text: str, file_name: str, rks: list):
    l = len(encrypted_text)
    den = ''
    for i in range(0, l-1, 32):
        temp = decrypt_text(rkList=rks, cipherText=encrypted_text[i:i+32])
        #print("Decipher", temp)
        den = den + temp

    f = open(file_name, 'a')
    f.write(den)

def encrypt_image(file_name: str, rks: list):
    with open(file_name, "rb") as image2string: 
        text = base64.b64encode(image2string.read()) 
    text = text.decode('utf-8')
    l = len(text)
    encrypted_text = ''
    for i in range(0, l-1, 16):
        t = text[i:i+16]
        if i+16 > l:
            t = t.ljust(16)
        temp = encrypt_text(rkList=rks, text=t)
        print('Cipher', temp)
        encrypted_text = encrypted_text + temp

    return encrypted_text

def decrypt_image(encrypted_text: str, file_name: str, rks: list):
    l = len(encrypted_text)
    den = ''
    for i in range(0, l-1, 32):
        temp = decrypt_text(rkList=rks, cipherText=encrypted_text[i:i+32])
        den = den + temp
    decodeit = open(file_name, 'wb') 
    decodeit.write(base64.b64decode((den)))



key = "Thats my Kung Fuhgjhghg"

rks = init(key=key)

input_filename = "input.txt"
output_filename = "output.txt"

if  input_filename.endswith('.png') or input_filename.endswith('.jpg') or input_filename.endswith('.jpeg'):
    en_text = encrypt_image(file_name=input_filename, rks=rks)
    decrypt_image(encrypted_text=en_text, file_name=output_filename, rks=rks)
else:
    en_text = encrypt(f_name=input_filename, rks=rks)
    decrypt(encrypted_text=en_text, file_name=output_filename, rks=rks)
