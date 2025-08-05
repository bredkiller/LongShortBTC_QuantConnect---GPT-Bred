# region imports
from AlgorithmImports import *
from portfolio import BetaNeutralMeanVariancePortfolioConstructionModel
# endregion

class LongShortBitcoinBeta(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2018, 8, 5)
        self.SetEndDate(datetime.now())
        self.SetCash(1000000)  # Set Strategy Cash

        self.SetBrokerageModel(BrokerageName.Kraken, AccountType.Margin)

        # Definindo o benchmark como BTC/USD
        btc = self.AddCrypto("BTCUSD", Resolution.Hour, Market.Kraken).Symbol
        self.SetBenchmark(btc)

        # Universo dinâmico baseado em volume, com filtro de tokens mortos
        self.UniverseSettings.Resolution = Resolution.Minute
        self.AddUniverse(CryptoCoarseFundamentalUniverse(Market.Kraken, self.UniverseSettings, self.UniverseSelectionFilter))

        # Modelo de Alpha simples para ativar entradas simuladas
        self.AddAlpha(ConstantAlphaModel(InsightType.Price, InsightDirection.Up, timedelta(90)))

        # Construtor de portfólio customizado (já implementado no arquivo portfolio.py)
        pcm = BetaNeutralMeanVariancePortfolioConstructionModel(
            algorithm=self,
            benchmark=self.benchmark,
            period=365*3,
            resolution=Resolution.Daily
        )
        self.SetPortfolioConstruction(pcm)

        # Execution e risco simples por enquanto
        self.SetExecution(ImmediateExecutionModel())
        self.SetRiskManagement(NullRiskManagementModel())

    def UniverseSelectionFilter(self, coarse):
        return [x.Symbol for x in sorted(coarse, key=lambda x: x.DollarVolume, reverse=True)[:10]]
