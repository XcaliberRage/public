from nltk.tokenize import sent_tokenize


def lines(a, b):
    """Return lines in both a and b"""

    # Take both a and b and generate a list each using split, we use \n as the delimiter
    lineSetA = unDuple(a.split('\n'))
    lineSetB = unDuple(b.split('\n'))

    return matchMyLists(lineSetA, lineSetB)


def sentences(a, b):
    """Return sentences in both a and b"""

    sentenceSetA = unDuple(sent_tokenize(a, language='english'))
    sentenceSetB = unDuple(sent_tokenize(b, language='english'))

    return matchMyLists(sentenceSetA, sentenceSetB)


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    aLen = len(a)
    bLen = len(b)

    subStringsA = unDuple([a[i:i+n] for i in range(aLen) if i+n <= aLen])
    subStringsB = unDuple([b[i:i+n] for i in range(bLen) if i+n <= bLen])

    return matchMyLists(subStringsA, subStringsB)


# This helper function sieves out duplicates
# By turning the list into a dictionary, we automatically eliminate dupes due to type constraints
# Then we just return the dictionary back as a list
def unDuple(x):
    return list(dict.fromkeys(x))


# This helper function is where I take two lists and return a single list consisting only elements found in both
def matchMyLists(listA, listB):
    return [item for item in listA if item in listB]