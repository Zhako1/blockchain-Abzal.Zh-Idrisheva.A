import random

class AsymmetricEncryption:
    def __init__(self):
        self.p = self.generate_prime()
        self.q = self.generate_prime()
        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)
        self.e = self.choose_e(self.phi)
        self.d = self.mod_inverse(self.e, self.phi)

    def generate_prime(self):
        # Генерация простого числа 
        return random.randint(100, 200)

    def choose_e(self, phi):
        e = 3
        while e < phi:
            if self.gcd(e, phi) == 1:
                return e
            e += 2

    def gcd(self, a, b):
        while b:
            a, b = b, a % b
        return a

    def mod_inverse(self, a, m):
        m0, x0, x1 = m, 0, 1
        if m == 1:
            return 0
        while a > 1:
            q = a // m
            m, a = a % m, m
            x0, x1 = x1 - q * x0, x0
        if x1 < 0:
            x1 += m0
        return x1

    def encrypt(self, plaintext):
        return pow(plaintext, self.e, self.n)

    def decrypt(self, ciphertext):
        return pow(ciphertext, self.d, self.n)

    def get_public_key(self):
        return (self.e, self.n)

    def get_private_key(self):
        return (self.d, self.n)
