class LongShortBitcoinBeta(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2020, 1, 1)
        self.SetEndDate(datetime.now())
        self.SetCash(25000)

        self.SetBrokerageModel(BrokerageName.Kraken, AccountType.Margin)

        self.benchmark_symbol = self.AddCrypto("BTCUSD", Resolution.Hour, Market.Kraken).Symbol
        self.SetBenchmark(self.benchmark_symbol)

        self.UniverseSettings.Resolution = Resolution.Minute
        self.AddUniverse(CryptoCoarseFundamentalUniverse(Market.Kraken, self.UniverseSettings, self.UniverseSelectionFilter))

        self.AddAlpha(ConstantAlphaModel(InsightType.Price, InsightDirection.Up, timedelta(90)))

        pcm = BetaNeutralMeanVariancePortfolioConstructionModel(
            algorithm=self,
            benchmark=self.benchmark_symbol,
            period=365*3,
            resolution=Resolution.Daily
        )
        self.SetPortfolioConstruction(pcm)

        self.SetExecution(ImmediateExecutionModel())
        self.SetRiskManagement(NullRiskManagementModel())

    def UniverseSelectionFilter(self, coarse):
        valid = [x for x in coarse if x.Price > 0 and x.Volume > 0]
        sortedByDollarVol = sorted(valid, key=lambda x: x.Price * x.Volume, reverse=True)
        return [x.Symbol for x in sortedByDollarVol[:10]]
