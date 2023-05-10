# Alumnos: Gallegos Zamora Ivan
#          Nieto Licona Victor Manuel

#Para TXT
import nltk
nltk.download('punkt')
import re

class Tokenizador:   
    def __init__(self,cadena):
        self.token  = nltk.word_tokenize(cadena)
    def getTokens(self):
        return self.token

class Automata:
    def __init__(self,cadena):
        validacion, tipo = self.validacion(cadena)
        if(validacion == None and tipo == None):
            print(f"Cadena inválida: {cadena}\n")
        else:
            print(f"Cadena: {validacion}\nTipo: {tipo}\n")
        
    def validacion(self,cadena):
        estado = 0
        # Recorriendo la cadena
        for i in range(len(cadena)): 
            tran = cadena[i]
            
            # Verificando en que estado se encuentra
            if(estado == 0):  # Estado inicial            
                # Verificando la transición
                if(tran == "i"):
                    estado = 1
                    if(i == len(cadena)-1):  # Verificando si es el final
                        return cadena,"Identificador"                    
                elif(re.search("[a-h]|[j-z]|[A-H]|[J-Z]",tran) != None):
                    estado = 3
                    if(i == len(cadena)-1):  # Verificando si es el final
                        return cadena,"Identificador"                   
                elif(re.search("\d",tran) != None): 
                    estado = 4
                    if(i == len(cadena)-1):  # Verificando si es el final
                        return cadena,"Entero"                   
                elif(re.search("[-+]",tran) != None): 
                    estado = 5
                    if(i == len(cadena)-1):  # Verificando si es el final
                        return None,None           
                else:
                    return None,None
                    
            elif(estado == 1):  # Estado 1               
                # Verificando la transición
                if(tran == "i"):
                    estado = 1
                    # Verificando si es el final
                    if(i == len(cadena)-1):
                        return cadena,"Identificador"                
                elif(tran == "f"):
                    estado = 2
                    if(len(cadena)==2 and i==len(cadena)-1): # Verificando si es IF
                        return cadena,"Palabra reservada"
                    elif(len(cadena)!=2 and i==len(cadena)-1):  # Verificando si es el final
                        return cadena, "Identificador"                    
                else:
                    return None,None
                
            elif(estado == 2):  # Estado 2                
                # Verificando la transición
                if(re.search("[a-z]|[A-Z]|_|\d", tran) != None):
                    estado = 3
                    if(i == len(cadena)-1):  # Verificando si es el final
                        return cadena,"Identificador"
                else:
                    return None,None
            
            elif(estado == 3):  # Estado 3                
                # Verificando la transición
                if(re.search("[a-z]|[A-Z]|_|\d", tran) != None):
                    estado = 3
                    if(i == len(cadena)-1):  # Verificando si es el final
                        return cadena,"Identificador"
                else:
                    return None,None
                
            elif(estado == 4):  # Estado 4                
                # Verificando la transición
                if(re.search("\d", tran) != None):
                    estado = 4
                    if(i == len(cadena)-1):  # Verificando si es el final
                        return cadena,"Entero"     
                else:
                    return None,None
                
            elif(estado == 5):  # Estado 5                
                # Verificando la transición
                if(re.search("\d", tran) != None):
                    estado = 4
                    if(i == len(cadena)-1):  # Verificando si es el final
                        return cadena,"Entero"
                else:
                    return None,None

            else:  # Inválida
                return None,None

class AutomataLexico:
    def __init__(self,texto):      
        if(texto.__contains__(".txt")):
            with open(f'{texto}', 'r') as file:
              textoA = file.read().replace('\n', '')
              tokens = Tokenizador(textoA).getTokens()
            for token in tokens:
              Automata(token)
        else:
            tokens = Tokenizador(texto).getTokens()
            for token in tokens:
              Automata(token)

            
AutomataLexico("texto.txt")
AutomataLexico("fdsr13")
AutomataLexico("fd_sr13")
AutomataLexico("iffff")
AutomataLexico("ie")
AutomataLexico("123")
AutomataLexico("-6456")
AutomataLexico("-6456vdfb")
AutomataLexico("if norman is a dog, tell me what is his max life 15 or 80")