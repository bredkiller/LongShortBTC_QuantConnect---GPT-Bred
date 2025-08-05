# LongShortBTC_QuantConnect---GPT-Bred
Estratégia de Long &amp; Short beta-neutra aplicada a criptomoedas com dados da Kraken via QuantConnect.



# LongShortBTC_QuantConnect — GPT-Bred

📈 Estratégia de Long & Short beta-neutra aplicada ao mercado de criptomoedas com dados da Kraken, usando o motor da QuantConnect.

## 💡 Visão Geral

Esta estratégia:
- Usa BTC/USD como benchmark de risco
- Monta portfólios **dollar neutral** e **beta neutral**
- Otimiza alocações via `scipy.optimize.minimize` (método SLSQP)
- Faz rebalanceamento **trimestral**
- Seleciona os 10 criptoativos mais líquidos em USD, excluindo tokens extintos

## 📁 Estrutura dos Arquivos

| Arquivo | Função |
|--------|--------|
| `main.py` | Estrutura principal da estratégia no QuantConnect |
| `portfolio.py` | Modelo customizado de construção de portfólio beta-neutro |
| `optimizer.py` | Otimizador de média-variância com restrições de beta e retorno mínimo |
| `excluded_tokens.py` | Lista externa de tokens mortos/extintos a serem evitados |
| `README.md` | Esta documentação |

## ⚙️ Requisitos

- Conta no [QuantConnect](https://www.quantconnect.com/)
- Ambiente com acesso ao LEAN Engine (nuvem ou local)

## 🧪 Teste Rápido

Você pode rodar essa estratégia diretamente no ambiente da QuantConnect com o botão **"Run Backtest"** após importar os arquivos.

---

## 📜 Licença

Uso privado e educacional por enquanto. Nenhuma garantia de retorno ou segurança é oferecida.
