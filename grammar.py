from tokens import*
from ply.yacc import yacc


gramaticaerror=""
imprimircad=""
def cargar_codigo(a):
    
    lexer = lex.lex()

    lexer.input(a)
    # print(a)

    _var_names = {}

    def p_statements_multiple(p):
        # declaraciones declaración
        # declaraciones sentencia
        # sentecia
        '''
        statements : statements statement
                | statements sentencia
                | sentencia
        '''
        
    def p_statements_single(p):
        # declaraciones declaración
        '''
        statements : statement
        '''
        p[0] = p[1]

    def p_asignamiento_statements(p):
        # declaración asignación
        '''
        statement : asignacion
        '''
        p[0] = p[1]

    def p_comentario_statements(p):
        # declaración comentarios
        '''
        statement : COMENTARIOS
        '''

    def p_asignar(p):
        #identificador signo(=) expresión ;
        '''
            asignacion : ID ASIGNAR expr PUNTOYCOMA
        '''
        _var_names[p[1]] = p[3]
        #print("p_asignar: {}".format(_var_names[p[1]]))

    def p_tipodato(p):
        '''
        tipodato : NUMERICO
                | CARACTER
                | ESTADO
                | CADENA
        '''
        p[0] = p[1]

    def p_leer_statement(p):
        # leer : expresión
        '''
        statement : LEER DOSPUNTOS expr
        '''
        p[0] = p[3]

    def p_imprimir_statement(p):
        # imprimir : expresión
        '''
        statement : IMPRIMIR DOSPUNTOS expr PUNTOYCOMA
        '''
        global imprimircad
        if p[3] in _var_names:
           imprimircad=_var_names[p[3]]
        else:
           imprimircad=p[3]

    def p_expr_name(p):
        '''
        expr : ID
        '''
        p[0] = p[1]

    def p_expr_numerico(p):
        '''
        expr : NUMERICO
        '''
        p[0] = p[1]

    def p_expr_cadena(p):
        '''
        expr : CADENA
        '''
        p[0] = p[1]

    def p_expr_caracter(p):
        '''
        expr : CARACTER
        '''
        p[0] = p[1]

    def p_expr_estado(p):
        '''
        expr : ESTADO
        '''
        p[0] = p[1]

    def p_expr_opbin(p):
        '''
        expr : expr MAS expr
            | expr MULTIPLICAR expr
            | expr DIVIDIR expr
            | expr MENOS expr
        '''
        try:
            if p[2] == '+' : p[0] = p[1] + p[3]
            elif p[2] == '*' : p[0] = p[1] * p[3]
            elif p[2] == '/' : p[0] = p[1] / p[3]
            elif p[2] == '-' : p[0] = p[1] - p[3]
        except:
            pass

    def p_expr_group(p):
        '''
        expr : LPAREN expr RPAREN
        '''
        p[0] = p[2]


    def p_condiciones(p):
        '''
        condiciones : MENOR
                    | MENORIGUAL
                    | MAYOR
                    | MAYORIGUAL
                    | ASIGNAR
                    | IGUALDAD
                    | DISTINTO
        '''
        try:
            if p[1] == '<': p[0] = '<'
            elif p[1] == '<=': p[0] = '<='
            elif p[1] == '>': p[0] = '>'
            elif p[1] == '>=': p[0] = '>='
            elif p[1] == '=': p[0] = '='
            elif p[1] == '==': p[0] = '=='
            elif p[1] == '!=': p[0] = '!='
        except:
            pass

    def p_condicion(p):
        '''condicion : expr condiciones expr'''
        try:
            if p[2] == '<': p[0] = (p[1]) < (p[3])
            elif p[2] == '<=': p[0] = (p[1]) <= (p[3])
            elif p[2] == '>': p[0] = (p[1]) > (p[3])
            elif p[2] == '>=': p[0] = (p[1]) >= (p[3])
            elif p[2] == '=': p[0] = (p[3])
            elif p[2] == '==': p[0] = (p[1]) is (p[3])
            elif p[2] == '!=': p[0] = (p[1]) != (p[3])
        except:
            pass

    def p_sentencia_si(p):
        # si ( condicción ) { lista_sentencia }
        # si ( condición ) { lista_sentencia } no { lista_sentencia }
        """sentencia_si : SI LPAREN condicion RPAREN LBLOCK lista_sentencia RBLOCK
                        | SI LPAREN condicion RPAREN LBLOCK lista_sentencia RBLOCK NO  LBLOCK lista_sentencia RBLOCK
        """
        # print("p[1]={} p[2]={} p[3]={} p[4]={} p[5]={} p[6]={} p[7]={} p[8]={} p[9]={} p[10]={} p[11]={}".format(p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8],p[9],p[10],p[11]))
        # print(p)
        #try:
        #   if p[3] == True:
               #print("p[6]{}".format(p[6]))
        #       p[0] = p[6]
        #   else:
               #print("p[10]{}".format(p[10]))
        #       p[0] = p[10]
        #except:
        #   pass

    def p_sentencia_mientras(p):
        #mientras(condición){lista_sentencia}
        #haz{lista_sentencia}mientras(condición);
        """
            sentencia_mientras : MIENTRAS LPAREN condicion RPAREN LBLOCK lista_sentencia RBLOCK
                            | HAZ LBLOCK lista_sentencia  RBLOCK MIENTRAS LPAREN condicion RPAREN PUNTOYCOMA
        """

    def p_sentencia_para(p):
        # para(asignación condición; aignación){lista_sentencia}
        "sentencia_para : PARA LPAREN asignacion condicion PUNTOYCOMA asignacion RPAREN LBLOCK lista_sentencia RBLOCK"


    def p_sentencia(p):
        """sentencia :   sentencia_si
                        | sentencia_mientras
                        | sentencia_para
                        | statement
        """
        p[0] = p[1]

    def p_lista_sentencia(p):
        """lista_sentencia : lista_sentencia sentencia
                        | sentencia
        """
        #print("p[0]={} p[1]={}".format(p[0], p[1]))
        #p[0] = p[1]

    def p_error(p):
        global gramaticaerror
        global caracterilegal
        if p:
           gramaticaerror="error sintactico en la linea {},token='{}' ".format(p.lineno,p.value)
           print("error sintactico en la linea {},token='{}' ".format(len(p.value),p.value))
        elif caracterilegal=="":
            gramaticaerror="verifique si falta un ';' "
            print("verifique si falta un ';' ")
               
    parser = yacc()
    parser.parse(a)

   
# cargar_codigo()
def get_gramaticaerror():
    global gramaticaerror
    return gramaticaerror  

def clear_gramaticaerror():
    global gramaticaerror
    gramaticaerror=""

def imprimircadena():
    global imprimircad
    return imprimircad

def clear_imprimircadena():
    global imprimircad
    imprimircad=""
