import math
import random

# Calcular promedio de los objetos
def calcular_promedio(lista: list) -> float:
    return sum(lista)/len(lista) if lista else 0 


# Generar numeros aleatorios que siguen una distribucion de Poisson para 
# representar el numero de goles simulados basado en el promedio esperado de goles (lamda)
def generar_poisson(goles_esperados: float) -> float:
    L = math.exp(-goles_esperados) # Calcular e^() -> umbral para terminar
    k = 0
    p = 1
    while(p > L):
        k += 1
        p *= random.uniform(0,1) # Generar un numero aleatorio para actualizar p
    return k-1 # Ajusta el índice porque el ciclo incrementa k al inicio


# Calcular el valor para el ataque del equipo basado en las estadisticas
def calcular_ataque(goles_anotados: int, partidos_jugados: int, tiros_a_puerta: float) -> float:
    promedio_goles = goles_anotados/partidos_jugados
    return promedio_goles*(1+(tiros_a_puerta/10)) # Aplicando ajuste por tiros a puerta


# Calcular el valor para la defensa del equipo basado en las estadisticas
def calcular_defensa(goles_recibidos: int, partidos_jugados: int, porterias_imbatidas: int) -> float:
    prom_goles_recibidos = goles_recibidos/partidos_jugados
    porteria_a_cero = porterias_imbatidas/partidos_jugados
    return 1/ (prom_goles_recibidos+0.5)+porteria_a_cero # Aplicando ajuste por porterias a cero

# Calcular el promedio de goles esperado basado en la fuerza de ataque, de defensa y
# un porcentaje de localia
def calcular_promedio_goles(ataque: float, defensa: float, factor_local=1.0) -> float:
    return ataque*defensa*factor_local


# Ajustar las estadisticas del equipo segun su forma reciente. La forma reciente son los 
# goles anotados o recibidos en los ultimos partidos
def ajustar_forma(estadistica: float, goles_recientes: list) -> float:
    promedio_reciente = calcular_promedio(goles_recientes)
    return estadistica*(1+(promedio_reciente-estadistica)*0.2) # Ponderacion del 20%


# Realizar simulaciones del partido entre los equipos, regresa un diccionario con 
# el promedio de goles y probabilidad de ganar, perder o empatar. Se simulan varios
# partidos y se obtiene el promedio de las simulaciones
def simular_partido(equipo1: dict, equipo2: dict, num_simulaciones=1000) -> dict:
    resultados = {
        "equipo1_goles":[],
        "equipo2_goles":[]
    }

    for _ in range(num_simulaciones):
        # Calcular ataque y defensa de los equipos
        ataque1 = calcular_ataque(equipo1['goles_anotados'], equipo1['partidos_jugados'], equipo1['tiros_a_puerta'])
        defensa1 = calcular_defensa(equipo1['goles_recibidos'], equipo1['partidos_jugados'], equipo1['porterias_imbatidas'])
        ataque2 = calcular_ataque(equipo2['goles_anotados'], equipo2['partidos_jugados'], equipo2['tiros_a_puerta'])
        defensa2 = calcular_defensa(equipo2['goles_recibidos'], equipo2['partidos_jugados'], equipo2['porterias_imbatidas'])

        # Ajustando estadisticas segun la forma reciente
        ataque1 = ajustar_forma(ataque1, equipo1['goles_recientes'])
        defensa1 = ajustar_forma(defensa1, equipo1['goles_recientes'])
        ataque2 = ajustar_forma(ataque2, equipo2['goles_recientes'])
        defensa2 = ajustar_forma(defensa2, equipo2['goles_recientes'])

        # Obtener el promedio de los goles esperados
        goles_esperados1 = calcular_promedio_goles(ataque1, defensa2, equipo1['factor_local'])
        goles_esperados2 = calcular_promedio_goles(ataque2, defensa1, equipo2['factor_local'])

        # Obtener goles simulados
        goles1 = generar_poisson(goles_esperados1)
        goles2 = generar_poisson(goles_esperados2)

        # Guardar resultados
        resultados["equipo1_goles"].append(goles1)
        resultados["equipo2_goles"].append(goles2)

    # Obtener promedio de goles finales, victoria y empate
    goles_promedio1 = calcular_promedio(resultados['equipo1_goles'])
    goles_promedio2 = calcular_promedio(resultados['equipo2_goles'])
    victorias_equipo1 = sum(1 for g1,g2 in zip(resultados['equipo1_goles'], resultados['equipo2_goles']) if g1>g2) /num_simulaciones
    victorias_equipo2 = sum(1 for g1,g2 in zip(resultados['equipo1_goles'], resultados['equipo2_goles']) if g1<g2) /num_simulaciones
    empates = 1-(victorias_equipo1+victorias_equipo2)

    return {
        "goles_promedio_eq1":goles_promedio1,
        "goles_promedio_eq2":goles_promedio2,
        "probabilidad_victoria_eq1":victorias_equipo1,
        "probabilidad_victoria_eq2":victorias_equipo2,
        "probabilidad_empate":empates,
        "estadisticas_originales":[equipo1,equipo2],
        "historial":resultados
    }


# Estadisticas de ejemplo
equipo1 = {
    "nombre": "Equipo A",
    "goles_anotados": 45,
    "goles_recibidos": 30,
    "partidos_jugados": 20,
    "tiros_a_puerta": 5.5,  # Tiros a puerta por partido
    "porterias_imbatidas": 8,
    "goles_recientes": [2, 1, 3, 1, 2],  # Ultimos goles anotados
    "factor_local": 1.2  # Puntos por jugar de local (mayor que 1 es local, menor que 1 es visitante)
}

equipo2 = {
    "nombre": "Equipo B",
    "goles_anotados": 38,
    "goles_recibidos": 35,
    "partidos_jugados": 20,
    "tiros_a_puerta": 4.8,
    "porterias_imbatidas": 5,
    "goles_recientes": [1, 0, 2, 1, 0],
    "factor_local": 0.9
}



if __name__ == "__main__":
    # Simular partido
    resultado = simular_partido(equipo1,equipo2)

    # Mostrar resultado
    print(f"Promedio de goles {equipo1['nombre']}: {resultado['goles_promedio_eq1']:.2f}")
    print(f"Promedio de goles {equipo2['nombre']}: {resultado['goles_promedio_eq2']:.2f}")
    print(f"Probabilidad de victoria {equipo1['nombre']}: {resultado['probabilidad_victoria_eq1']:.2%}")
    print(f"Probabilidad de victoria {equipo2['nombre']}: {resultado['probabilidad_victoria_eq2']:.2%}")
    print(f"Probabilidad de empate: {resultado['probabilidad_empate']:.2%}")
