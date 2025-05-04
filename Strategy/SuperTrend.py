def true_range(df):
    """
    This method calculates the True Range.
    :param df: The dataframe
    :return: The True Range values as a Dataframe column
    """
    df['previous_close'] = df['close'].shift(1)
    df['high-low'] = df['high'] - df['low']
    df['high-pc'] = abs(df['high'] - df['previous_close'])
    df['low-pc'] = abs(df['low'] - df['previous_close'])

    tr = df[['high-low', 'high-pc', 'low-pc']].max(axis=1)
    return tr


def average_true_range(df, period=14):
    """
    Calculate the average True Range
    :param df: The dataframe containing OHLCV data
    :param period: The period to calculate the average on. 14 candles as default
    :return: The Average True Range
    """

    print("Calculate average true range")
    df['tr'] = true_range(df)
    atr = df['tr'].rolling(period).mean()
    return atr


def super_trend(df, period=7, multiplier=3):
    """
    The SuperTrend indicator strategy
    :param df: The dataframe containing the OHLCV data
    :param period:  The period to calculate the average on. 14 candles as default
    :param multiplier: The multiplier needed to calculate the Upper/Lower band
    :return: The dataframe containing a new columns but particularly the up_trend which is the signal to buy/sell
    """

    df['atr'] = average_true_range(df, period)
    df['upper_band'] = ((df['high'] + df['low']) / 2) + (multiplier * df['atr'])
    df['lower_band'] = ((df['high'] + df['low']) / 2) - (multiplier * df['atr'])
    df['in_uptrend'] = True

    for current in range(1, len(df.index)):
        previous = current -1

        if df.loc[current, 'close'] > df.loc[previous, 'upper_band']:
            df.loc[current, 'in_uptrend'] = True
        elif df.loc[current, 'close'] < df.loc[previous, 'lower_band']:
            df.loc[current, 'in_uptrend'] = False
        else:
            df.loc[current, 'in_uptrend'] = df.loc[previous,'in_uptrend']

            if df.loc[current, 'in_uptrend'] and df.loc[current, 'lower_band'] < df.loc[previous, 'lower_band']:
                df.loc[current, 'lower_band'] = df.loc[previous, 'lower_band']

            if not df.loc[current, 'in_uptrend'] and df.loc[current, 'upper_band'] > df.loc[previous, 'upper_band']:
                df.loc[current, 'upper_band'] = df.loc[previous, 'upper_band']

    return df

