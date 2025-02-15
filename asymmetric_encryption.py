import random

class AsymmetricEncryption:
    def __init__(self, wallet_type='hot'):
        self.wallet_type = wallet_type
        self.p = self.generate_prime()
        self.q = self.generate_prime()
        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)
        self.e = 1  # Используем стандартное e
        self.d = self.mod_inverse(self.e, self.phi)

        print(f"[RSA] Сгенерированы ключи: p={self.p}, q={self.q}, n={self.n}, e={self.e}, d={self.d}")

    def generate_prime(self):
        while True:
            num = random.randint(100, 200)
            if self.is_prime(num):
                return num

    def is_prime(self, num):
        if num < 2:
            return False
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                return False
        return True

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
        ciphertext = pow(plaintext, self.e, self.n)
        print(f"[RSA] Зашифровано: {plaintext} -> {ciphertext}")
        return ciphertext

    def decrypt(self, ciphertext):
        decrypted_value = pow(ciphertext, self.d, self.n)
        print(f"[RSA] Расшифровано: {ciphertext} -> {decrypted_value}")
        return decrypted_value

    def get_public_key(self):
        return (self.e, self.n)

    def get_private_key(self):
        return (self.d, self.n)


