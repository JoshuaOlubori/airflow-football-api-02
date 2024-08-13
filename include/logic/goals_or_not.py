# import pandas as pd

# def both_teams_scored_or_not(df):
#     # Create a new column 'both_teams_scored' using vectorized operations
#     df['both_teams_scored'] = ((df['home_team_score'] > 0) & (df['away_team_score'] > 0)).astype(int)
#     df['teams_did_not_score'] = ((df['home_team_score'] == 0) & (df['away_team_score'] == 0)).astype(int)
#     return df


import pandas as pd

def both_teams_scored_or_not(df):
    # Initialize both new columns with 0 where match_status is not "Match Finished"
    df['both_teams_scored'] = 0
    df['teams_did_not_score'] = 0
    
    # Update the columns where match_status is "Match Finished"
    finished_matches = df['match_status'] == "Match Finished"
    
    df.loc[finished_matches, 'both_teams_scored'] = (
        (df['home_team_score'] > 0) & (df['away_team_score'] > 0)
    ).astype(int) + 1  # 2 if true, 1 if false
    
    df.loc[finished_matches, 'teams_did_not_score'] = (
        (df['home_team_score'] == 0) & (df['away_team_score'] == 0)
    ).astype(int) + 1  # 2 if true, 1 if false
    
    return df