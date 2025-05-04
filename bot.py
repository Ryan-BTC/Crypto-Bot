import websocket, json, pprint, config
from datetime import datetime
import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

from Strategy.SuperTrend import super_trend

from binance.client import Client
from binance.enums import *

import math

# wss://ws-api.testnet.binance.vision/ws-api/v3
SOCKET = "wss://stream.binance.com:9443/ws/btcusdc@kline_1m"
SYMBOL = 'BTCUSDC'
PAIR_SYMBOL = 'USDC'
ATR_PERIOD = 14
TR_PERIOD = 7
PERCENTAGE = 95

closes =[]
in_position = False

client = Client(config.API_KEY, config.API_SECRET)

df = pd.DataFrame({
    'timestamp': pd.Series(dtype='datetime64[ns]'),
    'open': pd.Series(dtype='float'),
    'high': pd.Series(dtype='float'),
    'low': pd.Series(dtype='float'),
    'close': pd.Series(dtype='float'),
    'volume': pd.Series(dtype='float'),
})


def get_amount(percent=100):
    # 1. Get current price of BTC
    price = float(client.get_symbol_ticker(symbol=SYMBOL)['price'])

    # 2. Get available USDT balance
    usdc_balance = float(client.get_asset_balance(asset=PAIR_SYMBOL)['free'])

    # 3. Calculate amount to spend
    usdc_to_spend = usdc_balance * (PERCENTAGE / 100)

    # 4. Convert to BTC quantity
    raw_qty = usdc_to_spend / price

    # Get step size for BTCUSDC
    info = client.get_symbol_info(SYMBOL)
    step_size = None
    for f in info['filters']:
        if f['filterType'] == 'LOT_SIZE':
            step_size = f['stepSize']
            break

    rounded_amount = round_step_size(raw_qty, step_size)
    print(rounded_amount)
    return rounded_amount


# 5. Round to correct step size (use exchange info)
def round_step_size(qty, stepsize):
    return float(f"{math.floor(float(qty) / float(stepsize)) * float(stepsize):f}")


def create_order(symbol, side, order_type, quantity):
    order = client.create_order(
        symbol=symbol,
        side=side,
        type=order_type,
        quantity=quantity
    )

    return order


def on_open(ws):
    """
    This is a callback function when the websocket connection is opened
    :param ws: WebSocket
    :return:
    """
    print("open connection")


def on_message(ws, message):
    """
    This is a callback function to retrieve data from the kLine timeframe endpoint.
    :param ws: WebSocket
    :param message: The data retrieved
    :return:
    """

    global closes
    global in_position

    try:
        json_string = json.loads(message)

        candle              = json_string['k']
        is_candle_closed    = candle['x']
        close               = candle['c']

        if is_candle_closed:
            print(f"candle closed at {close}")
            closes.append(float(close))

            candle = {
                'timestamp': pd.to_datetime(candle['t'], unit='ms'),
                'open': float(candle['o']),
                'high': float(candle['h']),
                'low': float(candle['l']),
                'close': float(candle['c']),
                'volume': float(candle['v']),
            }

            global df

            df = pd.concat([df, pd.DataFrame([candle])], ignore_index=True)
             # Print the latest candle

            if len(closes) > ATR_PERIOD:

                super_trend_data = super_trend(df)
                print(super_trend_data)

                previous_row = super_trend_data.iloc[-2]
                last_row = super_trend_data.iloc[-1]

                print("previous row: {}".format(previous_row))
                print("last row: {}".format(last_row))

                if not previous_row['in_uptrend'] and last_row['in_uptrend']:
                    print("Changed to uptrend, buy")

                    if not in_position:
                        order = create_order(SYMBOL, 'buy', ORDER_TYPE_MARKET, get_amount(PERCENTAGE))
                        # print(order)
                        in_position = True
                    else:
                        print("Already in position, nothing, to do")

                if previous_row['in_uptrend'] and not last_row['in_uptrend']:
                    print("Changed to downtrend, sell")

                    if in_position:
                        order = create_order(SYMBOL, 'sell', ORDER_TYPE_MARKET, quantity=rounded_amount)
                        in_position = False
                        print(order)
                    else:
                        print("You aren't in position nothing to Sell")
    except Exception as e:
        print(f"Something went wrong: {e}")



def on_close(ws):
    print("close connection")


ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()
