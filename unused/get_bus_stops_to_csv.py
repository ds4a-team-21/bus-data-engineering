import pandas as pd
from sptrans import SPTransClient
from tqdm import tqdm
import numpy as np

tqdm.pandas()

app_token = '0d2ac3fa88a05a1094c042a3489c94c0f75e85e06894e459c9cf39eb8ac5c249'
sp_trans = SPTransClient(app_token)
sp_trans.auth()

bus_lines_df = pd.read_csv('../data/prod/bus_routes.csv')

stops_series = bus_lines_df['cl'].progress_apply(lambda x: sp_trans.search_stops_by_bus(x))

stops_series.name = 'stops'
stops = pd.concat([stops_series, bus_lines_df['cl']], axis=1)
stops['stops'] = stops.apply(lambda x: x['stops'] if x['stops'] else np.nan, axis=1)

stops.dropna(subset=['stops'], inplace=True)
stops.reset_index(drop=True, inplace=True)

stops = pd.concat([pd.DataFrame(stops['stops'].to_list()), stops['cl']], axis=1)

stops_df = pd.melt(stops, id_vars=['cl'], value_vars=stops.columns[0:42]).drop('variable', axis=1)
stops_df.dropna(subset=['value'], inplace=True)

stops_df = pd.concat([stops_df['cl'], pd.DataFrame(stops_df['value'].to_list())], axis=1)

stops_df.to_csv('data/prod/bus_stops.csv', index=False)

