# region imports
from AlgorithmImports import *
from datetime import timedelta
from portfolio import BetaNeutralMeanVariancePortfolioConstructionModel
# endregion

class LongShortBitcoinBeta(QCAlgorithm):

    def Initialize(self):
        # Parâmetros iniciais
        self.SetStartDate(2020, 1, 1)
        self.SetEndDate(datetime.now())
        self.SetCash(25000)

        # Exchange e tipo de conta
        self.SetBrokerageModel(BrokerageName.Kraken, AccountType.Margin)

        # Benchmark definido como BTC/USD (Kraken)
        btc = self.AddCrypto("BTCUSD", Resolution.Hour, Market.Kraken).Symbol
        self.SetBenchmark(btc)

        # Universo dinâmico baseado em volume (filtrando tokens mortos)
        self.UniverseSettings.Resolution = Resolution.Minute
        self.AddUniverse(CryptoCoarseFundamentalUniverse(Market.Kraken, self.UniverseSettings, self.UniverseSelectionFilter))

        # Alpha simples com sinal de compra a cada 90 dias
        self.AddAlpha(ConstantAlphaModel(InsightType.Price, InsightDirection.Up, timedelta(90)))

        # Modelo de portfólio externo (arquivo portfolio.py)
        pcm = BetaNeutralMeanVariancePortfolioConstructionModel(
            algorithm=self,
            benchmark=self.benchmark,
            period=365*3,
            resolution=Resolution.Daily
        )
        self.SetPortfolioConstruction(pcm)

    # Filtro do universo: tokens com volume e preço válidos
    def UniverseSelectionFilter(self, coarse):
        filtered = [x for x in coarse if x.Price is not None and x.Volume is not None]
        sorted_by_volume = sorted(filtered, key=lambda x: x.Price * x.Volume, reverse=True)
        return [x.Symbol for x in sorted_by_volume[:10]]
