import streamlit as st
import pandas as pd
from filter_friend_finder import friendFinder, friends2Teams

#
SCHEDULE_FILE = '2026Spring_Schedule.csv'

st.title("Locate Your Friends :heart: \n RIP my boy TDO :skull::leg::boom:")
st.set_page_config(
    page_title="Locate Your Friends",
    page_icon='👬'
)


# Import Data
    # Schedule Data
data = pd.read_csv(SCHEDULE_FILE)
data['Time'] = pd.to_datetime(data['Time'], format= '%I:%M %p').dt.time
data["Date"] = pd.to_datetime(data["Date"], format="%a, %b %d %Y").dt.strftime("%m-%d-%Y")
    # Player-Team Data
column_names = ['Player','Division','Team Number']
players_df = pd.read_csv("26springteams.csv", names = column_names, skiprows=1,dtype=str)
# parts = players_df['Player'].str.split(' ', n=1, expand=True)
# players_df['Player'] = parts[0] + ' ' + parts[1].str[:1]


### Drop Downs
    # Default Value 
    # Date Dropdowns
date_options = data['Date'].unique().tolist()
selected_date = st.selectbox(
    'Select Date to Filter',
    options=date_options,
    index=5
)
    # Player Dropdown
players_options = players_df['Player'].unique().tolist()
selected_players = players_options
selected_players = st.multiselect(
    "Which Players are you looking for",
    options=players_options,
    max_selections=25,
    accept_new_options=True,
    default=["Eastian Shon","Nhi Bui","Mike Clancy","Marley Anderson","Junior Riengxay","Utmy Tran","Megan Silavongsa","Kevin Dinh","TonyTam Dinh","Pete Visounnaraj","Christopher Nguyen","Jay Bui", "Kristine Vital","Tommy Tran","Mark Le","TK Kittisubcharoen","Reagan Phonsa","Frederick Alejandro","Jet Li Thach","Kayu Southichark"]
)

filtered_search = friendFinder(friends2Teams(players_df,selected_players),data,selected_date)
st.write(filtered_search)
# # st.write(selected_players)






