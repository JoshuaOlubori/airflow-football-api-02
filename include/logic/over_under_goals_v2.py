import pandas as pd
import numpy as np

def add_over_columns(df):
    # Sum the home and away team scores
    total_goals = df['home_team_score'].add(df['away_team_score'], fill_value=np.nan)
    
    for threshold in [0.5, 1.5, 2.5, 3.5]:
        column_name = f'over_{threshold:.1f}'.replace('.', '_')
        
        # Check if either score is 99
        condition = (df['home_team_score'] == 99) | (df['away_team_score'] == 99)
        
        df[column_name] = np.where(total_goals.notna(), 
                                   np.where(condition, 99, (total_goals > threshold).astype('Int64')),
                                   pd.NA)
    return df


def add_under_columns(df):
    total_goals = df['home_team_score'].add(df['away_team_score'], fill_value=np.nan)
    
    for threshold in [0.5, 1.5, 2.5, 3.5, 4.5]:
        column_name = f'under_{threshold:.1f}'.replace('.', '_')

        condition = (df['home_team_score'] == "null") | (df['away_team_score'] == "null")
        df[column_name] = np.where(total_goals.notna(), 
                                   np.where(condition, 99, (total_goals > threshold).astype('Int64')),
                                   pd.NA)
    return df

def add_draw_columns(df):
    df = df.copy()
    df['draw'] = np.where((df['home_team_score'].ne("null")) | (df['away_team_score'].ne("null")),
                          (df['home_team_score'] == df['away_team_score']).astype('Int64'),
                          pd.NA)
    return df

def process_all_columns(df):
    df = add_over_columns(df)
    df = add_under_columns(df)
    df = add_draw_columns(df)
    return df