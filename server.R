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
    
})
