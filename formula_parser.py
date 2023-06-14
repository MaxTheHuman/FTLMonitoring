from collections import OrderedDict
from copy import copy
from formula import Conjunction, Disjunction, Implication, \
                      Negation, Variable, Always, AlmostAlways, \
                      WeakUntil, AlmostWeakUntil

class Token:
    ttype = ""
    tvalue = ""
    
    def __init__(self, ttype, tvalue):
        self.ttype = ttype
        self.tvalue = tvalue

class Parser:
    __digits    = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    __lowercase = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", \
                 "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    __uppercase = ["B", "C", "D", "E", "F", "H", "I", "J", "K", "L", "M", \
                 "N", "O", "P", "Q", "R", "S", "T", "V", "W", "X", "Y", "Z"]  # without A, G and U

    __letters   = __lowercase + __uppercase

    __tokens = {'CONJUNCT':      '∧',
                'DISJUNCT':      '∨',
                'IMPLY':         '→',
                'NEGATE':        '¬',
                'FALSE':         '0',
                'TRUE':          '1',
                'PAREN_OPEN':    '(',
                'PAREN_CLOSE':   ')',
                'ALWAYS':        'G',
                'ALMOST_ALWAYS': '@',
                'UNTIL': 'U',
                'ALMOST_UNTIL': '#',
             }
    
    __current_token = None
    __formula_input = ""
    formula = None
    variables = OrderedDict()

    def __init__(self, eta):
        self.eta = eta
    
    def __get_compound_lexeme(self, inp, chars):
        """ Returns a lexeme compounded of chars in list or '' if no match found """
        
        if not inp[0:1] in chars:
            return ''
        else:
            return inp[0:1] + self.__get_compound_lexeme(inp[1:], chars)
    
    def __consume(self):
        """ Stores next token in __current_token """
        
        if self.__formula_input == '':
            self.__current_token = Token('END', '')
            return
        
        if self.__formula_input[0] == ' ':
            #skip whitespace
            self.__formula_input = self.__formula_input[1:]
            self.__consume()
            return
        
        for token_name in self.__tokens:
            token_character = self.__tokens[token_name]
            
            if self.__formula_input[0] == token_character:
                self.__current_token = Token(token_name, token_character)
                self.__formula_input = self.__formula_input[1:]
                return
            
        if self.__formula_input[0] in self.__letters:
            lexeme = self.__get_compound_lexeme(self.__formula_input, self.__letters + self.__digits)
            self.__formula_input = self.__formula_input[len(lexeme):]
            self.__current_token = Token("VARIABLE", lexeme)
            return
        
        self.__current_token = Token("UNKNOWN", self.__formula_input)
        self.__formula_input = ""

    def __expect_token(self, ttype):
        if self.__current_token.ttype == ttype:
            self.__consume()
        else:
            error = "Expected token of type '{}', but found '{}' with type '{}'." \
                .format(ttype, self.__current_token.tvalue, self.__current_token.ttype)
            raise SyntaxError(error)

    def parse(self, alstring):
        """ Parses a formula """
        variables = OrderedDict()
        
        #replace ASCII representations by actual symbols
        alstring = alstring.replace("~",   "¬")
        alstring = alstring.replace("!",   "¬")
        alstring = alstring.replace("/\\", "∧")
        alstring = alstring.replace("&&",  "∧")
        alstring = alstring.replace("\\/", "∨")
        alstring = alstring.replace("||",  "∨")
        alstring = alstring.replace("<->", "↔")
        alstring = alstring.replace("->",  "→")
        alstring = alstring.replace("AG",  "@")
        alstring = alstring.replace("AU",  "#")
        
        self.__formula_input = alstring
        
        #fill __current_token with initial value
        self.__consume()
        
        self.formula = self.__parse_formula()
        
        if self.__current_token.ttype != "END":
            raise SyntaxError("Expected END, but found " + self.__current_token.ttype)
        
        return (self.formula, self.variables)
    
    def __parse_formula(self):
        if self.__current_token.ttype == "NEGATE":
            self.__consume()
            return Negation(self.__parse_formula())

        if self.__current_token.ttype == "ALWAYS":
            self.__consume()
            return Always(self.__parse_formula())

        if self.__current_token.ttype == "ALMOST_ALWAYS":
            self.__consume()
            return AlmostAlways(self.__parse_formula(), self.eta)

        if self.__current_token.ttype == "PAREN_OPEN":
            #__consume PAREN_OPEN
            self.__consume()
            left_formula = self.__parse_formula()

            if self.__current_token.ttype == "PAREN_CLOSE":
                self.__consume()
                return left_formula
            
            junctor = self.__current_token.ttype
            self.__consume()
            
            right_formula = self.__parse_formula()
            
            self.__expect_token("PAREN_CLOSE")
            
            if junctor == "CONJUNCT":
                return Conjunction(left_formula, right_formula)
            if junctor == "DISJUNCT":
                return Disjunction(left_formula, right_formula)
            if junctor == "IMPLY":
                return Implication(left_formula, right_formula)
            if junctor == "UNTIL":
                return WeakUntil(left_formula, right_formula)
            if junctor == "ALMOST_UNTIL":
                return AlmostWeakUntil(left_formula, right_formula, self.eta)
            
            error = "Invalid junctor: {}".format(junctor)
            raise SyntaxError(error)
        
        if self.__current_token.ttype == "VARIABLE":
            variable = self.__current_token.tvalue
            self.__consume()
            self.variables[variable] = 0
            return Variable(variable)
        
        if self.__current_token.ttype == "END":
            return
        
        error = "Invalid token: {} with type {}"\
            .format(self.__current_token.tvalue, self.__current_token.ttype)
        raise SyntaxError(error)
