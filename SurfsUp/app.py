# Import the dependencies.
import numpy as np

import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station



#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################


@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2017-08-01<br/>"
        f"/api/v1.0/2017-08-01/2017-08-30"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Find the most recent date in the data set.
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    
    #turn recent_date to string type
    recent_date_str = recent_date[0]

    #make recent_date_str to date format
    recent_date_dt = dt.datetime.strptime(recent_date_str, "%Y-%m-%d").date()

    #calculate the date a year from recent_date
    year_ago = recent_date_dt - dt.timedelta(days=365)

    results = session.query(Measurement.prcp,Measurement.date).order_by(Measurement.date.desc()).filter(Measurement.date<=recent_date_str).\
                filter(Measurement.date>= year_ago).all()
    
    session.close()

    results_list = []

    for prcp, date in results:
        results_dict = {}
        results_dict[date] =  prcp
        results_list.append(results_dict)

    return jsonify(results_list)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #query station and station names
    station_names = session.query(Station.station, Station.name).all()

    station_list = []

    for station, name in station_names:
        station_dict = {}
        station_dict[station] = name
        station_list.append(station_dict)

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def active_station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #query stations and sort by most active
    station_names = session.query(Station.station, func.count(Measurement.station)).\
            join(Measurement, Measurement.station==Station.station).\
            group_by(Measurement.station).\
            order_by(func.count(Measurement.station).desc()).all()
    
    #top of station_names is the most active
    most_active_station = station_names[0][0]

    #query most recent date for the most active station
    recent_date_mostAct = session.query(func.MAX(Measurement.date)).filter(Measurement.station==most_active_station).first()
    
    #change to string value
    recent_date_mostAct_str = recent_date_mostAct[0]

    #change to date value
    recent_date_mostAct_dt = dt.datetime.strptime(recent_date_mostAct_str, "%Y-%m-%d").date()

    #calculate the date a year from recent_date_mostAct
    year_ago_mostAct = recent_date_mostAct_dt - dt.timedelta(days=365)

    last12_act = session.query(Measurement.tobs).\
                order_by(Measurement.date.desc()).\
                filter(Measurement.date <= recent_date_mostAct_str).\
                filter(Measurement.date >= year_ago_mostAct).all()
    
    session.close()

    #convert rows to a list
    data_points = [row[0] for row in last12_act]

    return jsonify(data_points)
    
@app.route("/api/v1.0/<start>")
def temp_min_max_avg(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    stats = session.query(func.MIN(Measurement.tobs),
                                func.MAX(Measurement.tobs),
                                func.AVG(Measurement.tobs)).\
                    filter(Measurement.date >= start).all()

    session.close()

    stats_list = []

    for tobs in stats:
        stats_dict = {}
        stats_dict["Max_temp"] = stats[0][1]
        stats_dict["Min_temp"] = stats[0][0]
        stats_dict["Avg_temp"] = stats[0][2]
        stats_list.append(stats_dict)

    return jsonify(stats_list)

@app.route("/api/v1.0/<start>/<end>")
def temp_min_max_avg_se(start,end):

    # Create our session (link) from Python to the DB
    session = Session(engine)

    stats = session.query(func.MIN(Measurement.tobs),
                                func.MAX(Measurement.tobs),
                                func.AVG(Measurement.tobs)).\
                    filter(Measurement.date >= start).\
                    filter(Measurement.date <= end).all()

    session.close()

    stats_list = []

    for tobs in stats:
        stats_dict = {}
        stats_dict["Max_temp"] = stats[0][1]
        stats_dict["Min_temp"] = stats[0][0]
        stats_dict["Avg_temp"] = stats[0][2]
        stats_list.append(stats_dict)

    return jsonify(stats_list)


if __name__ == "__main__":
    app.run(debug=True)