import cbc
import random
import string


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    print("Random string of length", length, "is:", result_str)
    return result_str


def encrypt_text(text):
    key = cbc.buildKey("keys/keyPartC.txt")

    ivVector = get_random_string(len(text))
    with open("IvVectors/randomIvVector.txt", "w") as iv:
        iv.write(ivVector)

    encrypt = cbc.encryption(text, key, ivVector)

    with open("encrypt/encryptTextPartB.txt", "w") as en:
        en.write(encrypt)

    with open("encrypt/check_decryption.txt", "w") as de:
        de.write(cbc.decryption(encrypt, key, ivVector))


if __name__ == '__main__':
    with open("plainTexts/plainTextPartB.txt") as plainTxt:
        pTxt = plainTxt.read()

    encrypt_text(pTxt)
