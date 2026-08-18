import pandas as pd
from functools import reduce
import numpy as np
def friends2Teams(df,friends):
    friends = [s.lower() for s in friends]
    mask = df["PLAYER"].str.lower().isin(friends)
    df = df.loc[mask].copy()
    df.loc[:,"Search"] = df['TEAM']
    df = df.groupby('Search')['PLAYER'].agg(list).reset_index()
    return df


def friendFinder(teams_DF,schedule_DF,date):
    df = pd.DataFrame()
    # Filter By Date
    schedule_DF = schedule_DF[schedule_DF['DATE'] == date]
    # schedule_DF.drop_duplicates(inplace=True)

    # Get all rows that contain teams of interest
    pattern = '|'.join(teams_DF['Search']) 
    masks = [
        schedule_DF['TEAM 1'].str.contains(pattern, case=False, na=False),
        schedule_DF['TEAM 2'].str.contains(pattern, case=False, na=False),
    ]
    combined_mask = reduce(lambda x, y: x | y, masks)
    schedule_DF = schedule_DF[combined_mask]
    

    for team in teams_DF['Search']:
        temp_df = schedule_DF
        # check if matches one team
        conditions = [
            (temp_df['TEAM 1'].str.contains(team, case=False, na=False)),
            (temp_df['TEAM 2'].str.contains(team, case=False, na=False))
        ]
        choices = [temp_df['TEAM 1'].str[:4], temp_df['TEAM 2'].str[:4]]
        temp_df['Search'] = np.select(conditions,choices, default="?")
        temp_df = teams_DF.merge(temp_df,left_on='Search',right_on='Search',how="left")

        # Final Formatting
        columns_to_keep = ['DATE','TIME','PLAYER','COURT']
        temp_df = temp_df[columns_to_keep]
        temp_df['TIME'] = pd.to_datetime(temp_df['TIME'], format= '%H:%M:%S').dt.strftime("%I:%M %p")

        if df.empty:
            df = temp_df
        else:
            df = pd.concat([df,temp_df], ignore_index=True)

    if not df.empty:
        df.dropna(inplace=True)

        # Convert the list column 'X' to tuples
        df['PLAYER'] = df['PLAYER'].apply(tuple) # List are unhashable and must be changed to tuple before dropping duplicates
        df = df.drop_duplicates()
        df['PLAYER'] = df['PLAYER'].apply(list)

        # Combine Players that Match vs each other
        df = df.groupby(['DATE','TIME','COURT'], as_index=False).agg(list)
        # df.drop(["Date"],inplace=True)
        #df['COURT'] = df['COURT'].str.extract(r'(\d+)') ## previous data included address
        #df.rename(columns={'COURT':'COURT'},inplace=True)
        df.drop(columns=['DATE'],inplace=True)


    return df

