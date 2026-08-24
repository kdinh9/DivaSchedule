import streamlit as st
import pandas as pd
from filter_friend_finder import friendFinder, friends2Teams

#
SCHEDULE_FILE = './data/2026_fall/schedule.csv'
TEAM_FILE = './data/2026_fall/team_players.csv'

st.title("Locate Your Friends :heart: \n I miss u jr, emry, tommy, vinh, & kristine")
st.set_page_config(
    page_title="Locate Your Friends",
    page_icon='👬'
)


# Import Data
@st.cache_data
def load(SCHEDULE_FILE,TEAM_FILE):
        # Load Schedule-Team Data
    schedule_df = pd.read_csv(SCHEDULE_FILE)
    schedule_df.columns = schedule_df.columns.str.upper()
    schedule_df['TIME'] = pd.to_datetime(schedule_df['TIME'], format= '%I:%M %p').dt.time
    schedule_df["DATE"] = pd.to_datetime(schedule_df["DATE"], format="%b %d %y").dt.strftime("%m-%d-%Y")
        # Player-Team Data
    column_names = ['PLAYER','DIVISION','FULL NAME','TEAM','TEAM NUMBER','TEAM NAME']
    players_df = pd.read_csv(TEAM_FILE, names = column_names, skiprows=1,dtype=str)
    return players_df, schedule_df

players_df, schedule_df = load(SCHEDULE_FILE,TEAM_FILE)
### Drop Downs
    # Date Dropdowns
date_options = schedule_df['DATE'].unique().tolist()
selected_date = st.selectbox(
    'Select Date to Filter',
    options=date_options,
    index=1
)
    # Player Dropdown
players_options = players_df['PLAYER'].unique().tolist()
selected_players = players_options
selected_players = st.multiselect(
    "Which Players are you looking for",
    options=players_options,
    max_selections=25,
    accept_new_options=True,
    default=["Mike Clancy","Marley Anderson","Kevin Dinh","Megan Silavongsa","TonyTam Dinh", "Mark Le","Jet Li Thach","Kevin Vu","England Nguyen","Reagan Phonsa","Kayu Southichark","Travis Visounnaraj","Pete Visounnaraj","Olivia Cunningham"]
)

filtered_search = friendFinder(friends2Teams(players_df,selected_players),schedule_df,selected_date)
st.write(filtered_search)






