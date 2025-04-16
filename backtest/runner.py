import backtrader as bt
import pandas as pd
import tushare as ts
import json
from datetime import datetime
from strategy import MovingAverageCrossStrategy


def run_backtest(symbol, start_date, end_date, tushare_token):
    # dataset downloading 
    ts.set_token(tushare_token)
    pro = ts.pro_api()

    df = pro.daily(ts_code=symbol, start_date=start_date.replace('-', ''), end_date=end_date.replace('-', ''))
    df['trade_date'] = pd.to_datetime(df['trade_date'])
    df = df.sort_values('trade_date')

    data = bt.feeds.PandasData(dataname=df, datetime='trade_date', open='open', high='high', low='low', close='close', volume='vol')

    # back_test
    cerebro = bt.Cerebro()
    cerebro.broker.set_cash(1_000_000)
    cerebro.broker.set_slippage_perc(0.0001)
    cerebro.adddata(data)
    cerebro.addstrategy(MovingAverageCrossStrategy) # strategy module
    cerebro.run()

    final_value = cerebro.broker.getvalue()
    total_return = (final_value - 1_000_000) / 1_000_000

    result = {
        "total_return": round(total_return, 4),
        "final_equity": round(final_value, 2)
    }
    print(result)

    with open("backtest/result.json", "w") as f:
        json.dump(result, f)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 5:
        print("Usage: python runner.py <symbol> <start_date> <end_date> <tushare_token>")
        sys.exit(1)

    symbol = sys.argv[1]
    start_date = sys.argv[2]
    end_date = sys.argv[3]
    tushare_token = sys.argv[4]

    print(f"Starting backtest for {symbol} from {start_date} to {end_date}...")

    run_backtest(symbol, start_date, end_date, tushare_token)
