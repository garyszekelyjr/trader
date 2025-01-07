import pandas as pd


def ma(df: pd.DataFrame):
    return df.mean()


def avg_gain(df: pd.DataFrame):
    deltas = df.diff()
    return deltas.where(deltas > 0, 0).mean()


def avg_loss(df: pd.DataFrame):
    deltas = df.diff()
    return -deltas.where(deltas < 0, 0).mean()


def rsi(df: pd.DataFrame):
    gain = avg_gain(df)
    loss = avg_loss(df)

    if loss == 0:
        return 100

    rs = gain / loss
    return 100 - (100 / (1 + rs))
