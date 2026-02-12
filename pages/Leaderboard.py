import streamlit as st
import pandas as pd
import altair as alt


st.title("Diva Standings Over Time")
st.set_page_config(
    page_title="Leaderboard",
    page_icon='🏆'
)
# Import Data
data = pd.read_csv("all_Records.csv")

# Format Data for Graphing
data['cum_WLT_diff'] = data['Cum_Win'].astype(str) + '-' + data['Cum_Loss'].astype(str) + '-' + data['Cum_Tie'].astype(str)
#data["Date"] = pd.to_datetime(data["Date"], format="%m-%d-%Y")
data["Date"] = pd.to_datetime(data["Date"], format="%m-%d-%Y")
data["Date_Label"] = data["Date"].dt.strftime('%m-%d') 
data = data.sort_values(["Team", "Date"])

# Filters
  ## filter for weeks that no games are played
data = data.drop(data[(data.Win == 0) & (data.Loss == 0) & (data.Tie == 0)].index)
year = st.selectbox("Year",sorted(data["Date"].dt.year.unique(),reverse=True))
available_seasons = (data[data["Date"].dt.year == year]["Season"].unique())
season = st.selectbox("Season",sorted(available_seasons))
division = st.selectbox("Division", data["Division"].unique())

filtered = data[
    (data["Date"].dt.year == year)&
    (data["Season"] == season) &
    (data["Division"] == division) 
]

# Prepare Graph
chart = (
    alt.Chart(filtered)
    .mark_line(point=True)
    .encode(
        x=alt.X("Date_Label:O", title="Date"),
        y=alt.Y(
            "Standing:Q",
            scale=alt.Scale(reverse=True,domainMin=1),
            title="Standing"
        ),
        color=alt.Color("Team:N", legend=alt.Legend(title="Team")),
        tooltip=[
            alt.Tooltip("Team:N", title="Team"),
            alt.Tooltip("Date:T", title="Date"),
            alt.Tooltip("Standing:Q", title="Standing"),
            alt.Tooltip("cum_WLT_diff:N", title="W-L-T"),
            alt.Tooltip("Cum_Diff:Q", title="Point Diff")
        ]
    )
)

# Add Hover 
hover = alt.selection_point(
    fields=["Team"],
    on="mouseover",
    empty="none"
)

chart = chart.add_selection(hover).encode(
    strokeWidth=alt.condition(hover, alt.value(4), alt.value(1))
)
## Plot

st.altair_chart(chart, use_container_width=True)

## Add Image4fun
st.image("test_photo.jpg", caption="😘😘😘")
