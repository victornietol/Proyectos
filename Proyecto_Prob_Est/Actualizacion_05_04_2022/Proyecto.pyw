from cProfile import label
from cgitb import enable
from ctypes import resize
import tkinter as tk
from tkinter import PhotoImage, Toplevel, ttk
from tkinter import messagebox  as mb
from tokenize import String
from turtle import bgcolor, width
from typing import Text
import pandas as pd
from PIL import Image, ImageTk

class Interfaz:
    def __init__(self):
        self.probabilidades()
        self.ventana = tk.Tk()
        self.ventana.title('Sugerencia de bebida')
        self.ventana.iconbitmap('im_bebida.ico')
        self.ventana.resizable(0,0)
        self.barra_menu()
        self.v_frame = tk.Frame(self.ventana,width='600', height='225', bg='white')
        self.v_frame2 = tk.Frame(self.ventana, width='600', height='50')
        self.v_frame.pack(fill='both', expand='True')
        img = Image.open('pngwing2.png')
        img = ImageTk.PhotoImage(img)

        # Textos
        self.label_nCliente = tk.Label(self.v_frame, text='NUEVO CLIENTE', font=('Candara', 15), bg='white').place(x=235, y=10)
        self.label_edad = tk.Label(self.v_frame, text='Edad:', font=('Candara', 15), bg='white').place(x=136, y=70)
        self.label_tempDia = tk.Label(self.v_frame, text='Temperatura del día:', font=('Candara', 15), bg='white').place(x=10, y=110)
        self.label_sug = tk.Label(self.v_frame, text='La sugerencia es una bebida:', font=('Candara', 15), bg='white').place(x=10, y=170)

        # Entrada de texto
        self.dato_edad = tk.StringVar()
        self.dato_temp = tk.StringVar()
        self.entry_edad = ttk.Entry(self.v_frame, textvariable=self.dato_edad, font=('Bahnschrift Light', 12))
        self.entry_edad.place(x=192, y=74)
        self.entry_temp = ttk.Entry(self.v_frame, textvariable=self.dato_temp, font=('Bahnschrift Light', 12))
        self.entry_temp.place(x=192, y=115)

        # Botones
        self.boton_reinicio = ttk.Button(self.v_frame2, text = 'Nueva consulta', command = self.nueva_consula, cursor = 'hand2')
        self.boton_reinicio.place(x=495,y=11)
        self.boton_consult = ttk.Button(self.v_frame2, text = 'Consultar', command = self.sugerencia, cursor = 'hand2')
        self.boton_consult.place(x=413,y=11)
        self.boton_info = ttk.Button(self.v_frame, image= img, command = self.info, cursor = 'hand2').place(x=557, y=5)

        self.v_frame2.pack(side='bottom')

        self.ventana.mainloop()

    def probabilidades(self):
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
        self.priori_z = [0,0]
        for i in range(len(datos)):
            self.priori_z[datos.Bebida[i]] += 1

        # Divide entre el número de clientes para obtener la distribución de probabilidad
        for  j in range(0,2):
            self.priori_z[j] /= len(datos)

        # Punto 6
        # Cálculo de la distribución conjunta de X y Y
        # La distribución se almacena en una lista de listas (tamaño 3x3)
        # El primer índice corresponde a la edad X (0 para menor de edad, 1 para adulto, 2 para adulto mayor)
        # El segundo índice corresponde a la temperatura del día Y (0 para frío, 1 para templado, 2 para cálido)
        self.evidencia_xy = [[0,0,0] , [0,0,0], [0,0,0]]
        for i in range(0,len(datos)):
            self.evidencia_xy[datos.Edad[i]][datos.Temperatura[i]] += 1

        # Divide entre el número de clientes para obtener la distribución de probabilidad
        for i in range(3):
            for j in range(3):
                self.evidencia_xy[i][j] /= len(datos)

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
        self.likelihood = [[[0,0],[0,0],[0,0]] , [[0,0],[0,0],[0,0]], [[0,0],[0,0],[0,0]]]
        for i in range(3):
            for j in range(3):
                for x in range(2):
                    self.likelihood[i][j][x] = distribucionC_xyz[i][j][x] / self.priori_z[x]

    def sugerencia(self):
        self.boton_consult.config(state=tk.DISABLED)
        self.edad_limpio = self.dato_edad.get()
        self.temp_limpio = self.dato_temp.get()
        self.edad = self.edad_limpio.strip().lower()
        self.temperatura = self.temp_limpio.strip().lower()
        self.boton_consult.config(cursor='')

        try:
            self.edad = int(self.edad)
        except ValueError:
            pass

        try:
            self.temperatura = int(self.temperatura)
        except ValueError:
            pass

        if type(self.edad) == str:  # Verificando si edad es cadena
            if self.edad == 'menor':
                self.edad_c = 0
            elif self.edad == 'adulto':
                self.edad_c = 1
            elif self.edad == 'mayor':
                self.edad_c = 2
            else:
                self.boton_consult.config(state=tk.NORMAL)
                mb.showerror('Error','Edad inválida')
                #print('Edad inválida')

        if type(self.edad) == int:  # Verificando si edad es entero
            if self.edad < 0:
                self.boton_consult.config(state=tk.NORMAL)
                mb.showerror('Error','Edad inválida')
            elif self.edad < 18:
                self.edad_c = 0
            elif (self.edad >= 18) and (self.edad<60):
                self.edad_c = 1
            else:
                self.edad_c = 2

        if type(self.temperatura) == str: # Verificando si temp es cadena
            if (self.temperatura!='frio') and (self.temperatura!='frío') and (self.temperatura!='templado') and \
                (self.temperatura!='calido') and (self.temperatura!='cálido'):
                self.boton_consult.config(state=tk.NORMAL)
                mb.showerror('Error','Temperatura inválida')
                #print('Temperatura inválida')
            elif self.temperatura == 'frío' or self.temperatura == 'frio':
                self.temp_c = 0
            elif self.temperatura == 'templado':
                self.temp_c = 1
            elif self.temperatura == 'cálido' or 'calido':
                self.temp_c = 2

        if type(self.temperatura) == int:  # Verificando si temp es entero
            if self.temperatura <= 10:
                self.temp_c = 0
            elif (self.temperatura > 10) and (self.temperatura < 20):
                self.temp_c = 1
            else:
                self.temp_c = 2

        print(self.edad,self.edad_c)
        print(self.temperatura,self.temp_c)

        self.recomendacion_fria = (self.priori_z[0]*self.likelihood[self.edad_c][self.temp_c][0]) / self.evidencia_xy[self.edad_c][self.temp_c]
        self.recomendacion_caliente = (self.priori_z[1]*self.likelihood[self.edad_c][self.temp_c][1]) / self.evidencia_xy[self.edad_c][self.temp_c]

        if self.recomendacion_fria > self.recomendacion_caliente:
            #print('La sugerencia es una bebida: fría')
            self.label_resultado = tk.Label(self.v_frame, text = 'FRÍA', font=('Candara', 14), fg='blue', bg='white')
            self.label_resultado.place(x=260, y=172)
            
        else:
            #print('La sugerencia es una bebida: caliente')
            self.label_resultado = tk.Label(self.v_frame, text = 'CALIENTE', font=('Candara', 14), fg='red', bg='white')
            self.label_resultado.place(x=260, y=172)
    
    def nueva_consula(self):
        self.dato_edad.set('')
        self.dato_temp.set('')
        self.label_resultado['text'] = ''
        self.edad_c = ''
        self.temp_c = ''
        self.boton_consult.config(cursor = 'hand2', state=tk.NORMAL)

    def info(self):
        self.v_info = Toplevel(self.ventana)
        self.v_info.title('Información')
        self.v_info.geometry('550x350')
        self.v_info.iconbitmap('im_bebida.ico')
        self.v_info.resizable(0,0)
        self.label_inf1 = tk.Label(self.v_info, text='• Edad. El dato sobre la edad se puede ingresar con valores numéricos', font=('Candara', 13)).place(x=10, y= 10)
        self.label_inf2 = tk.Label(self.v_info, text='   o escribiendo menor, adulto o mayor según el siguiente rango', font=('Candara', 13)).place(x=55, y=30)
        self.label_inf6 = tk.Label(self.v_info, text='   de edades:', font=('Candara', 13)).place(x=55, y=50)
        self.label_inf3= tk.Label(self.v_info, text='  Menor  ➞ Personas con menos de 18 años', font=('Candara', 13)).place(x=55, y=90)
        self.label_inf4= tk.Label(self.v_info, text='  Adulto  ➞ Personas desde los 18 años hasta antes de los 60 años', font=('Candara', 13)).place(x=55, y=110)
        self.label_inf5= tk.Label(self.v_info, text='  Mayor  ➞ Personas de 60 años en adelante', font=('Candara', 13)).place(x=55, y=130)
        self.label_inf7= tk.Label(self.v_info, text='• Temperatura. El dato sobre la temperatura del día se puede ingresar', font=('Candara', 13)).place(x=10, y=170)
        self.label_inf8= tk.Label(self.v_info, text='  con el valor númerico sin poner la unidad de medición o', font=('Candara', 13)).place(x=55, y=190)
        self.label_inf9= tk.Label(self.v_info, text='  escribiendo frío, templado o cálido según el siguiente rango ', font=('Candara', 13)).place(x=55, y=210)
        self.label_inf13= tk.Label(self.v_info, text='  de temperaturas:', font=('Candara', 13)).place(x=55, y=230) 
        self.label_inf10= tk.Label(self.v_info, text='   Frío             ➞ De 10°C hacia abajo', font=('Candara', 13)).place(x=55, y=270)
        self.label_inf11= tk.Label(self.v_info, text='   Templado  ➞ Entre 10°C y 20°C', font=('Candara', 13)).place(x=55, y=290)
        self.label_inf12= tk.Label(self.v_info, text='   Cálido         ➞ De 20°C hacia arriba', font=('Candara', 13)).place(x=55, y=310)

    def barra_menu(self):
        self.menu_bar = tk.Menu(self.ventana)
        self.ventana.config(menu=self.menu_bar)
        self.opciones = tk.Menu(self.menu_bar, tearoff=0)
        self.opciones.add_command(label= 'Objetivo y definición', command= self.objetivo)
        self.opciones.add_command(label= 'Código del programa', command= self.codigo_github)
        self.opciones.add_command(label= 'Acerca de ...', command= self.acerca)
        self.menu_bar.add_cascade(label= 'Opciones', menu= self.opciones)

    def acerca(self):
        mb.showinfo('Acerca de ...', 'Universidad Nacional Autónoma de México\nFacultad de Estudios Superiores Aragón\nIngeniería en Computación\nProyecto de la materia Probabilidad y Estadística\nProfesor. Dr. Arturo Rodríguez García\nAlumno. Nieto Licona Victor Manuel\nGrupo. 2457\nSemestre 2022-II')

    def objetivo(self):
        self.v_objetivo = Toplevel(self.ventana)
        self.v_objetivo.title('Objetivo y definición del problema')
        self.v_objetivo.iconbitmap('im_bebida.ico')
        self.v_objetivo.geometry('970x425')
        self.text_obj = tk.Message(self.v_objetivo, text=('• Objetivo\n\nDiseñar un clasificador bayesiano ingenuo que permita'
        +' predecir el comportamiento de un cliente.\n\n• Definición del problema\n\nEn una cafetería se instala un robot que'
        +' atenderá a los clientes. Se desea que el robot tenga iniciativa al atender al cliente, y recomiende productos'
        +' antes de que se lo soliciten. El robot cuenta con un sistema de visión que le permite calcular la edad aproximada'
        +' del cliente y cuenta con acceso a la web para saber la temperatura actual. A partir de la edad del cliente, y de'
        +' la temperatura del día, el robot le recomendará una bebida fría o una bebida caliente.\n\n'
        +'¿Cómo va a tomar esta decisión el robot? Es aquí donde entra la probabilidad y estadística. El robot contará con' 
        +' datos previos sobre compras realizadas. En cada compra se registró la edad del cliente, la temperatura del día,' 
        +' y el tipo de bebida que compró (fría o caliente). Estos datos se encuentran en un archivo de texto y servirán para' 
        +' que el robot aprenda lo que debe hacer cuando llegue un nuevo cliente. Este aprendizaje lo haremos con un' 
        +' algoritmo bastante sencillo que se conoce como clasificador ingenuo de Bayes, y que consiste en calcular'
        +' probabilidades condicionales con ayuda de la regla de Bayes. En este caso, nuestras variables predictoras serán la'
        +' edad del cliente y la temperatura del día. Se dice que el método que usaremos es ingenuo, porque utiliza la'
        +' hipótesis de que estas variables predictoras son independientes entre sí. A partir de estas variables el robot'
        +' debe predecir el tipo de bebida adecuado para el cliente.'), padx=30, pady=5, aspect=250, font=('Candara', 13), justify=tk.LEFT)
        self.v_objetivo.resizable(0,0)
        self.text_obj.pack()
        
    def codigo_github(self):
        import webbrowser
        webbrowser.open('https://github.com/victornietol/Proyectos/blob/main/Proyecto_Prob_Est/Actualizacion_04_04_2022/Proyecto.pyw')

inicio = Interfaz()