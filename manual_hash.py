def manual_hash(data):
    hash_value = 0
    for char in data:
        hash_value = (hash_value * 31 + ord(char)) % (2**32)
    return hash_value

if __name__ == "__main__":
    print(manual_hash("Мысалы"))

