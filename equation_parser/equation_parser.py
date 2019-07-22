import ply.lex as lex
import ply.yacc as yacc

# Variables arrays
diff_variables = []
aux_variables = []
parameters = []
internal_variables = []
label_upper = ""
label_lower = ""

output_file = None

tokens = (
    'NAME','NUMBER',
    'PLUS','MINUS','TIMES','DIVIDE','EQUALS',
    'EXP','POWER',
    'SIN', 'COS', 'TAN', 'ARCSIN', 'ARCCOS', 'ARCTAN',
    'HSIN', 'HCOS', 'HTAN', 'HARCSIN', 'HARCCOS', 'HARCTAN',
    'LPAREN','RPAREN',
    'DIFFERENTIAL'
    )

# Tokens

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'

t_EXP = r'exp'
t_POWER = r'\^'
t_DIFFERENTIAL = r'd/dt'

t_EQUALS  = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_NAME    = r'\b(?!exp\b)[a-zA-Z0-9_]{1,10}' #añadir las trigonometricas

def t_NUMBER(t):
    r'\d+([.,\']\d+)?'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

# Ignored characters
t_ignore = " \t\r"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer
lexer = lex.lex()

# Parsing rules

precedence = (
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    ('left','POWER'),
    ('right','UMINUS'),
    )

# dictionary of names
names = { }

def p_statement(t):
    'statement : init equation'

def p_init(t):
    'init :'

def p_equation(t):
    '''equation : differential 
                | simple'''

def p_differential(t):
    'differential : DIFFERENTIAL NAME EQUALS expression'

    output_file.write("double "+label_lower+t[2]+" (double * vars, double * params) {\n")

    for var in internal_variables:
        output_file.write("\tdouble "+var+" = "+label_lower+var+"(vars, params);\n")

    output_file.write("\treturn %s;\n}\n\n"%(t[4]))

def p_simple(t):
    'simple : NAME EQUALS expression'

    output_file.write("double "+label_lower+t[1]+" (double * vars, double * params) {\n")

    for var in internal_variables:
        output_file.write("\tdouble "+var+" = "+label_lower+var+"(vars, params);\n")

    output_file.write("\treturn %s;\n}\n\n"%(t[3]))

def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    if t[2] == '+'  : 
        #t[0] = t[1] + t[3]
        t[0] = ""+t[1]+" + "+t[3]+""
    elif t[2] == '-': 
        #t[0] = t[1] - t[3]
        t[0] = ""+t[1]+" - "+t[3]+""
    elif t[2] == '*': 
        #t[0] = t[1] * t[3]
        t[0] = ""+t[1]+" * "+t[3]+""
    elif t[2] == '/': 
        #t[0] = t[1] / t[3]
        t[0] = ""+t[1]+" / "+t[3]+""

def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'
    #t[0] = -t[2]
    t[0] = "-"+t[2]+""

def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    #t[0] = t[2]
    t[0] = "("+t[2]+")"

def p_expression_number(t):
    'expression : NUMBER'
    #t[0] = t[1]
    t[0] = "%f"%(t[1])

def p_expression_power_int(t):
    'expression : expression POWER NUMBER'

    exponent = int(t[3])

    if t[3] - exponent == 0.0: #it is an int
        string = ""+t[1]+""

        for i in range(exponent-1):
            string = string + "*"+t[1]+""
    else: #it is a float
        string = "pow("+t[1]+", %f)"%(t[3])

    t[0] = string

def p_expression_power_name(t):
    'expression : expression POWER NAME'
    t[0] = "pow("+t[1]+", "+t[3]+")"

def p_expression_power_expr(t):
    'expression : expression POWER LPAREN expression RPAREN'
    t[0] = "pow("+t[1]+", "+t[4]+")"

def p_expression_exp(t):
    'expression : EXP LPAREN expression RPAREN'
    t[0] = "exp("+t[3]+")"

def p_expression_name(t):
    'expression : NAME'

    if t[1] in diff_variables:
        t[0] = "vars["+label_upper+t[1].upper()+"]"
    elif t[1] in aux_variables:
        internal_variables.append(t[1])
        t[0] = t[1]
    else:
        t[0] = "params["+label_upper+t[1].upper()+"]"

        if t[1] not in parameters:
            parameters.append(t[1])


def p_error(t):
    print("Syntax error at '%s'" % t.value)


def parse(diff_vars, aux_vars, params, model_name, s, fileptr):
    global diff_variables
    global aux_variables
    global parameters
    global label_upper
    global label_lower
    global internal_variables
    global output_file

    output_file = fileptr

    diff_variables = diff_vars
    aux_variables = aux_vars
    parameters = params
    label_upper = "NM_"+model_name.upper()+"_"
    label_lower = "nm_"+model_name.lower()+"_"
    internal_variables = []

    parser = yacc.yacc()
    parser.parse(s)

    return parameters


    
