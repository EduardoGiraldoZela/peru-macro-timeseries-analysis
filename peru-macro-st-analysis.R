#================================
#TASA DE DESEMPLEO Perú 1996-2026
#================================

#1. Leer el archivo omitiendo las líneas de la cabecera
ruta_archivo <- "C:/UNI/VIII CICLO/SERIES DE TIEMPO/peru_macro_st/tasa_desempleo_1996_2026.csv"

raw_data <- read.csv2(ruta_archivo, header = TRUE, dec = ".")
raw_data
attach(raw_data)
class(raw_data)

#2. Convertimos la columna 'Desempleo' en un objeto de serie temporal mensual
Maine.month.ts <- ts(Desempleo, start = c(2001, 5), freq = 12)
#3. Calculamos el promedio anual de la tasa de desempleo
Maine.annual.ts <- aggregate(Maine.month.ts)/12

#============================================
#GRAFICAMOS LA SERIE TEMPORAL MENSUAL Y ANUAL
#============================================

#1. Divide la pantalla gráfica en 2 filas y 1 columna
layout(1:1)
#2. Serie mensual
plot(Maine.month.ts, ylab = "Desempleo (%)", xlab = "Tiempo", main = "Serie Mensual")

#===================================================
#DIAGRMAS DE CAJA Y ESTACIONALIDAD PARA EL DESEMPLEO
#===================================================
#layout(matrix(1:2, nrow = 1)) = layaout(1:2) Otra manera de dividir la pantalla gráfica en 2 filas y 1 columna
layout(1:2)
plot(Maine.annual.ts, ylab = "Desempleo (%)", xlab = "Tiempo", main = "Tendencia Anual")
boxplot(Maine.month.ts ~ cycle(Maine.month.ts), 
        main = "Estacionalidad Mensual del Desempleo",
        xlab = "Meses", ylab = "Tasa (%)",
        col = "lightblue")

#====================================================================
#Extraemos subseries que contienen solo los febreros y solo agosto
#====================================================================
Maine.Feb <- window(Maine.month.ts, start = c(2002, 2), freq = TRUE)
Maine.Aug <- window(Maine.month.ts, start = c(2001, 8), freq = TRUE)

#Calculamos la proporción (ratio) frente al promedio de toda la serie
Feb.ratio <- mean(Maine.Feb)/mean(Maine.month.ts)
Aug.ratio <- mean(Maine.Aug)/mean(Maine.month.ts)

#Imprimimos los resultados 
Feb.ratio
Aug.ratio

#======================================================================
#SERIES TEMPORALES MÚLTIPLES: electricidad, chocolate y cerveza en Perú
#======================================================================
cbe_peru <- read.csv2("C:/UNI/PROGRAMACION/R/cbe_peru.csv", header = TRUE, dec = ".")
head(cbe_peru)

cbe_peru[1:4, ]
class(cbe_peru)

#======================================
#GRÁIFCA MÚLTIPLE DE LA SERIE DE TIEMPO
#======================================
Elec.ts <- ts(cbe_peru[, "elec"], start = c(2001, 1), freq = 12)
Choc.ts <- ts(cbe_peru[, "choc"], start = c(2001, 1), freq = 12)
Beer.ts <- ts(cbe_peru[, "beer"], start = c(2001, 1), freq = 12)

#Recortando hasta diciembre 2019
Elec.ts <- window(Elec.ts, end = c(2019, 12))
Choc.ts <- window(Choc.ts, end = c(2019, 12))
Beer.ts <- window(Beer.ts, end = c(2019, 12))

plot(cbind(Elec.ts, Choc.ts, Beer.ts),
     main = "Producción Industrial CBE Perú (2001 - 2026)",
     xlab = "Años",
     col = "darkblue",
     lwd = 1.5)

#=========================================
#CRUCE Y ALINEACIÓN DE SERIES EN EL TIEMPO
#=========================================
cruce.ts <- ts.intersect(Maine.month.ts, Elec.ts)
head(cruce.ts)

#Filtramos los datos para el periodo pre-pandemia
peru_pre_pand.ts <- window(cruce.ts, end = c(2019, 12))

#=============================================
#CONSULTA DE LÍMITES Y FILAS ALINEADAS EN PERÚ
#=============================================

start(cruce.ts) #Consulta inicio exacto de cruce
end(cruce.ts) #Consulta final exaxto del cruce
cruce.ts[1:3,]

#========================================
#ANÁLISIS DE RELACIÓN: ELEC VS. DESEMPLEO
#========================================
Desempleo <- cruce.ts[, 1]
Elec <- cruce.ts[, 2]

layout(1:3)
plot(Desempleo, main = "", ylab = "Desempleo")
plot(Elec, main = "", ylab = "Producción de Electricidad")

plot(as.vector(Desempleo), as.vector(Elec),
     xlab = "Desempleo (%)",
     ylab = "Producción de Electricidad")
abline(reg = lm(Elec ~ Desempleo))

#Otra manera de hacer la gráfica:
Desempleo1 <- peru_pre_pand.ts[, "Maine.month.ts"]
Elec1 <- peru_pre_pand.ts[, "Elec.ts"]
layout(matrix(c(1,2,3,3), 2, 2, byrow = TRUE))
plot(Elec1, main = "Producción de Electricidad", ylab = "índice IVF", col = "royalblue")
plot(Desempleo1, main = "Tasa de Desempleo", ylab = "Porcentaje (%)", col = "orange")
plot(as.vector(Elec1), as.vector(Desempleo1),
     main = "Análisis de Dispersión: Elec vs Desempleo",
     xlab = "Producción de Electricidad vs Desempleo",
     ylab = "Tasa de Desempleo(%)",
     col = "darkgray", pch = 16)
abline(reg = lm(Desempleo1 ~ Elec1), col = "black", lwd = 2, lty = 2)

#==============================================
#CALCULAMOS LA CORRELACIÓN ENTRE LAS DOS SERIES
#==============================================
#Covarianza
sum((Elec1 - mean(Elec1))*(Desempleo1 - mean(Desempleo1)))/(length(Elec1) - 1)
mean((Elec1 - mean(Elec1))*(Desempleo1 - mean(Desempleo1))) 
#Correlación
cor(Elec1, Desempleo1) 
cov(Elec1, Desempleo1)/(sd(Elec1)*sd(Desempleo1))

#==========================================
#DESCOMPOSICIÓN Y EXTRACCIÓN DE COMPONENTES
#==========================================
plot(decompose(Elec.ts)) #Descomposición Aditiva
Elec.decom <- decompose(Elec.ts, type = "mult") #Descomposición Multiplicativa
plot(Elec.decom)
Trend <- Elec.decom$trend
Seasonal <- Elec.decom$seasonal
layout(1:1)
ts.plot(cbind(Trend, Trend * Seasonal), main = "Electricidad Perú: Tendencia vs Tendencia * Estacionalidad",
        xlab = "Años", ylab = "Valores índice", lty = 1:2, col = c("blue", "red"))

#===================================================
#EXTRACCIÓN DE COEFICIENTES DE AUTOCORRELACIÓN LAG 1
#===================================================
acf(Elec1)$acf[2]
acf(Elec1, type = c("covariance"))$acf[2]





















