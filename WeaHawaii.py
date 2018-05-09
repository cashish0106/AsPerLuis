import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#####Database connection
engine = create_engine("sqlite:///Resources/Hawaii.sqlite",echo=False)

Base = automap_base()

Base.prepare(engine, reflect=True)
Station_class = Base.classes.station
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br>"       
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/<start> or /api/v1.0/<start>/<end><br>"
    )
@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all station"""
    stations = session.query(Station_class).all()
    all_stations=[]
    for station in stations:
        stat_dict={}
        stat_dict["Station ID"]=station.station
        stat_dict["Name"]=station.name
        stat_dict["latitude"]=station.latitude
        stat_dict["longitude"]=station.longitude
        stat_dict["elevation"]=station.elevation
        all_stations.append(stat_dict)
    return jsonify(all_stations)

if __name__ == '__main__':
    app.run(debug=True)