# import dependancies
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# import Flask
from flask import Flask, jsonify

#database set up
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
Base.classes.keys()
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
# session = Session(engine)

Measurement = Base.classes.measurement
Station = Base.classes.station

# create app and pass __name__
app = Flask(__name__)
# Routes
# /
# Home page.
@app.route("/")

# List all routes that are available.
# available routes precipitation, stations, tobs, start date and end date (I think)
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"<a href='/api/v1.0/precipitation'>Precipitation</a><br/>"
        f"<a href='/api/v1.0/stations'>Stations</a><br/>"
        f"<a href='/api/v1.0/tobs'>TOBS</a><br/>"
        f"<a href='/api/v1.0/temp/start'>Start</a><br/>"
        f"<a href='/api/v1.0/temp/start/end'>Start/End</a><br/>"
    )


# /api/v1.0/precipitation
# Convert the query results to a dictionary using date as the key and prcp as the value. - same query as before (last year of data but in a function).
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    # Calculate the date 1 year ago from last date in database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
#     # Query for the date and precipitation for the last year
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    session.close()
#     precipitation
# Return the JSON representation of your dictionary. - jsonify
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)
    
# /api/v1.0/stations 
# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stations = session.query(Station.station).all()
    session.close()
    station_results = list(np.ravel(stations))
    return jsonify(station_results)


# /api/v1.0/tobs
@app.route("/api/v1.0/tobs")

# Query the dates and temperature observations of the most active station for the last year of data.
# Return a JSON list of temperature observations (TOBS) for the previous year.
def results():
    session = Session(engine)
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    session.close()
    # Unravel results into a 1D array and convert to a list
    temps = list(np.ravel(results))
    # Return the results
    return jsonify(temps=temps)




# /api/v1.0/<start> and /api/v1.0/<start>/<end>
@app.route("/api/v1.0/temp/start")
@app.route("/api/v1.0/temp/start/end")
def calc_temps(start=None, end=None):
    session = Session(engine)
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    start = ("2017-07-28")
    end = ('2017-08-05')
    if not end:
        # calculate TMIN, TAVG, TMAX for dates greater than start
        
        results = session.query(sel).\
            filter(Measurement.date >= start).all()
        
        temps = list(np.ravel(results))
        return jsonify(temps)
    # calculate TMIN, TAVG, TMAX with start and stop
    if end:
        results = session.query(sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    # Unravel results into a 1D array and convert to a list
        session.close()
        temps = list(np.ravel(results_too))
        return jsonify(temps=temps)
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    

# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
if __name__ == "__main__":
    app.run(debug=True)



# Hints


# You will need to join the station and measurement tables for some of the queries.


# Use Flask jsonify to convert your API data into a valid JSON response object.


