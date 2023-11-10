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


## Maintainer

- [Iman Mohammadi](https://github.com/Imanm02)
- [Shayan Salehi](https://github.com/ShayanSalehi81)