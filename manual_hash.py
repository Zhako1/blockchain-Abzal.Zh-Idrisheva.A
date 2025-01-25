def manual_hash(data):
    hash_value = 0
    for char in data:
        hash_value = (hash_value * 31 + ord(char)) % (2 ** 32)

    hex_hash = hex(hash_value)[2:]
    return hex_hash.zfill(8)


if __name__ == "__main__":
    print(manual_hash("1"))
    print(manual_hash("Мысалы"))
