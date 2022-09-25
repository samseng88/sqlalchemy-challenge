import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

###########  The following code is nearly identical to Day 3 Activity 10 
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///surfsup/Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
###### Everything you need here can be found in Day 3 Activity 10
@app.route("/")
def welcome():
    return (f"Available routes<br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/start<br/>"
            f"/api/v1.0/startdate/enddate<br/><br/><br/>"
            f"Start and end date should be formatted as 'yyyy-mm-dd'")

###### the 'precipitation' route you will query and return the data Day 3 Activity 10
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    prcp_data = session.query(Measurement.date, Measurement.prcp).all()
    dict_prcp = dict(prcp_data)
    session.close()
    return jsonify(dict_prcp)

###### the 'stations' route you will query and return the data Day 3 Activity 10
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    station_data = session.query(Station.station, Station.name).all()
    station_data = dict(station_data)
    session.close()
    return jsonify(station_data)

###### the 'tobs' route you will query and return the data Day 3 Activity 10
@app.route("/api/v1.0/tobs")
def temp_monthly():
    session = Session(engine)
    temperature = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date>="2016-08-23").filter(Measurement.date<="2017-08-23").all()
    temp_dict = list(np.ravel(temperature))
    session.close()
    return jsonify(temp_dict)


###### the 'temp' route you will query the data with params in the url and return the data Day 3 Activity 10
@app.route("/api/v1.0/temp/<start>")
def start_date():
    session = Session(engine)
    temp_start=session.query()

@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    """Return TMIN, TAVG, TMAX."""

    # Select statement


    # calculate TMIN, TAVG, TMAX with start and stop


    # Unravel results into a 1D array and convert to a list



if __name__ == '__main__':
    app.run()
