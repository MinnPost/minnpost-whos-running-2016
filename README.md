# Who’s running for the Minnesota Legislature 2016

This project lists candidates for the Minnesota Legislature — both Senate and House
— and includes information on past election results for each seat. Users can filter
races by certain categories, such as "Open Seat" and/or "GOP Primary" and search
the text for specific names.

The live story can be found at [Here’s who’s running for the Minnesota Legislature](https://www.minnpost.com/politics-policy/2016/06/here-s-who-s-running-minnesota-legislature)
on MinnPost.

##Data

Data files are stored in the `/data` directory. The main data source is the
[Minnesota Secretary of State’s list of candidates for office](http://candidates.sos.state.mn.us/).
The downloadable text file is saved as `CF_FedStateCounty.csv`.

`senate-incumbents.csv` and `house-incumbents.csv` contain names, party affiliations,
and year first elected for current officeholders. It was compiled by hand.

`2012_statesenateresults.csv` and `2014_houseelectionresults.csv` were created from
election results files downloaded from the Minnesota Secretary of State. They were
edited to include only the results needed for this project.

##Development

This project uses flask to load data from the sources above into a jinja template.

To develop locally, we recommend setting up a virtual environment:

`virtualenv -p python3 venv`

Activate it:

`source venv/bin/activate`

Then install the requirements:

`pip install -r requirements.txt`

To run the app, use:

`python app.py`

This should launch a local server so you can load the page in your browser.

In general, to make changes to the way data is loaded or processed, look in `app.py`.
To change the appearance of the data, or to change the way it can be filtered,
look at the template in `templates/index.html`. All the CSS and Javascript (besides
  jQuery) are included in that template.

##Deployment
Currently, we’re deploying by running the app, viewing source, and copying
the generated HTML into our CMS. :flushed: Totally planning to use `frozen-flask`
to generate a deployable HTML file that can either be uploaded somewhere or
copied as CMS may require.
