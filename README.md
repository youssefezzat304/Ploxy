# Lox langauge using Python and C++ (WIP)

This repository contains an implementation of the Lox programming language from Robert Nystrom's book  *Crafting Interpreters* . The project is divided into two parts:

1. **Python Implementation (Part I) [completed]** ✅: A tree-walk interpreter for the Lox language, following the first part of the book. This serves as an accessible and concise implementation.
2. **C++ Implementation (Part II)** **[WIP]**: A high-performance bytecode interpreter for Lox, built during the second part of the book.

## What is Lox?

**Lox** is a programming language designed by  **Robert Nystrom** , the author of the book  *"Crafting Interpreters"* . It is a simple, dynamically-typed scripting language used primarily for educational purposes. The language is designed to be easy to implement and understand, making it an excellent tool for learning how programming languages and interpreters work.

## Installation

To set up the development environment:

```bash
https://github.com/youssefezzat304/Ploxy.git
cd ploxy
pip install -e .
```

## Interactive Mode

To start the REPL (interactive prompt):

```bash
ploxy run
```

To exit the interactive mode, type `exit`.

## REPL Capabilities

### Basic Operations

- Arithmetic expressions: `+`, `-`, `*`, `/`
- Comparison operators: `<`, `>`, `<=`, `>=`, `==`, `!=`
- Logical operators: `and`, `or`, `!`
- Grouping with parentheses: `(2 + 3) * 4`

### Variables and Data Types

- Variable declarations: `var name = "value";`
- Numbers (floating point): `var pi = 3.14159;`
- Strings: `var greeting = "Hello, world!";`
- Booleans: `var isTrue = true;`
- Nil: `var nothing = nil;`

### Control Flow

- If statements: `if (condition) { ... } else { ... }`
- While loops: `while (condition) { ... }`
- For loops: `for (var i = 0; i < 10; i = i + 1) { ... }`

### Functions

- Function declarations: `fun add(a, b) { return a + b; }`
- Function calls: `add(5, 3);`
- Closures: Functions capture their surrounding environment
- Recursion: `fun fib(n) { if (n <= 1) return n; return fib(n-1) + fib(n-2); }`

### Classes and OOP

- Class declarations: `class Person { ... }`
- Constructors: `init() { ... }`
- Instance methods: `sayName() { print this.name; }`
- Properties: `this.name = name;`
- Inheritance: `class Employee < Person { ... }`

### Other Features

- Print statements: `print "Hello, world!";`
- Comments: `// This is a comment`
- Exit REPL by typing `exit`

## Features

- Full implementation of the Lox language
- Support for variables, control flow, functions, and classes
- Lexical scoping
- Class inheritance

## Conventions

* In Python part, the double underscore `__` signifies that the method is private and meant for use only within its own class.

## License

MIT License
