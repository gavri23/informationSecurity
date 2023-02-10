import cbc
import itertools
import enchant
import argparse
import re

english_dictionary = enchant.Dict("en_US")
keyLetters = "abcdefgh"


def get_all_possible_keys(key):
    keys = [''.join(p) for p in itertools.permutations(key)]
    return keys


def check_valid_words(two_words):
    if english_dictionary.check(two_words[0]) and english_dictionary.check(two_words[1]):
        return 2
    elif english_dictionary.check(two_words[0]) or english_dictionary.check(two_words[1]):
        return 1
    else:
        return 0


def get_key(encrypt_msg, iv):
    list_of_all_keys = get_all_possible_keys(keyLetters)
    listkeyMaps = [cbc.buildkeyMap(key) for key in list_of_all_keys]
    maxCounterWords = 0
    list_of_key_candidates = []
    for keyMap in listkeyMaps:
        # vals = keyMap.values()
        # string_key = str(vals)  # the values of each map is the key itself
        decrypt = cbc.decryption(encrypt_msg, keyMap, iv).split(' ')
        counterWords = 0
        for word in decrypt:
            if '\n' in word or '\x0b' in word:  # it means there is an end line character that connects to words together
                two_words = ' '.join(word.split())
                # two_words = word.replace('\x0b', '\n')
                # two_words = two_words.replace('\n', ' ')
                number_of_valid_words = check_valid_words(two_words)
                counterWords += number_of_valid_words
            elif english_dictionary.check(word):
                counterWords += 1
            else:
                pass
        maxCounterWords = max(maxCounterWords, counterWords)
        # TODO generate list of map of encryption_key : counterWords
    print(maxCounterWords)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--encrypt_text', type=str, required=True)
    parser.add_argument('--iv_vector', type=str, required=True)
    args = parser.parse_args()
    with open(args.iv_vector) as ivVector:
        iv = ivVector.read()

    with open(args.encrypt_text) as encrypt:
        encrypt_msg = encrypt.read()
        final_key = get_key(encrypt_msg, iv)
