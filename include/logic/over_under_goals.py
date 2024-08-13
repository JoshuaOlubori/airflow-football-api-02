# import pandas as pd

# def add_over_columns(df):
#     total_goals = df['home_team_score'] + df['away_team_score']
#     df['over_0_5'] = (total_goals > 0).astype(int)
#     df['over_1_5'] = (total_goals > 1).astype(int)
#     df['over_2_5'] = (total_goals > 2).astype(int)
#     df['over_3_5'] = (total_goals > 3).astype(int)
#     return df

# def add_under_columns(df):
#     total_goals = df['home_team_score'] + df['away_team_score']
#     df['under_0_5'] = (total_goals == 0).astype(int)
#     df['under_1_5'] = (total_goals <= 1).astype(int)
#     df['under_2_5'] = (total_goals <= 2).astype(int)
#     df['under_3_5'] = (total_goals <= 3).astype(int)
#     df['under_4_5'] = (total_goals <= 4).astype(int)
#     return df

# def add_draw_columns(df):
#     df['draw'] =  (df['home_team_score'] == df['away_team_score']).astype(int)
#     return df


import pandas as pd

def add_over_columns(df):
    # Initialize all over_* columns with 0 where match_status is not "Match Finished"
    df['over_0_5'] = 0
    df['over_1_5'] = 0
    df['over_2_5'] = 0
    df['over_3_5'] = 0
    
    # Filter rows where match_status is "Match Finished"
    finished_matches = df['match_status'] == "Match Finished"
    total_goals = df['home_team_score'] + df['away_team_score']
    
    df.loc[finished_matches, 'over_0_5'] = (total_goals > 0).astype(int) + 1
    df.loc[finished_matches, 'over_1_5'] = (total_goals > 1).astype(int) + 1
    df.loc[finished_matches, 'over_2_5'] = (total_goals > 2).astype(int) + 1
    df.loc[finished_matches, 'over_3_5'] = (total_goals > 3).astype(int) + 1
    
    return df


def add_draw_columns(df):
    # Initialize draw column with 0 where match_status is not "Match Finished"
    df['draw'] = 0
    
    # Filter rows where match_status is "Match Finished"
    finished_matches = df['match_status'] == "Match Finished"
    
    df.loc[finished_matches, 'draw'] = (df['home_team_score'] == df['away_team_score']).astype(int) + 1
    
    return df


def add_under_columns(df):
    # Initialize all under_* columns with 0 where match_status is not "Match Finished"
    df['under_0_5'] = 0
    df['under_1_5'] = 0
    df['under_2_5'] = 0
    df['under_3_5'] = 0
    df['under_4_5'] = 0
    
    # Filter rows where match_status is "Match Finished"
    finished_matches = df['match_status'] == "Match Finished"
    total_goals = df['home_team_score'] + df['away_team_score']
    
    df.loc[finished_matches, 'under_0_5'] = (total_goals == 0).astype(int) + 1
    df.loc[finished_matches, 'under_1_5'] = (total_goals <= 1).astype(int) + 1
    df.loc[finished_matches, 'under_2_5'] = (total_goals <= 2).astype(int) + 1
    df.loc[finished_matches, 'under_3_5'] = (total_goals <= 3).astype(int) + 1
    df.loc[finished_matches, 'under_4_5'] = (total_goals <= 4).astype(int) + 1
    
    return df

