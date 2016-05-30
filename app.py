from flask import Flask, render_template
import csv
from collections import OrderedDict

app = Flask(__name__)

def candidate_data():

    elections = OrderedDict()

    with open('data/CF_FedStateCounty.csv', 'r') as f:
        reader = csv.reader(f, delimiter=";", quotechar='"')

        for row in reader:
            district = row[3]
            candidate = row[1]
            candidate_party = row[5]

            if district in elections:
                elections[district].append([candidate, candidate_party])
            else:
                elections[district] = [[candidate, candidate_party]]

    return elections

def formatted_elections(elections):

    f_elections = []

    for election in elections:
        title = election
        candidates = elections[election]
        classes = ""

        if len(candidates) == 1:
            classes += " uncontested"

        parties = [candidate[1] for candidate in candidates]
        dflers = parties.count("DFL")
        if dflers > 1:
            classes += " dfl-primary"
        gopers = parties.count("R")
        if gopers > 1:
            classes += " gop-primary"

        #tk incumbent handling to add open class and to move incumbent up list

        #filtering to Lege elections
        if "State Senator" in title or "State Representative" in title:
            f_elections.append({
                                    "title": title,
                                    "candidates": candidates,
                                    "classes": classes
                                })

    return f_elections

@app.route("/")
def main_view():
    template = "index.html"
    return render_template(template, contests = formatted_elections(candidate_data()))

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
