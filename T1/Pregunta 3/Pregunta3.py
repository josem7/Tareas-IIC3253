#!/usr/bin/env python
# coding: utf-8

# Importamos las librerías que vamos a utilizar

# In[25]:


import pandas as pd


# Re definimos la función de la pregunta 2 con pequeños cambios para definir a0, b0, c0, d0 y ademas definimos las funciones dadas en el notebook de OTP que nos serán útiles

# In[508]:


from bitarray import bitarray
from bitarray.util import int2ba
from math import sin, floor
import struct

def leftrotate (x, c):
    return (x << c) | (x >> (32-c));

def generate_k():
    k = []
    for i in range(64):
        k.append(floor(pow(2, 32) * abs(sin(i + 1))))
    return k

def generate_s():
    s = [7, 12, 17, 22] * 4
    s += [5,  9, 14, 20] * 4
    s += [4, 11, 16, 23] * 4
    s += [6, 10, 15, 21] * 4
    return s
'''
Igual a la función usada en la pregunta 2 pero con cambios pequeños para definir a0, b0, c0, d0
'''  
def custom_md5 ( m : str , h0 : int ) -> str :

    a0 = h0 % (pow(2,32))
    b0 = 0xefcdab89
    c0 = 0x98badcfe
    d0 = 0x10325476 
    
    my_bit_array = bitarray(endian="little")
    my_bit_array.frombytes(m.encode('utf-8'))
    length_bits = len(my_bit_array) %  pow(2, 64)
    my_bit_array.append(0)
    my_bit_array.append(0)
    my_bit_array.append(0)
    my_bit_array.append(0)
    my_bit_array.append(0)
    my_bit_array.append(0)
    my_bit_array.append(0)
    my_bit_array.append(1)
    while len(my_bit_array) % 512 != 448:
        my_bit_array.append(0)
    
    length_bits_array = bitarray(endian="little")
    length_bits_array.frombytes(struct.pack('<Q', length_bits))
    my_bit_array.extend(length_bits_array)
    
    K = generate_k()
    s = generate_s()
    for chunk in range(len(my_bit_array) // 512 ):
        M_bit = []
        for j in range(16):
            M_bit.append(my_bit_array[chunk * 512 + j * 32: chunk * 512 + (j + 1)* 32 ])
        M = []
        for word in M_bit:
            M.append(struct.unpack("<L", word)[0])
        A = a0
        B = b0
        C = c0
        D = d0
        for i in range(64):
            if (0 <= i <= 15):
                F = (B & C) | ((~ B) & D)
                g = i
            elif 16 <= i <= 31:
                F = (D & B) | ((~ D) & C)
                g = (5*i + 1) % 16
            elif 32 <= i <= 47:
                F = B ^ C ^ D
                g = (3*i + 5) % 16
            elif 48 <= i <= 63:
                F = C ^ (B | (~ D))
                g = (7*i) % 16
            F = (F + A + K[i] + M[g]) % pow(2, 32)
            A = D
            D = C
            C = B
            B = (B + leftrotate(F, s[i])) % pow(2, 32)
        a0 = (a0 + A) % pow(2, 32)
        b0 = (b0 + B) % pow(2, 32)
        c0 = (c0 + C) % pow(2, 32)
        d0 = (d0 + D) % pow(2, 32)
        
    a0 = struct.unpack("<I", struct.pack(">I", a0))[0]
    b0 = struct.unpack("<I", struct.pack(">I", b0))[0]
    c0 = struct.unpack("<I", struct.pack(">I", c0))[0]
    d0 = struct.unpack("<I", struct.pack(">I", d0))[0]
    
    return f"{format(a0, '08x')}{format(b0, '08x')}{format(c0, '08x')}{format(d0, '08x')}"

def _check_strings(*args):
    for arg in args:
        if not isinstance(arg, str):
            raise AttributeError("Expected a string")


def xor(k, m):
    _check_strings(k, m)
    result = ""
    for i in range(len(m)):
        result += chr((ord(k[i % len(k)]) ^ ord(m[i])) % 255)

    return result


def as_binary_strings(string):
    _check_strings(string)
    return [bin(n)[2:].zfill(8) for n in as_integers(string)]


def as_binary_string(string):
    _check_strings(string)
    return "".join(as_binary_strings(string))


def as_integers(string):
    _check_strings(string)
    return [ord(c) for c in string]


def print_as_binary(*args):
    _check_strings(*args)
    result = ""
    for a in args:
        result += as_binary_string(a) + "\n"
    print(result[:-1])
 


# Importamos los datos a un data frame y luego los pasamos a un diccionario con llave = indice y valor = mensaje. Hacemos esto para que sea más rápido encontrar los mensajes!

# In[509]:


df = pd.read_csv("mensajes_pregunta_3/mensajes_pregunta_3.csv", header=None, names=["indice", "mensajes"])
msj_dict = dict(zip(df.indice, df.mensajes))
messages = []
count = 0


# Creamos un loop que corre hasta que no se encuentran más mensajes. (Cuando la llave del diccionario no existe).
# Esto nos deja con una lista de 200 mensajes, cada uno de largo 10.

# In[510]:


while msj_dict.get(custom_md5("jndominguez@uc.cl", 17637449 * 100 + count)):
    messages.append(str(msj_dict.get(custom_md5("jndominguez@uc.cl", 17637449 * 100 + count))))
    count+=1


# Definimos varias funciones útiles:
# 
# bits2a: sacada de https://stackoverflow.com/questions/9916334/bits-to-string-python
# nos ayuda a pasar de binario a caracteres.
# 
# probable_space_count_vector: igual a la función utilizada en clases encuentra la probabilidad de que haya un espacio en el lugar.
# 
# 
# max_index: es igual a la función definida en clases, dada una lista encuentra los indices máximos.
# 
# 
# count_letters: es una función para contar cuantas letras minúsculas hay en un mensaje.
# 
# 
# find_1_probable_key: Dada una lista de mensajes encriptados (todos los mensajes) encuentra la llave más probable entre start y finish. Similar a las funciones utilizadas en clases.
# 
# find_msj: Esta función encuentra los mensajes, parte con 15 mensajes y encuentra la llave más probable pero si el siguente mensaje tiene más de 5 letras minúsculas utilizando la llave lo agrega y re calcula la llave (diremos que la llave probablemente funcionó para ese mensaje). Luego retorna los mensajes decriptados con esa llave y la última posición donde se encontró un mensaje que funcionaba con la llave.
# 
# break_random_otp: Recibe los mensajes encriptados y corre la función find_msj hasta que se acaban los mensajes. Retorna una lista con los mensajes decriptados con cada llave, el largo de esta lista son las llaves.

# In[545]:


def bits2a(b):
    return ''.join(chr(int(''.join(x), 2)) for x in zip(*[iter(b)]*8))

def probable_space_count_vector(cyphertext, enc_messages):
    length = len(cyphertext)
    counts = [0] * length
    for c in enc_messages:
        messages_xor = xor(c, cyphertext)
        messages_xor_ints = as_integers(messages_xor)
        for i in range(length):
            if messages_xor_ints[i] > 64:
                counts[i] += 1
    return [round(c / len(enc_messages), 4) for c in counts]

def max_index(i, l):
    result = 0
    max_value = 0
    for j in range(len(l)):
        if l[j][i] > max_value:
            result = j
            max_value = l[j][i]
    return result

def count_letters(msg):
    msg_inter = as_integers(msg)
    count = 0
    for letter in msg_inter:
        if 97 <= letter <= 122:
            count += 1
    return count

def find_1_probable_key(enc_messages, start, finish):
    enc_messages2 = enc_messages[start:finish]
    probable_vectors = [probable_space_count_vector(c, enc_messages2) for c in enc_messages2]
    max_indexes = [max_index(i, probable_vectors) for i in range(len(enc_messages2[0]))]
    enc_spaces = "" 
    for index, value in enumerate(max_indexes):
        enc_spaces += enc_messages2[value][index]
    probable_key = xor(enc_spaces, " " * len(enc_spaces))
    return probable_key
    
def find_msj(enc_messages, i):
    start = i
    finish = i + 15
    next_letter = True
    while next_letter:
        if finish > len(enc_messages) - 15:
            finish = len(enc_messages) - 1
        key = find_1_probable_key(enc_messages, start, finish)
        next_letter = False
        if finish + 1 < 200:
            if count_letters(xor(key, enc_messages[finish + 1])) >= 5:
                finish += 1
                next_letter = True
    msj = ""
    enc_messages2 = enc_messages[start:finish + 1]
    for msg in enc_messages2:
        msj += xor(key, msg)
    return msj, finish

def break_random_otp( encrypted_messages : [ str ] ) -> [ str ] :    
    enc_messages = [bits2a(msj) for msj in encrypted_messages]
    start = 0
    dec_msj = []
    while start < len(enc_messages) - 15:
        msj, start = find_msj(enc_messages, start)
        start += 1
        dec_msj.append(msj)
    return dec_msj


# Corremos la función con los mensajes e imprimimos el mensaje final decriptado. Casi todo el mensaje está bien, se puede ver que es un mensaje del libro 1984 de George Orwell (Muy buen libro! PD: Si les gustó ese libro recomiendo Brave New World de Aldous Huxley)

# In[546]:


result = break_random_otp(messages)
for m in result:
    print(m)


# In[ ]:




