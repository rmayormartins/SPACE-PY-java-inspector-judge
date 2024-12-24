---
title: Java-Judge-OO
emoji: ⚖️☕♨️🖥️
colorFrom: blue
colorTo: indigo
sdk: gradio
sdk_version: 4.7.1
app_file: app.py
pinned: false
license: mit
---

# Avaliador de POO em Java

Este projeto avalia códigos Java com base nos conceitos da Programação Orientada a Objetos (POO), fornecendo feedback detalhado e pontuações de acordo com uma rubrica bem definida. 

## Desenvolvedor

Desenvolvido por Ramon Mayor Martins (2024)

- Email: rmayormartins@gmail.com
- Homepage: https://rmayormartins.github.io/
- Twitter: @rmayormartins
- GitHub: https://github.com/rmayormartins
- Space: https://huggingface.co/rmayormartins

## Funcionalidades Principais

- **Análise de Sintaxe**:
  - Detecta tipos primitivos, constantes e variáveis.
  - Identifica estruturas de controle como `if/else`, `switch/case`, laços e operadores.
  - Analisa operações de entrada e saída (e.g., `System.out.print`, `Scanner`).

- **Análise de POO**:
  - Conta classes, objetos e métodos.
  - Avalia encapsulamento, herança, polimorfismo e abstração.

- **Interface Amigável**:
  - Permite upload de múltiplos arquivos Java.
  - Exibe resultados detalhados em um formato legível e intuitivo.

## Rubrica de Avaliação

### Pontuação Essencial (60 pontos)
- **Classes e Objetos**: 20 pontos.
- **Métodos**: 20 pontos.
- **Atributos**: 20 pontos.

### Pontuação Bonificada (40 pontos)
- **Encapsulamento**: 10 pontos.
- **Herança**: 10 pontos.
- **Polimorfismo**: 10 pontos.
- **Abstração**: 10 pontos.

> Para mais detalhes, visualize a rubrica completa no arquivo [rubric.pdf](rubric.pdf) ou confira a tabela resumida abaixo.

![Tabela da Rubrica](rubric_table.png)

## Como Usar

1. Abra a interface do aplicativo.
2. Envie um ou mais arquivos `.java`.
3. Veja a pontuação e o feedback detalhado para cada arquivo.

## Desenvolvimento Local

Para rodar localmente:

```bash
pip install -r requirements.txt
python app.py
```

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
