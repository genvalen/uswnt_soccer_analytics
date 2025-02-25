import streamlit as st
from soccerplots.radar_chart import Radar
import pandas as pd
from typing import List

from utils import load_data, get_player_data, get_metric_labels_and_bounds, get_metric_values, format_metrics

st.set_page_config(
    page_title="Scout USWNT Midfielder",
    page_icon=":soccer_ball:", #  Favicon
)

# Load Data and define constant variables
df = load_data("sample_uswnt_cm_data.csv")
METRICS, METRIC_BOUNDS = get_metric_labels_and_bounds(df)
print(type(METRICS))
METRICS_CLEAN = format_metrics(METRICS)
PLAYER_OPTIONS = list(df['player_name'].sort_values().unique())
ENDNOTE = f"\nExcept for those denoted by a percent sign,\nALL UNITS ARE IN PER-90"



# Color Codes
USWNT_RED = "#BB2533"
USWNT_BLUE = "#1F2742"

# Streamlit app layout configuration begings here:
st.title("USWNT Midfielders Analysis")

tab1, tab2, tab3 = st.tabs(["Demographic data", "Individual Performance", "Player Comparison"])

with tab1: #  Demographic data section
    st.subheader("Player Demographics")
    demographic_data = df[['player_name', 'age', 'team_name']]
    demographic_data.columns = ['Player Name', 'Age', 'Team Name']
    df.style.hide(axis="index")  #  hiding index appears not to work in streamlit
    st.table(demographic_data)

with tab2: #  Individual player performance section
    selected_player: str = st.selectbox("Select a Player", PLAYER_OPTIONS, index=0)
    selected_player_data: pd.Series = get_player_data(df, selected_player)  # returns as Series due to being a singular row

    st.subheader(f"Performance Metrics", divider="gray")

    # Prepare arguments needed to plot the radar chart:
    # - player data
    # - radar chart titles
    # - endnote
    selected_player_metric_values: List = get_metric_values(selected_player_data, METRICS)

    title = dict(
        title_name=selected_player_data['player_name'],
        title_color=USWNT_BLUE,
        subtitle_color=USWNT_BLUE,
        subtitle_name=f"{selected_player_data['team_name']}, {selected_player_data['season_name']}",

        title_fontsize=18,
        subtitle_fontsize=15,
    )

    #  Configure radar plot and settings
    radar = Radar(
        background_color="#FFFFFF", patch_color="#D6D6D6", fontfamily="Liberation Serif",
        label_fontsize=10, range_fontsize=6.5, label_color="#000000", range_color="#000000"
    )

    fig, ax = radar.plot_radar(
        ranges=METRIC_BOUNDS,
        params=METRICS_CLEAN,
        values=selected_player_metric_values,
        radar_color=['#B6282F', '#344D94'],
        title=title,
        endnote=ENDNOTE,
    )

    #  Display radar plot on streamlit.
    st.pyplot(fig)

with tab3: #  Compare players section
    #  Note: we can compare up to two players due to library limitations
    selected_players: List = st.multiselect("Select Players to Compare", PLAYER_OPTIONS, max_selections=2, default=PLAYER_OPTIONS[:2])

    st.subheader(f"Compare Players", divider="gray")

    selected_player_metric_values = [] #  this value will be updated if more than one player is selected
    is_compare = False  #  this value will be updated if more than one player is selected

    if selected_players:
        # CONFIGURE PLAYER 1.
        player1_data = get_player_data(df, selected_players[0])
        title = dict(
            title_name=player1_data['player_name'],
            subtitle_name=f"{player1_data['team_name']}, {player1_data['season_name']}",
            title_color=USWNT_RED,
            subtitle_color=USWNT_RED,
            title_fontsize=18,
            subtitle_fontsize=15,
        )
        selected_player_metric_values = get_metric_values(player1_data, METRICS)

        #  CONFIGURE PLAYER 2, if available.
        if len(selected_players) > 1:
            player2_data = get_player_data(df, selected_players[1])
            title_player2 = dict(
                title_name_2=player2_data['player_name'],
                subtitle_name_2=f"{player2_data['team_name']}, {player2_data['season_name']}",
                title_color_2=USWNT_BLUE,
                subtitle_color_2=USWNT_BLUE,
            )
            title.update(title_player2)
            is_compare = True
            player2_metric_values = get_metric_values(player2_data, METRICS)
            selected_player_metric_values = [selected_player_metric_values, player2_metric_values]

        #  Configure radar plot.
        radar = Radar(
            background_color="#FFFFFF", patch_color="#D6D6D6", fontfamily="Liberation Serif",
            label_fontsize=10, range_fontsize=6.5, label_color="#000000", range_color="#000000"
        )

        fig, ax = radar.plot_radar(
            ranges=METRIC_BOUNDS,
            params=METRICS_CLEAN,
            values=selected_player_metric_values,
            radar_color=['#B6282F', '#344D94'],
            title=title,
            endnote=ENDNOTE,
            compare=is_compare
        )

        #  Display radar plot on streamlit.
        st.pyplot(fig)


