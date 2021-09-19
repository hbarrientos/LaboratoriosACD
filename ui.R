library(shiny)
library(shinydashboard)
library(shinyjs)

# Define UI for application that draws a histogram
dashboardPage(
    dashboardHeader(title = "Algoritmos en la Ciencia de Datos"),
    dashboardSidebar(
        sidebarMenu(
            menuItem("Ceros", tabName = "Ceros"),
            menuItem("Derivaci\u00F3n f(X)", tabName = "DerivacionX"),
            menuItem("Derivaci\u00F3n f(X,Y)", tabName = "DerivacionXY"),
            menuItem("Bisecci\u00F3n f(X)", tabName = "bisection"),
            menuItem("Newton Raphson f(X)", tabName = "newtonraphson"),
            menuItem("Gradient Descent (QP)", tabName = "gradient"),
            #menuItem("Funci\u00F3n de Rosenbrock f(x,y)", tabName = "rosenbrock_function"),
            menuItem("Funci\u00F3n de Rosenbrock", tabName = "rosenbrock")
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
            ),
            
            tabItem("gradient", h1("Algoritmo Gradient Descent (QP)"),
                    fluidRow(
                        box(width = "100%",
                    tabsetPanel(id="paneles",
                        tabPanel("parámetros",
                            textInput("tinput_Q", "Q", "[[2, -1, 0],[-1 , 2, -1],[0, -1, 2]]"),
                            textInput("tinput_x",  "x", "[3, 5, 7]"),
                            textInput("tinput_c",  "c", "[1, 0, 1]"),
                            textInput("tinput_error",  "error", "10**(-6)"),
                            textInput("tinput_kmax",  "Iteraciones", "30"),
                            selectInput("tinput_alpha", label = "Step size",
                                      choices = list("Exacto" = 0,
                                                    "Variable" = 2,
                                                    "0.001" = 0.001,
                                                    "0.01" = 0.01,
                                                    "0.1" = 0.1,
                                                    "0.5" = 0.5,
                                                    "1" = 1)),
                        actionButton("btn_gd",   "Ejecutar m\u00E9todo", icon = icon("table")),
                        helpText("Nota: la Matriz Q, los vectores x y c, así como el error deben estar escritos en sintaxis de python")
                        ),
                    tabPanel(title="resultados",
                           dataTableOutput("tbl_gd")
                    ),tabPanel(title="plot",
                               plotOutput("plot_gd")
                    ))))),
            tabItem("rosenbrock", h1("Función Rosenbrock"),
                    fluidRow(
                        box(width = "100%",
                            tabsetPanel(id="paneles_r",
                                        tabPanel("parámetros",
                                                 textInput("tinput_x_r",  "x", "[-1.2, 1]"),
                                                 textInput("tinput_error_r",  "error", "0.05"),
                                                 textInput("tinput_kmax_r",  "Iteraciones", "1000"),
                                                 selectInput("tinput_alpha_r", label = "Step size",
                                                             choices = list("Step Constante (0.5)" = 0.5,
                                                                            "Backtracking" = 1)),
                                                 actionButton("btn_r",   "Ejecutar m\u00E9todo", icon = icon("table")),
                                                 helpText("Nota: Los vectores x deben estar escritos en sintaxis python")
                                        ),
                                        tabPanel(title="resultados_r",
                                                 dataTableOutput("tbl_r")
                                        ),tabPanel(title="plot_r",
                                                   plotOutput("plot_r")
                                        ))))
            )
    )
))
