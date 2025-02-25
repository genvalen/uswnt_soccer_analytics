import pandas as pd
from datetime import datetime

from typing import List, Tuple


# Load Data
def load_data(filepath: str) -> pd.DataFrame:
    """
    Return a Dataframe from a CSV file.
    """
    file_path = filepath
    df = pd.read_csv(file_path)
    df['age'] = df['birth_date'].apply(lambda x: datetime.now().year - int(x.split('/')[-1]))
    return df

def get_player_data(df: pd.DataFrame, selected_player: str) -> pd.Series:
    """
    Return a Series object of data for the player specified.
    """
    player_data = df[df['player_name'] == selected_player].iloc[0]
    return player_data


def get_metric_labels_and_bounds(df: pd.DataFrame) -> Tuple[List[str], List[Tuple[float, float]]]:
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

            if x in ["pass_completion_pressure", "tackle_win_percentage"]:
                lower_bound = 0.0
                upper_bound = 1.0

            metric_lower_upper_bounds.append((lower_bound, upper_bound))

    metrics_labels = list(metrics.columns)

    return metrics_labels, metric_lower_upper_bounds


def get_metric_values(player_data: pd.Series, metrics: List) -> List[float]:
    """
    Return player's values for each metric. Metrics units are normalized in per-90.
    """
    return [player_data[m] for m in metrics]


def format_metrics(metrics: List) -> List:
    formatted_metrics = list(metrics)

    for i, m in enumerate(formatted_metrics):
        if m == "pass_completion_pressure":
            formatted_metrics[i] = "pass_completion_pressure_%"

        elif m == "tackle_win_percentage":
            formatted_metrics[i] = "tackle_win_%"

    return list(map(lambda x: x.replace("_", " "), formatted_metrics))



