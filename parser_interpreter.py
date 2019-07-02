# The Fast Pelicans
# Parser and Interpreter
# TODO:
# global scope symbol table - if x is global and x = something inside a function - global x
# local scope symbol table - only if a new variable is declared within a function
# can use the env table or a separate symbol table to store variable names and types
# I think we can stick part of our ast for the type fo the function (return type, etc)
# do this at the parsing stage
# run into a func call and look up the func decl, now create a local env with the passed params
# if there is a local value in the function that needs to be returned we need to preserve that from the function decl
# with type checking - do a separate pass over the ast to add the types in to the symbol table
# then when we actually run the evaluation we do the type checking and return errors

# For Tuesday
# Do our actual algorithm
    # also timing and comparison
# Create presentation

import lexer_a5
import ply.yacc as yacc
import sys
import os
import numpy as np


output = False # opens only if command line has specified "test" flag
tokens = lexer_a5.tokens # need token list from lexer!
ERRCOUNT = 0
precedence = (
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
        ('left', 'COLON')
)
# INTERPRETER BLOCK ============
def p_interpreter_block(p):
    '''
    interpreter_block : statement
                      | function_decl
                      | interpreter_block_cont
    '''
    p[0] = p[1]
#    print(p[0])

def p_interpreter_block_cont(p):
    '''
    interpreter_block_cont : statement interpreter_block
                           | function_decl interpreter_block
    '''
    p[0] = (p[1], p[2])
# FUNCTIONS ===================
def p_function_decl(p):
    '''
    function_decl : FUNCTION return_type_spec IDENTIFIER param_list compound_statement
    '''
    p[0] = (p[1], p[2], p[3], p[4], p[5])

def p_return_type_spec(p):
    '''
    return_type_spec : LPAREN type_spec RPAREN
    '''
    p[0] = p[2]

def p_type_spec(p):
    '''
    type_spec : VOID
              | NULL
              | LOGICAL
              | INTEGER
              | FLOAT
              | STRING
              | NUMERIC
              | PLUS
              | TIMES
    '''
    p[0] = p[1]

def p_param_list(p):
    '''
    param_list : LPAREN VOID RPAREN
                | LPAREN param_spec RPAREN
                | LPAREN param_spec_list RPAREN
    '''
    p[0] = p[2]

def p_param_spec_list(p):
    '''
    param_spec_list : param_spec
    '''
    p[0] = p[1]

def p_param_spec_list2(p):
    '''
    param_spec_list : param_spec COMMA param_spec_list
    '''
    p[0] = (p[1], p[3])

def p_param_spec(p):
    '''
    param_spec : LBRACKET type_spec IDENTIFIER EQUAL const RBRACKET
              | LBRACKET type_spec IDENTIFIER EQUAL IDENTIFIER RBRACKET
    '''
    p[0] = (p[2], (p[4], p[3], p[5]))

def p_param_spec2(p):
    '''
    param_spec : type_spec IDENTIFIER
    '''
    p[0] = (p[1], p[2])

"""
def p_c_function(p):
    '''
    c_function : CFUNK LPAREN NUMBER_LITERAL RPAREN
               | CFUNK LPAREN num_list RPAREN
    '''
    p[0] = ('const', np.array(list(p[3])))


def p_num_list_temp(p):
    '''
    num_list_temp : NUMBER_LITERAL
                  | num_list
    '''
    p[0] = p[1]

def p_num_list(p):
    '''
    num_list : NUMBER_LITERAL COMMA num_list_temp
    '''
    p[0] = (p[1], p[3])
"""

# STATEMENTS ===================

def p_compound_statement(p):
    '''
    compound_statement : LCURLBRACE statement_list RCURLBRACE
    '''
    p[0] = p[2]

def p_statement_list(p):
    '''
    statement_list : statement
    '''
    p[0] = p[1]

def p_statement_list2(p):
    '''
    statement_list : statement statement_list
    '''
    p[0] = (p[1], p[2])

def p_statement(p):
    '''
    statement : compound_statement
              | expr_statement
              | selection
              | for
              | do_while
              | while
              | jump
    '''
    p[0] = p[1]

def p_expr_statement2(p):
    '''
    expr_statement : assignment_expr SEMICOLON
    '''
    p[0] = p[1]
"""
def p_expr_statement(p):
    '''
    expr_statement : SEMICOLON
    '''
    p[0] = p[1]
"""
def p_selection_else(p):
    '''
    selection : IF LPAREN expr RPAREN statement ELSE statement
    '''
    p[0] = (p[1], p[3], p[5], p[7])

def p_selection(p):
    '''
    selection : IF LPAREN expr RPAREN statement
    '''
    p[0] = (p[1], p[3], p[5])

def p_for(p):
    '''
    for : FOR LPAREN IDENTIFIER IN expr RPAREN statement
    '''
    p[0] = (p[1], p[3], p[4], p[5], p[7])

def p_do_while(p):
    '''
    do_while : DO statement WHILE LPAREN expr RPAREN SEMICOLON
    '''
    p[0] = (p[1], p[2], p[3], p[5])

def p_while(p):
    '''
    while : WHILE LPAREN expr RPAREN statement
    '''
    p[0] = (p[1], p[3], p[5])

def p_jump_jump(p):
    '''
    jump : RETURN expr SEMICOLON
    '''
    p[0] = (p[1], p[2])

def p_jump(p):
    '''
    jump : NEXT SEMICOLON
         | BREAK SEMICOLON
         | RETURN SEMICOLON
    '''
    p[0] = p[1]

# EXPRESSIONS ====================
def p_expr(p):
    '''
    expr : conditional_expr
    '''
    p[0] = p[1]


def p_assignment_expr_op(p):
    '''
    assignment_expr : conditional_expr EQUAL conditional_expr
    '''
    p[0] = (p[2], p[1], p[3])

def p_assignment_expr(p):
    '''
    assignment_expr : conditional_expr
    '''
    p[0] = p[1]

def p_conditional_expr_op(p):
    '''
    conditional_expr : logical_or_expr QUESTION conditional_expr ELSE conditional_expr
    '''
    p[0] = (p[2], p[1], p[3], p[4], p[5])

def p_conditional_expr(p):
    '''
    conditional_expr : logical_or_expr
    '''
    p[0] = p[1]

def p_logical_or_expr_op(p):
    '''
    logical_or_expr : logical_and_expr PIPE logical_or_expr
    '''
    p[0] = (p[2], p[1], p[3])

def p_logical_or_expr(p):
    '''
    logical_or_expr : logical_and_expr
    '''
    p[0] = p[1]

def p_logical_and_expr_op(p):
    '''
    logical_and_expr : equality_expr AMPER logical_and_expr
    '''
    p[0] = (p[2], p[1], p[3])

def p_logical_and_expr(p):
    '''
    logical_and_expr : equality_expr
    '''
    p[0] = p[1]

def p_equality_expr_op(p):
    '''
    equality_expr : relational_expr NOTEQUAL equality_expr
                  | relational_expr ISEQUAL equality_expr
    '''
    p[0] = (p[2],  p[1], p[3])

def p_equality_expr(p):
    '''
    equality_expr : relational_expr
    '''
    p[0] = p[1]

def p_relational_expr_op(p):
    '''
    relational_expr : add_expr LESSTHAN relational_expr
                    | add_expr LESSEQUAL relational_expr
                    | add_expr GREATERTHAN relational_expr
                    | add_expr GREATEQUAL relational_expr
    '''
    p[0] = (p[2], p[1], p[3])

def p_relational_expr(p):
    '''
    relational_expr : add_expr
    '''
    p[0] = p[1]

def p_add_expr_op(p):
    '''
    add_expr : mult_expr PLUS add_expr
             | mult_expr MINUS add_expr
    '''
    p[0] = (p[2], p[1], p[3])


def p_add_expr(p):
    '''
    add_expr : mult_expr
    '''
    p[0] = p[1]

def p_mult_expr_op(p):
    '''
    mult_expr : seq_expr TIMES mult_expr
              | seq_expr DIVIDE mult_expr
              | seq_expr MODULO mult_expr
    '''
    p[0] = (p[2], p[1], p[3])

def p_mult_expr(p):
    '''
    mult_expr : seq_expr
    '''
    p[0] = p[1]


def p_seq_expr_multi(p):
    '''
    seq_expr : exp_expr COLON exp_expr
    '''
    p[0] = (p[2], p[1], p[3])

def p_seq_expr(p):
    '''
    seq_expr : exp_expr
    '''
    p[0] = p[1]

def p_exp_expr_exp(p):
    '''
    exp_expr : unary_expr CARAT exp_expr
    '''
    p[0] = (p[2], p[1], p[3])

def p_exp_expr(p):
    '''
    exp_expr : unary_expr
    '''
    p[0] = p[1]


def p_unary_expr_sym(p):
    '''
    unary_expr : BANG unary_expr
               | PLUS unary_expr
               | MINUS unary_expr
    '''
    p[0] = (p[1], p[2])

def p_unary_expr(p):
    '''
    unary_expr : postfix_expr
    '''
    p[0] = p[1]

def p_function_call(p):
    '''
    function_call : IDENTIFIER LPAREN argument_expr_list RPAREN
                 |  IDENTIFIER  LPAREN RPAREN
    '''
    if len(p) == 5:
        p[0] = ('fun_call', p[1],p[3])
    else:
        p[0] = ('fun_call', p[1])

def p_postfix_expr(p):
    '''
    postfix_expr : primary_expr
                | function_call
                | postfix_expr_index
    '''
    p[0] = p[1]

def p_postfix_expr_more(p):
    '''
    postfix_expr : primary_expr postfix_expr_between
    '''
    p[0] = (p[1],p[2])

def p_postfix_expr_nomore(p):
    '''
    postfix_expr_between : empty
    '''
    p[0] = p[1]


# deleted "postfixe_expr_between" from end
def p_postfix_expr_index(p):
    '''
    postfix_expr_index : IDENTIFIER LBRACKET something RBRACKET
    '''
    p[0] = ('index', p[1],p[3])


def p_something(p):
    '''
    something : expr_list_temp
              | empty
    '''
    p[0] = p[1]

def p_postfix_c(p):
    '''
    postfix_expr : CFUNK LPAREN argument_expr_list RPAREN
    '''
    p[0] = (p[1], p[3])

def p_postfix_floor(p):
    '''
    postfix_expr : FLOOR LPAREN argument_expr_list RPAREN
    '''
    p[0] = (p[1], p[3])

def p_postfix_print(p):
    '''
    postfix_expr : PRINT LPAREN argument_expr_list RPAREN
    '''
    p[0] = (p[1], p[3])

def p_postfix_length(p):
    '''
    postfix_expr : LENGTH LPAREN argument_expr_list RPAREN
    '''
    p[0] = (p[1], p[3])

def p_postfix_size(p):
    '''
    postfix_expr : SIZE LPAREN argument_expr_list RPAREN
    '''
    p[0] = (p[1], p[3])

def p_expr_list_temp(p):
    '''
    expr_list_temp : expr
                   | expr_list
    '''
    p[0] = p[1]

def p_expr_list(p):
    '''
    expr_list : expr COMMA expr_list_temp
    '''
    p[0] = (p[1], p[3])

def p_postfix_between_arglist(p):
    '''
    postfix_expr_between : LPAREN argument_expr_list RPAREN postfix_expr_between
    '''
    p[0] = (p[1],p[2],p[3], p[4])

def p_postfix_between_arglist_empty(p):
    '''
    postfix_expr_between : LPAREN RPAREN postfix_expr_between
    '''
    p[0] = (p[1],p[2],p[3])

def p_postfix__between_attr(p):
    '''
    postfix_expr_between : DOT IDENTIFIER postfix_expr_between
    '''
    p[0] = (p[2], p[1], p[3])

def p_primary_expr_parens(p):
    '''
    primary_expr : LPAREN expr RPAREN
    '''
    p[0] = p[2]

def p_primary_expr_const(p):
    '''
    primary_expr : const
    '''
    p[0] = p[1]

def p_primary_expr_ID(p):
    '''
    primary_expr : IDENTIFIER
    '''
    p[0] = ("var", p[1])


def p_argument_expr_list2(p):
    '''
    argument_expr_list : argument_expr COMMA argument_expr_list
    '''
    p[0] = (p[1], p[3])

def p_argument_expr_list(p):
    '''
    argument_expr_list : argument_expr
    '''
    p[0] = p[1]

def p_argument_expr(p):
    '''
    argument_expr : IDENTIFIER EQUAL conditional_expr
    '''
    p[0] = (p[2], p[1], p[3])

def p_argument_expr2(p):
    '''
    argument_expr : conditional_expr
    '''
    p[0] = p[1]

def p_const_bool(p):
    '''
    const : BOOL_LITERAL
    '''
    if p[1] == "T":
        p[0] = ('const', np.array([True]))
    else:
        p[0] = ('const', np.array([False]))

def p_const(p):
    '''
    const : NUMBER_LITERAL
          | STRING_LITERAL
    '''
    p[0] = ('const', np.array([p[1]]))

def p_empty(p):
    '''
    empty :
    '''
    p[0] = p[0]

def p_error(p):
    print("Syntax error found. p: ", p)
    global ERRCOUNT
    ERRCOUNT += 1
    if output:
        output.write("Syntax error found\n")
        output.write(str(p) + '\n')

parser = yacc.yacc()
types = {'integer': 'int64', 'float' : 'float64', 'string': '<U2', 'logical' : 'bool'}
nptypes = {'int64':'integer', 'float64' : 'float', '<U2' : 'string', 'bool': 'logical'}
env = {}
symbol ={}

def run(p, context):
    ans = 0
    while len(p) > 1:
        if type(p[0]) == tuple:
            for statement in p:
                run_run(statement, context)
            p = p[1]
        else:
            ans = run_run(p, context)
            return ans

def run_run(p, context):
    global env
    global symbol
    if type(p) == tuple:
        if p[0] == "var":
            if p[1] in context:
                return context[p[1]]
            else:
                print("Unbound variable ", p[1])
                return p
        if p[0] == "const":
            return p[1]
        elif p[0] == '+':
            if binop_typecheck(run(p[1], context), run(p[2], context), "+"):
                return np.add(run(p[1], context),run(p[2], context))
        elif p[0] == '-':
            if binop_typecheck(run(p[1], context), run(p[2], context), "-"):
                return np.subtract(run(p[1], context), run(p[2], context))
        elif p[0] == "*":
            if binop_typecheck(run(p[1], context), run(p[2], context), "*"):
                return np.multiply(run(p[1], context),run(p[2], context))
        elif p[0] == "/":
            if binop_typecheck(run(p[1], context), run(p[2], context), "/"):
                return np.divide(run(p[1], context),run(p[2], context))
        elif p[0] == "=":
            context[p[1][1]] = run(p[2], context)
            #print(env)
        elif p[0] == "==":
            return np.array_equal(run(p[1], context),run(p[2], context))
        elif p[0] == "!=":
            return np.not_equal(run(p[1], context), run(p[2], context))
        elif p[0] == "<":
            if binop_typecheck(run(p[1], context), run(p[2], context), "<"):
                return np.less(run(p[1], context),run(p[2], context))
        elif p[0] == "<=":
            if binop_typecheck(run(p[1], context), run(p[2], context), "<="):
                return np.less_equal(run(p[1], context), run(p[2], context))
        elif p[0] == ">":
            if binop_typecheck(run(p[1], context), run(p[2], context), ">"):
                return np.greater(run(p[1], context), run(p[2], context))
        elif p[0] == ">=":
            if binop_typecheck(run(p[1], context), run(p[2], context), ">="):
                return np.great_equal(run(p[1], context), run(p[2], context))
        elif p[0] == "&":
            if binop_typecheck(run(p[1], context), run(p[2], context), "&"):
                return np.logical_and(run(p[1], context), run(p[2], context))
        elif p[0] == "|":
            if binop_typecheck(run(p[1], context), run(p[2], context), "|"):
                return np.logical_or(run(p[1], context), run(p[2], context))
        elif p[0] == "^":# need float_power and power?
            if binop_typecheck(run(p[1], context), run(p[2], context), "^"):
                return np.power(run(p[1], context), run(p[2], context))
        elif p[0] == "%":
            if binop_typecheck(run(p[1], context), run(p[2], context), "%"):
                return np.mod(run(p[1], context), run(p[2], context))
        elif p[0] == "c":
            lst = p[1]
            vector = []
            while len(lst) > 1:
                if type(lst[0]) == tuple:
                    print('lst[0][1]', lst[0][1])
                    vector.append(lst[0][1])
                    lst = lst[1]
                else:
                    vector.append(lst[1])
                    break
            print("vector = ", vector)
            return list(np.array(vector).flatten())
        elif p[0] == "print":
            print(run(p[1], context))
        elif p[0] == "floor":
            return np.floor(run(p[1], context)).astype(int)
        elif p[0] == "length": # not working yet
            return len(run(p[1], context))
        elif p[0] == "size": # not working yet
            
            return np.array([len(run(p[1], context))])
        elif p[0] == "?":
            if run(p[1], context):
                return run(p[2], context)
            else:
                return run(p[4], context)
        elif p[0] == ":":
            return list(range(int(run(p[1], context)), int(run(p[2], context))))
        elif p[0] == "!":
            return not run(p[1], context)
        elif p[0] == "while":
            while run(p[1], context):
                if run(p[2], context) == "break":
                    break
        elif p[0] == "if":
            if len(p) == 3:
                if run(p[1], context):
                   return run(p[2], context)
            else:
                if run(p[1], context):
                    return run(p[2], context)
                else:
                    return run(p[3], context)
        elif p[0] == "for":
            lst = run(p[3], context)
            for i in range(len(lst)):
                env[p[1]] = lst[i]
                if run(p[4], context) == "break":
                    break
        elif p[0] == "do":
            run(p[1], context)
            while run(p[3], context):
                if run(p[1], context) == "break":
                    break
        elif p[0] == "next":
            pass
        elif p[0] == "break":
            return "break";
        elif p[0] == "return":
            if len(p) == 2:
                return run(p[1], context)
        elif p[0] == "index":
            print("context = ", context)
            theseq = context[p[1]]
            print("theseq = ", theseq)
            index = run(p[2], context)
            newthing = []
            for element in index:
                newthing.append(theseq[int(element)])
            print("INDEX = ", index)
            print("type of = ", type(index))
            return newthing
            #KALEY can we do list access here?
            
        elif p[0] == "function":
            #env[p[2]] = p[3]
            symbol[p[2]] = p

        elif p[0] == "fun_call":
            #print('fun call parse')
            if p[1] not in symbol:
                print("Unknown symbol ", p[1])
            else:
                fun_ast = symbol[p[1]]
                #print('made it!', fun_ast)
                params = fun_ast[3]
                #print(params)
                return_t = fun_ast[1]
                body = fun_ast[4]
                local_env = {}
                #print(p, '<-- this is p')

                args = p[2]
                print("args is first", args)
                arglist = []
                while len(args) > 1:
                    if type(args[0]) == tuple:
                        arglist.append(args[0])
                    else:
                        arglist.append(args)
                        break
                    args = args[1]
                #print("ARGLIST: ", arglist)

                arg_vals = []
                for arg in arglist:
                    arg_vals.append(run(arg, context))
                print("===arg_vals=== ", arg_vals)
                print("params is second", params)
                paramlist = []
                while len(params) > 1:
                    if type(params[0]) == tuple:
                        paramlist.append(params[0])
                    else:
                        paramlist.append(params)
                    params = params[1]
                #print("PARMLIST: ", paramlist)
                #check length of arglist and param list match
                print('arglist: ', arglist)                
                for i in range(len(arg_vals)):
                    #print('arglist[i][1]: ', arglist[i][1])
                    tempArg = arg_vals[i]
                    if type(tempArg) == list:
                        t1 = str(tempArg[0].dtype)
                        print("t1 arr: ", t1)
                    else:
                        t1 = str(tempArg.dtype)
                        print("t1 alone: ", t1)
                    t2 =  paramlist[i][0]

                    print("t2: ", t2)
                    if t1 == types[t2]:
                        local_env[paramlist[i][1]] = arg_vals[i]
                    else:
                        print("TypeError: Expected type", t2, "recieved type", t1)
                        break
                return run(body, local_env)
                #print(run(body, local_env))

    else:
        return p

"""def binop_typecheck(left, right, op):

    nptypes = {'int64':'integer', 'float64' : 'float', '<U2' : 'string', 'bool': 'logical'}
    #pytypes = {int : "integer", float: "float", bool : "logical", str :"string"}
    l = nptypes[str(left.dtype)]
    tr = nptypes[str(right.dtype)]
    if tl != tr:
        print("TypeError: Unsupported operand types for ", op, ": ", tl, ", ",  tr, ".", sep = "")
        return False
    else:
        return True
"""
def binop_typecheck(left, right, op):
    try:
        print("in binop, left = ", left)
        print("in binop, right = ", right)
        for i in range(len(left)):
            tl = type(left[i]);
            print('left type: ',tl)
            for j in range(len(right)):
                tr = type(right[j]);
                if tl != tr:
                    print("TypeError: Unsupported operand types for ", op, ": ", tl, ", ",  tr, ".", sep = "")
                    return False
    except TypeError:
        if type(left) != type(right):
            print("TypeError: Unsupported operand types for ", op, ": ", type(left), ", ",  type(right), ".", sep = "")
    return True

if (len(sys.argv) > 1) and sys.argv[1] == "test":
    output = open("testresults", 'w')
    if len(sys.argv) > 2:
        path = sys.argv[2]
    else:
        path = os.getcwd()+'/eidos-test/unit/no_error_expected/'

    for filename in os.listdir(path):
        output.write(filename + '\n\n')

        f = open(path+filename)
        s = f.read()
        output.write(s + '\n')
        ast = parser.parse(s)
        output.write(str(run(ast)))
        output.write('\n')
        output.write('\n===============================================\n')
        f.close()

    print(ERRCOUNT)
    output.write(str(ERRCOUNT))
    output.close()

elif (len(sys.argv) == 3) and sys.argv[1] == "run":
    progfile = open(sys.argv[2], 'r')
    prog = progfile.read()
    ast = parser.parse(prog)
    print(ast)
    print(run(ast, env))


else:
    while True:
        try:
            s = input('>> ')
        except EOFError:
            break
        ast = parser.parse(s)
        print(ast)
        print(run(ast, env))
        """
        if type(ast[0]) == tuple:
            for statement in ast:
                print(run(statement, env))
        else:
            print(run(ast, env))
        """
