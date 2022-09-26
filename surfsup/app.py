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

@app.route("/")
def welcome():
    return (f"Welcome!<br/>"
            f"-------------------------------<br/>"
            f"Available Routes<br/></br>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/<start>enter any date between <strong>2010-01-01 and 2017-08-23</strong> in 'YYYY-MM-DD' format<br/>"
            f"/api/v1.0/<startdate>enter <strong>start date </strong>'YYYY-MM-DD' format/enter <strong>end date</strong> \
            'YYYY-MM-DD' format<br/><br/><br/>")

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

###### Query dates and temp observations of most active station for the previous year of data
@app.route("/api/v1.0/tobs")
def temp_monthly():
    session = Session(engine)
    temperature = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date>="2016-08-23").\
        filter(Measurement.date<="2017-08-23").all()
    
    temp_dict = list(np.ravel(temperature))
    session.close()
    return jsonify(temp_dict)

# Query dates and temp of the most active station for previous year of data
@app.route("/api/v1.0/<start>")
def start_date(start):
    list = []
    session = Session(engine)
    temperature = session.query(Measurement.date,func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                  filter(Measurement.date >= start).group_by(Measurement.date).all()

    session.close()
    for data in temperature:
        dict = {}
        dict['Date'] = data[0]
        dict['TMIN'] = data[1]
        dict['TAVG'] = round(data[2],2)
        dict['TMAX'] = data[3]
        list.append(dict)

    #Return a JSON list
    return jsonify(list)
    
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    session = Session(engine)
    list = []
    session = Session(engine)
    temperature = session.query(Measurement.date,func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                  filter(Measurement.date >= start).filter(Measurement.date <= end).group_by(Measurement.date).all()

    session.close()
    for data in temperature:
        dict = {}
        dict['Date'] = data[0]
        dict['TMIN'] = data[1]
        dict['TAVG'] = round(data[2],2)
        dict['TMAX'] = data[3]
        list.append(dict)

    #Return a JSON list
    return jsonify(list)

if __name__ == '__main__':
    app.run(debug=True)