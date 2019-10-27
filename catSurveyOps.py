# This file takes care off most of the hlper functions and operational features, essentially keeping the "netcode" seperate from the "hardcode"

import csv
from collections import OrderedDict

surveyFile = 'survey.csv'

# We deal in cats so I made a cat
class Cat():

    def __init__(self, name, breed, gender, neutered, ageGroup, years, months, ageUnknown):
        self.name = name
        self.breed = breed
        self.gender = gender
        self.neutered = neutered
        self.ageGroup = ageGroup
        self.years = years
        self.months = months
        self.ageUnknown = ageUnknown

    def printCat(self):
        print("{}: {} - {} - Neutered: {} - {} ({}y{}m)".format(self.name,
            self.breed, self.gender, self.neutered, self.ageGroup, self.years, self.months))


# Write the Cat class as a dictionary to a csv file
def writeCSV(thisCat, fieldnames):

    with open(surveyFile, 'a', newline='') as csvfile_writing:
        # First check if this cat already exists

        writer = csv.DictWriter(csvfile_writing, fieldnames=fieldnames, delimiter=',')

        if csvfile_writing.tell() == 0:
            writer.writeheader()

        # Only add this cat if it doesn't already exist
        if not checkCSV(fieldnames, thisCat):
            writer.writerow({
                'name' : thisCat.name,
                'breed' : thisCat.breed,
                'gender' : thisCat.gender,
                'neutered' : thisCat.neutered,
                'age_group' : thisCat.ageGroup,
                'age_year' : thisCat.years,
                'age_month' : thisCat.months,
                'age_unknown' : thisCat.ageUnknown
            })


# Load the csv file of cats into a dictionary of Cats using the cats name as it's key.
def loadCSV(fieldnames):

    try:
        with open(surveyFile) as csvfile:

            output = {}
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

            return output

    except FileNotFoundError:
        return {}


# Search the csv file for an identical copy of this cat
def checkCSV(fieldnames, thisCat):

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
        return {}


# Basic C implementation of a switch/case for the ageGroup category
def switcher(argument):
    return {
        'kitten' : [0, 0],
        'adult' : [0, 3],
        'prime' : [3, 6],
        'mature' : [7, 10],
        'senior' : [11, 14],
        'geriatric' : [15, 50]
        }[argument]