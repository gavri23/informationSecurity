import argparse


def join_list_to_string(list_chars):
    return ''.join(str(c) for c in list_chars).replace(" ", "")


def join_list_to_string_with_white_spaces(list_chars):
    return ''.join(str(c) for c in list_chars)


def xorTxt(pTxt, iV):
    return [chr(ord(a) ^ ord(b)) for a, b in zip(pTxt, iV)]


def buildkeyMap(key):
    return {'a': key[0], 'b': key[1], 'c': key[2], 'd': key[3], 'e': key[4], 'f': key[5], 'g': key[6], 'h': key[7]}


def buildKeyMap(keys, values):
    dict_key = {}
    if len(keys) != len(values):
        raise "Can't build encryption key! sizes of the keys and values not equal!"
    for i in range(len(keys)):
        dict_key.update({keys[i]: values[i]})


def encryption(pTxt, key, iV):
    res = xorTxt(pTxt, iV)
    encryptListChars = []
    for char in res:
        if char in key.keys():
            encryptListChars.append(key[char])
        else:
            encryptListChars.append(char)

    encrypt = join_list_to_string(encryptListChars)
    return encrypt


def get_keys_from_value(d, val):
    a = [k for k, v in d.items() if v.lower() == val.lower()][0]
    return [k for k, v in d.items() if v.lower() == val.lower()][0]


def decryption(encryption_res, key, iV):
    decrypt_with_key = []
    for char in encryption_res:
        if char in key.values():
            decrypt_with_key.append(get_keys_from_value(key, char))
        else:
            decrypt_with_key.append(char)
    temp_decryption = join_list_to_string(decrypt_with_key)
    decryption_chars = xorTxt(iV, temp_decryption)
    if ' ' in decryption_chars:
        decryption = join_list_to_string_with_white_spaces(decryption_chars)
    else:
        decryption = join_list_to_string(decryption_chars)

    return decryption


def buildKey(file_name):
    with open(file_name) as keyC:
        string_key = keyC.read()
        split_key_and_val = string_key.split('\n')
        dictKey = {}
        for s in split_key_and_val:
            key_and_val = s.split(' ')
            dictKey.update({key_and_val[0]: key_and_val[1]})
    return dictKey


if __name__ == '__main__':
    # give 3 parameters - plain_text, key, iv
    parser = argparse.ArgumentParser()
    parser.add_argument('--plain_text', type=str, required=True)
    parser.add_argument('--iv_vector', type=str, required=True)
    parser.add_argument('--key', type=str, required=True)
    args = parser.parse_args()
    with open(args.plain_text) as plainTxt:
        pTxt = plainTxt.read()

    key = buildKey(args.key)

    with open(args.iv_vector) as iv:
        iV = iv.read()

    print(f"Plain text before encryption : {pTxt}")
    encryption_res = encryption(pTxt, key, iV)
    print(f"Encryption result is : {encryption_res}")

    decryption_res = decryption(encryption_res, key, iV)
    print(f"Decryption result is : {decryption_res}")
