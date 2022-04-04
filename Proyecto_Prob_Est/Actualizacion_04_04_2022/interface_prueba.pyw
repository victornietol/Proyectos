from tkinter import *

class interfaz:
    def __init__(self):
        self.ventana = Tk()
        self.ventana.title('Sugerencia de bebida')
        self.ventana.iconbitmap('im_bebida.ico')
        self.v_frame = Frame(self.ventana,width='600', height='250')
        #self.v_frame.config(bg='blue')
        self.v_frame.pack(fill='both', expand='True')

        # Textos
        Label(self.v_frame, text='Nuevo cliente', font=('Candara', 15)).place(x=235, y=15)
        Label(self.v_frame, text='Edad:', font=('Candara', 15)).place(x=10, y=90)
        Label(self.v_frame, text='Temperatura del día:', font=('Candara', 15)).place(x=10, y=130)
        Label(self.v_frame, text='La sugerencia es una bebida:', font=('Candara', 15)).place(x=10, y=190)

        # Entrada de texto
        edad_text = Entry(self.v_frame).place(x=70, y=98)
        temp_text = Entry(self.v_frame).place(x=194, y=137)

        # Boton nueva consulta
        #def codigo_boton():

        #boton_reinicio = Button(ventana, text = 'Nueva consulta',command = codigo_boton)
        boton_reinicio = Button(self.ventana, text = 'Nueva consulta').place(x=495,y=212)
        boton_reinicio = Button(self.ventana, text = 'Consultar').place(x=395,y=212)

        self.ventana.mainloop()

inicio = interfaz()