import pandas as pd
from datetime import datetime

from typing import List, Tuple


# Load Data
def load_data(filepath) -> pd.DataFrame:
    """
    Return a Dataframe from a CSV file.
    """
    file_path = filepath
    df = pd.read_csv(file_path)
    df['age'] = df['birth_date'].apply(lambda x: datetime.now().year - int(x.split('/')[-1]))
    return df

def get_player_data(df, selected_player) -> pd.Series:
    """
    Return a Series object of data for the player specified.
    """
    player_data = df[df['player_name'] == selected_player].iloc[0]
    return player_data


def get_metric_labels_and_bounds(df) -> Tuple[List[str], List[Tuple[float, float]]]:
    """
    Return metrics, and a range of the
    lower and upper bound for each metric.
    """
    metrics = df.drop(
        labels = [
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

    metric_lower_upper_bounds = []

    for x in metrics:
        if "percentile" in x:
            metrics = metrics.drop([x], axis=1)

        else:
            lower_bound = min(metrics[x])
            lower_bound -= (lower_bound * .15)  # buffer value by 15%
            upper_bound = max(metrics[x])
            upper_bound += (upper_bound * .15)  # buffer value by 15%
            metric_lower_upper_bounds.append((lower_bound,upper_bound))

    return metrics, metric_lower_upper_bounds


def get_metric_values(player, metrics):
    """
    Return player's values for each metric. Metrics units are normalized in per90.
    """
    return [player[m] for m in metrics]




