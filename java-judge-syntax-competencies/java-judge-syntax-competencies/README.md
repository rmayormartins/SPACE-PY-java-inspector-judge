---
title: Java-Judge-Syntax-Competencies
emoji: ⚖️✏️☕♨️🖥️
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 4.7.1
app_file: app.py
pinned: false
license: mit
---

# Avaliador de POO em Java

Este projeto avalia códigos Java com base nos conceitos da Programação Orientada a Objetos (POO), fornecendo feedback detalhado e pontuações de acordo com duas rubricas bem definidas: **Estrutural** e **Competências**.

## Desenvolvedor

Desenvolvido por Ramon Mayor Martins (2024)

- **Email**: rmayormartins@gmail.com
- **Homepage**: [rmayormartins.github.io](https://rmayormartins.github.io/)
- **Twitter**: [@rmayormartins](https://twitter.com/rmayormartins)
- **GitHub**: [github.com/rmayormartins](https://github.com/rmayormartins)
- **Space**: [Hugging Face Space](https://huggingface.co/rmayormartins)

## Funcionalidades Principais

### **Avaliação Estrutural**
- Detecta tipos primitivos, constantes e variáveis.
- Identifica estruturas de controle como `if/else`, `switch/case`, laços e operadores.
- Analisa operações de entrada e saída (e.g., `System.out.print`, `Scanner`).

### **Avaliação por Competências**
- Examina a corretude sintática de estruturas básicas e elementos essenciais.
- Avalia competências como organização, clareza e resolução de problemas.
- Fornece feedback detalhado com base no uso de estruturas adequadas.

### **Interface Amigável**
- Permite upload de múltiplos arquivos Java.
- Exibe resultados detalhados em abas separadas para cada tipo de avaliação.

## Rubricas de Avaliação

### Avaliação Estrutural

| Categoria              | Pontos |
|------------------------|--------|
| Declarações e Tipos    | 25     |
| Estruturas de Controle | 25     |
| Operadores e Expressões| 25     |
| Entrada e Saída        | 25     |

### Avaliação por Competências

| Categoria                 | Pontos |
|---------------------------|--------|
| Corretude Sintática       | 50     |
| Competências Demonstradas | 50     |

> Para mais detalhes, visualize a rubrica completa no arquivo [rubric.pdf](rubric.pdf) ou confira a tabela resumida abaixo.

![Tabela da Rubrica](rubric_table.png)

## Como Usar

1. Abra a interface do aplicativo.
2. Escolha entre **Avaliação Estrutural** ou **Avaliação por Competências**.
3. Envie um ou mais arquivos `.java`.
4. Veja a pontuação e o feedback detalhado para cada arquivo.

## Desenvolvimento Local

Para rodar localmente:

```bash
pip install -r requirements.txt
python app.py
