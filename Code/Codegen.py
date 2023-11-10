class Codegen:
    def __init__(self):
        self.current_token, self.current_word = None, None
        self.program_block, self.scope_stack = [], []
        self.symbol_table = {}
        self.current_address, self.temporary_address, self.pointer = 508, 508, 2
        for _ in range(200): self.program_block.append("None")
        self.program_block[0] = "(ASSIGN, #4, 0,   )"
        self.is_break, self.is_main = 0, False

    def action_choser(self, input, current_token):
        print(input)
        self.current_token = current_token
        self.current_word = self.current_token[1]
        if input == "ACTION_assign": self.action_assign()
        elif input == "ACTION_pid": self.action_pid()
        elif input == "ACTION_number": self.action_number()
        elif input == "ACTION_save": self.action_save()
        elif input == "ACTION_label": self.action_label()
        elif input == "ACTION_savejump": self.action_savejump()
        elif input == "ACTION_savecase": self.action_savecase()
        elif input == "ACTION_jump": self.action_jump()
        elif input == "ACTION_loopwhile": self.action_loopwhile()
        elif input == "ACTION_op": self.action_op()
        elif input == "ACTION_sign": self.action_sign()
        elif input == "ACTION_jumpif": self.action_jumpif()
        elif input == "ACTION_array": self.action_array()
        elif input == "ACTION_print": self.action_print()
        elif input == "ACTION_break": self.action_break()
        elif input == "ACTION_callbreak": self.action_callbreak()
        elif input == "ACTION_clearassign": self.action_clearassign()
        print(current_token, end='#')
        print(self.scope_stack, end='#')
        print(self.current_address, end='#')
        print(self.pointer)
        # print(self.program_block)

    def action_assign(self):
        self.program_block[self.pointer] = "(ASSIGN, " + str(self.scope_stack.pop()) + ", " + str(self.scope_stack[-1]) + ",   )"
        self.move_pointer()

    def action_pid(self):
        if self.current_word == 'main': 
            self.is_main = True
            self.initial_value()
            return
        address = self.find_address()
        if address is False: return
        self.scope_stack.append(address)

    def action_number(self):
        self.scope_stack.append("#" + self.current_word)

    def action_save(self):
        self.scope_stack.append(self.pointer)
        self.move_pointer()

    def action_label(self):
        self.scope_stack.append(self.pointer)

    def action_savejump(self):
        self.move_pointer()
        self.program_block[self.scope_stack[-1]] = "(JPF, " + str(self.scope_stack[-2]) + ", " + str(self.pointer) + ",   )"
        self.scope_stack.pop()
        self.scope_stack.pop()
        self.scope_stack.append(self.pointer - 1)

    def action_savecase(self):
        self.get_temporary_memory()
        self.program_block[self.pointer] = "(ASSIGN, " + str(0) + ", " + str(self.temporary_address) + ",   )"
        self.move_pointer()
        self.program_block[self.pointer] = "(EQ, " + str(self.scope_stack[-2]) + ", " + str(self.scope_stack.pop()) + ", " + str(self.temporary_address) + " )"
        self.move_pointer()
        self.scope_stack.append(self.temporary_address)
        self.scope_stack.append(self.pointer)
        self.move_pointer()

    def action_jump(self):
        if int(self.scope_stack[-1]) >= 500 or len(self.scope_stack) == 0: return
        self.program_block[self.scope_stack.pop()] = "(JP, " + str(self.pointer) + ",  ,   )"

    def action_loopwhile(self):
        self.program_block[self.scope_stack[-1]] = "(JPF, " + str(self.scope_stack[-2]) + ", " + str(self.pointer + 1) + ",   )"
        self.program_block[self.pointer] = "(JP, " + str(self.scope_stack[-3]) + ",  ,   )"
        self.scope_stack.pop()
        self.scope_stack.pop()
        self.scope_stack.pop()
        self.move_pointer()
    
    def action_op(self):
        self.get_temporary_memory()
        
        dynamic_str = str(self.scope_stack[-1]) + ", " + str(self.scope_stack[-3]) + ", " + str(self.temporary_address) + " )"
        static_str = str(self.scope_stack[-3]) + ", " + str(self.scope_stack[-1]) + ", " + str(self.temporary_address) + " )"
        if self.scope_stack[-2] == "-": self.program_block[self.pointer] = "(SUB, " + static_str
        elif self.scope_stack[-2] == "+": self.program_block[self.pointer] = "(ADD, " + static_str
        elif self.scope_stack[-2] == "*": self.program_block[self.pointer] = "(MULT, " + dynamic_str
        elif self.scope_stack[-2] == "/": self.program_block[self.pointer] = "(DIV, " + static_str
        elif self.scope_stack[-2] == "<": self.program_block[self.pointer] = "(LT, " + static_str
        elif self.scope_stack[-2] == "==": self.program_block[self.pointer] = "(EQ, " + static_str
        self.scope_stack.pop()
        self.scope_stack.pop()
        self.scope_stack.pop()
        self.scope_stack.append(self.temporary_address)
        self.move_pointer()

    def action_sign(self):
        self.scope_stack.append(self.current_word)
        
    def action_jumpif(self):
        if self.scope_stack[-1] >= 500: return
        self.program_block[self.scope_stack[-1]] = "(JPF, " + str(self.scope_stack[-2]) + ", " + str(self.pointer) + ",   )"
        self.scope_stack.pop()
        self.scope_stack.pop()

    def action_array(self):
        if len(self.scope_stack) != 1:
            self.get_temporary_memory()
            self.program_block[self.pointer] = "(MULT, " + str(self.scope_stack[-1]) + ", #4, " + str(self.temporary_address) + " )"
            self.move_pointer()
            self.program_block[self.pointer] = "(ADD, #" + str(self.scope_stack[-2]) + ", " + str(self.temporary_address) + ", " + str(self.temporary_address) + " )"
            self.scope_stack.pop()
            self.scope_stack.pop()
            self.scope_stack.append("@" + str(self.temporary_address))
            self.move_pointer()
            return
        self.current_address = self.symbol_table[list(self.symbol_table.keys())[-1]] + int(self.scope_stack[-1][1:]) * 4
        if self.is_main is False: self.current_address = self.current_address + 8
        self.scope_stack.pop()

    def action_print(self):
        self.program_block[self.pointer] = "(PRINT, " + str(self.scope_stack.pop()) + ",  ,   )"
        self.move_pointer()

    def action_break(self):
        self.scope_stack.insert(0, self.pointer)
        self.move_pointer()
        self.is_break = self.is_break + 1

    def action_callbreak(self):
        if self.is_break == 0: return
        if len(self.scope_stack) == 0: return
        if self.scope_stack[0] >= 500: return
        self.program_block[self.scope_stack[0]] = "(JP, " + str(self.pointer) + ",  ,   )"

    def action_clearassign(self):
        # if self.scope_stack[-1] < 500: return
        self.scope_stack.pop()

    def find_address(self):
        if self.current_word in self.symbol_table.keys(): return self.symbol_table[self.current_word]
        temp = self.current_address
        if self.is_main is False: temp = temp - 8
        self.symbol_table[self.current_word] = temp
        self.program_block[self.pointer] = "(ASSIGN, #0, " + str(temp) + ",   )"
        self.move_pointer()
        self.move_address()
        return False

    def move_pointer(self):
        self.pointer = self.pointer + 1

    def move_address(self):
        self.current_address = self.current_address + 4

    def get_temporary_memory(self):
        self.temporary_address = self.current_address
        self.move_address()

    def write_output(self):
        index = 0
        with open('output.txt', 'w') as file:
            for line in self.program_block:
                if line == "None": continue
                file.write(str(index) + "\t" + line + "\n")
                index = index + 1

    def initial_value(self):
        sum = 0
        for line in self.program_block:
                if line == "None": continue
                sum = sum + 1
        self.program_block[1] = "(JP, " + str(sum + 1) + ",  ,   )"