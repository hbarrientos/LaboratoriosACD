library(shiny)
library(reticulate)
library(ggplot2)
library(dplyr)

source_python("algoritmos.py")
source_python("gd.py")
source_python("rosenbrock.py")
source_python("newton.py")

#tableOut, soluc = newtonSolverX(-5, "2x^5 - 3", 0.0001)

shinyServer(function(input, output, session) {
    
    #Evento y evaluación de metodo de newton para ceros
    newtonCalculate<-eventReactive(input$nwtSolver, {
        inputEcStr<-input$ecuacion[1]
        print(inputEcStr)
        initVal<-input$initVal[1]
        error<-input$Error[1]
        #outs<-add(initVal, error)
        outs<-newtonSolverX(initVal, inputEcStr, error)
        outs
    })
    
    #Evento y evaluación de diferencias finitas
    diferFinitCalculate<-eventReactive(input$diferFinEval, {
        algortimo<-input$algoritmo
        inputEcStr<-input$difFinEcu[1]
        valX<-input$valorX[1]
        h<-input$valorH[1]
        
        if (algortimo == 1) {
            outs<-evaluate_derivate_fx1(inputEcStr, valX, h)    
        }else if (algortimo == 2){
            outs<-evaluate_derivate_fx2(inputEcStr, valX, h) 
        }else{
            outs<-evaluate_derivate_fx3(inputEcStr, valX, h) 
        }
        outs
    })
    
    #Evento y evaluación de diferencias finitas
    diferFinitCalculateXY<-eventReactive(input$diferFinEvalXY, {
        algortimo<-input$algoritmoXY
        inputEcStr<-input$difFinEcuXY[1]
        valX<-input$valorXXY[1]
        valY<-input$valorYXY[1]
        h<-input$valorHXY[1]
        
        if (algortimo == 1) {
            outs<-evaluate_derivate_fx1XY(inputEcStr, valX, valY, h)    
        }else if (algortimo == 2){
            outs<-evaluate_derivate_fx2XY(inputEcStr, valX, valY, h) 
        }else{
            outs<-evaluate_derivate_fx3XY(inputEcStr, valX, valY, h) 
        }
        outs
    })
    
    
    #REnder metodo de Newton
    output$salidaTabla<-renderTable({
        newtonCalculate()
    })
    
    #Render Diferncias Finitas
    output$difFinitOut<-renderTable({
        diferFinitCalculate()
    })
    
    output$difFinitOutXY<-renderTable({
        diferFinitCalculateXY()
    })
    
    # Laboratory 2nd, Bisection method
    bisectionMethod<-eventReactive(input$btnBisection, {
        functionn <- input$tinputBisectionFunc
        a <-    strsplit(input$tinputBisectionAB, split = ",")[[1]][1]
        b <-    strsplit(input$tinputBisectionAB, split = ",")[[1]][2]
        kmax <- input$tinputBisectionKmax
        tolerance <- input$tinputBisectionTol
        tableout <- evaluate_bisection(functionn, a, b, kmax, tolerance)
    })
    
    output$tblBisection<-renderTable(
        bisectionMethod(), 
        digits=6,
        striped = TRUE, bordered = TRUE, hover = TRUE
    )
    
    # Laboratory 2nd, NR method
    NRMethod<-eventReactive(input$btnNR,{ 
        functionn <- input$tinputNRFunc
        x <- input$tinputNRX
        kmax <- input$tinputNRKmax
        tolerance <- input$tinputNRTol
        tableout <- evaluate_NR(functionn, x, kmax, tolerance)
        
        tableout
    })
    
    output$tblNR<-renderTable(
        NRMethod(),
        digits=6
    )
    
    gradient_method <- eventReactive(input$btn_gd, {
        Q <- input$tinput_Q
        x <- input$tinput_x
        c <- input$tinput_c
        error <- input$tinput_error
        kmax <- input$tinput_kmax
        step <- input$tinput_alpha
        gd <- GD(Q, x, c, error, kmax, step)
        gd$algorithm()
        gd$iterations()
    })
    
    gradient_method_plot <- eventReactive(input$btn_gd, {
        Q <- input$tinput_Q
        x <- input$tinput_x
        c <- input$tinput_c
        error <- input$tinput_error
        kmax <- input$tinput_kmax
        step <- input$tinput_alpha
        gd <- GD(Q, x, c, error, kmax, step)
        gd$algorithm()
        gd$results %>%
            ggplot(aes(x=k, y=grad_fxk)) +
            geom_line(color="grey") +
            geom_point(shape=21, color="black", fill="#69b3a2", size=3) +
            theme_bw()+
            ggtitle("Gradient Descent´")
        
    })
    
    observeEvent(input$btn_gd,{
        updateTabsetPanel(session, "paneles",
                          selected = "resultados"                    )
    })
    
    output$tbl_gd <- renderDataTable(
        gradient_method(),
        options = list(pageLength=10, autoWidth= TRUE, searching=FALSE)
    )
    
    output$plot_gd <- renderPlot({
        gradient_method_plot()
    }) 


    
    # 3rd laboratory, Rosenbrock's frunction
    rosenbrock_method <- eventReactive(input$btn_rbck, {
        xo <- input$tinput_rbckxo
        alpha <- input$tinput_rbck_alpha
        epsilon <- input$tinput_rbck_epsilon
        kmax <- input$tinput_rbck_kmax
        tableout <- evaluate_rosenbrock(xo, alpha, epsilon, kmax)
    })

    output$tbl_rosenbrock <- renderTable(
        rosenbrock_method(),
        digits = 8, striped = TRUE, bordered = TRUE, hover = TRUE
    )
    
    #Rosenbrock's Function Lab 4
    r_method <- eventReactive(input$btn_r, {
        x <- input$tinput_x_r
        error <- input$tinput_error_r
        kmax <- input$tinput_kmax_r
        step <- input$tinput_alpha_r
        r <- Rosenbrock(x, error, kmax, step)
        r$algorithm()
        r$iterations()
    })
    
    r_method_plot <- eventReactive(input$btn_r, {
        x <- input$tinput_x_r
        error <- input$tinput_error_r
        kmax <- input$tinput_kmax_r
        step <- input$tinput_alpha_r
        r <- Rosenbrock(x, error, kmax, step)
        r$algorithm()
        r$results %>%
            ggplot(aes(x=k, y=grad_fx_k)) +
            geom_line(color="grey") +
            geom_point(shape=21, color="black", fill="#69b3a2", size=3) +
            theme_bw()+
            ggtitle("Rosenbrock's Function´")
        
    })
    
    observeEvent(input$btn_r,{
        updateTabsetPanel(session, "paneles_r",
                          selected = "resultados_r"                    )
    })
    
    output$tbl_r <- renderDataTable(
        r_method(),
        options = list(pageLength=10, autoWidth= TRUE, searching=FALSE)
    )
    
    output$plot_r<- renderPlot({
        r_method_plot()
    })

    #Newton Backtracking Lba 4

    n_method <- eventReactive(input$btn_n, {
        x <- input$tinput_x_n
        error <- input$tinput_error_n
        kmax <- input$tinput_kmax_n
        step <- input$tinput_alpha_n
        n <- Newton(x, error, kmax, step)
        n$algorithm()
        n$iterations()
    })
    
    n_method_plot <- eventReactive(input$btn_n, {
        x <- input$tinput_x_n
        error <- input$tinput_error_n
        kmax <- input$tinput_kmax_n
        step <- input$tinput_alpha_n
        n <- Newton(x, error, kmax, step)
        n$algorithm()
        n$results %>%
            ggplot(aes(x=k, y=grad_fx_k)) +
            geom_line(color="grey") +
            geom_point(shape=21, color="black", fill="#69b3a2", size=3) +
            theme_bw()+
            ggtitle("Newton Backtracking")
        
    })
    
    observeEvent(input$btn_n,{
        updateTabsetPanel(session, "paneles_n",
                          selected = "resultados_n"                    )
    })
    
    output$tbl_n <- renderDataTable(
        n_method(),
        options = list(pageLength=10, autoWidth= TRUE, searching=FALSE)
    )
    
    output$plot_n<- renderPlot({
        n_method_plot()
    })
    
})
