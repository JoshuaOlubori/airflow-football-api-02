import pandas as pd
import math
from include.global_variables import global_variables as gv

def core_filter_2(df):
    try:
        gv.task_log.info(f"BEFORE CORE FILTER 2, COLUMNS ARE {df.columns}")

        gv.task_log.info("Applying core filtering logic 2...  This would take some time.\n")

        # Initialize an empty list to store the column values
        won_all_last_5_games = []

        def team_won_all_last_5_games(team, g):
            win_count = 0
            for index, row in g.iterrows():
                if row["home_team"] != team:
                    g.loc[index, "home_team"] = row["away_team"]
                    g.loc[index, "away_team"] = row["home_team"]

                    g.loc[index, "home_team_score"] = row["away_team_score"]
                    g.loc[index, "away_team_score"] = row["home_team_score"]

            win_count = 0
            for index, row in g.iterrows():
                if g.loc[index, "home_team_score"] > g.loc[index, "away_team_score"]:
                    win_count += 1
            if win_count == 5:
                return True
            else:
                return False

        

        def convert_missing_values_to_null(match):
            for key, value in match.items():
                if pd.isna(value) or (isinstance(value, float) and math.isnan(value)):
                    match[key] = "null"
            return match

        # Find all match containers
        match_containers = df.to_dict('records')
        # Extract 'match_status' values from each dictionary
        
        match_containers = [convert_missing_values_to_null(match) for match in match_containers]

        # Get unique values using set
        
        #gv.task_log.info("FILLING NA WITH 0")
        df = df.fillna(0)

        # Loop through each match container
        for match in match_containers:
            home_team = match['home_team']
            away_team = match['away_team']

            # Get the last 5 fixtures for both home and away teams
            last_5_home_team_fixtures = df[(df['home_team'] == home_team) | (df['away_team'] == home_team)].sort_values(by='date', ascending=False).head(5)
            last_5_away_team_fixtures = df[(df['home_team'] == away_team) | (df['away_team'] == away_team)].sort_values(by='date', ascending=False).head(5)

            # Check if either team has won all their last 5 games
            if match['match_status'] == "Match Finished":
                gv.task_log.info(f"MATCH VALUES ARE {match}")
                won_all_last_5_games.append(0)
            else:
        # If the match is finished, check if either team has won all their last 5 games
                if team_won_all_last_5_games(home_team, last_5_home_team_fixtures) or team_won_all_last_5_games(away_team, last_5_away_team_fixtures):
                    won_all_last_5_games.append(2)
                else:
                    won_all_last_5_games.append(1)


        # Add the new column to the original dataframe if the length is equal
        try:
            if len(won_all_last_5_games) == len(df):
                df['team_won_all_last_5_games'] = won_all_last_5_games
                gv.task_log.info("New column 'team_won_all_last_5_games' added to the dataframe.")
            else:
                gv.task_log.warning("Length of 'team_won_all_last_5_games' list does not match the length of the dataframe.")
        except Exception as e:
            gv.task_log.warning(f"Error adding new column: {e}")

        gv.task_log.info("New column 'team_won_all_last_5_games' added to the dataframe.")

    except Exception as e:
        gv.task_log.warning(f"Error during processing: {e}")
    
    gv.task_log.info(f"AFTER CORE FILTER 2, COLUMNS ARE {df.columns}")

    return df




def core_filter_2_optimised(df):
    try:
        gv.task_log.info("Applying filtering logic...  This would take some time.\n")

        # Vectorized implementation
        teams = df[['home_team', 'away_team']].stack().unique()
        won_all_last_5_games = []

        def team_won_all_last_5_games(team, g):
            g = g.copy()  # Create a copy to avoid modifying the original DataFrame
            swapped = (g['home_team'] != team)
            g.loc[swapped, ['home_team', 'away_team']] = g.loc[swapped, ['away_team', 'home_team']].values
            g.loc[swapped, ['home_team_score', 'away_team_score']] = g.loc[swapped, ['away_team_score', 'home_team_score']].values
            win_count = (g['home_team_score'] > g['away_team_score']).sum()
            return win_count == len(g)

        for team in teams:
            team_fixtures = df[(df['home_team'] == team) | (df['away_team'] == team)].sort_values(by='date', ascending=False).head(5)
            if team_won_all_last_5_games(team, team_fixtures):
                won_all_last_5_games.extend([1] * len(df))
            else:
                won_all_last_5_games.extend([0] * len(df))

        # Add the new column to the original dataframe if the length is equal
        try:
            if len(won_all_last_5_games) == len(df):
                df['team_won_all_last_5_games'] = won_all_last_5_games
                gv.task_log.info("New column 'team_won_all_last_5_games' added to the dataframe.")
            else:
                gv.task_log.warning("Length of 'team_won_all_last_5_games' list does not match the length of the dataframe.")
        except Exception as e:
            gv.task_log.warning(f"Error adding new column: {e}")

    except Exception as e:
        gv.task_log.warning(f"Error during processing: {e}")

    # sorting by date
    df = df.sort_values(by=['date', 'league_name'], ascending=False)
    return df