import gradio as gr
import javalang
from collections import Counter
from typing import Dict, List

class JavaSyntaxAnalyzer:
    """Java-Inspector: Syntax and OO Paradigm  Inspection in Java Code """

    def analyze_syntax(self, code: str) -> Dict[str, int]:
        """Analisa sintaticamente o código em diferentes categorias"""
        results = Counter()

        try:
            tree = javalang.parse.parse(code)

            # Declarações
            results["Tipos Primitivos"] = len([
                node.type.name for _, node in tree.filter(javalang.tree.LocalVariableDeclaration)
                if node.type.name in {"int", "double", "boolean", "char", "float", "long", "byte", "short"}
            ])
            results["Constantes (final)"] = sum(
                1 for _, node in tree.filter(javalang.tree.FieldDeclaration) if "final" in node.modifiers
            )
            results["Variáveis Declaradas"] = len(list(tree.filter(javalang.tree.LocalVariableDeclaration)))

            # Estruturas de Controle
            results["If/Else"] = len(list(tree.filter(javalang.tree.IfStatement)))
            results["Switch/Case"] = len(list(tree.filter(javalang.tree.SwitchStatement)))
            results["For Loops"] = len(list(tree.filter(javalang.tree.ForStatement)))
            results["While Loops"] = len(list(tree.filter(javalang.tree.WhileStatement)))
            results["Do-While Loops"] = len(list(tree.filter(javalang.tree.DoStatement)))

            # Operadores
            code_snippet = code
            operators = {
                "Aritméticos": ["+", "-", "*", "/", "%"],
                "Comparação": ["==", "!=", ">", "<", ">=", "<="],
                "Lógicos": ["&&", "||", "!"],
                "Atribuição": ["+=", "-=", "*=", "/="],
            }
            for category, ops in operators.items():
                results[category] = sum(code_snippet.count(op) for op in ops)

            # Entrada/Saída e Strings
            results["System.out.print"] = code_snippet.count("System.out.print")
            results["Scanner"] = code_snippet.count("Scanner")
            results["Concatenação de Strings"] = code_snippet.count("+")
            string_methods = ["concat", "substring", "length", "equals", "compareTo"]
            results["Métodos de String"] = sum(code_snippet.count(f".{method}(") for method in string_methods)

        except Exception as e:
            results["Erro"] = str(e)

        return dict(results)

    def analyze_oo(self, code: str) -> Dict[str, int]:
        """Analisa elementos do paradigma OO"""
        results = Counter()

        try:
            tree = javalang.parse.parse(code)

            # Classes e Objetos
            results["Classes"] = len(list(tree.filter(javalang.tree.ClassDeclaration)))
            results["Objetos"] = len([
                node for _, node in tree.filter(javalang.tree.VariableDeclarator) 
                if node.initializer and "new" in str(node.initializer)
            ])

            # Métodos
            results["Métodos"] = len(list(tree.filter(javalang.tree.MethodDeclaration)))

            # Atributos e Encapsulamento
            fields = list(tree.filter(javalang.tree.FieldDeclaration))
            results["Atributos"] = len(fields)
            results["Encapsulamento"] = sum(
                1 for _, field in fields if "private" in field.modifiers
            )

            # Herança
            results["Herança"] = len([
                node for _, node in tree.filter(javalang.tree.ClassDeclaration) if node.extends
            ])

            # Polimorfismo
            results["Polimorfismo"] = len([
                node for _, node in tree.filter(javalang.tree.MethodDeclaration)
                if "Override" in (node.annotations or [])
            ])

        except Exception as e:
            results["Erro"] = str(e)

        return dict(results)

def process_files(files) -> List[Dict]:
    """Processa múltiplos arquivos e analisa sintaxe e OO"""
    analyzer = JavaSyntaxAnalyzer()
    file_results = []

    for file in files:
        with open(file.name, 'r', encoding='utf-8') as f:
            code = f.read()
        syntax_results = analyzer.analyze_syntax(code)
        oo_results = analyzer.analyze_oo(code)
        
        combined_results = {**syntax_results, **oo_results}
        combined_results["Arquivo"] = file.name
        file_results.append(combined_results)

    return file_results

# Interface Gradio
with gr.Blocks(title="Java-Inspector") as demo:
    gr.Markdown("# Java-Inspector: Syntax and OO Paradigm  Inspection in Java Code")
    gr.Markdown("Suba os arquivos Java para destrinchar as estruturas sintáticas e orientadas a objetos.")

    file_input = gr.File(label="Arquivos Java", file_types=[".java"], file_count="multiple")
    analyze_button = gr.Button("Analisar Arquivos")

    output_table = gr.Dataframe(
        label="Resultados", 
        headers=[
            "Arquivo", 
            "Tipos Primitivos", "Constantes", "Variáveis Declaradas", "If/Else", "Switch/Case", 
            "For Loops", "While Loops", "Do-While Loops", "Aritméticos", "Comparação", 
            "Lógicos", "Atribuição", "System.out", "Scanner", "Concatenação", "Métodos de String", 
            "Classes", "Objetos", "Métodos", "Atributos", "Encapsulamento", "Herança", "Polimorfismo"
        ]
    )

    def analyze_files(files):
        results = process_files(files)
        # Converte os resultados para uma lista de listas para exibição na tabela
        formatted_results = [
            [
                result["Arquivo"],
                result.get("Tipos Primitivos", 0),
                result.get("Constantes (final)", 0),
                result.get("Variáveis Declaradas", 0),
                result.get("If/Else", 0),
                result.get("Switch/Case", 0),
                result.get("For Loops", 0),
                result.get("While Loops", 0),
                result.get("Do-While Loops", 0),
                result.get("Aritméticos", 0),
                result.get("Comparação", 0),
                result.get("Lógicos", 0),
                result.get("Atribuição", 0),
                result.get("System.out.print", 0),
                result.get("Scanner", 0),
                result.get("Concatenação de Strings", 0),
                result.get("Métodos de String", 0),
                result.get("Classes", 0),
                result.get("Objetos", 0),
                result.get("Métodos", 0),
                result.get("Atributos", 0),
                result.get("Encapsulamento", 0),
                result.get("Herança", 0),
                result.get("Polimorfismo", 0),
            ]
            for result in results
        ]
        return formatted_results

    analyze_button.click(fn=analyze_files, inputs=file_input, outputs=output_table)

if __name__ == "__main__":
    demo.launch(share=True)
