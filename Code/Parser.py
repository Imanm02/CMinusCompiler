from Scanner import Scanner
from Codegen import Codegen
from anytree import Node, RenderTree
import json

class Parser:
    def __init__(self):
        # declaring initial values
        self.table_data = json.load(open('table.json'))
        self.first_collection = self.table_data['first']
        self.follow_collection = self.table_data['follow']
        self.non_terminals = self.table_data['non_terminals']
        self.terminals = self.table_data['terminals']
        self.grammar = self.table_data['grammar']
        self.parse_table = self.table_data['parse_table']
        self.stack, self.father_stack, self.error_stack = [0], [], []
        self.is_finished, self.get_next, self.temp_token = False, True, None
        self.token, self.action, self.top = None, None, None
        self.right_hand_side, self.left_hand_side, self.panic_error = None, None, None
        self.scanner = Scanner()
        self.codegen = Codegen()

    def parse(self):
        while True:
            # getting token
            if self.get_next == True: self.temp_token = self.scanner.get_token()
            if self.temp_token[0] in ['WHITESPACE', 'COMMENT']: continue # TODO
            if self.temp_token[0] in ['ID', 'NUM']: self.token = self.temp_token[0] # TODO
            else: self.token = self.temp_token[1]
        
            # checking if token is in parse table or not 
            if self.token in self.parse_table[str(self.stack[-1])].keys():
                self.top = str(self.stack[-1])
                self.action = self.parse_table[self.top][self.token]
                if self.action.startswith('reduce_'):
                    if self.grammar[self.action[7:]][0].startswith('ACTION_'): self.codegen.action_choser(self.grammar[self.action[7:]][0], self.temp_token)
                    self.right_and_left_hand_side_initializer()
                    self.reduce_by_epsilon()
                    self.stack = self.stack + [self.left_hand_side[0]] # missing for
                    self.goto_expression()
                    self.insert_node()
                elif self.action.startswith('shift_'): 
                    self.shift()
                else: break
            else:
                # checking errors 
                # TODO declaring line_number for scanner
                self.error_stack = self.error_stack + ["#" + str(self.scanner.line_number) + " : syntax error , illegal " + str(self.temp_token[1]) + "\n"]
                while not list(filter(lambda value: value.startswith('goto'), self.parse_table[str(self.stack[-1])].values())): self.tree_error()
                self.top = str(self.stack[-1])
                self.temp_token = self.scanner.get_token()
                while self.temp_token[0] in ['WHITESPACE', 'COMMENT']: self.temp_token = self.scanner.get_token()
                self.panic_error = None
                panic_mode = True
                while not self.panic_error:
                    for err in sorted(list(filter(lambda value: self.parse_table[str(self.stack[-1])][value].startswith('goto'), self.parse_table[str(self.stack[-1])]))):
                        if self.temp_token[0] in self.follow_collection[err]:
                            self.panic_error = err
                            break
                        elif self.temp_token[1] in self.follow_collection[err]:
                            self.panic_error = err
                            break
                        else: continue
                    if not self.panic_error:
                        if self.temp_token[1] != '$': 
                            self.error_stack = self.error_stack + ["#" + str(self.scanner.line_number) + " : syntax error , discarded " + str(self.temp_token[1]) + " from input\n"]
                            self.temp_token = self.scanner.get_token()
                            continue
                        else:
                            self.is_finished = True
                            self.error_stack = self.error_stack + ["#" + str(self.scanner.line_number) + " : syntax error , Unexpected EOF"]
                            break
                if self.is_finished: break
                self.end_error()
                

    def shift(self):
        self.stack.append(self.temp_token)
        self.stack.append(int(''.join(self.action[6:])))
        self.father_stack.append(Node('(' + self.temp_token[0] + ', ' + self.temp_token[1] + ')'))
        self.get_next = True
    
    def right_and_left_hand_side_initializer(self):
        temp_joint = self.grammar[''.join(self.action[7:])]
        self.right_hand_side = temp_joint[temp_joint.index("->") + 1:]
        self.left_hand_side = temp_joint[:temp_joint.index("->")]

    def reduce_by_epsilon(self):
        if 'epsilon' in self.right_hand_side: self.father_stack.append(Node('epsilon'))
        else:
            for _ in range(0, 2 * len(self.right_hand_side)):
                input = str(self.stack.pop())

    def goto_expression(self):
        temp_str = self.parse_table[str(self.stack[-2])][str(self.stack[-1])]
        self.stack.append(int(temp_str[5:]))
        self.get_next = False

    def insert_node(self):
        temp_node = Node(self.left_hand_side[0], children=self.father_stack[-len(self.right_hand_side):])
        for _ in range(0, len(self.right_hand_side)): self.father_stack.pop()
        self.father_stack.append(temp_node)

    def tree_error(self):
        self.stack.pop(-1)
        poped = self.stack.pop(-1)
        if type(poped) != tuple: self.error_stack = self.error_stack + ["syntax error , discarded " + str(poped) + " from stack\n"]
        else: self.error_stack = self.error_stack + ["syntax error , discarded (" + str(poped[0]) + ", " + str(poped[1]) + ") from stack\n"]
        self.father_stack.pop()

    def end_error(self):
        self.error_stack = self.error_stack + ["#" + str(self.scanner.line_number) + " : syntax error , missing " + str(self.panic_error) + "\n"]
        # TODO scanner line number
        self.stack.append(self.panic_error)
        self.father_stack.append(Node(self.panic_error))
        self.stack.append(self.parse_table[self.top][self.panic_error][5:])
        self.get_next = False

    def saving_tree(self):
        with open('parse_tree.txt', "w", encoding="utf-8") as file:
            if self.is_finished: return
            self.create_tree(file)
    
    def create_tree(self, file):
        Node('$', self.father_stack[0])
        for pre, _, node in RenderTree(self.father_stack[0]):
            pattern = "%s%s\n" % (pre, node.name)
            file.write(pattern)

    def saving_error(self):
        if not self.error_stack: self.error_stack = ['There is no syntax error.']
        with open('syntax_errors.txt', 'w') as file:
            for line in self.error_stack: file.write(line)

    def generating_output(self):
        self.codegen.write_output()
        with open('semantic_errors.txt', 'w') as file:
            file.write("The input program is semantically correct.")