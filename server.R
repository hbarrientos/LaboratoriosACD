library(shiny)
library(reticulate)

source_python("algoritmos.py")

#tableOut, soluc = newtonSolverX(-5, "2x^5 - 3", 0.0001)

shinyServer(function(input, output) {
    
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
    
    # 3rd laboratory, Gradient descent method
    # output$tbl_gd <- renderTable(eventReactive(input$btn_gd, {
    gd_method <- eventReactive(input$btn_gd, {
        q <- input$tinput_gdq
        c <- input$tinput_gdc
        e <- input$tinput_gdepsilon
        n <- input$tinput_gdn
        xo <- input$tinput_gdxo
        tableout <- evaluate_gd(q, c, e, n, xo)
    })
    # ,
    output$tbl_gd <- renderTable(
        gd_method(),
        digits=6,
        striped = TRUE, bordered = TRUE, hover = TRUE
    )
    
    # 3rd laboratory, Rosenbrock's frunction
    # output$tbl_rosenbrock <- renderTable(eventReactive(input$btn_rbck, {
    rosenbrock_method <- eventReactive(input$btn_rbck, {
        xo <- input$tinput_rbckxo
        a <- input$tinput_rbck_alpha
        tableout <- evaluate_rosenbrock(xo, a)
    })
    # ,
    output$tbl_rosenbrock <- renderTable(
        rosenbrock_method(),
        digits = 8, striped = TRUE, bordered = TRUE, hover = TRUE
    )
    
    
})
