# sqlalchemy-challenge
by: Panfilo Marbibi  

# Contents:  
- Resources (dir)  
--- hawaii.sqlite  
--- hawaii_measurements.csv  
--- hawaii_stations.csv  
- app.py  
- climate_starter.ipynb

# Summary: 
- Resources: directory containing CSV files and SQLite file 
- climate_starter.ipynb:
  - this jupyter notebook takes the hawaii.sqlite file in the resources folder and analyses the data
  - Precipitation Analysis:
    - finds the most recent date in the dataset
    - using that date, gets the previous 12 months of precipitation data by querying the previous 12 months of data
    - selects only the "date" and "prcp" values
    - loads the query results into Pandas DataFrame. Explicitly sets the column names
    - sorts the DataFrame values by "date"
    - plots the results by using the DataFrame plot method
    - uses Pandas to print the summary statistics for the precipitation data
  - Station Analysis:
    - designs a query to calculate the total number of stations in the dataset
    - designs a query to find the most active stations:
      - lists the stations and observation counts in descending order
      - answers the question: which station id has the greatest number of observations?
    - designs a query that calculates the lowest, highest, and average temperatures that filters on the most active station id found in the previous query
    - designs a query to get the previous 12 months of temperature observation (TOBS) data
      - filters by the station that has the greatest number of observations
      - queries the previous 12 months of TOBS data for that station
      - plots the results as a histogram
- app.py:
  - designs a Flask API based on the queries developed in teh climate_starter.ipynb jupyter notebook
    - "/"
      - Homepage
      - lists all available routes
    - "/api/v1.0/precipitation"
      - converts the query results from the precipitation analysis to a dictionary using date as the key and prcp as the value
      - returns the JSON representation of the dictionary
    - "/api/v1.0/stations"
      - returns a JSON dictionary of stations from the dataset
    - "/api/v1.0/tobs"
      - queries the dates and temperature observations of the most-active station for the previous year of data
      - returns a JSON list of temperature observations for the previous year
    - "/api/v1.0/<start> and /api/v1.0/<start>/<end>
      - returns a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range
      - for a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date
      - for a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
     
-- Code used in the .py and .ipynb files are derived from examples in classroom activities
