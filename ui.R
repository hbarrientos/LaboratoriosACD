library(shiny)
library(shinydashboard)
library(shinyjs)

# Define UI for application that draws a histogram
dashboardPage(
    dashboardHeader(title = "Algoritmos en la Ciencia de Datos"),
    dashboardSidebar(
        sidebarMenu(
            menuItem("Ceros", tabName = "Ceros"),
            menuItem("Derivacion f(X)", tabName = "DerivacionX"),
            menuItem("Derivacion f(X,Y)", tabName = "DerivacionXY"),
            menuItem("Bisecci\u00F3n f(X)", tabName = "bisection"),
            menuItem("Newton Raphson f(X)", tabName = "newtonraphson"),
            menuItem("Funci\u00F3n de Rosenbrock f(x,y)", tabName = "rosenbrock_function")
        )
    ),
    dashboardBody(
        tabItems(
            tabItem("Ceros",
                    h1("Método de Newton"),
                    box(textInput("ecuacion", "Ingrese la Ecuación"),
                        textInput("initVal", "X0"),
                        textInput("Error", "Error")),
                    actionButton("nwtSolver", "Newton Solver"),
                    tableOutput("salidaTabla")),
            
            tabItem("DerivacionX",
                    h1("Diferencias Finitas f(x)"),
                    box(radioButtons("algoritmo", label = h3("Algortimo"),
                                     choices = list("Centradas (1)" = 1,
                                                    "Progresivas" = 2,
                                                    "Centradas (2)" = 3)),
                        textInput("difFinEcu", "Ingrese la Ecuación"),
                        textInput("valorX", "x"),
                        textInput("valorH", "h")),
                        actionButton("diferFinEval", "Evaluar Derivada"),
                        tableOutput("difFinitOut")),
            
            tabItem("DerivacionXY",
                    h1("Diferencias Finitas f(x,y)"),
                    box(radioButtons("algoritmoXY", label = h3("Algortimo"),
                                     choices = list("Centradas (1)" = 1,
                                                    "Progresivas" = 2,
                                                    "Centradas (2)" = 3)),
                        textInput("difFinEcuXY", "Ingrese la Ecuación"),
                        textInput("valorXXY", "x"),
                        textInput("valorYXY", "y"),
                        textInput("valorHXY", "h")),
                    actionButton("diferFinEvalXY", "Evaluar Derivada"),
                    tableOutput("difFinitOutXY")),
            
            tabItem("bisection", 
                h1("M\u00E9todo de bisecci\u00F3n f(x)"),
                box(textInput("tinputBisectionFunc", "Ingrese la ecuaci\u00F3n"),
                    textInput("tinputBisectionAB",   "Intervalo [a,b]", "0,0"),
                    textInput("tinputBisectionKmax", "M\u00E1ximo iteraciones (kmax)"),
                    textInput("tinputBisectionTol",  "Tolerancia"),
                    actionButton("btnBisection",     "Ejecutar m\u00E9todo", icon = icon("table")),
                    helpText("Nota: Si la tabla se retorna vacia, pruebe modificar los puntos a,b.\n ", 
                             "Puede ser que: 1. se encontro la raiz en la primera iteracion; ", 
                             "2. no hay raiz en el intervalo.")),
                tableOutput("tblBisection")),
            
            tabItem("newtonraphson", 
                    h1("M\u00E9todo de Newton-Raphson f(x)"),
                    box(textInput("tinputNRFunc", "Ingrese la ecuaci\u00F3n"),
                        textInput("tinputNRX",   "Valor de X"),
                        textInput("tinputNRKmax", "M\u00E1ximo iteraciones (kmax)"),
                        textInput("tinputNRTol",  "Tolerancia"),
                        actionButton("btnNR",     "Ejecutar m\u00E9todo", icon = icon("table")),
                        helpText("Nota: Únicamente se aceptan expresiones de e elevado a x ej. e^x, dado que si la x viene\n",
                        "por un factor o elevada a otra potencia tendría que aplicar la regla de la cadena para derivar",
                        "\n lo cual está fuera del alcance de este código.\n\n",
                        "Si la variable x no tiene ninguna potencia explícita hay que indicarla x = x^1")),
                    tableOutput("tblNR")),
            
            tabItem("rosenbrock_function", 
                    h1("Funci\u00F3n de Rosenbrock f(x)"),
                    box(useShinyjs(),  # Set up shinyjs
                        disabled(textInput("tinput_rbck_func", "Funci\u00F3n de Rosenbrock", "100(x_2 - x_1^2)^2 + (1 - x_1)^2")),
                        textInput("tinput_rbckxo", "Xo:", "0,0"),
                        textInput("tinput_rbck_alpha", "\u03B1k:", "0.05"),
                        textInput("tinput_rbck_epsilon", "\u03B5:", "0.00000001"),
                        numericInput("tinput_rbck_kmax", "kmax:", "1000"),
                        actionButton("btn_rbck",   "Ejecutar m\u00E9todo", icon = icon("table")),
                        helpText("Tip:"),
                        width = 4),
                    tableOutput("tbl_rosenbrock")
                    )
        )
    )
)
