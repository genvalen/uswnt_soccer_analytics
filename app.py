# # add demographics
import streamlit as st
import pandas as pd
from soccerplots.radar_chart import Radar

from typing import List

from utils import load_data, get_player_data, get_metric_labels_and_bounds, get_metric_values

st.set_page_config(
    page_title="Scout USWNT Midfielder",
    page_icon=":soccer_ball:", #  Favicon
    # layout="wide",
)

# Load Data
df = load_data("sample_uswnt_cm_data.csv")

# streamlit app begins
with st.container():
    st.image("United-States-National-Football-Team-Logo-PNG-747x1024.webp")

st.title("USWNT Midfielders Analysis")

tab1, tab2, tab3 = st.tabs(["Demographic data", "Individual Performance", "Player Comparison"])

with tab1:
    st.subheader("Player Demographics")
    demographic_data = df[['player_name', 'age', 'team_name']]
    demographic_data.columns = ['Player Name', 'Age', 'Team Name']
    df.style.hide(axis="index")  #  hiding index appears not to work in streamlit
    st.table(demographic_data)

with tab2:
    # Sidebar: Player Selection
    player_options = df['player_name'].sort_values().unique()
    selected_player: str = st.selectbox("Select a Player", player_options, index=0)
    selected_player_data: pd.DataFrame = get_player_data(df, selected_player)  # returns as Series due to being a singular row

    st.subheader(f"Performance Metrics", divider="gray")

    # Prepare arguments needed to plot the radar chart:
    # - metrics
    # - metric bounds
    # - player data
    # - radar chart titles
    # - endnote
    metrics, metric_bounds = get_metric_labels_and_bounds(df)

    selected_player_metric_values: List = get_metric_values(selected_player_data, metrics)

    metrics_clean = list(map(lambda x: x.replace("_", " "), metrics))

    title = dict(
        title_name=selected_player_data['player_name'],
        title_color='#1F2742',
        subtitle_name=f"{selected_player_data['team_name']}, {selected_player_data['season_name']}",
        subtitle_color='#1F2742',
        title_fontsize=18,
        subtitle_fontsize=15,
    )

    endnote = "ALL UNITS ARE IN PER90."

    #  Configure radar plot and settings
    radar = Radar(
        background_color="#FFFFFF", patch_color="#D6D6D6", fontfamily="Liberation Serif",
        label_fontsize=10, range_fontsize=6.5, label_color="#000000", range_color="#000000"
    )

    fig, ax = radar.plot_radar(
        ranges=metric_bounds,
        params=metrics_clean,
        values=selected_player_metric_values,
        radar_color=['#B6282F', '#344D94'],
        title=title,
        endnote=endnote,
    )

    #  Display radar plot on stteamlit.
    st.pyplot(fig)

with tab3:
    pass
    # #  Compare players section
    # st.subheader("Compare Players")
    # selected_players = st.multiselect("Select Players to Compare", player_options, max_selections=2)

    # title = dict(
    #     title_name=selected_players[0],
    #     subtitle_name='AFC Ajax',
    #     subtitle_color='#B6282F',
    #     title_name_2=selected_players[1],
    #     subtitle_name_2='Fullback',
    #     subtitle_color_2='#B6282F',
    #     title_fontsize=18,
    #     subtitle_fontsize=15,
    # )



