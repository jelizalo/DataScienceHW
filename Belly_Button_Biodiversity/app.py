import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy import create_engine, func, desc
from sqlalchemy import inspect
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

from flask import Flask, jsonify, render_template, redirect

# Connect to database
engine = create_engine("sqlite:///belly_button_biodiversity.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

# References
bacteria = Base.classes.otu
samples = Base.classes.samples
samples_metadata = Base.classes.samples_metadata

session = Session(engine)

# Set up flask application

app = Flask(__name__)

@app.route("/")
def dashboard():
    return render_template("index.html")

@app.route("/names")
def names():
# Return a list of sample names
    results = session.query(samples)
    list_names = list(session.execute(results).keys())
    full_name_list = list_names[1:]
    stripped_list = [s.strip('samples_') for s in full_name_list]
    return jsonify(stripped_list)

@app.route("/otu")
def otu_list():
# Return list of OTU descriptions
    results = session.query(bacteria.lowest_taxonomic_unit_found).all()
    descriptions = results
    return jsonify(descriptions)

@app.route("/metadata/<sample>")
def metadata(sample):
    y = session.query(samples_metadata.AGE, samples_metadata.BBTYPE, samples_metadata.ETHNICITY, samples_metadata.GENDER, samples_metadata.LOCATION, samples_metadata.SAMPLEID).filter(samples_metadata.SAMPLEID == "BB_" + sample)
    metadata_list = []
    for result in y:
        row = {}
        row["AGE"] = result[0]
        row["BBTYPE"] = result[1]
        row["ETHNICITY"] = result[2]
        row["GENDER"] = result[3]
        row["LOCATION"] = result[4]
        row["SAMPLEID"] = result[5]
        metadata_list.append(row)
    return jsonify(metadata_list)

@app.route('/samples/<sample>')
def samples_id_values(sample):
    q = session.execute("SELECT otu_id, "+sample+" FROM samples ORDER BY "+sample+" DESC")
    b = list(q)
    sample_list = []
    otu_id_list = []
    sample_value_list = []
    for i in range(0, len(b)):
        otu_id_list.append(b[i][0])
        sample_value_list.append(b[i][1])
    nested_dict = {'otu_ids': otu_id_list, 'sample_values': sample_value_list}
    sample_list.append(nested_dict)
    return jsonify(sample_list)

if __name__ == '__main__':
    app.run(debug=True)
