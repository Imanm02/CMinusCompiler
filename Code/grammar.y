%token NUM
%token ID
%start program
%%
program: declaration_list
;
declaration_list: declaration_list declaration
| declaration
;
declaration: var_declaration 
| fun_declaration 
;
var_declaration: type_specifier ACTION_pid ID ';' 
| type_specifier ACTION_pid ID '[' ACTION_number NUM ']' ACTION_array ';'
;
type_specifier: "int" 
| "void"
;
fun_declaration: type_specifier ACTION_pid ID '(' params ')' compound_stmt
;
params: param_list
| "void"
;
param_list: param_list ',' param
| param
;
param: type_specifier ACTION_pid ID
| type_specifier ACTION_pid ID '[' ']'
;
compound_stmt: '{' local_declarations statement_list '}'
;
local_declarations: local_declarations var_declaration
| /* epsilon */
;
statement_list: statement_list statement
| /* epsilon */
;
statement: expression_stmt
| compound_stmt
| selection_stmt
| iteration_stmt
| return_stmt
| switch_stmt
| output_stmt
;
expression_stmt: expression ';' ACTION_clearassign
| "break" ACTION_break ';'
| ';'
;
selection_stmt: "if" '(' expression ')' ACTION_save statement "endif" ACTION_jumpif
| "if" '(' expression ')' ACTION_save statement "else" ACTION_savejump statement ACTION_jump "endif"
;
iteration_stmt: "while" ACTION_label '(' expression ')' ACTION_save statement ACTION_loopwhile ACTION_callbreak
;
return_stmt: "return" ';'
| "return" expression ';'
;
switch_stmt: "switch" '(' expression ')' '{' case_stmts default_stmt '}' ACTION_callbreak
;
case_stmts: case_stmts case_stmt
| /* epsilon */
;
case_stmt: "case" ACTION_jumpif ACTION_number NUM ACTION_savecase ':' statement_list
;
default_stmt: "default" ACTION_jumpif ':' statement_list
| /* epsilon */
;
expression: var '=' expression ACTION_assign
| simple_expression
;
var: ACTION_pid ID
| ACTION_pid ID '[' expression ']' ACTION_array
;
simple_expression: additive_expression ACTION_sign relop additive_expression ACTION_op
| additive_expression
;
relop: '<'
| "=="
;
additive_expression: additive_expression ACTION_sign addop term ACTION_op
| term
;
addop: '+'
| '-'
;
term: term ACTION_sign mulop factor ACTION_op
| factor
;
mulop: '*'
| '/'
;
factor: '(' expression ')'
| var
| call
| ACTION_number NUM
;
call: ACTION_pid ID '(' args ')'
;
args: arg_list
| /* epsilon */
;
arg_list: arg_list ',' expression
| expression
;
output_stmt: "output" '(' expression ')' ACTION_print ';'
;
ACTION_assign: /* epsilon */
;
ACTION_pid: /* epsilon */
;
ACTION_number: /* epsilon */
;
ACTION_save: /* epsilon */
;
ACTION_label: /* epsilon */
;
ACTION_savejump: /* epsilon */
;
ACTION_savecase: /* epsilon */
;
ACTION_jump: /* epsilon */
;
ACTION_loopwhile: /* epsilon */
;
ACTION_op: /* epsilon */
;
ACTION_sign: /* epsilon */
;
ACTION_jumpif: /* epsilon */
;
ACTION_array: /* epsilon */
;
ACTION_print: /* epsilon */
;
ACTION_break: /* epsilon */
;
ACTION_callbreak: /* epsilon */
;
ACTION_clearassign: /* epsilon */
;
%%
