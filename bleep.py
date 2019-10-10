from cs50 import get_string
import sys


def main():

    argc = len(sys.argv)
    arg1 = sys.argv[1]

    # Check that only one argument was given
    if argc == 2:

        # Attempt to open the given file
        dictionary = load_Dictionary(arg1)

        # Request a message and save each word (seperated by whitespace) in a list
        msgList = get_string("What message would you like to censor?\n").split()

        # Censor the message and return a complete string
        msgOut = censor(msgList, dictionary)

        print(msgOut)
        sys.exit(0)

    print("Usage: python bleep.py dictionary.txt")
    sys.exit(1)


# Attempts to load a given file and returns each word as a set element
def load_Dictionary(fileName):

    try:
        file = open(fileName, 'r')
    except OSError:
        print("Could not open ", fileName)
        sys.exit(1)

    # For each entry remove the whitespace and put it in a set element
    return {line.strip() for line in file}


# Cross checks a list of input words against a set of flagged words
# Replaces each character of the matched words in the list with *
# Outputs a compiled string of the updated list
def censor(userMsg, flagged):

    # For each element of the list run the censorWord helper function
    outputMsg = map(lambda word: censorWord(word, flagged), userMsg)

    return " ".join(outputMsg)


def censorWord(word, flagged):

    # Whatever word is given, check the list of flagged words
    # If the word is there, replace each character with *
    return "".join(["*" for char in word]) if word in flagged else word


if __name__ == "__main__":
    main()
