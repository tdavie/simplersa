# RSA Proof of Concept
# NOT CRYPTOGRAPHICALLY SECURE
import sys
import argparse
import math
import secrets
import random

# read key file
# return values separated by newline as a tuple of ints
def read_key(key_file):
    with key_file as f:
        return tuple(map(int, f))

def decrypt(ciphertext, priv_key):
    plaintext = ""
    # split ciphertext into space-delineated 'words' representing plaintext chars
    for word in ciphertext.split():
        plaintext += chr(int(word)**priv_key[1] % priv_key[0])
    return plaintext

# very basic ecb mode implementation, encrypts each char sequentially
def encrypt(plaintext, pub_key):
    ciphertext = ""
    for line in plaintext:
        for char in line:
            ciphertext += str((ord(char)**pub_key[1]) % pub_key[0])
            # add space between encrypted chars
            ciphertext += ' '
    return ciphertext

# PLACEHOLDER
def keygen():
    # generate two primes similar size
    # t = 40 per justification below
    p1 = gen_prime(64, 40)
    p2 = gen_prime(64, 40)

    n = p1*p2

    # pick small odd e
    # 65537 is the standard
    e = 65537   

	# calculate private exponent
	# d = modular multiplicative inverse of e modulo lambda(n)
    d = pow(e, -1, math.lcm((p1-1),(p2-1)))

    print(f"Private key: {n}, {d}")
    print(f"Public key: {n}, {e}")

# random prime generator
# miller-rabin method simpler
# consider gordon's algo for strong prime generation
# k = target no. bits (i.e. 2^k)
# t = security parameter
def gen_prime(k, t):
	while True:
		# generate random odd of ~k bits
		n = 2*secrets.randbits(int(k/2))+1
		if miller_rabin(n, t):
			return n

""" Return boolean primality of n

Miller-rabin primality test
This implementation courtesy https://gist.github.com/Ayrx/5884790
"""
def miller_rabin(n, k):

    # Implementation uses the Miller-Rabin Primality Test
    # The optimal number of rounds for this test is 40
    # See http://stackoverflow.com/questions/6325576/how-many-iterations-of-rabin-miller-should-i-use-for-cryptographic-safe-primes
    # for justification

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True
    

if __name__ == "__main__":
    print("This is a toy implementation of RSA and not secure!")
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_text', type=str, help="Input string to be encrypted/decrypted")
    parser.add_argument('-pub', '--pub_key', type=argparse.FileType('r'), help="Public key file")
    parser.add_argument('-priv', '--priv_key', type=argparse.FileType('r'), help="Private key file")
    parser.add_argument('-e', action="store_true", default=False)
    parser.add_argument('-d', action="store_true", default=False)
    parser.add_argument('-k', action="store_true", default=False)
    args = parser.parse_args()


    if args.k:
        keygen()
    elif args.e:
        with args.pub_key as pub_key:
            print(encrypt(args.input_text, read_key(pub_key)))
    elif (args.d):
        with args.priv_key as priv_key:
            print(decrypt(args.input_text, read_key(priv_key)))
