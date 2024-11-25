import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import simulacion_partido as sim_p


# Cerrar plt al cerrar ventana
def al_cerrar(ventana: tk.Tk):
    plt.close("all")
    ventana.destroy()


# Cambiar el indicar para saber en que imagen se esta
def crear_indicador_img(frame_indicador: tk.Frame, indice_actual_grafica: int):
    if(indice_actual_grafica == -1): # Si ya se creo grafica se crea el indicador, de lo contrario, no se crea el indicador (-1=no se ha creado)
        # Borrar el frame actual
        for widget in frame_indicador.winfo_children():
            widget.destroy()
        # Crear el widget del indicador
        posicion = 0.460
        for i in range(3):
            color = "#e2e2e2" # Color gris
            canvas_indicador = tk.Canvas(frame_indicador, width=20, height=20, bg="white", highlightthickness=0)
            canvas_indicador.create_oval(5,5,15,15, fill=color)
            canvas_indicador.place(relx=posicion, rely=0, relwidth=0.025, relheight=1)
            posicion += 0.025 # Actualizar la posicion para la nueva bolita
    
    elif(indice_actual_grafica != -1): # Si ya se creo grafica se crea el indicador, de lo contrario, no se crea el indicador (-1=no se ha creado)
        # Borrar el widget actual
        for widget in frame_indicador.winfo_children():
            widget.destroy()
        # Crear el widget del indicador
        posicion = 0.460
        for i in range(len(graficas_global)):
            color = "#020057" if i == indice_actual_grafica else "#e2e2e2" # El indice de la imagen mostrada tendra otro color
            canvas_indicador = tk.Canvas(frame_indicador, width=20, height=20, bg="white", highlightthickness=0)
            canvas_indicador.create_oval(5,5,15,15, fill=color)
            canvas_indicador.place(relx=posicion, rely=0, relwidth=0.025, relheight=1)
            posicion += 0.025 # Actualizar la posicion para la nueva bolita


# Cambia a la siguiente o anterior imagen de la grafica, actualizar la posicion del indicador de imagen
def cambiar_imagen(frame_grafica: tk.Frame, frame_indicador_img: tk.Frame, direccion_mov: int):
    indice_graficas_global.set( (indice_graficas_global.get()+(direccion_mov)) % len(graficas_global) ) # Actualizar el indice con el movimiento (obtener nuevo indice con aritmetica modular)
    mostrar_graficas(frame_grafica, graficas_global, indice_graficas_global.get())
    crear_indicador_img(frame_indicador_img, indice_graficas_global.get()) # Acttualizar indicador


# Mostrar en el frame las graficas generadas
def mostrar_graficas(frame_grafica: tk.Frame, graficos: list, indice_actual):
    # Eliminar grafico si ya se habia construido uno
    for widget in frame_grafica.winfo_children():
        widget.destroy()

    # Colocando grafico en el frame
    grafica_actual = graficos[indice_actual]
    canvas = FigureCanvasTkAgg(grafica_actual, master=frame_grafica)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill="both", expand=True)
    canvas.draw()


# Crear grafico 1 (plot de goles)
def crear_grafica_estadisticas_plot(equipo1: dict, equipo2: dict):
    equipos_est = {key: [value,equipo2[key]] for key, value in equipo1.items()}
    nomb_equipos = equipos_est['nombre']
    #Plot de Estadisticas
    x = np.arange(len(nomb_equipos))  # Locación del nombre de los equipos
    width = 0.16  # Ancho de las barras
    multiplier = 0 #Espaciador de las barras
    fig, ax = plt.subplots(2,1,layout='constrained') #Subplots
    for attribute, measurement in equipos_est.items():
        if attribute not in ["nombre","goles_recientes"]:
            offset = width * multiplier
            rects = ax[0].bar(x + offset, measurement, width, label=attribute)
            ax[0].bar_label(rects, padding=2)
            multiplier += 1
    ax[0].set_ylabel('Estadisticas')
    ax[0].set_title('Estadisticas por equipo')
    ax[0].set_xticks(x + width, nomb_equipos)
    ax[0].legend(loc='upper left', ncols=2)
    ax[0].set_ylim(0, 100)
    ax[1].plot(np.arange(len(equipo1['goles_recientes'])),equipo1['goles_recientes'], label=equipo1["nombre"], color="red")
    ax[1].plot(np.arange(len(equipo2['goles_recientes'])),equipo2['goles_recientes'], label=equipo2["nombre"], color="blue")
    ax[1].set_ylabel('Goles')
    ax[1].legend(loc='upper left', ncols=2)
    ax[1].set_title('Goles recientes por partido')
    return fig


# Crear grafica 2 para mostrar estadisticas por equipo
def crear_grafica_estadisticas_simul(resultado:dict):
    victorias_equipo1 = sum(1 for g1,g2 in zip(resultado['historial']['equipo1_goles'], resultado['historial']['equipo2_goles']) if g1>g2)
    victorias_equipo2 = sum(1 for g1,g2 in zip(resultado['historial']['equipo1_goles'], resultado['historial']['equipo2_goles']) if g1<g2)
    empates = sum(1 for g1,g2 in zip(resultado['historial']['equipo1_goles'], resultado['historial']['equipo2_goles']) if g1==g2)

    sumulacionEquipo1 = { 
        "Victorias": [ victorias_equipo1, victorias_equipo2] ,
        "Derrotas": [ victorias_equipo2, victorias_equipo1],
        "Empates": empates,
    } 

    nomb_equipos = (resultado["estadisticas_originales"][0]["nombre"],resultado["estadisticas_originales"][1]["nombre"])
    width = 0.6  #Ancho de las barras
    fig, ax = plt.subplots()
    bottom = np.zeros(2)
    for detalle, valor in sumulacionEquipo1.items():
        p = ax.bar(nomb_equipos, valor, width, label=detalle,  bottom=bottom)
        bottom += valor
        ax.bar_label(p, label_type='center')
    ax.set_title('Estadisticas de simulación por equipo')
    ax.legend()
    return fig


# Crear grafica 3 para mostrar porcentajes de victoria por equipo
def crear_grafica_porcentajes_victoria(resultados:dict, nombre_eq1: str, nombre_eq2: str):
    # Valores
    valores = [resultados["probabilidad_victoria_eq1"], resultados["probabilidad_victoria_eq2"], resultados["probabilidad_empate"]]
    etiquetas = ["Victoria "+nombre_eq1, "Victoria "+nombre_eq2, "Empate"]
    separacion = [0.05, 0.05, 0.05]
    # Creando grafico
    fig, ax = plt.subplots()
    ax.pie(
        valores,
        labels=etiquetas,
        autopct="%1.2f%%",
        startangle=90,
        explode=separacion,
        shadow=True
    )
    ax.set_title("Probabilidades del partido")
    return fig


# Graficar los resultados de las probabilidades
def crear_grafica(resultados: dict, nombre_eq1: str, nombre_eq2: str) -> list:
    graficas = [] # Lista para guardar las graficas generadas

    # Creando graficas de resultados
    graficas.append(crear_grafica_estadisticas_plot(resultados["estadisticas_originales"][0], resultados["estadisticas_originales"][1]))
    graficas.append(crear_grafica_estadisticas_simul(resultados))
    graficas.append(crear_grafica_porcentajes_victoria(resultados, nombre_eq1, nombre_eq2))
    
    return graficas
    

# Cambiar el contenido de los Labels de la seccion "RESULTADOS" para mostrar resultados
def mostrar_resultados(resultados: dict, nombre_eq1: str, nombre_eq2: str, lista_labels, frame_grafica:tk.Frame, indice_graficas):
    lista_labels[0].config(text=f"Promedio de goles {nombre_eq1}: {resultados['goles_promedio_eq1']:.2f}")
    lista_labels[1].config(text=f"Promedio de goles {nombre_eq2}: {resultados['goles_promedio_eq2']:.2f}")
    lista_labels[2].config(text=f"Probabilidad de victoria {nombre_eq1}: {resultados['probabilidad_victoria_eq1']:.2%}")
    lista_labels[3].config(text=f"Probabilidad de victoria {nombre_eq2}: {resultados['probabilidad_victoria_eq2']:.2%}")
    lista_labels[4].config(text=f"Probabilidad de empate: {resultados['probabilidad_empate']:.2%}")

    # Crear graficas
    global graficas_global # Lista para almacenar las graficas generadas
    graficas_global = crear_grafica(resultados, nombre_eq1, nombre_eq2)

    # Mostrar graficas
    mostrar_graficas(frame_grafica, graficas_global, indice_graficas.get())

    
# Prepara los datos obtenidos de los Entrys para poder usarlos en la funcion "simular_partido"
def simular_previo(
        nombre_eq1, 
        goles_anotados_eq1,
        goles_recibidos_eq1,
        partidos_jugados_eq1,
        tiros_a_puerta_eq1,
        porterias_imbatidas_eq1,
        goles_recientes_eq1,
        factor_local_eq1,
        nombre_eq2, 
        goles_anotados_eq2,
        goles_recibidos_eq2,
        partidos_jugados_eq2,
        tiros_a_puerta_eq2,
        porterias_imbatidas_eq2,
        goles_recientes_eq2,
        factor_local_eq2,
        lista_labels,
        frame_grafica,
        frame_indicador_img
):
    
    try:
        equipo1 = {
            "nombre":nombre_eq1,
            "goles_anotados": float(goles_anotados_eq1),
            "goles_recibidos": float(goles_recibidos_eq1),
            "partidos_jugados": int(partidos_jugados_eq1),
            "tiros_a_puerta": float(tiros_a_puerta_eq1),
            "porterias_imbatidas": float(porterias_imbatidas_eq1),
            "goles_recientes": [int(valor) for valor in goles_recientes_eq1.split(",")],
            "factor_local": float(factor_local_eq1)
        }

        equipo2 = {
            "nombre":nombre_eq2,
            "goles_anotados": float(goles_anotados_eq2),
            "goles_recibidos": float(goles_recibidos_eq2),
            "partidos_jugados": int(partidos_jugados_eq2),
            "tiros_a_puerta": float(tiros_a_puerta_eq2),
            "porterias_imbatidas": float(porterias_imbatidas_eq2),
            "goles_recientes": [int(valor) for valor in goles_recientes_eq2.split(",")],
            "factor_local": float(factor_local_eq2)
        }

        resultados = sim_p.simular_partido(equipo1, equipo2)
        global indice_graficas_global # Variable global para el contador
        indice_graficas_global = tk.IntVar(value=0) # Indice para indicar que grafica mostrar
        mostrar_resultados(resultados, nombre_eq1, nombre_eq2, lista_labels, frame_grafica, indice_graficas_global) # lista_labels son los widgets donde se muestra el resutlados
        crear_indicador_img(frame_indicador_img, indice_graficas_global.get()) # Actualizar el indicador de los 3 puntos para indicar la grafica actual a mostrar
        boton_sig["state"] = "normal" # Habilitar botones para cambiar de grafica
        boton_ant["state"] = "normal" # Deshabilidar boton si no se ha generado grafica
    except ValueError as e:
        messagebox.showerror("Error:","Valor faltante o tipo de dato incorrecto.")
    except Exception as e:
        messagebox.showerror(f"Error",f"{e}")
    

# Limpia el contenido de los Entrys
def limpiar_campos(frame_grafica: tk.Frame, frame_indicador_img: tk.Frame, lista_labels: list, *campos: str):
    # Limpiar labels de resultados
    lista_labels[0].config(text=f"Promedio de goles equipo 1:")
    lista_labels[1].config(text=f"Promedio de goles equipo 2:")
    lista_labels[2].config(text=f"Probabilidad de victoria equipo 1:")
    lista_labels[3].config(text=f"Probabilidad de victoria equipo 2")
    lista_labels[4].config(text=f"Probabilidad de empate:")

    # Limpiar grafica
    for widget in frame_grafica.winfo_children():
        widget.destroy()

    # Reiniciar indicador
    crear_indicador_img(frame_indicador_img, -1) # Se reinicia con -1

    # Limpiar campos
    for campo in campos:
        campo.set("")

    # Deshabilitar botones para cambiar de grafica
    boton_sig["state"] = "disabled"
    boton_ant["state"] = "disabled"

    plt.close("all")


def crear_ventana():
    ## Creando ventana
    ventana = tk.Tk()
    ventana.geometry("1400x600")
    ventana.title("Simular partido")
    ventana.resizable(1,1)

    ## Frames principales
    frame_config = tk.Frame(ventana, bg="#e2e2e2") # Frame izquierdo
    #frame_config.pack(side="left", fill="both", expand=True)
    frame_config.place(relx=0, rely=0, relwidth=0.5, relheight=1)

    frame_separacion = tk.Frame(ventana, background="grey") # Linea separadora
    frame_separacion.place(relx=0.5, rely=0, relwidth=0.0025, relheight=1)

    frame_resultados = tk.Frame(ventana, bg="#e2e2e2") # Frame deerecho
    #frame_resultados.pack(side="right", fill="both", expand=True)
    frame_resultados.place(relx=0.5025, rely=0, relwidth=0.4975, relheight=1)


    ## Sub Frames de frame_config
    sub_frame_eq1 = tk.Frame(frame_config, bg="white") # Frame izquierdo, equipo1
    sub_frame_eq1.place(relx=0, rely=0, relwidth=0.5, relheight=0.9) # relx=ajustado izquierda(posicion), rely=ajustado arriba, relwidth=anchura relativa, relheight=altura relativa

    sub_frame_eq2 = tk.Frame(frame_config, bg="white") # Frame derecho, equipo2
    sub_frame_eq2.place(relx=0.5020, rely=0, relwidth=0.4980, relheight=0.9)

    sub_frame_separador_config = tk.Frame(frame_config, bg="#e2e2e2")
    sub_frame_separador_config.place(relx=0.5, rely=0, relwidth=0.002, relheight=1)

    sub_frame_btn = tk.Frame(frame_config, bg="#e2e2e2") # Frame de botones
    sub_frame_btn.place(relx=0, rely=0.9, relwidth=1, relheight=0.1)


    ## Labels (textos) y entrys (entradas de texto)
    # EQUIPO 1
    label_equipo1 = tk.Label(sub_frame_eq1, text="EQUIPO 1", bg="white", font="bold")
    label_equipo1.grid(row=0, column=0, columnspan=2, sticky="ew")

    label_nombre_eq1 = tk.Label(sub_frame_eq1, text="Nombre:", bg="white")
    label_nombre_eq1.grid(row=1, column=0, sticky="e", padx=(0,2))
    texto_nombre_eq1 = tk.StringVar()
    entry_nombre_eq1 = ttk.Entry(sub_frame_eq1, textvariable=texto_nombre_eq1, width=30, background="white")
    entry_nombre_eq1.grid(row=1, column=1, sticky="w")

    label_goles_anotados_eq1 = tk.Label(sub_frame_eq1, text="Goles anotados:", bg="white")
    label_goles_anotados_eq1.grid(row=2, column=0, sticky="e", padx=(0,2))
    texto_goles_anotados_eq1 = tk.StringVar()
    entry_goles_anotados_eq1 = ttk.Entry(sub_frame_eq1, textvariable=texto_goles_anotados_eq1, width=30, background="white")
    entry_goles_anotados_eq1.grid(row=2, column=1, sticky="w")

    label_goles_recibidos_eq1 = tk.Label(sub_frame_eq1, text="Goles recibidos:", bg="white")
    label_goles_recibidos_eq1.grid(row=3, column=0, sticky="e", padx=(0,2))
    texto_goles_recibidos_eq1 = tk.StringVar()
    entry_goles_recibidos_eq1 = ttk.Entry(sub_frame_eq1, textvariable=texto_goles_recibidos_eq1, width=30, background="white")
    entry_goles_recibidos_eq1.grid(row=3, column=1, sticky="w")

    label_partidos_jugados_eq1 = tk.Label(sub_frame_eq1, text="Partidos jugados:", bg="white")
    label_partidos_jugados_eq1.grid(row=4, column=0, sticky="e", padx=(0,2))
    texto_partidos_jugados_eq1 = tk.StringVar()
    entry_partidos_jugados_eq1 = ttk.Entry(sub_frame_eq1, textvariable=texto_partidos_jugados_eq1, width=30, background="white")
    entry_partidos_jugados_eq1.grid(row=4, column=1, sticky="w")

    label_tiros_a_puerta_eq1 = tk.Label(sub_frame_eq1, text="Tiros a puerta:", bg="white")
    label_tiros_a_puerta_eq1.grid(row=5, column=0, sticky="e", padx=(0,2))
    texto_tiros_a_puerta_eq1 = tk.StringVar()
    entry_tiros_a_puerta_eq1 = ttk.Entry(sub_frame_eq1, textvariable=texto_tiros_a_puerta_eq1, width=30, background="white")
    entry_tiros_a_puerta_eq1.grid(row=5, column=1, sticky="w")

    label_porterias_imbatidas_eq1 = tk.Label(sub_frame_eq1, text="Porterias imbatidas:", bg="white")
    label_porterias_imbatidas_eq1.grid(row=6, column=0, sticky="e", padx=(0,2))
    texto_porterias_imbatidas_eq1 = tk.StringVar()
    entry_porterias_imbatidas_eq1 = ttk.Entry(sub_frame_eq1, textvariable=texto_porterias_imbatidas_eq1, width=30, background="white")
    entry_porterias_imbatidas_eq1.grid(row=6, column=1, sticky="w")

    label_goles_recientes_eq1 = tk.Label(sub_frame_eq1, text="Goles recientes:", bg="white")
    label_goles_recientes_eq1.grid(row=7, column=0, sticky="e", padx=(0,2))
    texto_goles_recientes_eq1 = tk.StringVar()
    entry_goles_recientes_eq1 = ttk.Entry(sub_frame_eq1, textvariable=texto_goles_recientes_eq1, width=30, background="white")
    entry_goles_recientes_eq1.grid(row=7, column=1, sticky="w")

    label_factor_local_eq1 = tk.Label(sub_frame_eq1, text="Factor local:", bg="white")
    label_factor_local_eq1.grid(row=8, column=0, sticky="e", padx=(0,2))
    texto_factor_local_eq1 = tk.StringVar()
    entry_factor_local_eq1 = ttk.Entry(sub_frame_eq1, textvariable=texto_factor_local_eq1, width=30, background="white")
    entry_factor_local_eq1.grid(row=8, column=1, sticky="w")

    # EQUIPO 2
    label_equipo2 = tk.Label(sub_frame_eq2, text="EQUIPO 2", bg="white", font="bold")
    label_equipo2.grid(row=0, column=0, columnspan=2, sticky="ew")

    label_nombre_eq2 = tk.Label(sub_frame_eq2, text="Nombre:", bg="white")
    label_nombre_eq2.grid(row=1, column=0, sticky="e", padx=(0,2))
    texto_nombre_eq2 = tk.StringVar()
    entry_nombre_eq2 = ttk.Entry(sub_frame_eq2, textvariable=texto_nombre_eq2, width=30, background="white")
    entry_nombre_eq2.grid(row=1, column=1, sticky="w")

    label_goles_anotados_eq2 = tk.Label(sub_frame_eq2, text="Goles anotados:", bg="white")
    label_goles_anotados_eq2.grid(row=2, column=0, sticky="e", padx=(0,2))
    texto_goles_anotados_eq2 = tk.StringVar()
    entry_goles_anotados_eq2 = ttk.Entry(sub_frame_eq2, textvariable=texto_goles_anotados_eq2, width=30, background="white")
    entry_goles_anotados_eq2.grid(row=2, column=1, sticky="w")

    label_goles_recibidos_eq2 = tk.Label(sub_frame_eq2, text="Goles recibidos:", bg="white")
    label_goles_recibidos_eq2.grid(row=3, column=0, sticky="e", padx=(0,2))
    texto_goles_recibidos_eq2 = tk.StringVar()
    entry_goles_recibidos_eq2 = ttk.Entry(sub_frame_eq2, textvariable=texto_goles_recibidos_eq2, width=30, background="white")
    entry_goles_recibidos_eq2.grid(row=3, column=1, sticky="w")

    label_partidos_jugados_eq2 = tk.Label(sub_frame_eq2, text="Partidos jugados:", bg="white")
    label_partidos_jugados_eq2.grid(row=4, column=0, sticky="e", padx=(0,2))
    texto_partidos_jugados_eq2 = tk.StringVar()
    entry_partidos_jugados_eq2 = ttk.Entry(sub_frame_eq2, textvariable=texto_partidos_jugados_eq2, width=30, background="white")
    entry_partidos_jugados_eq2.grid(row=4, column=1, sticky="w")

    label_tiros_a_puerta_eq2 = tk.Label(sub_frame_eq2, text="Tiros a puerta:", bg="white")
    label_tiros_a_puerta_eq2.grid(row=5, column=0, sticky="e", padx=(0,2))
    texto_tiros_a_puerta_eq2 = tk.StringVar()
    entry_tiros_a_puerta_eq2 = ttk.Entry(sub_frame_eq2, textvariable=texto_tiros_a_puerta_eq2, width=30, background="white")
    entry_tiros_a_puerta_eq2.grid(row=5, column=1, sticky="w")

    label_porterias_imbatidas_eq2 = tk.Label(sub_frame_eq2, text="Porterias imbatidas:", bg="white")
    label_porterias_imbatidas_eq2.grid(row=6, column=0, sticky="e", padx=(0,2))
    texto_porterias_imbatidas_eq2 = tk.StringVar()
    entry_porterias_imbatidas_eq2 = ttk.Entry(sub_frame_eq2, textvariable=texto_porterias_imbatidas_eq2, width=30, background="white")
    entry_porterias_imbatidas_eq2.grid(row=6, column=1, sticky="w")

    label_goles_recientes_eq2 = tk.Label(sub_frame_eq2, text="Goles recientes:", bg="white")
    label_goles_recientes_eq2.grid(row=7, column=0, sticky="e", padx=(0,2))
    texto_goles_recientes_eq2 = tk.StringVar()
    entry_goles_recientes_eq2 = ttk.Entry(sub_frame_eq2, textvariable=texto_goles_recientes_eq2, width=30, background="white")
    entry_goles_recientes_eq2.grid(row=7, column=1, sticky="w")

    label_factor_local_eq2 = tk.Label(sub_frame_eq2, text="Factor local:", bg="white")
    label_factor_local_eq2.grid(row=8, column=0, sticky="e", padx=(0,2))
    texto_factor_local_eq2 = tk.StringVar()
    entry_factor_local_eq2 = ttk.Entry(sub_frame_eq2, textvariable=texto_factor_local_eq2, width=30, background="white")
    entry_factor_local_eq2.grid(row=8, column=1, sticky="w")

    # Asignando valores por defecto a los campos
    texto_nombre_eq1.set("Equipo A")
    texto_goles_anotados_eq1.set("45")
    texto_goles_recibidos_eq1.set("30")
    texto_partidos_jugados_eq1.set("20")
    texto_tiros_a_puerta_eq1.set("5.5")
    texto_porterias_imbatidas_eq1.set("8")
    texto_goles_recientes_eq1.set("2,1,3,1,2")
    texto_factor_local_eq1.set("1.2")
    texto_nombre_eq2.set("Equipo B")
    texto_goles_anotados_eq2.set("38")
    texto_goles_recibidos_eq2.set("35")
    texto_partidos_jugados_eq2.set("20")
    texto_tiros_a_puerta_eq2.set("4.8")
    texto_porterias_imbatidas_eq2.set("5")
    texto_goles_recientes_eq2.set("1,0,2,1,0")
    texto_factor_local_eq2.set("0.9")

    # Pesos de columans y renglones
    sub_frame_eq1.columnconfigure(0, weight=1)
    sub_frame_eq1.columnconfigure(1, weight=1)
    sub_frame_eq1.rowconfigure(0, weight=2)
    sub_frame_eq1.rowconfigure(1, weight=1)
    sub_frame_eq1.rowconfigure(2, weight=1)
    sub_frame_eq1.rowconfigure(3, weight=1)
    sub_frame_eq1.rowconfigure(4, weight=1)
    sub_frame_eq1.rowconfigure(5, weight=1)
    sub_frame_eq1.rowconfigure(6, weight=1)
    sub_frame_eq1.rowconfigure(7, weight=1)
    sub_frame_eq1.rowconfigure(8, weight=1)

    sub_frame_eq2.columnconfigure(0, weight=1)
    sub_frame_eq2.columnconfigure(1, weight=1)
    sub_frame_eq2.rowconfigure(0, weight=2)
    sub_frame_eq2.rowconfigure(1, weight=1)
    sub_frame_eq2.rowconfigure(2, weight=1)
    sub_frame_eq2.rowconfigure(3, weight=1)
    sub_frame_eq2.rowconfigure(4, weight=1)
    sub_frame_eq2.rowconfigure(5, weight=1)
    sub_frame_eq2.rowconfigure(6, weight=1)
    sub_frame_eq2.rowconfigure(7, weight=1)
    sub_frame_eq2.rowconfigure(8, weight=1)



    ### Contenido Frame de resultados
    sub_frame_stats_superior = tk.Frame(frame_resultados, bg="#020057") # Frame superior de la parte derecha de la ventana
    sub_frame_stats_superior.place(relx=0, rely=0, relwidth=1, relheight=0.21)

    # Labels para los resultados
    label_titulo = tk.Label(sub_frame_stats_superior, text="RESULTADOS", bg="#020057", font="bold", fg="white")
    label_titulo.grid(row=0, column=0, sticky="ew", columnspan=2)

    label_probab_vic_eq1 = tk.Label(sub_frame_stats_superior, text="Probabilidad de victoria equipo 1:", bg="#020057", fg="white")
    label_probab_vic_eq1.grid(row=1, column=0, sticky="w", padx=30)

    label_probab_vic_eq2 = tk.Label(sub_frame_stats_superior, text="Probabilidad de victoria equipo 2:", bg="#020057", fg="white")
    label_probab_vic_eq2.grid(row=2, column=0, sticky="w", padx=30)

    label_probab_empate = tk.Label(sub_frame_stats_superior, text="Probabilidad de empate:", bg="#020057", fg="white")
    label_probab_empate.grid(row=3, column=0, sticky="w", padx=30, pady=(0,15))

    label_promedio_goles_eq1 = tk.Label(sub_frame_stats_superior, text="Promedio de goles equipo 1:", bg="#020057", fg="white")
    label_promedio_goles_eq1.grid(row=1, column=1, sticky="w", padx=30)

    label_promedio_goles_eq2 = tk.Label(sub_frame_stats_superior, text="Promedio de goles equipo 2:", bg="#020057", fg="white")
    label_promedio_goles_eq2.grid(row=2, column=1, sticky="w", padx=30)

    sub_frame_stats_superior.columnconfigure(0, weight=1)
    sub_frame_stats_superior.columnconfigure(1, weight=1)
    sub_frame_stats_superior.rowconfigure(0, weight=1)
    #sub_frame_stats_superior.rowconfigure(1, weight=1)
    #sub_frame_stats_superior.rowconfigure(2, weight=1)
    #sub_frame_stats_superior.rowconfigure(3, weight=1)

    lista_resultados = [
        label_promedio_goles_eq1, label_promedio_goles_eq2, label_probab_vic_eq1,
        label_probab_vic_eq2, label_probab_empate
    ]

    ## Frame stats inferior (botones y grafica)
    sub_frame_stats_inferior = tk.Frame(frame_resultados, bg="white")
    sub_frame_stats_inferior.place(relx=0, rely=0.21, relwidth=1, relheight=0.75)

    # Frame para mostrar la grafica
    sub_frame_grafica = tk.Frame(sub_frame_stats_inferior, bg="white")
    sub_frame_grafica.place(relx=0.05, rely=0, relwidth=0.9, relheight=1)

    # Frames para los botones laterales (cambiar imagen)
    sub_frame_btn_sig = tk.Frame(sub_frame_stats_inferior, bg="white")
    sub_frame_btn_sig.place(relx=0.95, rely=0.35, relwidth=0.05, relheight=0.3)
    sub_frame_btn_ant = tk.Frame(sub_frame_stats_inferior, bg="white")
    sub_frame_btn_ant.place(relx=0, rely=0.35, relwidth=0.05, relheight=0.3)

    # Frame para el indicador del indice de la imagen
    sub_frame_indicador_img = tk.Frame(frame_resultados, bg="white")
    sub_frame_indicador_img.place(relx=0, rely=0.96, relwidth=1, relheight=0.04)
    crear_indicador_img(sub_frame_indicador_img, -1) # -1 indica que no se ha creado grafica

    # Botones para cambiar la imagen de la grafica
    img_sig = Image.open("C:/Victor/Trabajos Fes/9no Semestre/Modelado y Simulacion/Proyecto/btn_sig.png") 
    img_ant = Image.open("C:/Victor/Trabajos Fes/9no Semestre/Modelado y Simulacion/Proyecto/btn_ant.png")
    img_sig = img_sig.resize((20,20)) # Ancho y alto
    img_ant = img_ant.resize((20,20)) # Ancho y alto
    img_sig, img_ant = ImageTk.PhotoImage(img_sig), ImageTk.PhotoImage(img_ant)
    global boton_sig, boton_ant
    boton_sig = ttk.Button(sub_frame_btn_sig, image=img_sig, compound="center", text="", cursor="hand2", command=lambda: cambiar_imagen(sub_frame_grafica, sub_frame_indicador_img, +1))
    boton_sig.pack(side="right", expand=True)
    boton_sig["state"] = "disabled" # Deshabilidar boton si no se ha generado grafica 
    boton_ant = ttk.Button(sub_frame_btn_ant, image=img_ant, compound="center", text="", cursor="hand2", command=lambda: cambiar_imagen(sub_frame_grafica, sub_frame_indicador_img, -1))
    boton_ant.pack(side="left", expand=True)
    boton_ant["state"] = "disabled" # Deshabilidar boton si no se ha generado grafica


    ## Botones Iniciar y Limpiar
    boton_iniciar = ttk.Button(
        sub_frame_btn,
        text="Iniciar",
        command=lambda: simular_previo( # Obtener los datos indtroducidos en los campos antes de inicar la simulacion
            texto_nombre_eq1.get(),
            texto_goles_anotados_eq1.get(),
            texto_goles_recibidos_eq1.get(),
            texto_partidos_jugados_eq1.get(),
            texto_tiros_a_puerta_eq1.get(),
            texto_porterias_imbatidas_eq1.get(),
            texto_goles_recientes_eq1.get(),
            texto_factor_local_eq1.get(),
            texto_nombre_eq2.get(),
            texto_goles_anotados_eq2.get(),
            texto_goles_recibidos_eq2.get(),
            texto_partidos_jugados_eq2.get(),
            texto_tiros_a_puerta_eq2.get(),
            texto_porterias_imbatidas_eq2.get(),
            texto_goles_recientes_eq2.get(),
            texto_factor_local_eq2.get(),
            lista_resultados, # Lista con los objetos (Labels) donde se mostraran los resultados, deben ir en orde como se muestran en pantalla
            sub_frame_grafica,
            sub_frame_indicador_img # Frame donde se coloca el indicador con 3 puntos para indicar la grafica actual
        ),
        cursor="hand2", 
    )
    boton_iniciar.grid(row=0, column=0, sticky="nsew", padx=50, pady=12)

    boton_limpiar = ttk.Button(
        sub_frame_btn,
        text="Limpiar campos",
        command=lambda: limpiar_campos( # StringVar's a limpiar (objetos)
            sub_frame_grafica, # Limpiar grafica (siempre debe ser el primer argumento que se pasa)
            sub_frame_indicador_img, # Limpiar el indicador de la posicion de la grafica actual. Debe ser el 2do argumento
            lista_resultados, # Limpiar resultados. Debe ser el tercer argumento que se le pasa
            texto_nombre_eq1,
            texto_goles_anotados_eq1,
            texto_goles_recibidos_eq1,
            texto_partidos_jugados_eq1,
            texto_tiros_a_puerta_eq1,
            texto_porterias_imbatidas_eq1,
            texto_goles_recientes_eq1,
            texto_factor_local_eq1,
            texto_nombre_eq2,
            texto_goles_anotados_eq2,
            texto_goles_recibidos_eq2,
            texto_partidos_jugados_eq2,
            texto_tiros_a_puerta_eq2,
            texto_porterias_imbatidas_eq2,
            texto_goles_recientes_eq2,
            texto_factor_local_eq2
        ),
        cursor="hand2"
    )
    boton_limpiar.grid(row=0, column=1, sticky="nsew", padx=50, pady=12)

    ## Pesos de las comlumnas y renglones de los botones
    sub_frame_btn.columnconfigure(0, weight=1)
    sub_frame_btn.columnconfigure(1, weight=1)
    sub_frame_btn.rowconfigure(0, weight=1)
    
    ventana.protocol("WM_DELETE_WINDOW", lambda:al_cerrar(ventana)) # Al cerrar la ventana tambien cerrar procesos de plt
    ventana.mainloop()

crear_ventana()