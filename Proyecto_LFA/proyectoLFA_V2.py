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
        
    def crear_estados(self,resA,resB):
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
            
    def valorarEstados(self,estados):
        valAct = []
        resultado = []
        resA = []
        resB = []
        self.nuevasValoraciones = []       
        if(estados in self.valoracionesHechas):
            pass    
        else:
            self.valoracionesHechas.append(estados)                      
            if(estados==["0"]):
                self.crear_estados(["0"],["0"])               
            else:              
                for e in estados:   # valoracion con "a"
                    valAct = self.automataOriginal[e]["a"] # lista con la validacion por separado de cada "a"
                    for elem in valAct:
                        if(elem in resultado):  
                            pass
                        else:
                            resultado.append(elem)
                            resA.append(elem)
                        if("0" in resultado and len(resultado)>1):
                            resultado.remove("0")
                            resA.remove("0")
                        if(resultado not in self.nuevasValoraciones):
                            self.nuevasValoraciones.append(resultado)
                           
                resultado = [] 
                for e in estados:  # valoracion con "b"
                    valAct = self.automataOriginal[e]["b"] 
                    for elem in valAct:
                        if(elem in resultado):  
                            pass
                        else:
                            resultado.append(elem) 
                            resB.append(elem)
                        if("0" in resultado and len(resultado)>1):
                            resultado.remove("0")
                            resB.remove("0")
                        if(resultado not in self.nuevasValoraciones):
                            self.nuevasValoraciones.append(resultado)                  
                self.crear_estados(resA,resB)  # creando nuevos estados y su correspondencia
  
            
    def tablaEquivalencias(self):
        keysEst = list(self.nuevosEstados.keys())
        aux = 0
        for estado in keysEst:
            self.equivalencias.update({estado:self.valoracionesHechas[aux]})
            aux+=1 
            
    def obtener_valAB(self,estado):
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
        
            
    def hacer_nAutomata(self):      
        estados = list(self.nuevosEstados)
        for e in estados:
            self.nuevoAutomata[e]={}
            valorA,valorB = self.obtener_valAB(e)
            self.nuevoAutomata[e].setdefault("a",valorA)
            self.nuevoAutomata[e].setdefault("b",valorB)            
            
    def convertirAFD(self):
        vacio = False
        while(len(self.nuevasValoraciones)!=0):
            for val in self.nuevasValoraciones:
                if(val==["0"]):
                    vacio=True
                else:
                    self.valorarEstados(val)
        if(vacio):
            self.valorarEstados(["0"])
        
        self.tablaEquivalencias()
        self.hacer_nAutomata()
        
            

     

# Generando AFND
# *Estado vacio se representa con 0

conversion = Convertidor(4)    

conversion.agregar_estado("q0", "a", ["q1","q2"])
conversion.agregar_estado("q0", "b", ["0"])

conversion.agregar_estado("q1", "a", ["0"])
conversion.agregar_estado("q1", "b", ["q1","q2","q3"])

conversion.agregar_estado("q2", "a", ["q1","q3"])
conversion.agregar_estado("q2", "b", ["0"])

conversion.agregar_estado("q3", "a", ["0"])
conversion.agregar_estado("q3", "b", ["q1","q2"])

# Convirtiendo de AFND a AFD

conversion.convertirAFD()

# Mostrando ambos automatas

print(" - AFND - ")
conversion.recorrerAutomata()

print(" - AFD - ")
conversion.recorrerNuevoAutomata()