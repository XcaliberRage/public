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

