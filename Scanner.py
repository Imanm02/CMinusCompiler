allSymbols = []
allSymbols.append(';')
allSymbols.append(':')
allSymbols.append(',')
allSymbols.append('[')
allSymbols.append(']')
allSymbols.append('(')
allSymbols.append(')')
allSymbols.append('{')
allSymbols.append('}')
allSymbols.append('+')
allSymbols.append('-')
allSymbols.append('*')
allSymbols.append('/')
allSymbols.append('=')
allSymbols.append('<')

whiteSpaces = []
whiteSpaces.append(' ')
whiteSpaces.append('\n')
whiteSpaces.append('\r')
whiteSpaces.append('\t')
whiteSpaces.append('\v')
whiteSpaces.append('\f')

allKeywords = []
allKeywords.append('if')
allKeywords.append('else')
allKeywords.append('void')
allKeywords.append('int')
allKeywords.append('while')
allKeywords.append('break')
allKeywords.append('switch')
allKeywords.append('default')
allKeywords.append('case')
allKeywords.append('return')
allKeywords.append('endif')
allKeywords.append('output')

class Scanner(object):
    def __init__(self):
        self.str_input = open('input.txt', 'r').read()
        self.str_index = 0
        self.line_number = 1
        self.line_number_temp = 1

    def oneMore(self):
        self.str_index += 1

    def add(self, output, s):
        output = output + s
        return output

    def get_token(self):
        global allSymbols, whiteSpaces, allKeywords
        output = ''

        while True:
            if self.str_index == len(self.str_input):
                return 'EOF', '$'
            if self.str_index > len(self.str_input):
                return 'EOF', '$'
            s = self.str_input[self.str_index]
            if s == '\n':
                self.line_number = self.line_number + 1
            if  (s != '\n' and s != '\f' and s != '\v' and s != '\t' and s != '\r'):
                if ord(s) != 32:
                    if ord(s) in range(48, 58):
                        output = output + s
                        self.oneMore()
                        s = self.str_input[self.str_index]
                        while ord(s) in range(48, 54):
                            self.oneMore()
                            output = output + s
                            s = self.str_input[self.str_index]
                        if ord(s) in range(97, 123) or (not (s in allSymbols) and not (s in whiteSpaces)):
                            output += s
                            if ord(s) in range(65, 91):
                                self.oneMore()
                                return 'error', output, 'Invalid number'
                            elif ord(s) in range(97, 123):
                                self.oneMore()
                                return 'error', output, 'Invalid number'
                            else:
                                self.oneMore()
                                return 'error', output, 'Invalid input'
                        if ord(s) in range(65, 91):
                            output += s
                            if ord(s) in range(65, 91):
                                self.oneMore()
                                return 'error', output, 'Invalid number'
                            elif ord(s) in range(97, 123):
                                self.oneMore()
                                return 'error', output, 'Invalid number'
                            else:
                                self.oneMore()
                                return 'error', output, 'Invalid input'
                        else:
                            return 'NUM', output, ''

                    elif ord(s) in range(54, 58):
                        output = self.add(output, s)
                        self.oneMore()
                        s = self.str_input[self.oneMore()]
                        while ord(s) in range(48, 58):
                            output = self.add(output, s)
                            self.oneMore()
                            s = self.str_input[self.oneMore()]
                        if ord(s) in range(65, 91) or ord(s) in range(97, 123) or (not (s in allSymbols) and not (s in whiteSpaces)):
                            output = self.add(output, s)
                            if ord(s) in range(65, 91):
                                self.oneMore()
                                return 'error', output, 'Invalid number'
                            elif ord(s) in range(97, 123):
                                self.oneMore()
                                return 'error', output, 'Invalid number'
                            else:
                                self.oneMore()
                                return 'error', output, 'Invalid input'
                        else:
                            return 'NUM', output, ''

                    elif ord(s) in range(65, 91):
                        output = output + s
                        self.oneMore()
                        s = self.str_input[self.str_index]
                        while ord(s) in range(48, 58) or ord(s) in range(65, 91) or ord(s) in range(97, 123):
                            output = output + s
                            self.oneMore
                            s = self.str_input[self.str_index]
                        if not (s in allSymbols) and not (s in whiteSpaces):
                            output = output + s
                            return 'error', output, 'Invalid input'
                        else:
                            if output in allKeywords:
                                return 'KEYWORD', output, ''
                            else:
                                return 'ID', output, ''

                    elif ord(s) in range(97, 123):
                        output = output + s
                        self.oneMore()
                        s = self.str_input[self.str_index]
                        while ord(s) in range(48, 58) or ord(s) in range(65, 91) or ord(s) in range(97, 123):
                            output = output + s
                            self.oneMore()
                            s = self.str_input[self.str_index]
                        if not (s in allSymbols) and not (s in whiteSpaces):
                            output += s
                            self.oneMore
                            return 'error', output, 'Invalid input'
                        else:
                            if output in allKeywords:
                                return 'KEYWORD', output, ''
                            else:
                                return 'ID', output, ''

                    elif s == '=':
                        output += s
                        if self.str_index + 1 < len(self.str_input) and self.str_input[self.str_index + 1] == '=':
                            output += '='
                            self.oneMore()
                            self.oneMore()
                            return 'SYMBOL', output, ''
                        else:
                            if self.str_index + 1 >= len(self.str_input) or (self.str_input[self.str_index + 1] in whiteSpaces) or (self.str_input[self.str_index + 1] in allSymbols) or (
                                    ord(self.str_input[self.str_index + 1]) in range(48, 58)) or ord(s) in range(65, 91) or ord(s) in range(97, 123):
                                self.oneMore()
                                return 'SYMBOL', output, ''
                            else:
                                self.oneMore()
                                self.oneMore()
                                return 'error', output + self.str_input[self.str_index + 1], 'Invalid input'

                    elif s == '*' and self.str_input[self.str_index + 1] == '/':
                        self.oneMore()
                        self.oneMore()
                        return 'error', '*/', 'Unmatched COMMENT'

                    elif s == '/' and self.str_input[self.str_index + 1] == '/':
                        self.oneMore()
                        self.oneMore()
                        while self.str_input[self.str_index] != '\n' and self.str_index < len(self.str_input):
                            self.oneMore()
                        return 'COMMENT', '', ''

                    elif s == '/' and self.str_input[self.str_index + 1] == '*':
                        self.oneMore()
                        self.oneMore()
                        self.line_number_temp = self.line_number
                        while self.str_index < len(self.str_input) - 1 and not (self.str_input[self.str_index] == '*' and self.str_input[self.str_index + 1] == '/'):
                            output += self.str_input[self.str_index]
                            if self.str_input[self.str_index] == '\n':
                                self.line_number = self.line_number + 1
                            self.oneMore()
                        if self.str_index >= len(self.str_input) - 1:
                            self.oneMore()
                            return 'error', '/*' + output[:5] + '...', 'Unclosed COMMENT'
                        else:
                            self.oneMore()
                            self.oneMore()
                            return 'COMMENT', '', ''
                    elif s in allSymbols:
                        output = output + s
                        self.oneMore()
                        return 'SYMBOL', output, ''
                    else:
                        output = output + s
                        self.oneMore()
                        return 'error', output, 'Invalid input'
                else:
                    self.oneMore()
            else:
                self.oneMore()

    def write_error(self, inout, lastLineCode):
        zero = 0
        allErrors = ''
        lineNumber = inout[-2]
        if inout is not None:
            if inout[1] == 'error':
                if (not(lineNumber == lastLineCode)):
                    if lastLineCode == zero:
                        allErrors = allErrors + str(lineNumber) + '.\t'
                    elif lastLineCode != zero:
                        allErrors = allErrors + '\n'
                        allErrors = allErrors + str(lineNumber)
                        allErrors = allErrors + '.\t'
                    lastLineCode = lineNumber
                err = '('
                err = err + inout[0]
                err = err + ', '
                err = err + inout[2]
                err = err + ') '
                allErrors = allErrors + err
        return allErrors, lastLineCode


    def write_symbol_table(self, output):
        ID = 'ID'
        if output is not None:
            if output[1] == ID:
                inout = output[0]
                return inout

    def write_token(self, output, lastLineCode):
        stringToken = ''
        COMMENT = 'COMMENT'
        errorName = 'error'
        lineNumber = int(output[-2])
        if output[1] != COMMENT:
            if output[1] != errorName:
                if lineNumber != lastLineCode:
                    if lastLineCode == 0:
                        stringToken = stringToken + str(lineNumber)
                        stringToken = stringToken + '.\t'
                    elif lastLineCode != 0:
                        stringToken = stringToken + '\n'
                        stringToken = stringToken + str(lineNumber)
                        stringToken = stringToken + '.\t'
                    lastLineCode = lineNumber
                stringToken = stringToken + '('
                stringToken = stringToken + output[1]
                stringToken = stringToken + ', '
                stringToken = stringToken + output[0]
                stringToken = stringToken + ') '
        return stringToken, lastLineCode

