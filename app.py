from flask import Flask, render_template
import csv
from collections import OrderedDict

app = Flask(__name__)

def incumbent_data():
    incumbents = {}
    #senate
    with open("data/senate-incumbents.csv", "r") as f:
        reader = csv.reader(f, delimiter=",")
        for row in reader:
            district = "State Senator District " + row[0]
            name = row[1]
            year_elected = row[3]

            incumbents[district] = {"name": name, "year_elected": year_elected}

    #house
    with open("data/house-incumbents.csv", "r") as f:
        reader = csv.reader(f, delimiter=",")
        for row in reader:
            district = "State Representative District " + row[0]
            name = row[1]
            year_elected = row[3]

            incumbents[district] = {"name": name, "year_elected": year_elected}

    return incumbents

def prev_election_data():

    election_results = {}

    #senate results
    with open('data/2012_statesenateresults.csv', 'r') as f:
        reader = csv.reader(f, delimiter=";")
        for row in reader:
            district = row[4]
            name = row[7].title()
            party = row[10]
            percentage = row[14]

            inserted = False

            if district in election_results:
                for i in range(0, len(election_results[district])):
                    if float(percentage) > float(election_results[district][i]["percentage"]):
                        election_results[district].insert(i, {"name": name, "party": party, "percentage": percentage})
                        inserted = True
                        break
                if not inserted:
                    election_results[district].append({
                                                        "name": name,
                                                        "party": party,
                                                        "percentage": percentage
                                                    })
            else:
                election_results[district] = [{
                                                "name": name,
                                                "party": party,
                                                "percentage": percentage
                                              }]

    #house results
    with open('data/2014_houseelectionresults.csv', 'r') as f:
        reader = csv.reader(f, delimiter=";")
        for row in reader:
            district = row[4]
            name = row[7].title()
            party = row[10]
            percentage = row[14]

            inserted = False

            if district in election_results:
                for i in range(0, len(election_results[district])):
                    if float(percentage) > float(election_results[district][i]["percentage"]):
                        election_results[district].insert(i, {"name": name, "party": party, "percentage": percentage})
                        inserted = True
                        break
                if not inserted:
                    election_results[district].append({
                                                        "name": name,
                                                        "party": party,
                                                        "percentage": percentage
                                                    })
            else:
                election_results[district] = [{
                                                "name": name,
                                                "party": party,
                                                "percentage": percentage
                                            }]
    return election_results

def candidate_data():

    elections = OrderedDict()

    with open('data/CF_FedStateCounty.csv', 'r') as f:
        reader = csv.reader(f, delimiter=";", quotechar='"')

        for row in reader:
            district = row[3]
            candidate = row[1]
            candidate_party = row[5]

            if district in elections:
                first_party = elections[district][0][1]
                if candidate_party == first_party:
                    elections[district].insert(0, [candidate, candidate_party])
                else:
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

        #incumbent handling
        incumbents = incumbent_data()
        if title in incumbents:
            incumbent_name = incumbents[title]["name"]
            incumbent_year_elected = incumbents[title]["year_elected"]

            incumbent_running = False

            for i in range(0, len(candidates)):
                if candidates[i][0] == incumbent_name:
                    incumbent_candidate = candidates.pop(i)
                    incumbent_candidate.append(incumbent_year_elected)
                    incumbent_running = True
                    break

            if not incumbent_running:
                incumbent_candidate = ["Open seat","",""]
                classes += " open-seat"

        #previous elections
        if "State Senator" in title:
            last_election_year = "2012"
        else:
            last_election_year = "2014"

        last_election_results = prev_election_data().get(title)

        #filtering to Lege elections
        if "State Senator" in title or "State Representative" in title:
            f_elections.append({
                                    "title": title,
                                    "incumbent": incumbent_candidate,
                                    "candidates": candidates,
                                    "classes": classes,
                                    "last_election_year": last_election_year,
                                    "last_election_results": last_election_results
                                })


    return f_elections

@app.route("/")
def main_view():
    template = "index.html"
    return render_template(template, contests = formatted_elections(candidate_data()))

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
