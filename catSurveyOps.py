# This file takes care off most of the helper functions and operational features, essentially keeping the "netcode" seperate from the "hardcode"

import csv
from collections import OrderedDict
from cat import Cat

surveyFile = 'survey.csv'

# Write the Cat class as a dictionary to a csv file
def writeCSV(thisCat, fieldnames):

    with open(surveyFile, 'a', newline='') as csvfile_writing:
        # First check if this cat already exists

        writer = csv.DictWriter(csvfile_writing, fieldnames=fieldnames, delimiter=',')

        if csvfile_writing.tell() == 0:
            writer.writeheader()

        # Only add this cat if it doesn't already exist
        if not checkCSV(thisCat, fieldnames):
            writer.writerow({
                'name': thisCat.name,
                'breed': thisCat.breed,
                'gender': thisCat.gender,
                'neutered': thisCat.neutered,
                'age_group': thisCat.ageGroup,
                'age_year': thisCat.years,
                'age_month': thisCat.months,
                'age_unknown': thisCat.ageUnknown
            })


# Load the csv file of cats into a dictionary of Cats, each with a unique integer key.
# Return a tuple containing boolean success indicator and the loaded(or not) dictionary
def loadCSV(fieldnames):

    output = {}

    try:
        with open(surveyFile) as csvfile:


            catNo = 0

            reader = csv.DictReader(csvfile)

            # Iterate over each row (pulling it as an Ordered Dictionary) and add a new Cat element to the output dictionary
            for row in reader:
                # I use catNo as a key to avoid issues of cats with identical names
                output[catNo] = Cat(row['name'],
                    row['breed'],
                    row['gender'],
                    row['neutered'],
                    row['age_group'],
                    row['age_year'],
                    row['age_month'],
                    row['age_unknown'])
                catNo += 1

            return True, output

    except FileNotFoundError:
        return False, output


# Search the csv file for an identical copy of this cat
def checkCSV(thisCat, fieldnames):

    catVals = vars(thisCat)
    catList = [str(atts) for cat, atts in catVals.items()]

    try:
        with open(surveyFile) as csvfile:

            reader = csv.reader(csvfile)

            # If all values in a row are identical to this cat, return True
            for row in reader:
                print("Reading: ", row)
                if sorted(catList) == sorted(row):
                    print(f"Found: {catList} ({catVals})")
                    return True

            # Otherwise false
            return False

    except ValueError:
        return True


# Basic C implementation of a switch/case for the ageGroup category
def switcher(argument):
    return {
        'kitten': [0, 0],
        'adult': [0, 3],
        'prime': [3, 6],
        'mature': [7, 10],
        'senior': [11, 14],
        'geriatric': [15, 50]
        }[argument]


# Load list of breeds from CatBreeds.txt
def getBreeds():

    breeds = []
    errors = []

    try:
        with open('CatBreeds.txt', 'r') as file:
            for line in file:
                breeds.append(line.strip('\n'))
    except FileNotFoundError:
        errors.append("Error loading 'CatBreeds.txt'")
        return True, breeds, errors

    return False, breeds, errors


# Validate all elements of the Cat form in case JS gets bypassed
def validateThisCat(thisCat):

    nofile, breeds, errors = getBreeds()

    # Validation needs:
    # A name
    if not thisCat.name:
        errors.append("You didn't provide a name for your Cat!")

    # A chosen cat Breed
    if not nofile:
        if not thisCat.breed:
            errors.append("You didn't select a breed or Unknown'")
        elif not thisCat.breed in breeds:
            errors.append("Is this list of breeds really not extensive enough for you?")

    # A gender (or unkown)
    if not thisCat.gender:
        errors.append("You didn't select a gender")

    # A valid age Group
    ageGroups = ['kitten', 'adult', 'prime', 'mature', 'senior', 'geriatric']
    if not thisCat.ageGroup in ageGroups:
        errors.append(thisCat.ageGroup + " is not a valid age group, please choose one provided")

    # An age within range OR Age unknown checked (BUT NOT BOTH)
    if not thisCat.ageUnknown:
        if not (thisCat.years or thisCat.months):
            errors.append("You didn't provide a proper age in numerals or check 'Age Unknown'")
        else:
            try:
                givenYears = int(thisCat.years)
                givenMonths = int(thisCat.months)

                minVal, maxVal = switcher(thisCat.ageGroup)

                maxMonth = 12 if not thisCat.ageGroup == 'kitten' else 6
                minMonth = 6 if thisCat.ageGroup == 'adult' and givenYears == 0 else 0

                if not (minVal <= givenYears and (maxVal == 50 or givenYears <= maxVal)) and (minMonth <= givenMonths <= maxMonth):
                    errors.append("Given age is out of Age Group bounds")

            except ValueError:
                errors.append("You put something weird in the Year or Month box")


    validate = True if not errors else False

    return validate, errors