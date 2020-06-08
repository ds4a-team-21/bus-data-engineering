from sptrans import SPTransClient
import pandas as pd
import numpy as np
from sql_integration import SqlIntegration

sql_integration = SqlIntegration()


print('Running code...')
app_token = '0d2ac3fa88a05a1094c042a3489c94c0f75e85e06894e459c9cf39eb8ac5c249'
sp_trans = SPTransClient(app_token)
sp_trans.auth()

sp_bus_positions = sp_trans.get_all_bus_positions()

n = 0
while not sp_bus_positions:
    sp_bus_positions = sp_trans.get_all_bus_positions()
    n += 1

    if n > 100:
        print('Não consegui conectar... encerrando script.')
        break


if sp_bus_positions:
    print('Temos ônibus')
    bus_positions_df = pd.DataFrame.from_dict(sp_bus_positions)
    df = pd.concat([bus_positions_df['hr'],bus_positions_df['l'].apply(pd.Series)], axis=1)
    vs = df["vs"].apply(lambda x: x)
    p = []
    a = []
    ta = []
    py = []
    px = []
    lens = df['vs'].apply(lambda x: len(x))
    for i, v in enumerate(vs):
        for j in range(0,lens[i]):
            p.append(v[j]['p'])
            a.append(v[j]['a'])
            ta.append(v[j]['ta'])
            py.append(v[j]['py'])
            px.append(v[j]['px'])
    df_final = pd.DataFrame({'hr': np.repeat(df['hr'], lens),
                        'c': np.repeat(df['c'], lens),
                        'cl': np.repeat(df['cl'], lens),
                        'lt0': np.repeat(df['lt0'], lens),
                        'lt1': np.repeat(df['lt1'], lens),
                        'qv': np.repeat(df['qv'], lens),
                        'p': p,
                        'a': a,
                        'ta': ta,
                        'py': py,
                        'px': px})
    sql_integration.update_sqlite_table(df_final, "bus_position")

    print('Done!')
