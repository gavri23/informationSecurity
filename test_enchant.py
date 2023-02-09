import enchant

english_dictionary = enchant.Dict("en_US")

with open("encrypt/check_decryption.txt") as dec:
    decrypt = dec.read()


def check_valid_words(two_words):
    if english_dictionary.check(two_words[0]) and english_dictionary.check(two_words[1]):
        return 2
    elif english_dictionary.check(two_words[0]) or english_dictionary.check(two_words[1]):
        return 1
    else:
        return 0


de = decrypt.split(' ')
counterWords = 0
for word in de:
    if '\n' in word:  # it means there is an end line character that connects to words together
        two_words = word.split('\n')
        number_of_valid_words = check_valid_words(two_words)
        counterWords += number_of_valid_words
        continue
    if english_dictionary.check(word):
        counterWords += 1
    else:
        pass
print(counterWords)