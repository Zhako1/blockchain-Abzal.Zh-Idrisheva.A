def manual_hash(data):
    hash_value = 0
    for char in data:
        hash_value = (hash_value * 31 + ord(char)) % (2 ** 32)

    hex_hash = hex(hash_value)[2:]
    return hex(hash_value)[2:].zfill(8)

