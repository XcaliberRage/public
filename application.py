import cs50
import csv
import sys
from catSurveyOps import writeCSV, loadCSV, getBreeds, validateThisCat
from cat import Cat

from flask import Flask, jsonify, redirect, render_template, request

# Global constant fieldnames for the CSV, i need to use this list in two seperate functions
fieldnames = ['name', 'breed', 'gender', 'neutered', 'age_group', 'age_year', 'age_month', 'age_unknown']

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

    nofile, breeds, errors = getBreeds()

    if nofile:
        return render_template("error.html", messages=errors)

    return render_template("form.html", breeds=breeds)


# When submit is pressed on the form, validate all fields (in case JS got bypassed)
# If successful the Cat gets saved and the user is taken to the table of cats
@app.route("/form", methods=["POST"])
def post_form():

    form = request.form

    # Sure would be nice to not write form.get 7 times...
    thisCat = Cat(
        form.get("name"),
        form.get("breed"),
        form.get("gender"),
        form.get("neutered"),
        form.get("ageGroup"),
        form.get("years"),
        form.get("months"),
        form.get("ageUnknown")
    )

    thisCat.neutered = thisCat.neutered == 'neutered'
    thisCat.ageUnknown = thisCat.ageUnknown == 'unknown'

    validated, errors = validateThisCat(thisCat)

    # If there are any errors that got past the form validation, you get sent to a page that specifies them and there is no csv submission
    if not validated:
        return render_template("error.html", messages=errors)
    else:
        writeCSV(thisCat, fieldnames)
        return redirect("/sheet")


# Grab all the cats saved in survey.csv and show them in a happy table
@app.route("/sheet", methods=["GET"])
def get_sheet():

    # Load csv returns a tuple boolean, dictionary
    loaded, catDict = loadCSV(fieldnames)

    if not loaded:
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
