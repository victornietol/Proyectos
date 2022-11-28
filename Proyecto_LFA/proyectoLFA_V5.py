# AFND -> AFD

class Convertidor:
    def __init__(self,numEstados):
        self.automataOriginal = {}
        self.nuevoAutomata = {}
        self.transiciones = []   
        self.claves = []
        self.nuevasValoraciones = [["q0"]] # siempre se inicia la valoracion con q0
        self.valoracionesHechas = []
        self.nuevosEstados={}
        self.auxCrearE = 0
        self.equivalencias = {}
        aux = 0
        for i in range(numEstados):
            aux="q"+str(i)
            self.automataOriginal[aux]={}       
  
    def agregar_estado(self,estado,transicion,conectaCon):
        self.transiciones.append(transicion)   # guardando transiciones
        self.transiciones = list(set(self.transiciones)) # eliminando transiciones repetidas
        self.automataOriginal[estado].setdefault(transicion,conectaCon)
        
    def __crear_estados(self,resA,resB):
        ind="q"+str(self.auxCrearE)
        self.nuevosEstados.update({ind:{"a":resA,"b":resB}})
        self.auxCrearE+=1
           
    def recorrerAutomata(self):
        self.claves = list(self.automataOriginal.keys())
        for c in self.claves:
            print(f"{c} | {self.automataOriginal[c]}")
            
    def recorrerNuevoAutomata(self):
        estados = list(self.nuevoAutomata.keys())
        for e in estados:
            print(f"{e} | {self.nuevoAutomata[e]}")        
            
    def __valorarEstados(self,estados):
        valAct = []
        resultado = []
        resA = []
        resB = []
        if(estados in self.valoracionesHechas):
            pass    
        else:
            self.valoracionesHechas.append(estados)                      
            if(estados==["0"]):
                self.__crear_estados(["0"],["0"])               
            else:              
                for e in estados:   # valoración con "a"
                    valAct = self.automataOriginal[e]["a"] # lista con la validacion por separado de cada "a"
                    for elem in valAct:
                        if(elem in resultado):                          
                            pass
                        else:
                            resultado.append(elem)
                            resA.append(elem)
                            resultado.sort()    # acomodando los estados
                            resA.sort()
                        if("0" in resultado and len(resultado)>1):
                            resultado.remove("0")        
                            resA.remove("0")                           
                        if(resultado not in self.nuevasValoraciones and resultado not in self.valoracionesHechas):
                            self.nuevasValoraciones.append(resultado)       
                resultado = [] 
                for e in estados:  # valoración con "b"
                    valAct = self.automataOriginal[e]["b"] 
                    for elem in valAct:
                        if(elem in resultado):  
                            pass
                        else:
                            resultado.append(elem) 
                            resB.append(elem)
                            resultado.sort()
                            resB.sort()
                        if("0" in resultado and len(resultado)>1):
                            resultado.remove("0")
                            resB.remove("0")
                        if(resultado not in self.nuevasValoraciones and resultado not in self.valoracionesHechas):
                            self.nuevasValoraciones.append(resultado) 
                self.__crear_estados(resA,resB)  # creando nuevos estados y su correspondencia
                       
    def __tablaEquivalencias(self):
        keysEst = list(self.nuevosEstados.keys())
        aux = 0
        for estado in keysEst:
            self.equivalencias.update({estado:self.valoracionesHechas[aux]})
            aux+=1 
            
    def __obtener_valAB(self,estado):
        valorA = 0
        valorB = 0
        estadosE = list(self.equivalencias.keys())       
        valor = self.nuevosEstados[estado]["a"]            
        for e in estadosE:      # encontrando coincidencia en tabla equivalencias
            if(valor==self.equivalencias[e]):
                valorA = e
        valor = self.nuevosEstados[estado]["b"]
        for e in estadosE:
            if(valor==self.equivalencias[e]):
                valorB = e
        return valorA,valorB
                   
    def __hacer_nAutomata(self):      
        estados = list(self.nuevosEstados)
        for e in estados:
            self.nuevoAutomata[e]={}
            valorA,valorB = self.__obtener_valAB(e)
            self.nuevoAutomata[e].setdefault("a",valorA)
            self.nuevoAutomata[e].setdefault("b",valorB)            
            
    def convertirAFD(self):
        vacio = False
        while(len(self.nuevasValoraciones)!=0):
            for val in self.nuevasValoraciones:  
                if(val==["0"]):
                    vacio=True
                else:
                    self.__valorarEstados(val)
            self.nuevasValoraciones.remove(val)
        if(vacio):
            self.__valorarEstados(["0"])      
        self.__tablaEquivalencias()
        self.__hacer_nAutomata()
        
            

     
# Generando AFND
# *Estado vacio se representa con 0

# Ejemplo 1 
conversion_1 = Convertidor(4)    

conversion_1.agregar_estado("q0", "a", ["q1","q2"])
conversion_1.agregar_estado("q0", "b", ["0"])

conversion_1.agregar_estado("q1", "a", ["0"])
conversion_1.agregar_estado("q1", "b", ["q1","q2","q3"])

conversion_1.agregar_estado("q2", "a", ["q1","q3"])
conversion_1.agregar_estado("q2", "b", ["0"])

conversion_1.agregar_estado("q3", "a", ["0"])
conversion_1.agregar_estado("q3", "b", ["q1","q2"])

# Ejemplo 2
conversion_2 = Convertidor(4) 
conversion_2.agregar_estado("q0", "a", ["0"])
conversion_2.agregar_estado("q0", "b", ["q1","q2"])
conversion_2.agregar_estado("q1", "a", ["q2","q3"])
conversion_2.agregar_estado("q1", "b", ["0"])
conversion_2.agregar_estado("q2", "a", ["q1","q2"])
conversion_2.agregar_estado("q2", "b", ["q2","q3"])
conversion_2.agregar_estado("q3", "a", ["0"])
conversion_2.agregar_estado("q3", "b", ["q2","q3"])

# Ejemplo 3
conversion_3 = Convertidor(3)    
conversion_3.agregar_estado("q0", "a", ["q0","q1"])
conversion_3.agregar_estado("q0", "b", ["q0"])
conversion_3.agregar_estado("q1", "a", ["0"])
conversion_3.agregar_estado("q1", "b", ["q2"])
conversion_3.agregar_estado("q2", "a", ["0"])
conversion_3.agregar_estado("q2", "b", ["0"])

# Ejemplo 4
conversion_4 = Convertidor(4)    
conversion_4.agregar_estado("q0", "a", ["0"])
conversion_4.agregar_estado("q0", "b", ["q0","q1"])
conversion_4.agregar_estado("q1", "a", ["q1","q3"])
conversion_4.agregar_estado("q1", "b", ["0"])
conversion_4.agregar_estado("q2", "a", ["q0"])
conversion_4.agregar_estado("q2", "b", ["q1"])
conversion_4.agregar_estado("q3", "a", ["q2","q3"])
conversion_4.agregar_estado("q3", "b", ["q3"])


# Convirtiendo de AFND a AFD

conversion_1.convertirAFD()
conversion_2.convertirAFD()
conversion_3.convertirAFD()
conversion_4.convertirAFD()

# Mostrando ambas conversiones

print(" - AFND 1 - ")
conversion_1.recorrerAutomata()
print(" - AFD 1 - ")
conversion_1.recorrerNuevoAutomata()

print(" - AFND 2 - ")
conversion_2.recorrerAutomata()
print(" - AFD 2 - ")
conversion_2.recorrerNuevoAutomata()

print(" - AFND 3 - ")
conversion_3.recorrerAutomata()
print(" - AFD 3 - ")
conversion_3.recorrerNuevoAutomata()

print(" - AFND 4 - ")
conversion_4.recorrerAutomata()
print(" - AFD 4 - ")
conversion_4.recorrerNuevoAutomata()