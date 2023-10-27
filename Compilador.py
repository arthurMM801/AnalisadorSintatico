class Token:
    def __init__(self, token_type, value):
        self.token_type = token_type
        self.value = value

# Lexical Analyzer
def lexer(program):
    keywords = ["LET", "GO", "TO", "OF", "READ", "PRINT", "IF", "THEN", "ELSE", "LABEL"]
    operators = ["+", "-", "*", "/", "<", ">", "="]
    separators = [",", ";", "(", ")", ":=", ":"]  # Added ":=" as a separator

    tokens = []
    current_token = ""
    i = 0

    while i < len(program):

        if program[i].isalpha():
            current_token += program[i]
            i += 1
            while i < len(program) and (program[i].isalpha() or program[i].isdigit()):
                current_token += program[i]
                i += 1
            if current_token in keywords:
                tokens.append(Token(current_token, None))
            else:
                tokens.append(Token("IDENTIFIER", current_token))
            current_token = ""
        elif program[i].isdigit():
            current_token += program[i]
            i += 1
            while i < len(program) and program[i].isdigit():
                current_token += program[i]
                i += 1
            tokens.append(Token("NUMBER", current_token))
            current_token = ""
        elif program[i:i+2] == ":=":  # Recognize ":=" as a single token
            tokens.append(Token("SEPARATOR", ":="))
            i += 2  # Skip both characters
        elif program[i] in separators:
            tokens.append(Token("SEPARATOR", program[i]))
            i += 1
        elif program[i] in operators:
            current_token += program[i]
            i += 1
            while i < len(program) and program[i] in operators:
                current_token += program[i]
                i += 1
            tokens.append(Token("OPERATOR", current_token))
            current_token = ""
        elif program[i].isspace():
            i += 1
        elif program[i].isalnum() and program[i + 1] == ":":
            current_token += program[i]
            i += 1
            while i < len(program) and (program[i].isalpha() or program[i].isdigit()):
                current_token += program[i]
                i += 1
            if current_token.endswith(":"):
                tokens.append(Token("LABEL", current_token))
            else:
                print("Syntax error: Invalid label format.")
            current_token = ""
        else:
            i += 1

    return tokens


# Recursive Descent Parser
def programa(tokens):
    sequencia_de_comandos(tokens)
    # print()
    # print([tokens[0].token_type, tokens[0].value])

    if tokens[0].token_type == "IDENTIFIER" and tokens[0].value == "END":
        print("Program parsed successfully.")
    elif len(tokens) > 1:
        print("Syntax error: ';' expected.")
    else:
        print("Syntax error: 'END' expected.")

def sequencia_de_comandos(tokens):
    if tokens[0].token_type in ["LET", "GO", "TO", "READ", "PRINT", "IF", "IDENTIFIER"]:
        comando(tokens)
        if tokens[0].token_type == "SEPARATOR" and tokens[0].value == ";":
            tokens.pop(0)
            sequencia_de_comandos(tokens)

def comando(tokens):
    if tokens[0].token_type == "LET":
        atribuicao(tokens)
    elif tokens[0].token_type == "GO":
        desvio(tokens)
    elif tokens[0].token_type == "READ":
        leitura(tokens)
    elif tokens[0].token_type == "PRINT":
        impressao(tokens)
    elif tokens[0].token_type == "IF":
        decisao(tokens)
    elif tokens[0].token_type == "IDENTIFIER":
        rotulo(tokens)
        comando(tokens)
    elif tokens[0].token_type == "SEPARATOR" and tokens[0].value == ";":
        # Handle empty command (ε)
        tokens.pop(0)

    else:
        print("Syntax error: Invalid command.")

def rotulo(tokens):
    if tokens[0].token_type == "IDENTIFIER":
        tokens.pop(0)
        if tokens[0].token_type == "SEPARATOR" and tokens[0].value == ":":
            tokens.pop(0)
        else:
            print("Syntax error: ':' expected after the label.")
    else:
        print("Syntax error: Identifier expected after LABEL.")

def atribuicao(tokens):
    if tokens[0].token_type == "LET":
        tokens.pop(0)
        if tokens[0].token_type == "IDENTIFIER":
            tokens.pop(0)
            if tokens[0].token_type == "SEPARATOR" and tokens[0].value == ":=":
                tokens.pop(0)
                expressao(tokens)
            else:
                print("Syntax error: ':=' expected.")
        else:
            print("Syntax error: Identifier expected.")

def expressao(tokens):
    termo(tokens)
    if tokens[0].token_type == "OPERATOR" and tokens[0].value in ["+", "-"]:
        tokens.pop(0)
        termo(tokens)

def termo(tokens):
    fator(tokens)
    if tokens[0].token_type == "OPERATOR" and tokens[0].value in ["*", "/"]:
        tokens.pop(0)
        fator(tokens)

def fator(tokens):
    if tokens[0].token_type == "IDENTIFIER" or tokens[0].token_type == "NUMBER":
        tokens.pop(0)
    elif tokens[0].token_type == "SEPARATOR" and tokens[0].value == "(":
        tokens.pop(0)
        expressao(tokens)
        if tokens[0].token_type == "SEPARATOR" and tokens[0].value == ")":
            tokens.pop(0)
        else:
            print("Syntax error: ')' expected.")
    else:
        print("Syntax error: Identifier, Number, or '(' expected.")

def desvio(tokens):
    if tokens[0].token_type == "GO":
        tokens.pop(0)
        if(tokens[0].token_type == "TO"):
            tokens.pop(0)
            if tokens[0].token_type == "IDENTIFIER":
                tokens.pop(0)
                if tokens[0].token_type == "OF":
                    tokens.pop(0)
                    lista_de_rotulos(tokens)
                else:
                    print("Syntax error: 'OF' expected.")
            else:
                print("Syntax error: Identifier expected.")
        else:
            print("Syntax error: 'TO' expected.")
    else:
        print("Syntax error: 'GO' expected.")

def lista_de_rotulos(tokens):
    if tokens[0].token_type == "IDENTIFIER":
        tokens.pop(0)
        if tokens[0].token_type == "SEPARATOR" and tokens[0].value == ",":
            tokens.pop(0)
            lista_de_rotulos(tokens)

def leitura(tokens):
    if tokens[0].token_type == "READ":
        tokens.pop(0)
        lista_de_identificadores(tokens)

def lista_de_identificadores(tokens):
    if tokens[0].token_type == "IDENTIFIER":
        tokens.pop(0)
        if tokens[0].token_type == "SEPARATOR" and tokens[0].value == ",":
            tokens.pop(0)
            lista_de_identificadores(tokens)

def impressao(tokens):
    if tokens[0].token_type == "PRINT":
        tokens.pop(0)
        lista_de_expressoes(tokens)

def lista_de_expressoes(tokens):
    if tokens[0].token_type in ["IDENTIFIER", "NUMBER", "SEPARATOR"] or (tokens[0].token_type == "OPERATOR" and tokens[0].value == "-"):
        expressao(tokens)
        if tokens[0].token_type == "SEPARATOR" and tokens[0].value == ",":
            tokens.pop(0)
            lista_de_expressoes(tokens)

def decisao(tokens):
    if tokens[0].token_type == "IF":
        tokens.pop(0)
        comparacao(tokens)
        if tokens[0].token_type == "THEN":
            tokens.pop(0)
            comando(tokens)
            if tokens[0].token_type == "ELSE":
                tokens.pop(0)
                comando(tokens)
            else:
                print("Syntax error: 'ELSE' expected.")
        else:
            print("Syntax error: 'THEN' expected.")

def comparacao(tokens):
    expressao(tokens)
    if tokens[0].token_type == "OPERATOR" and tokens[0].value in ["<", ">", "="]:
        tokens.pop(0)
        expressao(tokens)

def Compile(input_program):
    # Tokenize the input program
    tokens = lexer(input_program)

    # for t in tokens:
    #     print([t.token_type, t.value])

    # Start parsing
    programa(tokens)
