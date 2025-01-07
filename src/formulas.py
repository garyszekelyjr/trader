import pandas as pd


def ma(series: pd.Series):
    return series.mean()


def avg_gain(series: pd.Series):
    deltas = series.diff()
    return deltas.where(deltas > 0, 0).mean()


def avg_loss(series: pd.Series):
    deltas = series.diff()
    return -deltas.where(deltas < 0, 0).mean()


def rsi(series: pd.Series):
    gain = avg_gain(series)
    loss = avg_loss(series)

    if loss == 0:
        return 100

    rs = gain / loss
    return 100 - (100 / (1 + rs))
