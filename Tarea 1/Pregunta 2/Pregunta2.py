#!/usr/bin/env python
# coding: utf-8

# ## Pregunta 2
# código basado en:
# 
# https://en.wikipedia.org/wiki/MD5
# 
# https://github.com/timvandermeij/md5.py/blob/master/md5.py
# 
# https://www.ietf.org/rfc/rfc1321.txt
# 
# Primero definimos 3 funciones que nos serán útil
# 
# #### leftrotate: 
# Esta es una función que rota a la izquierda similar a la definida en el pseudo código de Wikipedia.
# #### generate_s: 
# Esta función genera la lista s que define cuanto se rota cada turno.
# #### generate_k:
# Esta función genera la lista k.
# 
# ### función principal:
# Primero decomponemos el h0 en a0, b0, c0, d0.
# 
# Luego, generamos un bit array en little endian y pasamos el mensaje de UTF-8 a bits, calculamos el largo original del mensaje (se usará más tarde) y agregamos 1 al final de este (1 en byte). Luego, se agregan 0s hasta que el largo mod 512 sea 448. Esto es que está a 64 bits de ser divisible por 512. Por último, le agregamos el largo original del mensaje en little endian y de largo 64 bits. Esto deja al mensaje divisible en 512.
# 
# Generamos el k y el s que se utilizarán en el loop. Dividimos el mensaje en trozos de 512 bits como vimos anteriormente el mensaje siempre será divisible por 512. Lo siguiente se corre para cada trozo de 512 bits.
# 
# generamos las variables auxiliares:
# 
# A = a0
# 
# B = b0
# 
# C = c0
# 
# D = d0
# 
# Estos trozos luego los dividimos en 16 bloques de 32 bits. Definimos 4 funciones que son:
# 
# F = (B & C) | ((~ B) & D)
# 
# F = (D & B) | ((~ D) & C)
# 
# F = B ^ C ^ D
# 
# F = C ^ (B | (~ D))
# 
# corremos un loop 64 veces cada 16 veces corre una función distinta y define un g distinto. 
# 
# ##### 0-15:
# F = (B & C) | ((~ B) & D)
# 
# g = i
# 
# ##### 16-31:
# F = (D & B) | ((~ D) & C)
# 
# g = (5*i + 1) % 16
# 
# ##### 32-47:
# F = B ^ C ^ D
# 
# g = (3*i + 5) % 16
# 
# ##### 48-63:
# F = C ^ (B | (~ D))
# 
# g = (7*i) % 16
# 
# ##### MD5 define a como:
# 
# A = B + ((A + F + M[g] + K[i]) <<< s)
# 
# Esto es lo mismo que como el pseudo código de Wikipedia lo define, notar que el F cambia dependiendo de la iteración que estemos en el loop:
# 
# ##### Definimos F como:
# F = (F + A + K[i] + M[g]) % pow(2, 32)
# ##### y A como:
# (B + leftrotate(F, s[i])) % pow(2, 32)
# 
# ##### Solamente que MD5 rota A, B, C, D, esto es, B = A, C = B, D = C, A = D por lo que podemos definir directamente B como:
# B = (B + leftrotate(F, s[i])) % pow(2, 32)
# 
# 
# A = D
# 
# D = C
# 
# C = B
# 
# B = (B + leftrotate(F, s[i])) % pow(2, 32)
# 
# 
# Al salir del loop sumamos estos nuevos valores de A, B, C, D a los originales a0, b0, c0, d0 y los guardamos en a0, b0, c0 y d0 respectivamente. 
# 
# a0 = (a0 + A) % pow(2, 32)
# 
# b0 = (b0 + B) % pow(2, 32)
# 
# c0 = (c0 + C) % pow(2, 32)
# 
# d0 = (d0 + D) % pow(2, 32)
# 
# Por último, pasamos el a0, b0, d0, c0 a little endian y entregamos el output como se pide .
# 
# ##### Nota:
# - para las sumas usamos mod(pow(2, 32)) para que estas no se pasen de los 32 bits.
# - El h0 que define los párametros originales de MD5 es: 137269462086865085541390238039692956790

# In[14]:


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
Argumentos :
m : str - mensaje
h0 : int - constante inicial H_0

Retorna :
str - hash MD5 correcto del mensaje en formato hexadecimal
'''  
def custom_md5 ( m : str , h0 : int ) -> str :

    
    d0 = h0 & 0xffffffff
    c0 = (h0 >> 32) & 0xffffffff
    b0 = (h0 >> 64) & 0xffffffff
    a0 = (h0 >> 96) & 0xffffffff   
    
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
    


# In[18]:


custom_md5("The quick brown fox jumps over the lazy dog", 137269462086865085541390238039692956790)


# In[19]:


import hashlib
print(hashlib.md5("The quick brown fox jumps over the lazy dog".encode('utf-8')).hexdigest())


# In[ ]:





# In[ ]:




