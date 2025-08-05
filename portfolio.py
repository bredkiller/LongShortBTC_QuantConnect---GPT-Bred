#region imports
from AlgorithmImports import *
from optimizer import BetaNeutralMeanVarianceOptimizer
#endregion

class BetaNeutralMeanVariancePortfolioConstructionModel(PortfolioConstructionModel):
    def __init__(self,
                 algorithm,
                 benchmark,
                 rebalance = Expiry.EndOfQuarter,
                 portfolioBias = PortfolioBias.LongShort,
                 lookback = 1,
                 period = 252,
                 resolution = Resolution.Daily):
        super().__init__()
        self.algorithm = algorithm
        self.benchmark = benchmark
        self.lookback = lookback
        self.period = period
        self.resolution = resolution
        self.portfolioBias = portfolioBias
        self.sign = lambda x: -1 if x < 0 else (1 if x > 0 else 0)

        lower = 0 if portfolioBias == PortfolioBias.Long else -1
        upper = 0 if portfolioBias == PortfolioBias.Short else 1
        self.optimizer = BetaNeutralMeanVarianceOptimizer(algorithm, lower, upper)

        self.symbolDataBySymbol = {}

        rebalancingFunc = rebalance
        if isinstance(rebalance, int):
            rebalance = Extensions.ToTimeSpan(rebalance)
        if isinstance(rebalance, timedelta):
            rebalancingFunc = lambda dt: dt + rebalance
        if rebalancingFunc:
            self.SetRebalancingFunc(rebalancingFunc)

    def DetermineTargetPercent(self, activeInsights):
        targets = {}
        if len(activeInsights) == 0:
            self.algorithm.Log("No active insights, returning empty target")
            return targets

        symbols = [insight.Symbol for insight in activeInsights]

        beta = {}
        returns = {}
        for symbol, data in self.symbolDataBySymbol.items():
            if symbol in symbols:
                beta[str(symbol.ID)] = data.beta
                returns[str(symbol.ID)] = data.Return
        returns = pd.DataFrame(returns)

        weights = self.optimizer.Optimize(returns, beta)
        weights = pd.Series(weights, index = returns.columns)

        for insight in activeInsights:
            sid = str(insight.Symbol.ID)
            if sid not in weights:
                continue
            weight = weights[sid]

            if self.portfolioBias != PortfolioBias.LongShort and self.sign(weight) != self.portfolioBias:
                weight = 0
            targets[insight] = weight

        return targets

    def OnSecuritiesChanged(self, algorithm, changes):
        algorithm.Log(f"PortfolioConstructionModel.OnSecuritiesChanged: {changes}")

        super().OnSecuritiesChanged(algorithm, changes)
        for removed in changes.RemovedSecurities:
            symbolData = self.symbolDataBySymbol.pop(removed.Symbol, None)
            if symbolData:
                symbolData.Dispose()

        for added in changes.AddedSecurities:
            symbol = added.Symbol
            if symbol not in self.symbolDataBySymbol and symbol != self.benchmark:
                symbolData = self.SymbolData(algorithm, symbol, self.benchmark, self.lookback, self.period, self.resolution)
                self.symbolDataBySymbol[symbol] = symbolData

    class SymbolData:
        def __init__(self, algorithm, symbol, benchmark, lookback, period, resolution):
            self.algorithm = algorithm
            self.symbol = symbol
            self.benchmark = benchmark

            self.window = RollingWindow[IndicatorDataPoint](period)
            self.roc = RateOfChange(f'{symbol}.ROC({lookback})', lookback)
            self.roc.Updated += self.OnRateOfChangeUpdated
            self.beta = Beta("Beta", period, symbol, benchmark)

            self.consolidator1 = TradeBarConsolidator(timedelta(1))
            self.consolidator2 = TradeBarConsolidator(timedelta(1))

            algorithm.RegisterIndicator(symbol, self.roc, self.consolidator1)
            algorithm.RegisterIndicator(symbol, self.beta, self.consolidator1)
            algorithm.RegisterIndicator(benchmark, self.beta, self.consolidator2)

            history = algorithm.History[TradeBar](symbol, lookback * period, resolution)
            benchmark_history = algorithm.History[TradeBar](benchmark, lookback * period, resolution)
            for bar, benchmark_bar in zip(history, benchmark_history):
                self.roc.Update(IndicatorDataPoint(bar.EndTime, bar.Close))
                self.beta.Update(bar)
                self.beta.Update(benchmark_bar)

        def Dispose(self):
            self.roc.Updated -= self.OnRateOfChangeUpdated
            self.roc.Reset()
            self.beta.Reset()
            self.window.Reset()

        def OnRateOfChangeUpdated(self, roc, value):
            if roc.IsReady:
                self.window.Add(IndicatorDataPoint(value.EndTime, value.Value))

        @property
        def Return(self):
            return pd.Series(
                data = [x.Value for x in self.window],
                index = [x.EndTime for x in self.window])

        @property
        def IsReady(self):
            return self.window.IsReady
