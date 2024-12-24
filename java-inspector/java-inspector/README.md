---
title: Java-Inspector-Syntax-OO
emoji: 🔍️☕♨️💻
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 4.7.1
app_file: app.py
pinned: false
license: mit
---

# Java Syntax and OO Paradigm Inspector

This project analyzes Java code to extract insights about syntax elements and Object-Oriented (OO) paradigm usage. The tool identifies primitive types, constants, variable declarations, control structures, and more, helping developers understand and improve their Java code.

## Developer

Developed by Ramon Mayor Martins (2024)

- Email: rmayormartins@gmail.com
- Homepage: https://rmayormartins.github.io/
- Twitter: @rmayormartins
- GitHub: https://github.com/rmayormartins
- Space: https://huggingface.co/rmayormartins

## Key Features

- **Syntax Analysis**:
  - Detects primitive types and constants.
  - Identifies control structures like `if/else`, `switch/case`, loops, and operators.
  - Tracks input/output operations (e.g., `System.out.print`, `Scanner`).

- **OO Analysis**:
  - Counts classes, objects, and methods.
  - Examines encapsulation, inheritance, polymorphism, abstraction.

- **User-Friendly Interface**:
  - Upload multiple Java files for analysis.
  - Displays results in an easy-to-read table.

## How to Use

1. Open the application interface.
2. Upload one or more `.java` files.
3. View detailed syntax and OO paradigm statistics for each file.

## Local Development

To run locally:

```bash
pip install -r requirements.txt
python app.py
