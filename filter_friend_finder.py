import pandas as pd
from functools import reduce
import numpy as np
def friends2Teams(df,friends):
    friends = [s.lower() for s in friends]
    mask = df["Player"].str.lower().isin(friends)
    df = df.loc[mask].copy()
    df.loc[:,"Search"] = df['Division'].str[0]  + "-" + df['Team Number'].str.zfill(2)
    df = df.groupby('Search')['Player'].agg(list).reset_index()
    return df


def friendFinder(teams_DF,schedule_DF,date):
    df = pd.DataFrame()
    # Filter By Date
    schedule_DF = schedule_DF[schedule_DF['Date'] == date]
    # schedule_DF.drop_duplicates(inplace=True)

    # Get all rows that contain teams of interest
    pattern = '|'.join(teams_DF['Search']) 
    masks = [
        schedule_DF['Team 1'].str.contains(pattern, case=False, na=False),
        schedule_DF['Team 2'].str.contains(pattern, case=False, na=False),
    ]
    combined_mask = reduce(lambda x, y: x | y, masks)
    schedule_DF = schedule_DF[combined_mask]
    

    for team in teams_DF['Search']:
        temp_df = schedule_DF
        # check if matches one team
        conditions = [
            (temp_df['Team 1'].str.contains(team, case=False, na=False)),
            (temp_df['Team 2'].str.contains(team, case=False, na=False))
        ]
        choices = [temp_df['Team 1'].str[:4], temp_df['Team 2'].str[:4]]
        temp_df['Search'] = np.select(conditions,choices, default="?")
        temp_df = teams_DF.merge(temp_df,left_on='Search',right_on='Search',how="left")

        # Final Formatting
        columns_to_keep = ['Date','Time','Player','Location']
        temp_df = temp_df[columns_to_keep]
        temp_df['Time'] = pd.to_datetime(temp_df['Time'], format= '%H:%M:%S').dt.strftime("%I:%M %p")

        if df.empty:
            df = temp_df
        else:
            df = pd.concat([df,temp_df], ignore_index=True)

    if not df.empty:
        df.dropna(inplace=True)

        # Convert the list column 'X' to tuples
        df['Player'] = df['Player'].apply(tuple) # List are unhashable and must be changed to tuple before dropping duplicates
        df = df.drop_duplicates()
        df['Player'] = df['Player'].apply(list)

        # Combine Players that Match vs each other
        df = df.groupby(['Date','Time','Location'], as_index=False).agg(list)
        # df.drop(["Date"],inplace=True)
        df['Location'] = df['Location'].str.extract(r'(\d+)')
        df.rename(columns={'Location':'Court'},inplace=True)
        df.drop(columns=['Date'],inplace=True)


    return df

