# Importando los módulos para usar LEX y YACC en el compilador
import ply.lex as lex
import ply.yacc as yacc

# Importando los módulos para la interfaz gráfica
import os
import webbrowser
import tkinter as tk
from tkinter import LEFT, PhotoImage, Toplevel, ttk
from tkinter import messagebox  as mb
from PIL import Image, ImageTk

class Compilador:
    def __init__(self):
        # Base de la ventana
        self.ventana = tk.Tk()
        self.ventana.title("Proyecto. Compiladores")  #Titulo de la ventana
        self.ventana.resizable(False,False)        #Redimensionar ventana, valores True(1) y False(0)
        self.ventana.iconbitmap('imagenes/compilador.ico')  #Colocar imagen en la esquina
        self.ventana.geometry("650x600")      #Asignar el tamaño de la ventana
        self.ventana.config(bg="white")   #Asiganr color del fondo
        self.barra_menu()
        
        # Imagenes
        img_ayuda = tk.PhotoImage(file='imagenes/inter1.png')
        img_unam = tk.PhotoImage(file='imagenes/logo_unam.png')
        img_fes = tk.PhotoImage(file='imagenes/logo_fes.png')
                
        # Frames de la ventana
        v_frame_superior = tk.Frame(self.ventana, width='600', height='50', bg='#16345a')
        v_frame_intermedio = tk.Frame(self.ventana, width='650', height='450', bg='white')
        v_frame_inferior = tk.Frame(self.ventana, width='650', height='50', bg='#e7e9ec')
        separador = ttk.Separator(self.ventana, orient='horizontal')
        
        
        v_frame_superior.pack(side=tk.TOP, fill='both')
        v_frame_intermedio.pack(fill='both', expand='True')
        separador.pack(fill='x')
        v_frame_inferior.pack(side='bottom')
        
        
        # Botones
        boton_ayuda = tk.Button(v_frame_superior, image=img_ayuda, cursor='hand2', borderwidth=0,
                                        background='#16345a', command=self.ayuda).place(x=600, y=8) 
        boton_iniciar = ttk.Button(v_frame_inferior, text='Iniciar', cursor='hand2', 
                                   command=self.compilar).place(x=250, y=10)  
        boton_limpiar = ttk.Button(v_frame_inferior, text='Limpiar', cursor='hand2', 
                                   command=self.limpiar_texto).place(x=330, y=10)
        boton_modificar = ttk.Button(v_frame_inferior, text='Modificar', cursor='hand2',
                                     command=self.modificar_txt).place(x=550, y=10)
        boton_unam = tk.Button(v_frame_superior, cursor='hand2', image=img_unam, borderwidth=0, background='#16345a',
                                command=self.link_unam).place(x=20, y=0)
        boton_fes = tk.Button(v_frame_superior, cursor='hand2', image=img_fes, borderwidth=0, background='#16345a',
                                command=self.link_fes).place(x=70, y=0)
        

        # Caja de texto (Muestra resultados)
        self.caja_resultados = tk.Text(v_frame_intermedio, height=25, width=68, borderwidth=0, font=('Consolas', 12),
                                 wrap='word', state='disable')
        self.caja_resultados.place(x=18, y=10)
        
        # Scrollbar
        self.scrollbar = tk.Scrollbar(v_frame_intermedio)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar.config(command=self.caja_resultados.yview)
        self.caja_resultados.config(yscrollcommand=self.scrollbar.set) 
        
        # Texto superior
        titulo_top = tk.Label(v_frame_superior, text='Compilador', font=('Eras Bold ITC', 18),
                              background='#16345a', foreground='white').place(x=250, y=8)
        
        
        self.ventana.mainloop()
             
        
    def insertar_texto(self,texto):
        # Habilitando la escritura
        self.caja_resultados.configure(state='normal')
        self.caja_resultados.insert(tk.END,f'{texto}')
        # Deshabilitar la escritura
        self.caja_resultados.configure(state='disabled')
        self.caja_resultados.see(tk.END)

    def cerrar_ayuda(self):     
        self.v_ayuda.destroy()
        
    def cerrar_objetivo(self):
        self.v_objetivo.destroy()
        
    def limpiar_texto(self):
        self.caja_resultados.configure(state='normal')
        self.caja_resultados.delete("1.0","end")
        self.caja_resultados.configure(state='disable')
        
    def modificar_txt(self):
        try:          
            cmd = "entrada.txt"
            os.system(cmd)
        except Exception:
            mb.showerror('Error','No es posible abrir el archivo entrada.txt, ábralo manualmente.')

    def ayuda(self):
        # Nueva ventana
        self.v_ayuda = Toplevel(self.ventana)
        self.v_ayuda.title('Ayuda')
        self.v_ayuda.iconbitmap('imagenes/bot3.ico')
        self.v_ayuda.geometry('450x620')
        self.v_ayuda.config(background='white')
        separador_a = ttk.Separator(self.v_ayuda, orient='horizontal')
        separador_a.pack(fill='x')

        # Texto
        texto_ayuda = tk.Text(self.v_ayuda, height=40, width=60, borderwidth=0, font=('Bahnschrift Light', 10)
                                , wrap='word')
        texto_ayuda.place(x=12, y=12)    
        texto_ayuda.configure(state='normal')
        texto_ayuda.insert(tk.END,(open('informacion/ayuda.txt',encoding='utf-8').read()))  
        texto_ayuda.configure(state='disabled')
        self.v_ayuda.resizable(0,0)

        # Parte baja de la ventana
        ayuda_frame = tk.Frame(self.v_ayuda,width='450', height='40')
        ayuda_frame.pack(side='bottom')

        # Boton
        boton_aceptar = ttk.Button(ayuda_frame, cursor='hand2', 
                                text='Aceptar', command=self.cerrar_ayuda).place(x=360,y=8) 
       
    def objetivo(self):
        # Ventana objetivo
        self.v_objetivo = Toplevel(self.ventana)
        self.v_objetivo.title('Objetivo')
        self.v_objetivo.iconbitmap('imagenes/compilador.ico')
        self.v_objetivo.geometry('450x130')
        self.v_objetivo.config(background='white')
        separador = ttk.Separator(self.v_objetivo, orient='horizontal')
        separador.pack(fill='x')

        # Texto
        texto_objetivo = tk.Text(self.v_objetivo, height=30, width=60, borderwidth=0, font=('Bahnschrift Light', 10)
                                , wrap='word')
        texto_objetivo.place(x=12, y=12)    
        texto_objetivo.configure(state='normal')
        texto_objetivo.insert(tk.END,(open('informacion/objetivo.txt',encoding='utf-8').read()))  
        texto_objetivo.configure(state='disabled')
        self.v_objetivo.resizable(0,0)

        # Parte baja de la ventana
        objetivo_frame = tk.Frame(self.v_objetivo,width='450', height='40')
        objetivo_frame.pack(side='bottom')

        # Boton
        boton_aceptar =ttk.Button(objetivo_frame, cursor='hand2', 
                                text='Aceptar', command=self.cerrar_objetivo).place(x=360,y=8) 
      
    def acerca(self):
        mb.showinfo('Acerca de ...',(open('informacion/acerca.txt', encoding='utf-8').read()) )  
        
    def codigo_github(self):
        webbrowser.open('https://github.com/victornietol/Proyectos/blob/main/Proyecto_Compiladores/Versiones_gui/Actualizacion_21_05_2023/Proyecto_Compiladores.py')
        
    def link_unam(self):
        webbrowser.open('https://www.unam.mx/')

    def link_fes(self):
        webbrowser.open('https://www.aragon.unam.mx/fes-aragon/#!/inicio')
        
    def barra_menu(self):
        self.menu_bar = tk.Menu(self.ventana)
        self.ventana.config(menu=self.menu_bar)
        self.opciones = tk.Menu(self.menu_bar, tearoff=0)
        self.opciones.add_command(label= 'Objetivo', command= self.objetivo)
        self.opciones.add_command(label= 'Código del programa', command= self.codigo_github)
        self.opciones.add_command(label= 'Acerca de ...', command= self.acerca)
        self.menu_bar.add_cascade(label= 'Opciones', menu= self.opciones)
        
    def compilar(self):
        self.insertar_texto("EJECUTANDO ...\n\n")
        
        # Guardando cada instrucción por separado
        instrucciones = []
        with open('entrada.txt') as texto:
            for linea in texto:
                instrucciones.append(linea)
        
        # Definición de tokens
        tokens  = ('OPERACIONES','PARENT_IZQ','PARENT_DER','COR_IZQ','COR_DER','MAS','MENOS','POR',
                    'DIVIDIDO','DECIMAL','ENTERO','PUNT_COMA','MEZCLA','ROJO','AMARILLO',
                    'AZUL','CONVERSION','CONEXION','CELSIUS','FAHRENHEIT','KELVIN')
        
        # Valor de los tokens
        t_OPERACIONES  = r'Operacion'
        t_PARENT_IZQ = r'\('
        t_PARENT_DER = r'\)'
        t_COR_IZQ = r'\['
        t_COR_DER = r'\]'
        t_MAS = r'\+'
        t_MENOS = r'-'
        t_POR = r'\*'
        t_DIVIDIDO = r'/'
        t_PUNT_COMA = r';'
        t_MEZCLA = r'Mezcla'
        t_CONVERSION = r'Conversion|Conversión'
        t_CONEXION = r'[aA]'
        
        # Caracteres ignorados
        t_ignore = " \t|Â"
        
        # Tokens que regresan un valor
        def t_DECIMAL(t):
            r'\d+\.\d+'
            try:
                t.value = float(t.value)
            except ValueError:
                self.insertar_texto(f"Valor decimal demasiado grande &d {str(t.value)}")
                t.value = 0
            return t
        
        def t_ENTERO(t):
            r'\d+'
            try:
                t.value = int(t.value)
            except ValueError:
                self.insertar_texto(f"Valor entero demasiado grande %d {str(t.value)}")
                t.value = 0
            return t
        
        def t_ROJO(t):
            r'rojo|ROJO|Rojo'
            t.value = 'ROJO'
            return t
            
        def t_AMARILLO(t):
            r'amarillo|AMARILLO|Amarillo'
            t.value = 'AMARILLO'
            return t
        
        def t_AZUL(t):
            r'azul|AZUL|Azul'
            t.value = 'AZUL'
            return t
        
        def t_CELSIUS(t):
            r'Celsius|CELSIUS|°C|celsius'
            t.value = 'C'
            return t
        
        def t_FAHRENHEIT(t):
            r'Fahrenheit|FAHRENHEIT|°F|fahrenheit'
            t.value = 'F'
            return t
        
        def t_KELVIN(t):
            r'Kelvin|KELVIN|°K|kelvin'
            t.value = 'K'
            return t
        
        def t_newline(t):
            r'\n+'
            t.lexer.lineno += t.value.count("\n")
            
        def t_error(t):
            texto = "Caracter ilegal '%s'" % t.value[0]
            self.insertar_texto(texto+"\n")
            t.lexer.skip(1)
        
        
        # Construyendo el analizador léxico
        lexer = lex.lex()
        
        # Declarando reglas de precedencia
        precedence = (('left','MAS','MENOS'),('left','POR','DIVIDIDO'),
                        ('right','UMENOS'))
        
        # Definición de la gramática para los casos de operaciones, mezcla de colores y conversiones
        def p_instrucciones_lista(t):
            '''instrucciones    : instruccion instrucciones
                                | instruccion '''
        
        def p_instrucciones_tipo(t):
            '''instruccion : OPERACIONES COR_IZQ expresion_num COR_DER PUNT_COMA
                            | MEZCLA COR_IZQ expresion_color COR_DER PUNT_COMA
                            | CONVERSION COR_IZQ expresion_conver COR_DER PUNT_COMA'''
            self.insertar_texto(f"      El resultado es: {str(t[3])}\n\n")
        
        def p_expresion_binaria(t):
            '''expresion_num : expresion_num MAS expresion_num
                          | expresion_num MENOS expresion_num
                          | expresion_num POR expresion_num
                          | expresion_num DIVIDIDO expresion_num'''   
            if( t[2] == '+' ): 
                t[0] = t[1] + t[3]
            elif(t[2] == '-'): 
                t[0] = t[1] - t[3]
            elif(t[2] == '*'): 
                t[0] = t[1] * t[3]
            elif(t[2] == '/'): 
                t[0] = t[1] / t[3]
        
        def p_expresion_unaria(t):
            'expresion_num : MENOS expresion_num %prec UMENOS'
            t[0] = -t[2]
        
        def p_expresion_agrupacion(t):
            'expresion_num : PARENT_IZQ expresion_num PARENT_DER'
            t[0] = t[2]
        
        def p_expresion_number(t):
            '''expresion_num    : ENTERO
                            | DECIMAL'''
            t[0] = t[1]
            
        def p_expresion_colores(t):
            'expresion_color : valor_color MAS valor_color'
            if((t[1] == 'ROJO' and t[3] == 'AMARILLO') or (t[1] == 'AMARILLO' and t[3] == 'ROJO')):
                t[0] = 'Naranja'
            elif((t[1] == 'AMARILLO' and t[3] == 'AZUL') or (t[1] == 'AZUL' and t[3] == 'AMARILLO')):
                t[0] = 'Verde'
            elif((t[1] == 'AZUL' and t[3] == 'ROJO') or (t[1] == 'ROJO' and t[3] == 'AZUL')):
                t[0] = 'Violeta'
            elif(
                 (t[1] == 'ROJO' and t[3] == 'ROJO') or
                 (t[1] == 'AMARILLO' and t[3] == 'AMARILLO') or
                 (t[1] == 'AZUL' and t[3] == 'AZUL')
                 ):
                t[0] = t[1]
            
        def p_valor_color(t):
            '''valor_color :  ROJO
                            | AMARILLO
                            | AZUL'''
            t[0] = t[1]
            
        def p_expresion_conversiones(t):
            'expresion_conver : escala PARENT_IZQ expresion_num PARENT_DER CONEXION escala'
            if(t[1] == 'C' and t[6] == 'F'):   # Celsius a Fahrenheit
                t[0] = (float(t[3])*1.8) + 32.0
            elif(t[1] == 'F' and t[6] == 'C'):   # Faherenheit a Celsius
                t[0] = (float(t[3])-32.0) / 1.8
            elif(t[1] == 'C' and t[6] == 'K'):   # Celsius a Kelvin
                t[0] = float(t[3]) + 273.15
            elif(t[1] == 'K' and t[6] == 'C'):   # Kelvin a Celsius
                t[0] = float(t[3]) - 273.15
            elif(t[1] == 'F' and t[6] == 'K'):   # Fahrenheit a Kelvin
                t[0] = ((float(t[3])-32.0) / 1.8) + 273.15
            elif(t[1] == 'K' and t[6] == 'F'):   # Kelvin a Fahrenheit 
                t[0] = ((float(t[3]) - 273.15)*1.8) + 32.0
            
        def p_tipo_escala(t):
            '''escala : CELSIUS
                      | FAHRENHEIT
                      | KELVIN'''
            t[0] = t[1]
        
        # En caso de no cumplir con las reglas
        def p_error(t):
            texto = "Error sintáctico en '%s'" % t.value
            self.insertar_texto(texto+"\n")
        
        # Construyendo el analizador sintáctico
        parser = yacc.yacc()
        
        # Usando YACC
        for linea in instrucciones:
            self.insertar_texto(f"Instrucción:   {linea}")
            parser.parse(linea)
        
        self.insertar_texto("PROCESO TERMINADO.\n\n\n")
        
if __name__ == "__main__":
    Compilador()