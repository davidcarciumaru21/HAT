########################################
# CONSTANTS
########################################

DIGITS = '0123456789'

########################################
# ERROS
########################################

class Error:
    def __init__(self, posStart, posEnd, errorName, detalis):
        self.posStart = posStart
        self.posEnd = posEnd
        self.errorName = errorName
        self.detalis = detalis

    def asString(self):
        result = f'{self.errorName}: {self.detalis}'
        result += f'File {self.posStart.fn}, line {self.posStart.ln + 1}'
        return result
    
class IllegalCharError(Error):
    def __init__(self, posStart, posEnd, details):
        super().__init__(posStart, posEnd, 'Illegal Character', details)

########################################
# POSITION
########################################

class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, currentChar):
        self.idx += 1
        self.col += 1
        
        if currentChar == "\n":
            self.ln += 1
            self.col = 0

        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)

########################################
# TOKENS
########################################

TT_INT      = "INT"
TT_FLT    = "FLT"
TT_PLUS     = "PLUS"
TT_MINUS    = "MINUS"
TT_MUL      = "MUL"
TT_DIV      = "DIV"
TT_LPAREN   = "LPAREN"
TT_RPAREN   = "RPAREN"

class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __repr__(self):
        if self.value : return f'{self.type}:{self.value}'
        return f'{self.type}'
    
########################################
# LEXER
########################################

class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.currentChar = None
        self.advance()

    def advance(self):
        self.pos.advance(self.currentChar)
        self.currentChar = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def makeTokens(self):
        tokens = []

        while self.currentChar != None:
            if self.currentChar == '\t':
                self.advance()
            elif self.currentChar in DIGITS:
                tokens.append(self.makeNumber())
            elif self.currentChar == '+':
                tokens.append(Token(TT_PLUS))
                self.advance()
            elif self.currentChar == '-':
                tokens.append(Token(TT_MINUS))
                self.advance()
            elif self.currentChar == '*':
                tokens.append(Token(TT_MUL))
                self.advance()
            elif self.currentChar == '/':
                tokens.append(Token(TT_DIV))
                self.advance()
            elif self.currentChar == '(':
                tokens.append(Token(TT_LPAREN))
                self.advance()
            elif self.currentChar == ')':
                tokens.append(Token(TT_RPAREN))
                self.advance()
            else:
                posStart = self.pos.copy()
                char = self.currentChar
                self.advance()
                return [], IllegalCharError(posStart, self.pos, "'" + char + "' ")

        return tokens, None
    
    def makeNumber(self):
        numStr = ''
        dotCount = 0

        while self.currentChar != None and self.currentChar in DIGITS + '.':
            if self.currentChar == '.':
                if dotCount == 1: break
                dotCount += 1
                numStr += '.'
            else:
                numStr += self.currentChar
            self.advance()

        if dotCount == 0:
            return Token(TT_INT, int(numStr))
        else:
            return Token(TT_FLT, float(numStr))
        
########################################
# RUN
########################################

def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.makeTokens()

    return tokens, error