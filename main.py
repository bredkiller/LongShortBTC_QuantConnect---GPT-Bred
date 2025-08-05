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
        self.benchmark = self.AddCrypto("BTCUSD", Resolution.Minute, Market.Kraken).Symbol

        # Universo dinâmico baseado em volume, com filtro de tokens mortos
        self.UniverseSettings.Resolution = Resolution.Minute
        self.AddUniverse(CryptoCoarseFundamentalUniverse(Market.Kraken, self.UniverseSettings, self.UniverseSelectionFilter))

        # Modelo de Alpha simples para ativar entradas
        self.AddAlpha(ConstantAlphaModel(InsightType.Price, InsightDirection.Up, timedelta(90)))

        # Construtor de portfólio customizado (a ser implementado no arquivo portfolio.py)
        pcm = BetaNeutralMeanVariancePortfolioConstructionModel(
            algorithm=self,
            benchmark=self.benchmark,
            period=365*3,
            resolution=Resolution.Daily
        )
        pcm.RebalanceOnSecurityChanges = False
        self.SetPortfolioConstruction(pcm)

        self.SetWarmup(30)

        # Inicializa próxima data de rebalanceamento
        self.RebalancingTime = datetime.min

        # Tokens que devem ser excluídos (mortos, extintos, hackeados ou descontinuados)
        self.excluded_tokens = {
            "FTTUSD", "LUNCUSD", "USTUSD", "VGXUSD", "TITANUSD",
            "YAMUSD", "BCCUSD", "MIRUSD", "ICXUSD", "HOTUSD",
            "AMPUSD", "STRKUSD"
        }

    def UniverseSelectionFilter(self, data):
        # Evita rebalancear constantemente
        if self.RebalancingTime > self.Time:
            return Universe.Unchanged

        # Filtrar apenas pares USD e tokens ativos
        filtered = [
            x for x in data
            if x.Symbol.Value.endswith("USD") and self.is_token_active(x.Symbol)
        ]

        # Selecionar os 10 com maior volume
        top_10 = sorted(
            filtered,
            key=lambda x: x.VolumeInUsd,
            reverse=True
        )[:10]

        # Agendar próximo rebalanceamento para o fim do trimestre
        self.RebalancingTime = Expiry.EndOfQuarter(self.Time)

        self.Log(f"Selecionados para o universo: {[x.Symbol.Value for x in top_10]}")
        return [x.Symbol for x in top_10]

    def is_token_active(self, symbol: Symbol) -> bool:
        """
        Função genérica para checar se o token é considerado 'ativo',
        baseado na lista interna de exclusões. Pode ser reaproveitada em qualquer análise.
        """
        symbol_str = symbol.Value.upper()
        return symbol_str not in self.excluded_tokens
