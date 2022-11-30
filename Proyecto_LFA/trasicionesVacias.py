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
                #print(e)
                #print(self.automataInicial[e]["e"])
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
                
            
            #resA = self.automataInicial[e]["a"]
            #resB = self.automataInicial[e]["b"]
            e_resA = self.__resultado_eClasulas(resA)
            e_resB = self.__resultado_eClasulas(resB)
            self.automataFinal[e]={"a":e_resA,"b":e_resB}
        
    def eliminarTransiciones(self):
        estados = list(self.automataInicial.keys())
        for e in estados:
            self.__crear_eClausulas(e)
        self.__valorar_eClausulas()    
            

# Las transiciones vacias se representan con e
"""
eliminar = QuitarTranVacias(4)

eliminar.agregar_estado("q0", "a", ["q2"], "b", ["q1"], [])   

eliminar.agregar_estado("q1", "a", ["0"],  "b", ["q2"], [])

eliminar.agregar_estado("q2", "a", ["q3"], "b", ["0"], ["q3"])

eliminar.agregar_estado("q3", "a", ["q3"], "b", ["0"], ["q1"])
"""

eliminar = QuitarTranVacias(5)

eliminar.agregar_estado("q0", "a", ["q1","q2","q3"], "b", ["0"], [])   

eliminar.agregar_estado("q1", "a", ["0"],  "b", ["q4"], ["q4"])

eliminar.agregar_estado("q2", "a", ["q1"], "b", ["q4"], [])

eliminar.agregar_estado("q3", "a", ["q2","q3","q4"], "b", ["q3"], ["q2","q4"])

eliminar.agregar_estado("q4", "a", ["q1"], "b", ["q3"], [])


print(" - ORIGINAL - ")
eliminar.mostrarAutomataInicial()

eliminar.eliminarTransiciones()


print(" - SIN TRANSICIONES - ")
eliminar.mostrarAutomataFinal()