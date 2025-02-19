# # add demographics
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Load Data
def load_data():
    file_path = "sample_uswnt_cm_data.csv"
    df = pd.read_csv(file_path)
    df['age'] = df['birth_date'].apply(lambda x: datetime.now().year - int(x.split('/')[-1]))
    return df

df = load_data()

# streamlit app
st.title("USWNT Midfielders Analysis")

tab1, tab2, tab3 = st.tabs(["Demographic data", "Individual Performance", "Player Comparison"])

with tab1:
    st.header("Player Demographics")
    demographic_data = df[['player_name', 'age', 'team_name']]
    st.table(demographic_data)

with tab2:
    # Sidebar: Player Selection
    player_options = df['player_name'].sort_values().unique()
    selected_player = st.selectbox("Select a Player", player_options, index=0)

    player_data = df[df['player_name'] == selected_player].iloc[0]
    print(player_data)
    st.subheader(f"{selected_player} | {player_data['team_name']}, {player_data['season_name']}", divider=True)
    st.write(f"Age: {player_data['age']}")
    st.write(f"Birthdate: {player_data['birth_date']}")
    # st.write(f"Team: {player_data['team_name']}")

    # Primary plot: Radar Chart
    metrics = [
        'progressive_pass',
        'final_third_entry_pass',
        'shot_assist_op',
        'pass_completion_pressure',
        'pressure',
        'tackle',
        'tackle_win_percentage',
        'progressive_carry'
    ]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=[player_data[m] for m in metrics],
        theta=metrics,
        fill='toself',
        name=selected_player
    ))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=True)
    st.subheader(f"Performance Metrics")
    st.plotly_chart(fig)

with tab3:
    pass
    #  Compare players section