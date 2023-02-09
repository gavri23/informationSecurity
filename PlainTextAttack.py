import string

import cbc
import utility
import CipherTextAttack

list_of_all_the_letters = list(string.ascii_letters)


# with open("keyPartC.txt") as keyC:
#     string_key = keyC.read()
#     split_key_and_val = string_key.split('\n')
#     dictKey = {}
#     for s in split_key_and_val:
#         key_and_val = s.split(' ')
#         dictKey.update({key_and_val[0]: key_and_val[1]})
#
# with open("randomIvVector.txt") as iv_vector:
#     iv = iv_vector.read()
#
# with open("plainTextPartB.txt") as plainTxt:
#     pTxt = plainTxt.read()
#
# print(f"{pTxt}\n")
# encrypt = cbc.encryption(pTxt, dictKey, iv)
# with open("wholeEncryptionForPartC.txt",'w') as whole:
#     whole.write(encrypt)
# decrypt = cbc.decryption(encrypt, dictKey, iv)
# print(f"{decrypt}\n")
# print(f"{iv[35:108]}")
# with open("partTextForPartC.txt") as part:
#     p = part.read()
#     part_iv = iv[35:108]
#     encrypt2 = cbc.encryption(p, dictKey, part_iv)
#     decrypt2 = cbc.decryption(encrypt2, dictKey, part_iv)
#     print(decrypt2)

# with open("partTextForPartC.txt") as plainTxt:
#     pTxt = plainTxt.read()
#
# with open("randomIvVector.txt") as iv_vector:
#     iv = iv_vector.read()
#
# with open("partEncryptForPartC.txt",'w') as part:
#     a = encrypt2 = cbc.encryption(pTxt, dictKey, iv)
#     part.write(a)


def get_part_key(xored_text, part_encrypt_text):
    key = {}
    print(len(xored_text))
    print(len(part_encrypt_text))
    for char_in_xored, char_in_encrypt in zip(xored_text, part_encrypt_text):
        if char_in_xored != char_in_encrypt:
            key.update({char_in_xored: char_in_encrypt})
    return key


def cipher_text_attack(whole_encrypt_text, all_possible_rest_of_key, part_key, iv_vec):
    maxCounterWords = 0
    final_key = {}
    for possible_part_key in all_possible_rest_of_key:
        temp_key = part_key.update(possible_part_key)
        decryption = cbc.decryption(whole_encrypt_text, temp_key, iv_vec).split(' ')
        counterWords = 0
        for word in decryption:
            if '\n' in word or '\x0b' in word:  # it means there is an end line character that connects to words together
                two_words = ' '.join(word.split())
                number_of_valid_words = CipherTextAttack.check_valid_words(two_words)
                counterWords += number_of_valid_words
            elif CipherTextAttack.english_dictionary.check(word):
                counterWords += 1
            else:
                pass
        if counterWords > maxCounterWords:  # got more english words from the possible key
            maxCounterWords = counterWords
            final_key = temp_key

    return final_key


def plain_text_attack(whole_encrypt_text, part_encrypt_text, part_decrypt_text_iv, iv_vec):
    part_iv = iv_vec[35:108]
    xored_text = cbc.xorTxt(part_decrypt_text_iv, part_iv)
    part_key = get_part_key(xored_text, part_encrypt_text)
    letters_not_in_keys = []
    letters_not_in_values = []
    for letter in list_of_all_the_letters:
        if letter not in part_key.keys():  # if letter not in the dict_key at all neither as a key or a value
            letters_not_in_keys.append(letter)
        if letter not in part_key.values():
            letters_not_in_values.append(letter)
    value_letters = cbc.join_list_to_string(letters_not_in_values)
    possible_values = CipherTextAttack.get_all_possible_keys(value_letters)
    all_possible_rest_of_key = [cbc.buildkeyMap(letters_not_in_keys, possible_value) for possible_value in
                                possible_values]
    best_decryption = cipher_text_attack(whole_encrypt_text, all_possible_rest_of_key, part_key, iv_vec)
    print(best_decryption)
    return best_decryption


if __name__ == "__main__":
    with open("encrypt/wholeEncryptionForPartC.txt") as whole_encrypt:
        whole_encrypt_text = whole_encrypt.read()

    with open("encrypt/partEncryptForPartC.txt") as part_encrypt:
        part_encrypt_text = part_encrypt.read()

    with open("plainTexts/partTextForPartC.txt") as part_text:
        part_decrypt_text = part_text.read()

    with open("IvVectors/randomIvVector.txt") as iv:
        iv_vector = iv.read()

    key = plain_text_attack(whole_encrypt_text, part_encrypt_text, part_decrypt_text, iv_vector)
    a = 5
