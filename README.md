# CMinusCompiler

**Python3 based one-pass compiler for a simplified C-minus**

## Overview

In this project, we aim to create a one-pass compiler for a subset of the C programming language, referred to as C-minus. It is written in Python 3 and is designed to be lightweight and straightforward. The compiler takes C-minus source code and compiles it into an intermediate representation that can be executed or further processed.

## Features

- **Token Recognition:** The compiler can recognize various tokens such as identifiers, numbers, keywords, symbols, and comments.
- **Grammar Support:** It supports a predefined grammar for parsing the C-minus language constructs.
- **Error Handling:** Implements basic error handling for syntax and semantic errors.

## Token Types and Grammar

The tokens in the below table can be recognized by the compiler:

| **Token Type** | **Description**                                                |
|----------------|----------------------------------------------------------------|
| NUM            | Any string matching `[0-9]+`                                   |
| ID             | Any string matching `[A-Za-z][A-Za-z0-9]*`                     |
| KEYWORD        | `if`, `else`, `void`, `int`, `while`, `break`, `switch`, `default`, `case`, `return` |
| SYMBOL         | `;` `:` `,` `[` `]` `(` `)` `{` `}` `+` `-` `*` `=` `<` `==`    |
| COMMENT        | Any string between `/*` and `*/` OR after `//` and before a newline or EOF |
| WHITESPACE     | Spaces, tabs, and newline characters                           |

The `grammar.txt` file outlines the syntax rules that the compiler follows, which is included in the repository.

## Project Structure

The `Code` folder contains several components of the CMinusCompiler:

- `Codegen.py`: The code generation module that translates the parse tree into an intermediate representation or target code.
- `Compiler.py`: The main driver script that orchestrates the compilation process, invoking the scanner, parser, and code generator.
- `grammar.output`: Contains debugging information produced by Bison to help understand conflicts in grammar rules.
- `grammar.tab.c`: The C source code generated by Bison which includes the parsing tables and the parse function.
- `grammar.y`: The Bison grammar file defining the syntax rules of the C-minus language.
- `input.txt`: An example C-minus source code file used as input to the compiler for testing.
- `output.txt`: The output file where the result of the compilation process is stored, including intermediate code or errors.
- `Parser.py`: The parser module that takes tokens produced by the scanner and constructs a parse tree based on the grammar rules.
- `parse_table_generator.py`: A script to generate the parsing table from the grammar file which aids the parser module.
- `parse_tree.txt`: A text representation of the parse tree generated by the parser for debugging and analysis.
- `Scanner.py`: The lexical analyzer that breaks the input source code into tokens as defined in the token table.
- `semantic_errors.txt`: A log file where semantic errors detected during the compilation are recorded.
- `syntax_errors.txt`: A log file where syntax errors detected during the compilation are recorded.
- `table.json`: A JSON representation of the parse table used by the parser to guide the parsing process.

The `Docs` folder contains docs of the CMinusCompiler project and also the `grammar.txt` file is in the `Phase 2` folder.

For testing each phase of the project, we use the testcases in the `Tests` folder.

## Maintainer

- [Iman Mohammadi](https://github.com/Imanm02)
- [Shayan Salehi](https://github.com/ShayanSalehi81)

