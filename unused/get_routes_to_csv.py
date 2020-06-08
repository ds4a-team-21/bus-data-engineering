from sptrans import SPTransClient
import pandas as pd
from tqdm import tqdm

tqdm.pandas()


def return_only_bus_routes(route):
    not_route_first_letter = ['C', 'M']
    if route[0] not in not_route_first_letter:
        return route
    else:
        return float("NaN")


app_token = '0d2ac3fa88a05a1094c042a3489c94c0f75e85e06894e459c9cf39eb8ac5c249'
sp_trans = SPTransClient(app_token)
sp_trans.auth()

routes = pd.read_csv('../data/prod/routes.csv')

routes = routes['route_id'].progress_apply(return_only_bus_routes).dropna().to_list()

sp_bus_lines = list(map(sp_trans.search_by_busline, routes))

bus_lines_df = pd.DataFrame(sp_bus_lines)

bus_lines_df1 = bus_lines_df[1].dropna()
bus_lines_df2 = bus_lines_df[2].dropna()
bus_lines_df3 = bus_lines_df[3].dropna()

bus_series = pd.concat([bus_lines_df[0], bus_lines_df1, bus_lines_df2, bus_lines_df3]).reset_index(drop=True)

bus_lines_df = pd.DataFrame(bus_series.to_list()).sort_values('lt', ignore_index=True)

bus_lines_df.to_csv('data/prod/bus_routes.csv', index=False)
