import numpy as np
import matplotlib.pyplot as plt
from statistics_MC_functions import *

# En este script se simula el transporte 2D de una partícula contemplando la absorción y la dispersión elástica como los únicos eventos posibles.
# Para tener un muestreo estadístico, la región donde el transporte tiene lugar se divide en 10 regiones. Se cuentan en cada región el número de 
# partículas absorbidas, así como las que escapan de la región por la entrada (partículas reflejadas) como por la salida (partículas transmitidas).
# Finalmente, se representa un histograma con dichos resultados.
# Las funciones usadas se importan de un archivo aparte.


# parámetros
N_PART = 1000 # numero de particulas

SIGMA_A = 1 # sección eficaz de absorción [μm] --> 1,1,0.5
SIGMA_E = 1 # sección eficaz de dispersión elástica [μm] --> 1,2,0.1

L_X = 10 # longitud horizontal [μm]
L_Y = 10 # longitud vertical [μm] (not used)
X_0 = 0 # coordenada 'x' de la posición inicial [μm]
Y_0 = 5 # coordenada 'y' de la posición inicial [μm]
RHO_0 = 0 # ángulo inicial de incidencia -> ángulo con el que las partículas entran en la región [rad]


# ejecución
H = particles_stats(N_PART,SIGMA_A,SIGMA_E,L_X,X_0,Y_0,RHO_0)

# cálculo de los coeficientes
N_R = np.sum(H == -1) # número de partículas reflejadas
c_R = round(N_R/N_PART,4) # coeficiente de relfexión

N_T = np.sum(H == 11) # número de partículas transmitidas
c_T = round(N_T/N_PART,4) # coeficiente de transmisión

N_A = np.sum(H < 11) - np.sum(H == -1) # numero de particulas absorbidas
c_A = round(N_A/N_PART,4) # coeficiente de absorción


# representación del histograma
intervals = [ x for x in range(-1,13) ]
plt.hist(x=H, bins=intervals, color='#F2AB6D', rwidth=0.85)

plt.title('N$_{particles}$ = ' + str(N_PART) + ' '*20 + r'$\Sigma_a =' + str(SIGMA_A) + '\ \mu m^{-1}$' + ' '*5 + r'$\Sigma_e =' + str(SIGMA_E) + '\ \mu m^{-1}$') 
plt.title('A = ' + str(c_A) + " "*5 +'R = ' + str(c_R) + " "*5 +"T = " + str(c_T),loc = 'right')
plt.xlabel('Regions of final "x" position (-1=reflexion, 11=transmission)')
plt.ylabel('Frecuency')
plt.xticks(intervals)


#plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
for j in range(-1,12):
    n = round((np.sum(H == j)/N_PART)*100,2)
    #n = np.sum(H == j)
    plt.text(j +0.1,N_PART/40,str(n)+'%',color = 'blue') 

plt.grid()
plt.show() 


