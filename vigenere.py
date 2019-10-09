import cs50
import sys

#Globals
LOWERVAL = 97
CAPIVAL = 65
ALPHABET = 26

def main() :

    argc = len(sys.argv)

    # Verify given arguments (there is only one extra string and it is only letters)
    if len(sys.argv) == 2 and sys.argv[1].isalpha() :

        # Store each letter of the key in a list
        keyAlpha = list(sys.argv[1])
        keyLength = len(keyAlpha)
        key = []

        # Use the list to get the shiftKey (i.e. numerical value)
        for i in keyAlpha :
            uniVal = ord(i)
            key.append((uniVal - CAPIVAL) if i.isupper() else (uniVal - LOWERVAL))

        # Request the plaintext message
        plainText = cs50.get_string("Plaintext: ")

        # Execute functions to perform the cipher
        cipherText = encrypt(plainText, key, keyLength)

        # Output the cipher
        print("Ciphertext: ", cipherText)

    else :
        # If verification fails, exit the code and return an error
        print("Usage: python vigenere.py k")
        return 1


# Encrypt the plaintext using the given key
def encrypt(inputString, key, keyLength) :

    output = inputString

    stringLen = len(inputString)

    stringIndex = 0
    keyIndex = 0

    # Iterate across the length of the plainText
    while stringIndex < stringLen :

        # When we have iterated across the key, loop back to 0
        if keyIndex >= keyLength :
            keyIndex = 0

        # We do nothing to the item if it is not alphabetical
        if output[stringIndex].isalpha() :
            # Lets get the numeric value of the letter and remember its case
            rawVal = ord(output[stringIndex])
            isCap = True if output[stringIndex].isupper() else False
            charVal = (rawVal - CAPIVAL) if isCap else (rawVal - LOWERVAL)

            # Now modify the letter by the current key element
            rawCryptVal = (charVal + key[keyIndex]) % ALPHABET
            rawCryptVal += CAPIVAL if isCap else LOWERVAL
            charCryptVal = chr(rawCryptVal)

            stringShif = stringIndex + 1
            # Convert the value back into character form
            output = output[:stringIndex] + charCryptVal + output[stringShif:]

            # We used the key so we iterate
            keyIndex += 1

        # Now look at the next item in the plainText
        stringIndex += 1

    # Once we've finished iterating across the plainText, we can return that string
    return output


if __name__ == "__main__" :
    main()