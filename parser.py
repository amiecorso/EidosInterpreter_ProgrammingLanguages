# The Fast Pelicans
# Parser
# TODO
# - finish postfix rule
# - set up parser for file processing
# - run unit tests
# - make syntax error more specific
# - if time: partial implemention of function syntax and Op sem rules?

import lexer_a5
import ply.yacc as yacc
import sys
import os
output = open("testresults", 'w')

tokens = lexer_a5.tokens # need token list from lexer!

precedence = (
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
        ('left', 'COLON')
)
# INTERPRETER BLOCK ============
def p_interpreter_block(p):
    '''
    interpreter_block : statement
                      | interpreter_block_cont
    '''
    p[0] = p[1]
    print(p[0])
    #output.write(str(p[0]))

def p_interpreter_block_cont(p):
    '''
    interpreter_block_cont : statement interpreter_block
    '''
    p[0] = (p[1], p[2])

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
    # missing compound_statement
    p[0] = p[1]

def p_expr_statement2(p):
    '''
    expr_statement : assignment_expr SEMICOLON
    '''
    p[0] = p[1]

def p_expr_statement(p):
    '''
    expr_statement : SEMICOLON
    '''
    p[0] = p[1]

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

def p_postfix_expr(p):
    '''
    postfix_expr : primary_expr
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

def p_postfix_expr_between_brack(p):
    '''
    postfix_expr_between : LBRACKET something RBRACKET postfix_expr_between
    '''
    p[0] = (p[1],p[2], p[3],p[4])

def p_something(p):
    '''
    something : expr_list_temp
              | empty
    '''
    p[0] = p[1]

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

def p_primary_expr(p):
    '''
    primary_expr : const
                 | IDENTIFIER
    '''
    p[0] = p[1]

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

def p_const(p):
    '''
    const : NUMBER_LITERAL
          | STRING_LITERAL
    '''
    p[0] = p[1]

def p_empty(p):
    '''
    empty :
    '''
    p[0] = p[0]

def p_error(p):
    print("Syntax error found")
    output.write("Syntax error found\n")
    output.write(str(p) + '\n')

parser = yacc.yacc()
if (len(sys.argv) > 1) and sys.argv[1] == "test":
    if len(sys.argv) > 2:
        path = argv[2]
    else:
        path = os.getcwd()+'/eidos-test/unit/no_error_expected/'

    for filename in os.listdir(path):
        output.write(filename + '\n\n')

        f = open(path+filename)
        s = f.read()
        output.write(s + '\n')
        parser.parse(s)
        output.write('\n===============================================\n')
        f.close()

else:
    while True: #while files in directory
        try:
            s = input('')
        except EOFError:
            break
        parser.parse(s)


output.close()
