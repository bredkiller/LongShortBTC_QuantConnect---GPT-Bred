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






para o futuro:
seria muito bom incluir:
Receber um analyzer.py para interpretar seus logs e gerar métricas? sim

Rodar a mesma estratégia com IA em vez de ConstantAlpha? sim

Ativar visualização interativa dos pesos otimizados ao longo do tempo? sim


 e mais, podemos adicionar uma função de análise de métricas personalizadas, como:

Sharpe Ratio

Sortino Ratio

Máximo de ativos simultâneos

Porcentagem do capital alocado por operação

% de trades positivos vs negativos











Ações que vou montar para você (por etapas)
📦 Etapa 1 – analyzer.py para interpretar os logs e gerar métricas:
Será um script que:

Lê os logs do QuantConnect (via exportação ou arquivo)

Gera:

✅ Sharpe Ratio

✅ Sortino Ratio

✅ % de trades vencedores

✅ Capital alocado por ativo

✅ Ativos simultâneos ao longo do tempo

✅ Gráfico de curva de capital com anotação de rebalanceamento

🤖 Etapa 2 – Substituir ConstantAlphaModel por IA:
Implementação de um modelo de Machine Learning leve (ex: LogisticRegression ou RandomForest)

Treinamento direto no Research Notebook do QuantConnect

A IA gerará sinais de InsightDirection.Up ou Down com base em features como:

Retornos passados

Volatilidade

Posição relativa às médias

Volume

📊 Etapa 3 – Visualização dos pesos otimizados ao longo do tempo:
Criação de gráfico interativo (via matplotlib ou plotly)

Exportação dos pesos alocados por ativo a cada rebalanceamento

Integração com analyzer.py

📈 Etapa 4 – Métricas customizadas no backtest:
Função embutida no main.py (ou novo metrics.py) para:

Calcular Sharpe e Sortino no final do backtest

Registrar número de trades, vencedores vs perdedores

Avaliar uso de capital por operação

Medir ativos em carteira em cada rebalanceamento

🚀 O que preciso de você agora:
Deseja que o analyzer.py seja usado fora da QuantConnect (local com pandas) ou quer integrá-lo dentro do ambiente da QC?

Confirma que prefere começar com IA simples (ex: LogisticRegression) antes de evoluir para algo mais pesado como XGBoost?

Pode me enviar um trecho de log exportado da sua execução no QC (ou me contar quais colunas aparecem no log), caso queira que o analyzer.py processe isso automaticamente?

Assim que você me confirmar esses pontos, começo a montar o analyzer.py e a substituição do AlphaModel por IA. Pronto?




























