from sly import Lexer
from sly import Parser
from flask import Flask, make_response, jsonify
#Creación de clase Analizador Lexico.

class analizadorLexico(Lexer):
    tokens = { CARACTER, NUMERO_ENTERO, NUMERO_FLOTANTE, CADENA, SI, SINO,PARA,EN, LLAVE_IZQ, LLAVE_DER, IGUAL, MIENTRAS, MAYOR, MENOR, DIFERENTE }
    ignore = '\t '
    ignore_comentario = r'\##.*'
    ignore_nuevalinea = r'\n+'
    #Caracteres únicos que se devuelven tal cual.
    literals = { '=', '+', '-', '/', '*', '(', ')', ',', ';' }

    #Expresiones regulares para los Tokens.
    SINO = r'SINO'
    SI = r'SI'
    IGUAL = r'=='
    MAYOR = r'>>'
    MENOR = r'<<'
    DIFERENTE = r'!¡'
    LLAVE_IZQ = r'{{'
    LLAVE_DER = r'}}'
    PARA = r'PARA'
    MIENTRAS = r'MIENTRAS'
    EN = r'EN'
    CADENA = r'\".*?\"'
    CARACTER = r'[a-zA-Z_][a-zA-Z0-9_]*'
    #NUMERO_ENTERO = r'\d+'
    #NUMERO_FLOTANTE = r'\d+\.\d+'
    """
        Acciones con un método, y dar la expresión regular asociada con un @_()
    """

    @_(r'\d+.\d+')
    def NUMERO_FLOTANTE(self, token):
        token.value = float(token.value)
        return token

    @_(r'\d+')
    def NUMERO_ENTERO(self, token):
        token.value = int(token.value)
        return token
    
    @_(r'##.*')
    def COMENTARIO(self, token):
        pass
    
    @_(r'\n+')
    def LINEA_NUEVA(self, token):
        self.lineno += len(token.value)

    def error(self, token):
        print('Caracter invalido "%s"' % token.value[0])
        self.index += 1

#Creación de la clase Analizador Parser.
class analizadorParser(Parser):
    #Obtenemos la lista de Tokens del Analizador Léxico.
    tokens = analizadorLexico.tokens
    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS'),
        )

    @_('')
    def declaracion(self, parser):
        pass

    @_('expresion')
    def declaracion(self, parser):
        return (parser.expresion)

    @_('expresion "+" expresion')
    def expresion(self, parser):
        return ('suma', parser.expresion0, parser.expresion1)
    
    @_('expresion "-" expresion')
    def expresion(self, parser):
        return ('resta', parser.expresion0, parser.expresion1)
    
    @_('expresion "*" expresion')
    def expresion(self, parser):
        return ('multiplica', parser.expresion0, parser.expresion1)

    @_('expresion "/" expresion')
    def expresion(self, parser):
        return ('divide', parser.expresion0, parser.expresion1)

    @_('"-" expresion %prec UMINUS')
    def expresion(self, parser):
        return parser.expresion
    
    @_('asignacion')
    def declaracion(self, parser):
        return parser.asignacion
    
    @_('CARACTER "=" expresion')
    def asignacion(self, parser):
        return ('asignacion', parser.CARACTER, parser.expresion)
    
    @_('CARACTER "=" CADENA')
    def asignacion(self, parser):
        return ('asignacion', parser.CARACTER, parser.CADENA)
    
    @_('CARACTER')
    def expresion(self, parser):
        return ('variable', parser.CARACTER)

    @_('NUMERO_ENTERO')
    def expresion(self, parser):
        return ('numeroEntero', parser.NUMERO_ENTERO)
    
    @_('NUMERO_FLOTANTE')
    def expresion(self, parser):
        return ('numeroFlotante', parser.NUMERO_FLOTANTE)

    @_('expresion IGUAL expresion')
    def condicion(self, parser):
        return ('condicionIgual', parser.expresion0, parser.expresion1)
    
    @_('expresion MAYOR expresion')
    def condicion(self, parser):
        return ('condicionMayor', parser.expresion0, parser.expresion1)
    
    @_('expresion MENOR expresion')
    def condicion(self, parser):
        return ('condicionMenor', parser.expresion0, parser.expresion1)
    
    @_('expresion DIFERENTE expresion')
    def condicion(self, parser):
        return ('condicionDiferente', parser.expresion0, parser.expresion1)

    @_('SI condicion LLAVE_IZQ declaracion LLAVE_DER')
    def declaracion(self, parser):
        return ('si', parser.condicion, ('branch', parser.declaracion, parser.declaracion))
    
    @_('SI condicion LLAVE_IZQ declaracion LLAVE_DER SINO LLAVE_IZQ declaracion LLAVE_DER')
    def declaracion(self, parser):
        return ('sino', parser.condicion, ('branch', parser.declaracion0, parser.declaracion1))

    @_('PARA asignacion EN expresion LLAVE_IZQ declaracion LLAVE_DER')
    def declaracion(self, parser):
        return ('para', ('para-s', parser.asignacion, parser.expresion), parser.declaracion)

    @_('MIENTRAS condicion LLAVE_IZQ declaracion LLAVE_DER ')
    def declaracion(self, parser):
        return ('mientras', parser.condicion, ('branch', parser.declaracion, parser.declaracion))   
        
    
#Creacion de la clase ejecucion
class Ejecucion:
    def __init__(self, arbol, env):
            self.env = env
            resultado = self.r_arbol(arbol)
            if resultado is not None and isinstance(resultado, int):
                print(resultado)
            if resultado is not None and isinstance(resultado, float):
                print(resultado)
            if isinstance(resultado, str) and resultado[0] == '"':
                print(resultado)
    def r_arbol(self, node):
        if isinstance(node, int):
            return node
        if isinstance(node, float):
            return node
        if isinstance(node, str):
            return node
        if node is None:
            return None
        if node[0] == 'numeroEntero':
            return node[1]
        if node[0] == 'numeroFlotante':
            return node[1]
        if node[0] == 'str':
            return node[1]
        if node[0] == 'program':
            if node[1] == None:
                self.r_arbol(node[2])
            else:
                self.r_arbol(node[1])
                self.r_arbol(node[2])
       
        if node[0] == 'suma':
            return self.r_arbol(node[1]) + self.r_arbol(node[2])
        elif node[0] == 'resta':
            return self.r_arbol(node[1]) - self.r_arbol(node[2])
        elif node[0] == 'multiplica':
            return self.r_arbol(node[1]) * self.r_arbol(node[2])
        elif node[0] == 'divide':
            return self.r_arbol(node[1]) / self.r_arbol(node[2])
        
        if node[0] == 'asignacion':
            self.env[node[1]] = self.r_arbol(node[2])
            return node[1]
        
        if node[0] == 'si':
            resultado = self.r_arbol(node[1])
            if resultado:    
                self.r_arbol(node[2][1])
            return self.r_arbol(node[2][1])
        
        if node[0] == 'sino':
            resultado = self.r_arbol(node[1])
            if resultado:
                return self.r_arbol(node[2][1])
            return self.r_arbol(node[2][2])
            
        if node[0] == 'condicionIgual':
            return self.r_arbol(node[1]) == self.r_arbol(node[2])

        if node[0] == 'condicionMayor':
            return self.r_arbol(node[1]) > self.r_arbol(node[2])
        
        if node[0] == 'condicionMenor':
            return self.r_arbol(node[1]) < self.r_arbol(node[2])
        
        if node[0] == 'condicionDiferente':
            return self.r_arbol(node[1]) != self.r_arbol(node[2])

        if node[0] == 'variable':
            try:
                return self.env[node[1]]
            except LookupError:
                print("Variable indefinida '"+node[1]+"' encontrada")
                return 0
        if node[0] == 'para':
            if node[1][0] == 'para-s':
                loop_setup = self.r_arbol(node[1])
            
                loop_count = self.env[loop_setup[0]]
                loop_limit = loop_setup[1]
            
                for i in range(loop_count+1, loop_limit+1):
                    res = self.r_arbol(node[2])
                    if res is not None:
                        return res
                    self.env[loop_setup[0]] = i
                del self.env[loop_setup[0]]
        if node[0] == 'para-s':
            return (self.r_arbol(node[1]), self.r_arbol(node[2]))

        
        if node[0] == 'mientras':
            resultado = self.r_arbol(node[1])
            aux = resultado
            if resultado:
                while(aux == resultado):    
                    self.r_arbol(node[2][1])
                    resultado = self.r_arbol(node[1])
            return self.r_arbol(node[2][2])


if __name__ == "__main__":
    lexer = analizadorLexico()
    parser = analizadorParser()
    env = { }
    while True:
        try:
            texto = input('Ingrese expresión > ')
        except EOFError:
            break
        if texto:
            arbol = parser.parse(lexer.tokenize(texto))
            Ejecucion(arbol, env)