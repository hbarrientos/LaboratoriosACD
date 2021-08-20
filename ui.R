library(shiny)
library(shinydashboard)

# Define UI for application that draws a histogram
dashboardPage(
    dashboardHeader(title = "Algoritmos en la Ciencia de Datos"),
    dashboardSidebar(
        sidebarMenu(
            menuItem("Ceros", tabName = "Ceros"),
            menuItem("Derivacion f(X)", tabName = "DerivacionX"),
            menuItem("Derivacion f(X,Y)", tabName = "DerivacionXY"),
            menuItem("Bisecci\u00F3n f(X)", tabName = "bisection")
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
                    actionButton("btnBisection",     "Ejecutar m\u00E9todo")
                    , textOutput("selected")),
                tableOutput("tblBisection"))
        )
    )
)
