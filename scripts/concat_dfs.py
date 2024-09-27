import pandas as pd
import os

def concatenate_dfs(start_year, end_year, buy_or_sale):
    concat_df = pd.DataFrame()
    for year in range(start_year, end_year + 1):
        filepath = '../data'
        df = pd.read_csv(os.path.join(filepath, f"insider_{buy_or_sale}_{year}.csv"))
        concat_df = pd.concat([df, concat_df])
    return concat_df