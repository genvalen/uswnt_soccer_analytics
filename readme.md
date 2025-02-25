## Project Overview
Please find the github repo [here](https://github.com/genvalen/uswnt_soccer_analytics).

In order to scout a strong defensive midfielder from the data provided by Statsbomb, some Key Performance Identifiers (KPIs) to consider are high marks in the following metrics: **Tackles, Tackle Win Percentage, and Pressure.**

Alternatively, to scout a strong deep-lying midfielder, valuable KPIs to consider are high marks in metrics such as: **Progressive Pass and Shot Assist.**

I chose to display a radar plot for players' individual performance and player-comparison visualizations. The radar plot offers a quick way to identify players' top strengths and weaknesses compared to their other skills, as well as how those strength and weaknesses compare to other players.

The visualizations are served using Streamlit, a framework that enables developers to build light-weight applications using just python (without the need for HTML, CSS, or Javascript). I chose to work with Streamlit because its features make it quick and easy to set up and experiment with different visualizations and page-layouts.


## Development
Please follow the steps below to run the web app locally:
```
## create a virtual environment:
$ python3 -m venv venv
$ source venv/bin/activate

## install dependencies:
$ pip install -r requirements.txt

## run streamlit:
$ streamlit run app.py
```

## Or, Install Dependencies Independently
-- [Install Pandas](https://pandas.pydata.org/pandas-docs/version/2.1.3/getting_started/install.html)

-- [Install Streamlit](https://docs.streamlit.io/get-started/installation)

-- [Install Soccerplot](https://pypi.org/project/soccerplots/)

## Resources Referenced:

[Streamlit documentaion](https://docs.streamlit.io/)

[Soccerplot documentation](https://github.com/Slothfulwave612/soccerplots/blob/master/docs/radar_chart.md)

[Defensive Midfielder KPIs](https://community.sports-interactive.com/forums/topic/577736-key-metrics-kpi-for-each-position/)
