import pandas as pd
import numpy as np
import re
from sympy import diff, solveset, Eq, Interval, S
from sympy.abc import x,y
from math import *


p = re.compile('[\+|\-|*|/]')
math_operator = ["+", "-", "*", "/"]

def process_exp(func_str):
  e_index = func_str.find("e^")
  if (e_index >= 0):
    padd = 2
    if ( not(func_str[e_index + padd] == "(") ):
      k = p.search(func_str[e_index+padd:])
      if (k):
        i = e_index + padd + k.start()
        func_str = func_str[:i] + ")" + func_str[i:]
        func_str = func_str[:e_index] + "exp(" + func_str[e_index+padd:]
      else: #ya no encontro signo
        func_str = func_str[:e_index] + "exp(" + func_str[e_index+padd:] + ")"
    else:
      func_str = func_str[:e_index] + "exp" + func_str[e_index+padd:]
  if (func_str.find("e^") >= 0):
    func_str = process_exp(func_str)
    
  return func_str


def add_one_before_x(func_str):
  result_func = ""
  for i in range(len(func_str)):
    one = "1" if (func_str[i] == "x" and (i==0 or func_str[i-1] in math_operator) ) else ""
    result_func += one + func_str[i]
  return result_func


def replace_x(func_str):
  result_func = ""
  for i in range(len(func_str)):
    result_func += "*(x)" if (func_str[i] == "x" and func_str[i-1].isnumeric()) else func_str[i]
  return result_func


def transform_function(str_equ):
  str_equ = process_exp(str_equ)
  str_equ = add_one_before_x(str_equ)
  str_equ = replace_x(str_equ)

  # .replace("x", '*(x)')\
  strOut = str_equ\
          .replace("^", "**")
  # print("transform_function:", strOut)
  return strOut

  
#Evaluación REGREX
def evaluate_Fx(str_equ, valX):
  x = valX
  strOut = transform_function(str_equ)
  out = eval(strOut)
  #print("evaluate_Fx:::", strOut)
  return out

#Evaluación REGREX
def evaluate_derivate_Fx(str_equ, valX):
  x = valX
  strOut = transform_function(str_equ)
  strOut = derive_function(strOut)
  out = eval(strOut)
  #print("evaluate_derive_Fx:::", strOut)
  return out

def derive_function(str_equ):
  pattern1 = re.compile('\(x\)\*\*\d')
  pattern2 = re.compile('x\*\*\d')
  vars = pattern1.findall(str_equ) + pattern2.findall(str_equ)
  
  dictMap = {}
  for var in vars:
    out = var[-1] + '*' + var[0:-1] + '('+var[-1]+'-1)' 
    dictMap[var] = out
    
  for key, value in dictMap.items():
    str_equ = str_equ.replace(key, value)
  
  return str_equ
  
def derivar(str_equ, x):
  #dfx/dx
  strFx = str_equ.replace("x", '*(y)')
  strFx = strFx.replace("^", "**")
  dx = diff(strFx,y).subs(y,x) 
  return dx


#Deferencias finitas para derivadas
def evaluate_derivate_fx1(str_equ, x, h):
  x = float(x)
  h = float(h)
  
  dx = derivar(str_equ,x)
  
  #f(x0+h)
  strOut = str_equ.replace("x", '*(x + h)')
  strOut = strOut.replace("^", "**")
  out = eval(strOut)
  
  #f(x0-h)
  strOut = str_equ.replace("x", '*(x - h)')
  strOut = strOut.replace("^", "**")
  out = out - eval(strOut)
  
  #f(x0+h) - f(x0-h) / 2
  out = out/(2*h)
  
  datos = {'ValorReal':[float(dx)],
          'Aproximación':[out],
          'Error': [float(abs(dx-out))]}
  
  return pd.DataFrame(datos)

def evaluate_derivate_fx2(str_equ, x, h):
  x = float(x)
  h = float(h)
  
  dx = derivar(str_equ,x)
  
  strOut = str_equ.replace("x", '*(x + h)')
  strOut = strOut.replace("^", "**")
  strOut = "-4*(" + strOut + ")"
  out = eval(strOut)
  
  strOut = str_equ.replace("x", '*(x + 2*h)')
  strOut = strOut.replace("^", "**")
  out = out + eval(strOut)
  
  strOut = str_equ.replace("x", '*(x)')
  strOut = strOut.replace("^", "**")
  strOut = "3*(" + strOut + ")"
  out = out + eval(strOut)
  
  out = -out/(2*h)
  
  datos = {'ValorReal':[float(dx)],
          'Aproximación':[out],
          'Error': [float(abs(dx-out))]}
  
  return pd.DataFrame(datos)

def evaluate_derivate_fx3(str_equ, x, h):
  x = float(x)
  h = float(h)
  
  dx = derivar(str_equ,x)
  
  strOut = str_equ.replace("x", '*(x - 2*h)')
  strOut = strOut.replace("^", "**")
  out = eval(strOut)
  
  strOut = str_equ.replace("x", '*(x - h)')
  strOut = strOut.replace("^", "**")
  strOut = "8*(" + strOut + ")"
  out = out - eval(strOut)
  
  strOut = str_equ.replace("x", '*(x + h)')
  strOut = strOut.replace("^", "**")
  strOut = "8*(" + strOut + ")"
  out = out + eval(strOut)
  
  strOut = str_equ.replace("x", '*(x + 2*h)')
  strOut = strOut.replace("^", "**")
  out = out - eval(strOut)
  
  out = out/(12*h)
  datos = {'ValorReal':[float(dx)],
          'Aproximación':[out],
          'Error': [float(abs(dx-out))]}
  
  return pd.DataFrame(datos)


#Deferencias finitas para derivadas
def evaluate_derivate_fx(str_equ, x, h):
  x = float(x)
  h = float(h)
  
  #f(x0+h)
  strOut = str_equ.replace("x", '*(x + h)')
  strOut = strOut.replace("^", "**")
  out = eval(strOut)
  
  #f(x0-h)
  strOut = str_equ.replace("x", '*(x - h)')
  strOut = strOut.replace("^", "**")
  out = out - eval(strOut)
  
  #f(x0+h) - f(x0-h) / 2
  out = out/(2*h)
  
  return out

#Resolverdor de Newton
def newtonSolverX(x0, f_x, eps):
  x0 = float(x0)
  eps = float(eps)
  xn = x0
  error = 1
  arrayIters = []
  arrayF_x = []
  arrayf_x = []
  arrayXn = []
  arrayErr = []
  
  i = 0
  h = 0.000001
  while(error > eps):
    print("...")
    x_n1 = xn - (evaluate_Fx(f_x, xn)/evaluate_derivate_fx(f_x, xn, h))
    error = abs(x_n1 - xn)
    i = i + 1
    xn = x_n1
    arrayIters.append(i)
    arrayXn.append(xn)
    arrayErr.append(error)
    solution = [i, xn, error]

  print("Finalizo...")
  TableOut = pd.DataFrame({'Iter':arrayIters, 'Xn':arrayXn, 'Error': arrayErr})
  return TableOut

def add(a, b):
  a = int(a)
  b = int(b)
  resultado = a + b
  return "El resultado es: " + str(resultado)


#Deferencias finitas para derivadas
def evaluate_derivate_fx1XY(str_equ, x, y, h):
  x = float(x)
  y = float(y)
  h = float(h)
  
  #f(x0+h,y)
  ecuacionX1 = str_equ
  ecuacionX1 = ecuacionX1.replace("x", '*(x + h)')
  ecuacionX1 = ecuacionX1.replace("y", '*(y)')
  ecuacionX1 = ecuacionX1.replace("^", "**")
  outX = eval(ecuacionX1)
  
  #f(x0-h,y)
  ecuacionX2 = str_equ
  ecuacionX2 = ecuacionX2.replace("x", '*(x - h)')
  ecuacionX2 = ecuacionX2.replace("y", '*(y)')
  ecuacionX2 = ecuacionX2.replace("^", "**")
  outX = outX - eval(ecuacionX2)
  
  #f(x0+h,y) - f(x0-h,y) / 2h
  outX = outX/(2*h)
  
  #f(x0,y0+h)
  ecuacionY1 = str_equ
  ecuacionY1 = ecuacionY1.replace("y", '*(y + h)')
  ecuacionY1 = ecuacionY1.replace("x", '*(x)')
  ecuacionY1 = ecuacionY1.replace("^", "**")
  outY = eval(ecuacionY1)
  
  #f(x0,y0-h)
  ecuacionY2 = str_equ
  ecuacionY2 = ecuacionY2.replace("y", '*(y - h)')
  ecuacionY2 = ecuacionY2.replace("x", '*(x)')
  ecuacionY2 = ecuacionY2.replace("^", "**")
  outY = outY - eval(ecuacionY2)
  
  #f(x0,y0+h) - f(x0,y0-h) / 2h
  outY = outY/(2*h)
  
  datos = {'Aprox df/dx':[outX],
          'Aprox df/dy':[outY]}
  
  return pd.DataFrame(datos)


def evaluate_derivate_fx2XY(str_equ, x, y, h):
  x = float(x)
  y = float(y)
  h = float(h)
  
  #dx = derivar(str_equ,x)
  dx=0
  
  ecuacionX = str_equ
  ecuacionX = ecuacionX.replace("x", '*(x + h)')
  ecuacionX = ecuacionX.replace("y", '*(y)')
  ecuacionX = ecuacionX.replace("^", "**")
  ecuacionX = "-4*(" + ecuacionX + ")"
  outX = eval(ecuacionX)
  
  ecuacionX = str_equ
  ecuacionX = ecuacionX.replace("x", '*(x + 2*h)')
  ecuacionX = ecuacionX.replace("y", '*(y)')
  ecuacionX = ecuacionX.replace("^", "**")
  outX = outX + eval(ecuacionX)
  
  ecuacionX = str_equ
  ecuacionX = ecuacionX.replace("x", '*(x)')
  ecuacionX = ecuacionX.replace("y", '*(y)')
  ecuacionX = ecuacionX.replace("^", "**")
  ecuacionX = "3*(" + ecuacionX + ")"
  outX = outX + eval(ecuacionX)
  
  outX = -outX/(2*h)
  
  ecuacionY = str_equ
  ecuacionY = ecuacionY.replace("y", '*(y + h)')
  ecuacionY = ecuacionY.replace("x", '*(x)')
  ecuacionY = ecuacionY.replace("^", "**")
  ecuacionY = "-4*(" + ecuacionY + ")"
  outY = eval(ecuacionY)
  
  ecuacionY = str_equ
  ecuacionY = ecuacionY.replace("y", '*(y + 2*h)')
  ecuacionY = ecuacionY.replace("x", '*(x)')
  ecuacionY = ecuacionY.replace("^", "**")
  outY = outY + eval(ecuacionY)
  
  ecuacionY = str_equ
  ecuacionY = ecuacionY.replace("x", '*(x)')
  ecuacionY = ecuacionY.replace("y", '*(y)')
  ecuacionY = ecuacionY.replace("^", "**")
  ecuacionY = "3*(" + ecuacionY + ")"
  outY = outY + eval(ecuacionY)
  
  outY = -outY/(2*h)
  
  datos = {'ValorReal df/dx':[float(dx)],
           'ValorReal df/dy':[float(dx)],
          'Aprox df/dx':[outX],
          'Aprox df/dy':[outY],
          'Norma': [float(np.sqrt(outX**2+outY**2))]}
  
  return pd.DataFrame(datos)


def evaluate_derivate_fx3XY(str_equ, x, y, h):
  x = float(x)
  y = float(y)
  h = float(h)
  
  #dx = derivar(str_equ,x)
  dx=0
  
  
  ecuacionX = str_equ
  ecuacionX = ecuacionX.replace("x", '*(x - 2*h)')
  ecuacionX = ecuacionX.replace("y",'*(y)')
  ecuacionX = ecuacionX.replace("^", "**")
  outX = eval(ecuacionX)
  
  ecuacionX = str_equ
  ecuacionX = ecuacionX.replace("x", '*(x - h)')
  ecuacionX = ecuacionX.replace("y",'*(y)')
  ecuacionX = ecuacionX.replace("^", "**")
  ecuacionX = "8*(" + ecuacionX + ")"
  outX = outX - eval(ecuacionX)
  
  ecuacionX = str_equ
  ecuacionX = ecuacionX.replace("x", '*(x + h)')
  ecuacionX = ecuacionX.replace("y",'*(y)')
  ecuacionX = ecuacionX.replace("^", "**")
  ecuacionX = "8*(" + ecuacionX + ")"
  outX = outX + eval(ecuacionX)
  
  ecuacionX = str_equ
  ecuacionX = ecuacionX.replace("x", '*(x + 2*h)')
  ecuacionX = ecuacionX.replace("y",'*(y)')
  ecuacionX = ecuacionX.replace("^", "**")
  outX = outX - eval(ecuacionX)
  
  outX = outX/(12*h)
  
  ecuacionY = str_equ
  ecuacionY = ecuacionY.replace("y", '*(y - 2*h)')
  ecuacionY = ecuacionY.replace("x",'*(x)')
  ecuacionY = ecuacionY.replace("^", "**")
  outY = eval(ecuacionY)
  
  ecuacionY = str_equ
  ecuacionY = ecuacionY.replace("y", '*(y - h)')
  ecuacionY = ecuacionY.replace("x",'*(x)')
  ecuacionY = ecuacionY.replace("^", "**")
  ecuacionY = "8*(" + ecuacionY + ")"
  outY = outY - eval(ecuacionY)
  
  ecuacionY = str_equ
  ecuacionY = ecuacionY.replace("y", '*(y + h)')
  ecuacionY = ecuacionY.replace("x",'*(x)')
  ecuacionY = ecuacionY.replace("^", "**")
  ecuacionY = "8*(" + ecuacionY + ")"
  outY = outY + eval(ecuacionY)
  
  ecuacionY = str_equ
  ecuacionY = ecuacionY.replace("y", '*(y + 2*h)')
  ecuacionY = ecuacionY.replace("x",'*(x)')
  ecuacionY = ecuacionY.replace("^", "**")
  outY = outY - eval(ecuacionY)
  
  outY = outY/(12*h)
  
  datos = {'ValorReal df/dx':[float(dx)],
           'ValorReal df/dy':[float(dx)],
          'Aprox df/dx':[outX],
          'Aprox df/dy':[outY],
          'Norma': [float(np.sqrt(outX**2+outY**2))]}
  
  return pd.DataFrame(datos)


"""
Ejecuta y evalua el metodo de biseccion.
PARAMETROS:
  f_x, 
  a, 
  b, 
  kmax, 
  tolerance
Retorna un pandas.dataframe con los valores de las iteraciones.
"""
def evaluate_bisection(f_x, a, b, kmax, tolerance):
  a = float(a)
  b = float(b)
  f_a = float(evaluate_Fx(f_x, a))
  f_b = float(evaluate_Fx(f_x, b))
  dict_result= {'Iteracion':[],
                'Xk':[],
                'Error':[]}
  if ((f_a*f_b) > 0):
    return pd.DataFrame.from_dict(dict_result)
  kmax = float(kmax)
  tolerance = float(tolerance)
  k = 0
  xk = (a+b)/2
  f_xk = evaluate_Fx(f_x, xk)
  # transformed_fx = transform_function(f_x) 
  # equation = Eq(*S(transformed_fx+", 0"))
  # rootss = solveset(equation, x, Interval(a,b))
  # real_x = eval(str( tuple(rootss)[0] ))
  while k < kmax and abs(f_xk) > tolerance:
    f_a = evaluate_Fx(f_x, a)
    # print("k:",k, "  a:",a, "\tb",b, "\txk:",xk, "\tf_xk:",f_xk, "\tf_a:",f_a)
    if (f_a*f_xk < 0):
      b = xk
    else:
      a = xk
    k += 1
    dict_result["Iteracion"].append(int(k))
    dict_result["Xk"].append(float(xk))
    dict_result["Error"].append(float(abs(f_xk)))
    xk = (a+b)/2
    f_xk = evaluate_Fx(f_x, xk)

  return pd.DataFrame.from_dict(dict_result)

"""
Ejecuta y evalua el metodo de Newton Raphson.
PARAMETROS:
  f_x, 
  x, 
  kmax, 
  tolerance
Retorna un pandas.dataframe con los valores de las iteraciones.
"""
def evaluate_NR(f_x, x, kmax, tolerance):
  x = float(x)
  kmax = float(kmax)
  tolerance = float(tolerance)
  F_x = float(evaluate_Fx(f_x, x))
  k = 0
  
  dict_result= {'Iteracion':[],
                'Xk':[],
                'Error':[]}
  
  while k < kmax and abs(F_x) > tolerance:
    x -= evaluate_Fx(f_x, x)/evaluate_derivate_Fx(f_x, x)
    k += 1
    
    dict_result["Iteracion"].append(int(k))
    dict_result["Xk"].append(float(x))
    dict_result["Error"].append(float(abs(F_x)))
    
    F_x = float(evaluate_Fx(f_x, x))
  
  return pd.DataFrame.from_dict(dict_result)


"""
"""
def evaluate_gd(q, c, e, n, xo):
  q = np.matrix(q, dtype=float)
  c = np.matrix(c, dtype=float)
  e = float(e)
  n = int(n)
  xo = np.matrix(xo, dtype=float)
  dict_result= {'k':[],
                'Xk':[],
                'Pk':[],
                'GDf(Xk)':[]}
  return pd.DataFrame.from_dict(dict_result)



def evaluate_rosenbrock(xo, a):
  xo = np.matrix(xo, dtype=float)
  a = float(a)
  dict_result= {'k':[],
                'Xk':[],
                'Pk':[],
                'GDf(Xk)':[]}
  return pd.DataFrame.from_dict(dict_result)


