# region imports
from AlgorithmImports import *
from scipy.optimize import minimize
# endregion

class BetaNeutralMeanVarianceOptimizer:
    '''Otimiza pesos de portfólio com restrição de beta neutro e retorno mínimo'''

    def __init__(self, 
                 algorithm,
                 minimum_weight = -1, 
                 maximum_weight = 1,
                 minimum_return = 0.02):
        self.algorithm = algorithm
        self.minimum_weight = minimum_weight
        self.maximum_weight = maximum_weight
        self.minimumReturn = minimum_return

    def Optimize(self, historicalReturns, historicalBeta, expectedReturns = None, covariance = None):
        if covariance is None:
            covariance = historicalReturns.cov()
        if expectedReturns is None:
            expectedReturns = historicalReturns.mean()

        size = historicalReturns.columns.size
        beta = np.array([historicalBeta[symbol].Current.Value for symbol in historicalReturns.columns]).reshape(-1, 1)
        x0 = np.array(size * [1. / size])

        constraints = [
            {'type': 'eq', 'fun': lambda weights: self.get_abs_budget_constraint(weights)},
            {'type': 'eq', 'fun': lambda weights: self.get_beta_constraint(weights, beta)},
            {'type': 'eq', 'fun': lambda weights: self.get_budget_constraint(weights)},
            {'type': 'ineq', 'fun': lambda weights: self.get_min_return(weights, expectedReturns)}
        ]

        opt = minimize(lambda x: self.get_objective(x, covariance),
                       x0,
                       bounds = self.get_boundary_conditions(size),
                       constraints = constraints,
                       method = 'SLSQP')

        if not opt['success']:
            self.algorithm.Log(f"Optimizer falhou: {opt['message']} — retornando pesos iguais")
            return x0

        return opt['x']

    def get_objective(self, weights, covariance):
        '''Função objetivo: minimizar variância da carteira'''
        return 0.5 * weights.T @ covariance @ weights

    def get_boundary_conditions(self, size):
        '''Limites para os pesos: long e short'''
        return tuple((self.minimum_weight, self.maximum_weight) for _ in range(size))

    def get_abs_budget_constraint(self, weights):
        '''Soma dos valores absolutos dos pesos = 1'''
        return np.sum(np.abs(weights)) - 1

    def get_budget_constraint(self, weights):
        '''Portfólio dollar neutral (soma dos pesos = 0)'''
        return np.sum(weights)

    def get_beta_constraint(self, weights, beta):
        '''Beta neutro'''
        return weights.T @ beta

    def get_min_return(self, weights, expectedReturns):
        '''Retorno mínimo exigido'''
        return weights.T @ expectedReturns - self.minimumReturn
