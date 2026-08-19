#=================================================
#CARGAMOS LA DATA DESEMEPLEO EN PERÚ (2001 - 2026)
#=================================================
import pandas as pd
ruta_archivo = "C:\\UNI\\VIII CICLO\\SERIES DE TIEMPO\\peru_macro_st\\tasa_desempleo_1996_2026.csv"
raw_data = pd.read_csv(ruta_archivo, sep = ";")
type(raw_data)
raw_data['Desempleo']

#Convertimos la columna texto de fechaa formato DateTime real
raw_data["Fecha"] = pd.to_datetime(raw_data["Fecha"], dayfirst = True)

#Copia de la tabla original para no alterar
raw_data_ts = raw_data.copy()

#Columna fecha como índice
raw_data_ts.set_index("Fecha", inplace = True)

#Creamos el onjeto de serie de tiempo asignando frecuencia mensual
fechas_lima = pd.date_range(start = "2001-05", periods = len(raw_data), freq = "MS")
raw_data.index = fechas_lima
Maine_month_ts = raw_data["Desempleo"]
#Maine_month_ts = raw_data_ts["Desempleo"].asfreq("MS")

Maine_annual_ts = Maine_month_ts.resample("YE").mean()

#=====================================================
#VISUALIZACIÓN DE LA SERIE DE TIEMPO DESEMPLEO EN PERÚ
#=====================================================

import matplotlib.pyplot as plt
fig, axes = plt.subplots(2, 1, figsize = (11,8))
axes[0].plot(Maine_month_ts, color = "blue", linewidth = 1.5)
axes[0].set_title("Tasa de Desempleo - Serie Mensual")
axes[0].set_ylabel("Desempleo (%)")
axes[0].grid(True, linestyle = ":", alpha = 0.6)

axes[1].plot(Maine_annual_ts, color = "red", linewidth = 2, marker = "o")
axes[1].set_title("Tendencia Anual Promedio")
axes[1].set_ylabel("Desempleo (%)")
axes[1].set_xlabel("Tiempo")
axes[1].grid(True, linestyle = ":", alpha = 0.6)

plt.tight_layout()
plt.show()

#====================================================
#DIAGRAMAS DE CAJA Y ESTACIONALIDAD PARA EL DESEMPLEO
#====================================================
import seaborn as sns
import matplotlib.pyplot as plt
fig, axes = plt.subplots(2, 1, figsize = (11, 9))

axes[0].plot(Maine_annual_ts, color = "red", linewidth = 2, marker = "o")
axes[0].set_title("Tendencia Anual Promedio")
axes[0].set_ylabel("Desempleo")
axes[0].grid(True, linestyle = ":", alpha = 0.6)

sns.boxplot(x = Maine_month_ts.index.month, y = Maine_month_ts.values, ax = axes[1], palette = "Set3")
axes[1].set_title("Estacionalidad Mensual del Desempleo")
axes[1].set_xlabel("Meses")
axes[1].set_ylabel("Desempleo")
axes[1].grid(True, linestyle = ":", alpha = 0.6)
plt.tight_layout()
plt.show()


Maine_Feb = Maine_month_ts[Maine_month_ts.index.month == 2]
Maine_Aug = Maine_month_ts[Maine_month_ts.index.month == 8]

Feb_ratio = Maine_Feb.mean() / Maine_month_ts.mean()
Aug_ratio = Maine_Aug.mean() / Maine_month_ts.mean()

print(f"Feb.ratio: {Feb_ratio: .4f}")
print(f"Aug_ratio: {Aug_ratio: .4f}")

#=========================
#SERIES DE TIEMPO MÚLTIPLE
#=========================

df_cbe = pd.read_csv("C:\\UNI\\PROGRAMACION\\R\\cbe_peru.csv", sep = ";")
print(df_cbe.head())

df_cbe['Fecha'] = pd.to_datetime(df_cbe['Fecha'], dayfirst = True)
df_cbe.set_index('Fecha', inplace = True)
print(df_cbe.head())
type(df_cbe)

df_cbe_filtrado = df_cbe[df_cbe.index <= '2019-12-31']
#====================================
#GRÁFICO MÚLTIPLE DE SERIES DE TIEMPO
#====================================
axes = df_cbe_filtrado[['elec', 'choc', 'beer']].plot(subplots = True,
                                             figsize = (10, 8),
                                             sharex = True,
                                             color = 'darkblue',
                                             linewidth = 1.5)
plt.suptitle("Producción Industrial CBE Perú (2001 - 2026)", y = 0.96,
             fontsize = 14)
axes[0].set_ylabel("Electricidad")
axes[1].set_ylabel("Chocolate")
axes[2].set_ylabel("Cerveza")

for ax in axes:
    ax.grid(True, linestyle = "--", alpha = 0.6)

    
plt.xlabel("Años")
plt.tight_layout()
plt.show()

#=========================================
#CRUCE Y ALINEACIÓN DE SERIES EN EL TIEMPO
#=========================================
df_cruce = df_cbe[['elec']].join(Maine_month_ts, how = 'inner')
print(df_cruce.head())

#Filtramos la data para que nos queda datos de la pre pandemia
df_pre_pand = df_cruce[df_cruce.index < '2020-01-01'] 
#==============================================
# CONSULTA DE LÍMITES Y FILAS ALINEADAS EN PERÚ
#==============================================
print(df_cruce.index.min()) #Inicio exacto del cruce
print(df_cruce.index.max()) #Final exacto del cruce

#========================================
#ANÁLISIS DE RELACIÓN: ELEC VS. DESEMPLEO
#========================================
import scipy.stats as stats
elec_vec = df_pre_pand['elec']
desempleo_vec = df_pre_pand['Desempleo']

fig = plt.figure(figsize = (12, 10))
ax1 = plt.subplot(2, 2, 1)
ax2 = plt.subplot(2, 2, 2)
ax3 = plt.subplot(2, 1, 2)

#Gráfico cronológico de Elec
ax1.plot(df_pre_pand.index, elec_vec, color = "royalblue")
ax1.set_title("Producción de Electricidad")
ax1.set_ylabel("Índice IVF")
ax1.grid(True, linestyle = ":")

#Gráfico cronológico de Desempleo
ax2.plot(df_pre_pand.index, desempleo_vec, color = "orange")
ax2.set_title("Tasa de Desempleo")
ax2.set_ylabel("Porcentaje (%)")
ax2.grid(True, linestyle = ":")

#Gráfico de dispersión
ax3.scatter(elec_vec, desempleo_vec, color = "darkgray", alpha = 0.7, edgecolors = "none")
ax3.set_title("Análisis de Dispersión: Elec vs Desempleo")
ax3.set_xlabel("Producción de Electricidad (Índice)")
ax3.set_ylabel("Tasa de Desempleo (%)")
ax3.set_ylabel("Tasa de Desempleo (%)")

#Línea de tendencia matemática
pendiente, intercepto, r_value, p_value, std_err = stats.linregress(elec_vec, desempleo_vec)
linea_tendencia = pendiente * elec_vec + intercepto
ax3.plot(elec_vec, linea_tendencia, color = "black", linestyle = "--", linewidth = 2)
ax3.grid(True, linestyle = ":")

plt.tight_layout()
plt.show()

#Coeficiente de correlación
correlacion = elec_vec.corr(desempleo_vec)
print(correlacion)

#==========================================
#DESCOMPOSICIÓN Y EXTRACCIÓN DE COMPONENTES
#==========================================
from statsmodels.tsa.seasonal import seasonal_decompose

decomp_aditiva = seasonal_decompose(df_cbe_filtrado['elec'], model = 'additive', period = 12)
decomp_aditiva.plot()
plt.suptitle("Descomposición Aditiva - Elec Perú", y = 0.98)
plt.show()

Elec_decom = seasonal_decompose(df_cbe_filtrado['elec'], model = 'multiplicative', period = 12)
Elec_decom.plot()

Trend = Elec_decom.trend
Seasonal = Elec_decom.seasonal

plt.figure(figsize = (12, 6))
plt.plot(df_cbe_filtrado.index, Trend, label = "Tendencia", color = "blue", linestyle = "-")
plt.plot(df_cbe_filtrado.index, Trend * Seasonal, label = "Tendencia * Estacionalidad (Modelo Multiplicativo)")

plt.title("Electricidad Perú: Tendencia vs Tendencia * Estacionalidad (Modelo Multiplicativo)")
plt.xlabel("Años")
plt.ylabel("Valores del índice")
plt.legend(loc = "upper left")
plt.grid(True, linestyle = ":", alpha = 0.6)
plt.tight_layout()
plt.show()

#===================================
#EXTRACCIÓN DE LA AUTOCOVARIANZA LAG
#===================================
import statsmodels.api as sm
import numpy as np

#Coeficiente de Autocorrelación
valores_acf = sm.tsa.stattools.acf(df_pre_pand['elec'], nlags = 5, fft = True)
#Coeficiente de Autocovarianza
valores_acov = sm.tsa.stattools.acovf(df_pre_pand['elec'], adjusted = False, fft = True)

print(f"Autocorrelación en Lag 1: {valores_acf[1]:.4f}")
print(f"Autocovarianza en Lag 1: {valores_acov[1]:.4f}")
print(f"Varianza de la serie (Lag 0): {valores_acov[0]: .4f}")