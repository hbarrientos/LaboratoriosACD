import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Newton:
    """Clase que realiza calculo el mínimo de la
    Función Rosenbrock's con el algortimo de
    Newton"""
    
    def __init__(self, x, error, kmax, step = '1'):
        """Inicialización de clase"""
        
        self.function = '100*(x[1]-x[0]**2)**2 + (1-x[0])**2'
        self.df1_dx = '2*(200*self.x[0]**3 - 200*self.x[0]*self.x[1] + self.x[0] - 1)'
        self.df1_dy = '200*(self.x[1]-self.x[0]**2)'
        self.df2_11_dx = '1200*self.x[0]**2-400*self.x[1]+2'
        self.df2_12_dy = '-400*self.x[0]'
        self.df2_22_dy = '200'
        self.x = eval('np.array('+x+')')
        self.error = float(eval(error))
        self.kmax = int(kmax)
        self.step = float(step)
        self.results = None
        
    def p(self):
        """Cálculo de p"""
        g = np.array([eval(self.df1_dx), eval(self.df1_dy)])

        hessianInverse = np.linalg.inv(np.array([[eval(self.df2_11_dx), eval(self.df2_12_dy)],
                                  [eval(self.df2_12_dy), eval(self.df2_22_dy)]]))
        return -np.matmul(hessianInverse,g), np.array([np.matmul(hessianInverse,g)])

    def L1(self):
        """Cálculo de Norma L1"""
        g,_ = self.p()
        return np.sum(abs(g))
    
    def alpha(self):
        """Cálculo del alpha"""

        # Init values
        alpha = 1
        ro = 1/2
        c = 10**-4

        # Gradient, Gradient T
        g, gT = self.p()

        x = self.x + alpha*g
        fx_i = eval(self.function)

        x = self.x
        fx_d = eval(self.function) + c*alpha*np.matmul(gT,g)[0]

        while fx_i > fx_d: #Armijo Condition
          alpha = ro*alpha
          
          x = self.x + alpha*g
          fx_i = eval(self.function)

          x = self.x
          fx_d = eval(self.function) + c*alpha*np.matmul(gT,g)[0]
    
        return alpha
    
   
    def algorithm(self):
        
        """
            Cálculo del Algoritmo Newton
            para la Función Rosenbrock
            
            x = Xo
            error = epsilon
            step = 1: step size unitario
                  otro valor: Backtracking"""
        
        resultados = {'k':[],
                      'xk':[],
                      'pk':[],
                      'grad_fx_k':[]}

        for k in range(1,self.kmax+1):
            e = self.L1()
            
            if e < self.error:
                break
            else:
            
                pk,_ = self.p()
                
                resultados['k'].append(k-1)
                resultados['xk'].append(str(self.x))
                resultados['pk'].append(str(pk))
                resultados['grad_fx_k'].append(e)
            
                if self.step == 1:
                  self.x = self.x + pk
                else:
                  self.x = self.x + self.alpha() * pk
           
        self.results = pd.DataFrame.from_dict(resultados)
    
    def iterations(self):
        """Devuelve la tabla de iteraciones"""
        return self.results
    
    def plot(self):
        plt.plot(np.array(self.results.k), np.array(self.results.grad_fx_k), linewidth = '2')
        plt.xlabel("k (iterations)")
        plt.ylabel("||f'(xk)||")
        plt.title("Gradiente Descent")
