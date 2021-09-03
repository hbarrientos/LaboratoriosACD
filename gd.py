import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class GD:
    """Clase que realiza todos los cálculos
    del algortimo de Gradient Descent"""
    
    def __init__(self, Q, x, c, error, kmax, step):
        """Inicialización de clase"""
        
        self.Q = eval('np.array('+Q+')')
        self.x = eval('np.array('+x+')')
        self.c = eval('np.array('+c+')')
        self.error = float(eval(error))
        self.kmax = int(kmax)
        self.step = float(step)
        self.results = None
        
    def p(self):
        """Cálculo de p"""
        g = -np.matmul(self.Q,self.x) + self.c
        return g,np.array([g])

    def L1(self):
        """Cálculo de Norma L1"""
        g,_ = self.p()
        return np.sum(abs(g))
    
    def alpha(self):
        """Cálculo del alpha"""
        g, gT = self.p()
        return np.matmul(gT,g) / np.matmul(np.matmul(gT,self.Q),g)
    
   
    def algorithm(self):
        
        """
            Cálculo del Algoritmo Gradient Descent
            Q = Matriz Cuadrática
            x = Xo
            c = Constante
            error = epsilon
            step = 0: step size exacto (default)
                   >1: step size variable
                   todo lo demás: step size constante
        """
        
        resultados = {'k':[],
                      'xk':[],
                      'pk':[],
                      'grad_fxk':[]}

        for k in range(1,self.kmax+1):
            e = self.L1()
        
            if e < self.error:
                break
            else:
            
                pk,_ = self.p()
            
                resultados['k'].append(k-1)
                resultados['xk'].append(str(self.x))
                resultados['pk'].append(str(pk))
                resultados['grad_fxk'].append(e)
            
                if self.step == 0:
                    self.x = self.x + self.alpha() * pk
                elif self.step > 1:
                    self.x = self.x + 1/k * pk
                else:
                    self.x = self.x + self.step * pk
                k+=1
            
        self.results = pd.DataFrame.from_dict(resultados)
    
    def iterations(self):
        """Devuelve la tabla de iteraciones"""
        return self.results
    
    def plot(self):
        plt.plot(np.array(self.results.k), np.array(self.results.grad_fxk), linewidth = '2')
        plt.xlabel("k (iterations)")
        plt.ylabel("||f'(xk)||")
        plt.title("Gradiente Descent")
        plt.savefig("plot.png")
