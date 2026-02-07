import streamlit as st
import pandas as pd
from filter_friend_finder import friendFinder, friends2Teams

# Import Data
    # Schedule Data
data = pd.read_csv("output.csv")
data['Time'] = pd.to_datetime(data['Time'], format= '%I:%M %p').dt.time
data['Date'] = pd.to_datetime(data['Date'], format='%a, %b %d').dt.strftime('%m-%d')
    # Player-Team Data
column_names = ['Player','Division','Team Number']
players_df = pd.read_csv("26springteams.csv", names = column_names, skiprows=1,dtype=str)

st.title("Watch Your Friends :heart: \n RIP my boy TDO :skull::leg::boom:")
### Drop Downs
    # Default Value 
DEFAULT_FILTER_VALUE = "Select a category"
    # Date Dropdowns
date_options = data['Date'].unique().tolist()
selected_date = st.selectbox(
    'Select Date to Filter',
    options=date_options,
    index=3
)
    # Player Dropdown
players_options = players_df['Player'].unique().tolist()
selected_players = players_options
selected_players = st.multiselect(
    "Which Players are you looking for",
    options=players_options,
    max_selections=15,
    accept_new_options=True,
    default=["Junior Riengxay","Utmy Tran","Megan Silavongsa","Kevin Dinh","TonyTam Dinh","Pete Visounnaraj","Christopher Nguyen","Jay Bui", "Kristine Vital","Olivia Cunningham"]
)


# # Filter
# selected_players = ["Kevin Dinh","TonyTam Dinh", "Megan Silavongsa","Pete Visounnaraj", "Tommy Tran","Christine Trinh"]
# selected_players = [s.lower() for s in selected_players]


filtered_search = friendFinder(friends2Teams(players_df,selected_players),data,selected_date)
st.write(filtered_search)
# # st.write(selected_players)

