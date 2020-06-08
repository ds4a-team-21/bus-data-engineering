import pandas as pd
from sql_integration import SqlIntegration

sql_integration = SqlIntegration()

# Transforms all the .CSVs into SQL tables
bus_routes = pd.read_csv('data/prod/bus_routes.csv')
bus_stops = pd.read_csv('data/prod/bus_stops.csv')

stops = pd.read_csv('data/prod/stops.csv')
routes = pd.read_csv('data/prod/routes.csv')
shapes = pd.read_csv('data/prod/shapes.csv')

trips = pd.read_csv('data/prod/trips.csv')
frequencies = pd.read_csv('data/prod/frequencies.csv')
stop_times = pd.read_csv('data/prod/stop_times.csv')

agency = pd.read_csv('data/prod/agency.csv')

overview = pd.read_csv('data/prod/overview.csv')
try:
    overview.drop('Unnamemed: 0')
except Exception:
    pass

passengers = pd.read_csv('data/prod/passengers.csv')


parameters = [(stops, 'stops'), (routes, 'routes'), (shapes, 'shapes'), (trips, 'trips'), (frequencies, 'frequencies'),
              (stop_times, 'stop_times'), (agency, 'agency'), (overview, 'overview'), (passengers, 'passengers')]

for parameter in parameters:

    df = parameter[0]
    table = parameter[1]

    sql_integration.create_sqlite_table(df, table)
