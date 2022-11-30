# Covertidor completo

# Elimnar transicioes vacias

class QuitarTranVacias:
    def __init__(self,numEstados):
        self.automataInicial = {}
        self.e_clausulas = {}
        self.automataFinal = {}
        aux = 0
        for i in range(numEstados):
            aux="q"+str(i)
            self.automataInicial[aux]={}
            self.e_clausulas[aux]={}
            
    def agregar_estado(self,estado,tranA,conectaConA,tranB,conectaConB,tranVacia):   
        self.automataInicial[estado]={tranA:conectaConA,tranB:conectaConB,"e":tranVacia}
        
    def mostrarAutomataInicial(self):
        self.claves = list(self.automataInicial.keys())
        for c in self.claves:
            print(f"{c} | {self.automataInicial[c]}")
            
    def mostrarAutomataFinal(self):
        self.claves = list(self.automataFinal.keys())
        for c in self.claves:
            print(f"{c} | {self.automataFinal[c]}")
    
    def __crear_eClausulas(self,estado):
        e_clausula = []
        e_clausula = self.automataInicial[estado]["e"]
        if(len(e_clausula)==0):
            pass
        else:
            e_temp = 0
            for e in e_clausula:
                if(self.automataInicial[e]["e"]==[]):
                    pass
                else:  
                    e_temp = self.automataInicial[e]["e"]
                    for i in e_temp:  # agregando las conexiones con las otras transiciones vacias
                        if(i in e_clausula):
                            pass
                        else:
                            e_clausula.append(i)
        if(estado in e_clausula):
            pass
        else:
            e_clausula.append(estado)
            e_clausula.sort()
        self.e_clausulas[estado]={"e":e_clausula}
        
    def __valorarEstados(self,estados):
        resA = []
        resB = []
        temp_A = []
        temp_B = []
        for e in estados:
            temp_A = self.automataInicial[e]["a"]
            temp_B = self.automataInicial[e]["b"]
            for i in temp_A:
                resA.append(i)
            for i in temp_B:
                resB.append(i)
        resA = list(set(resA))
        resB = list(set(resB))
        resA.sort()
        resB.sort()
        if("0" in resA and len(resA)>1):
            resA.remove("0")
        if("0" in resB and len(resB)>1):
            resB.remove("0")
        return resA,resB
            
        
    def __resultado_eClasulas(self,res):
        resFinal = []
        if(res==["0"]):   # si se busca una e clausula de 0
            return ["0"]
        elif("q" in res): # si se busca un solo estado
            temp = self.e_clausulas[res]["e"]  
            for i in temp:
                resFinal.append(i)
            resFinal = list(set(resFinal))
            resFinal.sort()
            return resFinal
        else: # si se busca mas de un estado
            for estado in res:
                temp = self.e_clausulas[estado]["e"]
                for i in temp:
                    resFinal.append(i)
            resFinal = list(set(resFinal))
            resFinal.sort()
            return resFinal
        
    def __valorar_eClausulas(self):
        e_claus = []
        resA = []
        resB = []
        e_resA = []
        e_resB = []
        estados = list(self.e_clausulas.keys())
        for e in estados:
            e_claus = self.__resultado_eClasulas(e)
            resA, resB = self.__valorarEstados(e_claus)
            e_resA = self.__resultado_eClasulas(resA)
            e_resB = self.__resultado_eClasulas(resB)
            self.automataFinal[e]={"a":e_resA,"b":e_resB}
        
    def eliminarTransiciones(self):
        estados = list(self.automataInicial.keys())
        for e in estados:
            self.__crear_eClausulas(e)
        self.__valorar_eClausulas() 
        
    def regresarResultado(self):
        return self.automataFinal



# Covertidor AFND -> AFD

class Convertidor:
    def __init__(self,numEstados):  # En numEstados se puede introducir el número de estados o el automata completo en forma de diccionario
        self.automataOriginal = {}
        self.nuevoAutomata = {}
        self.transiciones = []   
        self.claves = []
        self.nuevasValoraciones = [["q0"]] # siempre se inicia la valoracion con q0
        self.valoracionesHechas = []
        self.nuevosEstados={}
        self.auxCrearE = 0
        self.equivalencias = {}
        if(type(numEstados)==dict):
            self.automataOriginal = numEstados
        else:
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
    




# Generando el automata 
# *Estado vacio se represeta con 0
# agregar_estado() acepta lo siguiente: agregar_estado(estado, "a", transiciones con a, "b", transiciones con b, transiciones vacias del estado)

automataInicial = QuitarTranVacias(5)
automataInicial.agregar_estado("q0", "a", ["q1","q2","q3"], "b", ["0"], [])   
automataInicial.agregar_estado("q1", "a", ["0"],  "b", ["q4"], ["q4"])
automataInicial.agregar_estado("q2", "a", ["q1"], "b", ["q4"], [])
automataInicial.agregar_estado("q3", "a", ["q2","q3","q4"], "b", ["q3"], ["q2","q4"])
automataInicial.agregar_estado("q4", "a", ["q1"], "b", ["q3"], [])

# Mostrando automata inicial

print(" - Automata con transiciones vacías - ")
automataInicial.mostrarAutomataInicial()

# Eliminando trasiciones vacías

automataInicial.eliminarTransiciones()

# Asignando el automata sin transiciones vacías

automataSinVacias = automataInicial.regresarResultado()

# Convirtiendo de AFND a AFD

automataFinal = Convertidor(automataSinVacias)
automataFinal.convertirAFD()

# Mostrando el automata final

print(" - AFD - ")
automataFinal.recorrerNuevoAutomata()