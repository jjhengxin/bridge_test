import backtrader as bt

class MovingAverageCrossStrategy(bt.Strategy):
    params = dict(
        short_window=12,
        long_window=26
    )

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None

        self.sma_short = bt.indicators.SimpleMovingAverage(
            self.datas[0].close, period=self.params.short_window)
        self.sma_long = bt.indicators.SimpleMovingAverage(
            self.datas[0].close, period=self.params.long_window)

    def next(self):
        if self.order:
            return

        if not self.position:
            if self.sma_short[0] > self.sma_long[0] and self.sma_short[-1] <= self.sma_long[-1]:
                size = int(self.broker.getcash() * 0.2 / self.dataclose[0])
                self.order = self.buy(size=size)
        else:
            if self.dataclose[0] < self.sma_long[0]:
                self.order = self.sell()