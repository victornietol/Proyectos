# Proyecto LFA
# Gallegos Zamora Ivan
# Nieto Licona Victor Manuel 

# AFNDTV -> AFD

class Convertidor:
    def __init__(self,numEstados):
        self.automataOriginalVacio = {} 
        self.automataOriginal = {}
        self.nuevoAutomata = {}
        self.eClausula = {}
        self.estados = [] 
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
            self.automataOriginalVacio[aux]={} 
            self.eClausula.setdefault(aux) 
            self.estados.append(aux)
            self.automataOriginal[aux] = {} 
            
    def __eTabla(self,estado,conectaCon): #agregar
        if conectaCon[0] == "0":
            self.eClausula[estado] = set()
            self.eClausula[estado].add(estado)
        else:
            self.eClausula[estado] = set([ i for i in conectaCon])
            self.eClausula[estado].add(estado)  
    
    def __unionClausulasVacias(self): #agregar
        for clausula in self.estados:
            for conjunto in self.eClausula[clausula]:
                if len(self.eClausula[clausula]) == 1:
                    pass
                else:
                    self.eClausula[clausula] = self.eClausula[clausula].union(self.eClausula[conjunto])
            
         
    def agregar_estado(self,estado,transicion,conectaCon):
        self.automataOriginalVacio[estado].setdefault(transicion,conectaCon) #cambiar
        if transicion != "e":
            self.transiciones.append(transicion)   # guardando transiciones
            self.transiciones = list(set(self.transiciones)) # eliminando transiciones repetidas
            self.automataOriginal[estado].setdefault(transicion,{})        
        elif transicion == "e":
            self.__eTabla(estado,conectaCon)
            if estado == self.estados[-1]:
                self.__unionClausulasVacias()
                
    def convertirAFND(self):
        for estado in self.eClausula:
            for transicion in self.transiciones:
                for conjunto in self.eClausula[estado]:
                    estado_clausula = self.automataOriginalVacio[conjunto][transicion]
                    if estado_clausula == ["0"]:
                        if len(self.automataOriginal[estado][transicion]) == 0:
                            self.automataOriginal[estado][transicion] = estado_clausula
                        else:
                            pass
                    else:                       
                        for elemento in estado_clausula:
                            conjuntoClausula = self.eClausula[elemento]
                            if list(conjuntoClausula) != ["0"]:
                                self.automataOriginal[estado][transicion] = list(set(self.automataOriginal[estado][transicion]).union(conjuntoClausula))
                temp = self.automataOriginal[estado][transicion]
                temp.sort()
                if("0" in temp and len(temp)>1):
                    temp.remove("0")
                self.automataOriginal[estado][transicion] = temp
                
               
    def __crear_estados(self,resA,resB):
        ind="q"+str(self.auxCrearE)
        self.nuevosEstados.update({ind:{"a":resA,"b":resB}})
        self.auxCrearE+=1
           
    def recorrerAutomataVacio(self):
        self.claves = list(self.automataOriginalVacio.keys())
        for c in self.claves:
            print(f"{c} -> {self.automataOriginalVacio[c]}")
    
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
        
            

     
# Generando AFNDTV
# *Estado vacio se representa con 0

# Ejemplo 1 
conversion_1 = Convertidor(5)
conversion_1.agregar_estado("q0", "a", ["q1","q2","q3"])
conversion_1.agregar_estado("q0", "b", ["0"])
conversion_1.agregar_estado("q0", "e", ["0"])

conversion_1.agregar_estado("q1", "a", ["0"])
conversion_1.agregar_estado("q1", "b", ["q4"])
conversion_1.agregar_estado("q1", "e", ["q4"])

conversion_1.agregar_estado("q2", "a", ["q1"])
conversion_1.agregar_estado("q2", "b", ["q4"])
conversion_1.agregar_estado("q2", "e", ["0"])

conversion_1.agregar_estado("q3", "a", ["q2","q3","q4"])
conversion_1.agregar_estado("q3", "b", ["q3"])
conversion_1.agregar_estado("q3", "e", ["q2","q4"])

conversion_1.agregar_estado("q4", "a", ["q1"])
conversion_1.agregar_estado("q4", "b", ["q3"])
conversion_1.agregar_estado("q4", "e", ["0"])

# Convirtiendo de AFND a AFD
conversion_1.convertirAFND()

# Convirtiendo de AFND a AFD

conversion_1.convertirAFD()

# Mostrando conversiones
print(" - AFNDTV 1 - ")
conversion_1.recorrerAutomataVacio()

print(" - AFND 1 - ")
conversion_1.recorrerAutomata()
print(" - AFD 1 - ")
conversion_1.recorrerNuevoAutomata()