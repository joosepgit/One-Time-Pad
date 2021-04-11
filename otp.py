#!/usr/bin/env python3
import os
import sys


def bn(b):
    # b - bytes to encode as integer
    i = b[0]
    for idx in range(1, len(b)):
        i = (i << 8) | b[idx]
    return i


def nb(i, length):
    # i - integer to encode as bytes
    # length - specifies in how many bytes the number should be encoded
    result = []
    for j in range(0, length):
        result.append(i >> (j * 8) & 0xff)
    result.reverse()
    return bytes(result)


def encrypt(pfile, kfile, cfile):
    with open(pfile, 'rb') as f:
        b = f.read()
    print(b)
    byteamount = len(b)
    plain_integer = bn(b)
    key_integer = bn(os.urandom(byteamount))
    cipher_integer = plain_integer ^ key_integer
    cipher_bytes = nb(cipher_integer, (len(bin(cipher_integer)) + 7) // 8)
    with open(kfile, 'w') as f:
        f.write(str(key_integer))
    with open(cfile, 'wb') as f:
        f.write(cipher_bytes)
    pass


def decrypt(cfile, kfile, pfile):
    with open(cfile, 'rb') as f:
        cipher_bytes = f.read()
    with open(kfile, 'r') as f:
        key_integer = int(f.read())
    cipher_integer = bn(cipher_bytes)
    plain_integer = cipher_integer ^ key_integer
    plain_bytes = nb(plain_integer, (len(bin(plain_integer)) + 7) // 8)
    with open(pfile, 'wb') as f:
        f.write(plain_bytes)
    pass


def usage():
    print("Usage:")
    print("encrypt <plaintext file> <output key file> <ciphertext output file>")
    print("decrypt <ciphertext file> <key file> <plaintext output file>")
    sys.exit(1)


if len(sys.argv) != 5:
    usage()
elif sys.argv[1] == 'encrypt':
    encrypt(sys.argv[2], sys.argv[3], sys.argv[4])
elif sys.argv[1] == 'decrypt':
    decrypt(sys.argv[2], sys.argv[3], sys.argv[4])
else:
    usage()
