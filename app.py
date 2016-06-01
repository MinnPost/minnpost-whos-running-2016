from flask import Flask, render_template
import csv
from collections import OrderedDict

app = Flask(__name__)

metro_districts = ["State Representative District 30A", "State Representative District 31A", "State Representative District 31B", "State Representative District 32B", "State Representative District 29B", "State Representative District 30B", "State Representative District 35A", "State Representative District 35B", "State Representative District 39A", "State Representative District 34A", "State Representative District 29A", "State Representative District 36A", "State Representative District 37A", "State Representative District 37B", "State Representative District 38A", "State Representative District 33A", "State Representative District 44A", "State Representative District 34B", "State Representative District 45A", "State Representative District 40A", "State Representative District 36B", "State Representative District 40B", "State Representative District 41A", "State Representative District 41B", "State Representative District 42A", "State Representative District 38B", "State Representative District 42B", "State Representative District 39B", "State Representative District 43B", "State Representative District 59A", "State Representative District 59B", "State Representative District 45B", "State Representative District 60A", "State Representative District 61A", "State Representative District 60B", "State Representative District 62A", "State Representative District 62B", "State Representative District 63A", "State Representative District 61B", "State Representative District 49A", "State Representative District 49B", "State Representative District 44B", "State Representative District 48A", "State Representative District 33B", "State Representative District 63B", "State Representative District 50A", "State Representative District 50B", "State Representative District 48B", "State Representative District 47B", "State Representative District 51A", "State Representative District 51B", "State Representative District 52A", "State Representative District 52B", "State Representative District 64B", "State Representative District 65B", "State Representative District 65A", "State Representative District 64A", "State Representative District 66B", "State Representative District 66A", "State Representative District 43A", "State Representative District 67A", "State Representative District 67B", "State Representative District 53A", "State Representative District 53B", "State Representative District 54A", "State Representative District 54B", "State Representative District 46A", "State Representative District 46B", "State Representative District 15B", "State Representative District 58A", "State Representative District 58B", "State Representative District 47A", "State Representative District 55A", "State Representative District 55B", "State Representative District 57A", "State Representative District 57B", "State Representative District 56A", "State Representative District 56B", "State Representative District 32A", "State Senator District 15", "State Senator District 29", "State Senator District 30", "State Senator District 31", "State Senator District 32", "State Senator District 33", "State Senator District 34", "State Senator District 35", "State Senator District 36", "State Senator District 37", "State Senator District 38", "State Senator District 39", "State Senator District 40", "State Senator District 41", "State Senator District 42", "State Senator District 43", "State Senator District 44", "State Senator District 45", "State Senator District 46", "State Senator District 47", "State Senator District 48", "State Senator District 49", "State Senator District 50", "State Senator District 51", "State Senator District 52", "State Senator District 53", "State Senator District 54", "State Senator District 55", "State Senator District 56", "State Senator District 57", "State Senator District 58", "State Senator District 59", "State Senator District 60", "State Senator District 61", "State Senator District 62", "State Senator District 63", "State Senator District 64", "State Senator District 65", "State Senator District 66", "State Senator District 67"]

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

def map_url(election_title):
    if "State Representative" in election_title:
        district = election_title[30:]
        if len(district) == 2:
            district = "0" + district
        url = "http://www.gis.leg.mn/redist2010/Legislative/L2012/maps/house/" + district + ".pdf"
    else:
        district = election_title[23:]
        if len(district) == 1:
            district = "0" + district
        url = "http://www.gis.leg.mn/redist2010/Legislative/L2012/maps/senate/" + district + ".pdf"

    return url

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

        if title in metro_districts:
            classes += " metro"
        else:
            classes += " greatermn"

        if "State Senator" in title:
            classes += " senate"
        if "State Representative" in title:
            classes += " house"

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
                                    "map_url": map_url(title),
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
