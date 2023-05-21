# Importando los módulos para usar LEX y YACC
import ply.lex as lex
import ply.yacc as yacc
# Definición de tokens
tokens  = ('OPERACIONES','PARIZQ','PARDER','CORIZQ','CORDER','MAS','MENOS','POR',
            'DIVIDIDO','DECIMAL','ENTERO','PTCOMA','MEZCLA','ROJO','AMARILLO',
            'AZUL','CONVERSION','CONEXION','CELSIUS','FAHRENHEIT','KELVIN')

# Tokens
t_OPERACIONES  = r'Operacion'
t_PARIZQ = r'\('
t_PARDER = r'\)'
t_CORIZQ = r'\['
t_CORDER = r'\]'
t_MAS = r'\+'
t_MENOS = r'-'
t_POR = r'\*'
t_DIVIDIDO = r'/'
t_PTCOMA = r';'

t_MEZCLA = r'Mezcla'
t_CONVERSION = r'Conversion|Conversión'
t_CONEXION = r'[aA]'


# Caracteres ignorados
t_ignore = " \t|Â"

def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Floaat value too large %d", t.value)
        t.value = 0
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t
###
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
    print("Caracter ilegal '%s'" % t.value[0])
    t.lexer.skip(1)


# Construyendo el analizador léxico
lexer = lex.lex()

precedence = (('left','MAS','MENOS'),('left','POR','DIVIDIDO'),
                ('right','UMENOS'),)

# Definición de la gramática
def p_instrucciones_lista(t):
    '''instrucciones    : instruccion instrucciones
                        | instruccion '''

def p_instrucciones_tipo(t):
    '''instruccion : OPERACIONES CORIZQ expresion_num CORDER PTCOMA
                    | MEZCLA CORIZQ expresion_color CORDER PTCOMA
                    | CONVERSION CORIZQ expresion_conver CORDER PTCOMA'''
    print('El resultado es: ' + str(t[3]))

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
    'expresion_num : PARIZQ expresion_num PARDER'
    t[0] = t[2]

def p_expresion_number(t):
    '''expresion_num    : ENTERO
                    | DECIMAL'''
    t[0] = t[1]
    
###
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
    'expresion_conver : escala PARIZQ expresion_num PARDER CONEXION escala'
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

def p_error(t):
    print("Error sintáctico en '%s'" % t.value)


# Construyendo el analizador sintáctico
parser = yacc.yacc()

# Abriendo el archivo de texto
f = open("./entrada2.txt", "r")
input = f.read()
print(input)

# Usando YACC
parser.parse(input)