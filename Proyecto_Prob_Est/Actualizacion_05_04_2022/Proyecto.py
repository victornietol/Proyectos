import pandas as pd


# Punto 1

datos = pd.read_csv('bebidas.csv', index_col=0)

# Punto 3

# -- CATEGORIZACIÓN DE EDADES --
# 0 si la edad es menor que 18 años
# 1 si la edad es mayor o igual a 18 años, y menor que 60 años
# 2 si la edad es mayor o igual a 60 años

for i in range(len(datos)):
    if datos.Edad[i] < 18:
        datos.Edad[i] = 0
    elif (datos.Edad[i] >= 18) and (datos.Edad[i] < 60):
        datos.Edad[i] = 1
    else:
        datos.Edad[i] = 2

# -- CATEGORIZACIÓN DE TEMPERATURAS --
# 0 si la temperatura es menor o igual a 10°C (Frío)
# 1 si la temperatura es mayor a 10°C y menor a 20°C (Templado)
# 2 si la temperatura es mayor o igual a 20°C (Cálido)

for j in range(len(datos)):
    if datos.Temperatura[j] <= 10:
        datos.Temperatura[j] = 0
    elif (datos.Temperatura[j] > 10) and (datos.Temperatura[j] < 20):
        datos.Temperatura[j] = 1
    else:
        datos.Temperatura[j] = 2

# Punto 5

# Cálculo de la distribucion de Z 
# La distribución se almacena en una lista, donde [ P(Z=fría) , P(Z=caliente) ]
# Se esta representando fría con 0 y caliente con 1
# Inicio del conteo en cero

priori_z = [0,0]

for i in range(len(datos)):
    priori_z[datos.Bebida[i]] += 1

# Divide entre el número de clientes para obtener la distribución de probabilidad
for  j in range(0,2):
    priori_z[j] /= len(datos)

# Punto 6

# Cálculo de la distribución conjunta de X y Y
# La distribución se almacena en una lista de listas (tamaño 3x3)
# El primer índice corresponde a la edad X (0 para menor de edad, 1 para adulto, 2 para adulto mayor)
# El segundo índice corresponde a la temperatura del día Y (0 para frío, 1 para templado, 2 para cálido)

evidencia_xy = [[0,0,0] , [0,0,0], [0,0,0]]

for i in range(0,len(datos)):
    evidencia_xy[datos.Edad[i]][datos.Temperatura[i]] += 1

# Divide entre el número de clientes para obtener la distribución de probabilidad
for i in range(3):
    for j in range(3):
        evidencia_xy[i][j] /= len(datos)

# Punto 7

# Cálculo de la distribución conjunta de X y Y y Z
# El primer índice corresponde a la edad X (0 para menor de edad, 1 para adulto, 2 para adulto mayor)
# El segundo índice corresponde a la temperatura del día Y (0 para frío, 1 para templado, 2 para cálido)
# El tercer índice corresponde a la bebida (0 para fría, 1 para caliente)

distribucionC_xyz = [[[0,0],[0,0],[0,0]] , [[0,0],[0,0],[0,0]], [[0,0],[0,0],[0,0]]]

for i in range(0,len(datos)):
    distribucionC_xyz[datos.Edad[i]][datos.Temperatura[i]][datos.Bebida[i]] += 1

# Divide entre el número de clientes para obtener la distribución de probabilidad
for i in range(3):
    for j in range(3):
        for x in range(2):
            distribucionC_xyz[i][j][x] /= len(datos)

# Punto 7 parte 2

# Cálculo de likelihood o verosimilitud
likelihood = [[[0,0],[0,0],[0,0]] , [[0,0],[0,0],[0,0]], [[0,0],[0,0],[0,0]]]

for i in range(3):
    for j in range(3):
        for x in range(2):
            likelihood[i][j][x] = distribucionC_xyz[i][j][x] / priori_z[x]

# Código clasificador bayesiano

print('Nuevo cliente')
edad = input('Edad: ')
temperatura = input('Temperatura del día: ')

if edad == 'menor':
    edad_c = 0
elif edad == 'adulto':
    edad_c = 1
elif edad == 'mayor':
    edad_c = 2
else:
    print('Edad inválida')

if temperatura == 'frío' or temperatura == 'frio':
    temp_c = 0
elif temperatura == 'templado':
    temp_c = 1
elif temperatura == 'cálido' or 'calido':
    temp_c = 2
else:
    print('Temperatura inválida')

recomendacion_fria = (priori_z[0]*likelihood[edad_c][temp_c][0]) / evidencia_xy[edad_c][temp_c]
recomendacion_caliente = (priori_z[1]*likelihood[edad_c][temp_c][1]) / evidencia_xy[edad_c][temp_c]

if recomendacion_fria > recomendacion_caliente:
    print('La sugerencia es una bebida: fría')
else:
    print('La sugerencia es una bebida: caliente')