import pandas
import numpy as np
import re
from sympy import diff
from sympy.abc import x,y

#Evaluación REGREX
def evaluate_Fx(str_equ, valX):
  x = valX
  strOut = str_equ.replace("x", '*(x)')
  strOut = strOut.replace("^", "**")
  out = eval(strOut)
  print(strOut)

  return out

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
  
  return pandas.DataFrame(datos)

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
  
  return pandas.DataFrame(datos)

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
  
  return pandas.DataFrame(datos)


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
  TableOut = pandas.DataFrame({'Iter':arrayIters, 'Xn':arrayXn, 'Error': arrayErr})
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
  
  return pandas.DataFrame(datos)

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
  
  return pandas.DataFrame(datos)


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
  
  return pandas.DataFrame(datos)
