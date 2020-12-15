import ply.lex as lex

palabrasReservadas = {
    "imprimir": "IMPRIMIR",
    "leer": "LEER",
    "numerico": "NUMERICO",
    "falso": "ESTADO",
    "verdadero": "ESTADO",
    "cadena": "CADENA",
    "caracter": "CARACTER",
    "si": "SI",
    "no": "NO",
    "mientras": "MIENTRAS",
    "para": "PARA",
    "haz":"HAZ"
}
ERROR2 = ""
# lista de tokens

tokens =(

    # Palabras Reservadas
    'NUMERICO',
    'ESTADO',
    'CADENA',
    'CARACTER',
    'SI',
    'NO',
    'IMPRIMIR',
    'LEER',
    'PARA',
    'MIENTRAS',
    'HAZ',
    # Symbolos
    'MAS',  # +
    'MENOS',  # -
    'MULTIPLICAR',  # *
    'DIVIDIR',  # /
    'MENOR',  # <
    'MENORIGUAL',  # <=
    'MAYOR',  # >
    'MAYORIGUAL',  # >=
    'ASIGNAR',  # =
    'IGUALDAD',  # ==
    'DISTINTO',  # !=
    'PUNTOYCOMA',  # ;
    'DOSPUNTOS',  #:
    'LPAREN',  # (
    'RPAREN',  # )
    'LBLOCK',  # {
    'RBLOCK',  # }
    'COMILLA',  # "
    'COMILLASIMPLE',  # '
    'SALTODELINEA',

    # Otros
    'ID',
    'COMENTARIOS' #multilinea
   # 'COMENTARIO' #una linea
)

# Reglas de Expresiones Regualres para token de Contexto simple
t_CADENA = r'\"[\w*\t*\n*\ *]+\"'
t_CARACTER = r"\'[a-zA-Z_0-9]\'"
#t_NUMERICO = r'[0-9]+([.][0-9]+)?'

t_COMENTARIOS = r'\*\*[\w*\t*\n*\ *]+\*\*'
t_SALTODELINEA = r'\n'
t_MAS = r'\+'
t_MENOS = r'-'
t_MULTIPLICAR = r'\*'
t_DIVIDIR = r'/'
t_ASIGNAR = r'='
t_MENOR = r'<'
t_MAYOR = r'>'
t_MENORIGUAL = r'<='
t_MAYORIGUAL = r'>='
t_IGUALDAD = r'=='
t_PUNTOYCOMA = '\;'
t_DOSPUNTOS = r'\:'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBLOCK = r'{'
t_RBLOCK = r'}'
t_ESTADO = r'verdadero|falso'
t_PARA = r'PARA'
t_MIENTRAS = r'MIENTRAS'
t_HAZ = r'HAZ'
t_COMILLA = r'\"'
t_COMILLASIMPLE = r"\'"

def t_NUMERICO(t):
    r'[0-9]+([.][0-9]+)?'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if (t.value in palabrasReservadas):
        t.type = palabrasReservadas[t.value]
    return t

def t_SALTODELINEAe(t):
     r'\n+'
     t.lexer.lineno += len(t.value)

t_IMPRIMIR = r'imprimir'
t_LEER = r'leer'
t_SI = r'SI'
t_NO = r'NO'
# t_ignore = ' \t\n'  # Para ignorar los espacios
t_ignore = ' \t' 



caracterilegal=""
def t_error(t):
    # print(f'Caracter ilegal {t.value[0]!r}')
    global caracterilegal
    # caracterilegal+=f'Caracter ilegal {t.value[0]!r}'+"\n"
    # caracterilegal+='Caracter ilegal "'+str(t.value)+'"en la linea '+str(t.lineno)
    caracterilegal+="caracter ilegal en la linea {},token='{}' ".format(t.lineno,t.value[0])+"\n"
    print(caracterilegal)
    t.lexer.skip(1)

def get_caracter_ilegal():
    global caracterilegal
    if caracterilegal=="":
        return ""
    else:
        return caracterilegal
        
def clear_caracter_ilegal():
    global caracterilegal
    caracterilegal=""
   
