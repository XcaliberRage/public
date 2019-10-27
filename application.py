import cs50
import csv
import sys
from catSurveyOps import Cat, writeCSV, switcher, loadCSV

from flask import Flask, jsonify, redirect, render_template, request

# Global constant fieldnames for the CSV
fieldnames = ['name', 'breed', 'gender', 'neutered', 'age_group', 'age_year', 'age_month', 'age_unknown']
# Global constant names for the ageGroups (for validation)
ageGroups = ['kitten', 'adult', 'prime', 'mature', 'senior', 'geriatric']
# Having breeds as a global variable is helpful
breeds = []

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():

    try:
        with open('CatBreeds.txt', 'r') as file:
            for line in file:
                breeds.append(line.strip('\n'))
    except FileNotFoundError:
        errors = ["Error loading 'CatBreeds.txt'"]
        return render_template("error.html", messages=errors)

    return render_template("form.html", breeds=breeds)


# When submit is pressed on the form, validate all fields (in case JS got bypassed)
# If successful the Cat gets saved and the user is taken to the table of cats
@app.route("/form", methods=["POST"])
def post_form():

    errors = []

    # Sure would be nice to not write request.form.get 7 times...
    thisCat = Cat(
        request.form.get("name"),
        request.form.get("breed"),
        request.form.get("gender"),
        request.form.get("neutered"),
        request.form.get("ageGroup"),
        request.form.get("years"),
        request.form.get("months"),
        request.form.get("ageUnknown")
        )

    thisCat.neutered = False if not thisCat.neutered else True
    thisCat.ageUnknown = False if not thisCat.ageUnknown else True

    # Validation needs:
    # A name
    if not thisCat.name:
        errors.append("You didn't provide a name for your Cat!")

    # A chosen cat Breed
    if not thisCat.breed:
        errors.append("You didn't select a breed or Unknown'")
    elif not thisCat.breed in breeds:
        errors.append("Is this list of breeds really not extensive enough for you?")

    # A gender (or unkown)
    if not thisCat.gender:
        errors.append("You didn't select a gender")

    # A valid age Group
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

    # If there are any errors that got past the form validation, you get sent to a page that specifies them and there is no csv submission
    if errors:
        return render_template("error.html", messages=errors)
    else:
        writeCSV(thisCat, fieldnames)
        return redirect("/sheet")


# Grab all the cats saved in survey.csv and show them in a happy table
@app.route("/sheet", methods=["GET"])
def get_sheet():

    catDict = loadCSV(fieldnames)

    if not catDict:
        errors = ["Error loading 'survey.csv'"]
        return render_template("error.html", messages=errors)

    # Create a fieldnames string with good looking format ('_' = ' ' and title case)
    # This is pretty bad because I'll have to keep changing this if my fields update
    # I don't add the last 3 categories because I'm purely passing this list for table headers and I don't want those 3 specifically
    fmatField = [fieldnames[i].replace('_', ' ').title() for i in range(len(fieldnames) - 3)]
    # I don't use Neutered and I want to combine years and months into one table header
    fmatField.remove('Neutered')
    fmatField.append('Age')

    return render_template("survey.html", cats=catDict, fieldnames=fmatField)
