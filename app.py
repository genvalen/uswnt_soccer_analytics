# # add demographics
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from soccerplots.radar_chart import Radar
from datetime import datetime

# Load Data
def load_data():
    file_path = "sample_uswnt_cm_data.csv"
    df = pd.read_csv(file_path)
    df['age'] = df['birth_date'].apply(lambda x: datetime.now().year - int(x.split('/')[-1]))
    return df

df = load_data()

# streamlit app begins
st.title("USWNT Midfielders Analysis")

tab1, tab2, tab3 = st.tabs(["Demographic data", "Individual Performance", "Player Comparison"])

with tab1:
    st.header("Player Demographics")
    demographic_data = df[['player_name', 'age', 'team_name']]
    demographic_data.columns = ['Player Name', 'Age', 'Team Name']
    df.style.hide(axis="index")  #  hiding index appears not to work in streamlit
    st.table(demographic_data)

with tab2:
    # Sidebar: Player Selection
    player_options = df['player_name'].sort_values().unique()
    selected_player = st.selectbox("Select a Player", player_options, index=0)

    player_data = df[df['player_name'] == selected_player].iloc[0]
    # print(player_data)
    # st.subheader(f"{selected_player} | {player_data['team_name']}, {player_data['season_name']}", divider=True)
    # st.write(f"Age: {player_data['age']}")
    # st.write(f"Birthdate: {player_data['birth_date']}")
    # st.write(f"Team: {player_data['team_name']}")

    # Primary plot: Radar Chart
    # params
    # ranges
    params = df.drop(
        [
            'player_name',
            'birth_date',
            'team_name',
            'competition_name',
            'season_name',
            'position_general',
            'age',
        ],
        axis=1
    )

    ranges = []

    for metric in params:
        if "percentile" in metric:
            params = params.drop([metric], axis=1)

        else:
            a = min(params[metric])
            a -= (a * .25)
            b = max(params[metric])
            b += (b * .25)
            ranges.append((a,b))


    # Set up argumnets for the Radar plot.
    params = list(params.columns)

    cur_player_values = [player_data[m] for m in params]

    title = dict(
        title_name=player_data['player_name'],
        title_color='#B6282F',
        subtitle_name=f"{player_data['team_name']}, {player_data['season_name']}",
        subtitle_color='#B6282F',
        title_fontsize=18,
        subtitle_fontsize=15,
    )

    st.subheader(f"Performance Metrics", divider="gray")

    radar = Radar()
    fig, ax = radar.plot_radar(
        ranges=ranges,
        params=params,
        values=cur_player_values,
        radar_color=['#B6282F', '#344D94'],
        alpha=[0.3, 0.6],
        title=title,
        filename='compare.jpg',
    )

    # Display jpeg of Radar plot on stteamlit.
    st.image("./compare.jpg")
    # fig = go.Figure()
    # fig.add_trace(go.Scatterpolar(
    #     r=[player_data[m] for m in metrics],
    #     theta=metrics,
    #     fill='toself',
    #     name=selected_player
    # ))
    # fig.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=True)

    # st.plotly_chart(fig)

with tab3:
    pass
