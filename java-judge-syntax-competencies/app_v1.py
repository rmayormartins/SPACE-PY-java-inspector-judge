
import gradio as gr
import javalang
from typing import Dict, List, Tuple
import re

class JavaStructuralEvaluator:
    """Avaliador baseado em estruturas usadas"""
    def __init__(self):
        self.rubric = {
            "declaracoes": 25,  # Declarações e tipos
            "estruturas_controle": 25,  # if, switch, loops
            "operadores": 25,  # Operadores e expressões
            "io_strings": 25  # System.out, concatenação, etc
        }
    
    def analyze_declarations(self, code: str) -> Tuple[float, List[str]]:
        """Analisa declarações e tipos"""
        score = 0
        feedback = []
        
        try:
            tree = javalang.parse.parse(code)
            
            # Verificar tipos primitivos
            primitives = {
                'int': 'números inteiros',
                'double': 'números decimais',
                'boolean': 'valores lógicos',
                'char': 'caracteres',
                'float': 'números decimais (float)',
                'long': 'números longos',
                'byte': 'valores byte',
                'short': 'números curtos'
            }
            
            used_types = set()
            for _, node in tree.filter(javalang.tree.LocalVariableDeclaration):
                type_name = node.type.name
                used_types.add(type_name)
                
            for type_name, description in primitives.items():
                if type_name in used_types:
                    score += 3
                    feedback.append(f"✓ Uso correto de {type_name} para {description}")
            
            # Verificar declarações de variáveis
            total_vars = len(list(tree.filter(javalang.tree.LocalVariableDeclaration)))
            if total_vars > 0:
                score += 5
                feedback.append(f"✓ {total_vars} variáveis declaradas corretamente")
            
            # Verificar constantes
            constants = list(tree.filter(javalang.tree.FieldDeclaration))
            if any('final' in node.modifiers for _, node in tree.filter(javalang.tree.FieldDeclaration)):
                score += 4
                feedback.append("✓ Uso adequado de constantes (final)")
            
        except Exception as e:
            feedback.append("⚠ Erro na análise de declarações")
            
        return score, feedback

    def analyze_control_structures(self, code: str) -> Tuple[float, List[str]]:
        """Analisa estruturas de controle"""
        score = 0
        feedback = []
        
        try:
            tree = javalang.parse.parse(code)
            
            # If/Else
            if_count = len(list(tree.filter(javalang.tree.IfStatement)))
            if if_count > 0:
                score += 5
                feedback.append(f"✓ Uso correto de {if_count} estrutura(s) if/else")
            
            # Switch
            switch_count = len(list(tree.filter(javalang.tree.SwitchStatement)))
            if switch_count > 0:
                score += 5
                feedback.append(f"✓ Uso correto de {switch_count} switch/case")
            
            # For loops
            for_count = len(list(tree.filter(javalang.tree.ForStatement)))
            if for_count > 0:
                score += 5
                feedback.append(f"✓ Uso correto de {for_count} loop(s) for")
            
            # While loops
            while_count = len(list(tree.filter(javalang.tree.WhileStatement)))
            if while_count > 0:
                score += 5
                feedback.append(f"✓ Uso correto de {while_count} loop(s) while")
            
            # Do-While loops
            do_while_count = len(list(tree.filter(javalang.tree.DoStatement)))
            if do_while_count > 0:
                score += 5
                feedback.append(f"✓ Uso correto de {do_while_count} loop(s) do-while")
            
        except Exception as e:
            feedback.append("⚠ Erro na análise de estruturas de controle")
            
        return score, feedback

    def analyze_operators(self, code: str) -> Tuple[float, List[str]]:
        """Analisa operadores e expressões"""
        score = 0
        feedback = []
        
        try:
            # Operadores aritméticos
            arithmetic = ['+', '-', '*', '/', '%']
            for op in arithmetic:
                if op in code:
                    score += 2
                    feedback.append(f"✓ Uso do operador aritmético {op}")
            
            # Operadores de comparação
            comparison = ['==', '!=', '>', '<', '>=', '<=']
            for op in comparison:
                if op in code:
                    score += 2
                    feedback.append(f"✓ Uso do operador de comparação {op}")
            
            # Operadores lógicos
            logical = ['&&', '||', '!']
            for op in logical:
                if op in code:
                    score += 2
                    feedback.append(f"✓ Uso do operador lógico {op}")
            
            # Operadores de atribuição
            assignment = ['+=', '-=', '*=', '/=']
            for op in assignment:
                if op in code:
                    score += 2
                    feedback.append(f"✓ Uso do operador de atribuição {op}")
            
        except Exception as e:
            feedback.append("⚠ Erro na análise de operadores")
            
        return score, feedback

    def analyze_io_strings(self, code: str) -> Tuple[float, List[str]]:
        """Analisa entrada/saída e manipulação de strings"""
        score = 0
        feedback = []
        
        try:
            # System.out
            if 'System.out.print' in code:
                score += 5
                feedback.append("✓ Uso correto de System.out.print")
            
            # Scanner
            if 'Scanner' in code:
                score += 5
                feedback.append("✓ Uso correto da classe Scanner para entrada")
            
            # Concatenação de strings
            if '+' in code and '"' in code:
                score += 5
                feedback.append("✓ Concatenação de strings com operador +")
            
            # Métodos de String
            string_methods = ['concat', 'substring', 'length', 'equals', 'compareTo']
            for method in string_methods:
                if f'.{method}(' in code:
                    score += 2
                    feedback.append(f"✓ Uso do método String.{method}")
            
        except Exception as e:
            feedback.append("⚠ Erro na análise de I/O e strings")
            
        return score, feedback

    def evaluate_code(self, code: str) -> Dict:
        """Avalia o código Java"""
        # Análises individuais
        decl_score, decl_feedback = self.analyze_declarations(code)
        ctrl_score, ctrl_feedback = self.analyze_control_structures(code)
        op_score, op_feedback = self.analyze_operators(code)
        io_score, io_feedback = self.analyze_io_strings(code)
        
        # Calcular pontuação total
        total_score = sum([
            decl_score,
            ctrl_score,
            op_score,
            io_score
        ])
        
        # Normalizar para 100
        total_score = min(100, total_score)
        
        # Determinar nível
        proficiency = "Necessita Melhorias"
        if total_score >= 90:
            proficiency = "Excelente"
        elif total_score >= 75:
            proficiency = "Bom"
        elif total_score >= 60:
            proficiency = "Satisfatório"
            
        return {
            "total_score": total_score,
            "proficiency": proficiency,
            "feedback": {
                "declaracoes": decl_feedback,
                "estruturas_controle": ctrl_feedback,
                "operadores": op_feedback,
                "io_strings": io_feedback
            }
        }

class CompetencyEvaluator:
    """Avaliador baseado em competências"""
    def __init__(self):
        self.rubric = {
            "syntax_correctness": 50,  # Corretude sintática
            "competencies": 50         # Competências demonstradas
        }
    
    def analyze_syntax_correctness(self, code: str) -> Tuple[float, List[str]]:
        """Analisa corretude sintática (50 pontos)"""
        score = 0
        feedback = []
        
        try:
            tree = javalang.parse.parse(code)
            
            # 1. Estrutura básica do programa (10 pontos)
            if 'class' in code:
                score += 5
                feedback.append("✓ Estrutura de classe correta")
            if 'public static void main' in code:
                score += 5
                feedback.append("✓ Método main corretamente declarado")

            # 2. Declarações e Tipos (10 pontos)
            declarations = list(tree.filter(javalang.tree.LocalVariableDeclaration))
            if declarations:
                score += 5
                feedback.append("✓ Declarações de variáveis sintáticamente corretas")
                if any(d.type.name in ['int', 'double', 'String', 'boolean'] for d in declarations):
                    score += 5
                    feedback.append("✓ Tipos de dados usados corretamente")

            # 3. Expressões e Operadores (10 pontos)
            if list(tree.filter(javalang.tree.BinaryOperation)):
                score += 10
                feedback.append("✓ Expressões e operadores usados corretamente")

            # 4. Blocos e Estruturas (10 pontos)
            open_braces = code.count('{')
            close_braces = code.count('}')
            if open_braces == close_braces and open_braces > 0:
                score += 5
                feedback.append("✓ Blocos corretamente delimitados")
            
            semicolons = len(re.findall(';[^;]*$', code, re.MULTILINE))
            if semicolons > 0:
                score += 5
                feedback.append("✓ Instruções corretamente terminadas")

            # 5. Entrada/Saída (10 pontos)
            if 'System.out' in code:
                score += 5
                feedback.append("✓ Sintaxe de saída correta")
            if 'Scanner' in code:
                score += 5
                feedback.append("✓ Sintaxe de entrada correta")

        except Exception as e:
            feedback.append(f"⚠ Erro de sintaxe: {str(e)}")
            
        return score, feedback

    def analyze_competencies(self, code: str) -> Tuple[float, List[str]]:
        """Analisa competências demonstradas (50 pontos)"""
        score = 0
        feedback = []
        
        try:
            tree = javalang.parse.parse(code)
            
            # 1. Seleção de Estruturas (15 pontos)
            structures = {
                'if': list(tree.filter(javalang.tree.IfStatement)),
                'for': list(tree.filter(javalang.tree.ForStatement)),
                'while': list(tree.filter(javalang.tree.WhileStatement))
            }
            
            appropriate_use = True
            for struct_type, instances in structures.items():
                if instances:
                    if struct_type == 'for' and any('length' in str(inst) for inst in instances):
                        score += 5
                        feedback.append("✓ Uso adequado de for para iteração em arrays")
                    elif struct_type == 'while' and any('hasNext' in str(inst) for inst in instances):
                        score += 5
                        feedback.append("✓ Uso adequado de while para leitura de dados")
                    else:
                        score += 5
                        feedback.append(f"✓ Uso apropriado de {struct_type}")

            # 2. Manipulação de Dados (15 pontos)
            operations = list(tree.filter(javalang.tree.BinaryOperation))
            if operations:
                if any(op.operator in ['*', '/', '+', '-'] for op in operations):
                    score += 5
                    feedback.append("✓ Cálculos implementados corretamente")
                if any(op.operator in ['>', '<', '>=', '<=', '=='] for op in operations):
                    score += 5
                    feedback.append("✓ Comparações implementadas corretamente")
                if any('=' in str(op) for op in operations):
                    score += 5
                    feedback.append("✓ Atribuições implementadas corretamente")

            # 3. Clareza e Organização (10 pontos)
            # Verificar nomes significativos
            if all(len(decl.declarators[0].name) > 1 for _, decl in tree.filter(javalang.tree.LocalVariableDeclaration)):
                score += 5
                feedback.append("✓ Nomes de variáveis significativos")
            
            # Verificar indentação e comentários
            lines = code.split('\n')
            if any('//' in line or '/*' in line for line in lines):
                score += 5
                feedback.append("✓ Código bem documentado")

            # 4. Resolução do Problema (10 pontos)
            # Verificar se tem entrada, processamento e saída
            has_input = 'Scanner' in code
            has_processing = bool(operations)
            has_output = 'System.out' in code
            
            if has_input and has_output:
                score += 5
                feedback.append("✓ Programa com entrada e saída")
            if has_processing:
                score += 5
                feedback.append("✓ Lógica de processamento implementada")

        except Exception as e:
            feedback.append(f"⚠ Erro na análise de competências: {str(e)}")
            
        return score, feedback

    def evaluate_code(self, code: str) -> Dict:
        # Análises individuais
        syntax_score, syntax_feedback = self.analyze_syntax_correctness(code)
        comp_score, comp_feedback = self.analyze_competencies(code)
        
        # Calcular pontuação total
        total_score = syntax_score + comp_score
        
        # Determinar nível
        proficiency = "Necessita Melhorias"
        if total_score >= 90:
            proficiency = "Excelente"
        elif total_score >= 75:
            proficiency = "Bom"
        elif total_score >= 60:
            proficiency = "Satisfatório"
            
        return {
            "total_score": total_score,
            "proficiency": proficiency,
            "feedback": {
                "corretude_sintatica": syntax_feedback,
                "competencias": comp_feedback
            }
        }

def process_java_files(files) -> str:
    """Avalia código usando a rubrica estrutural"""
    evaluator = JavaStructuralEvaluator()
    return evaluate_files(files, evaluator, "Estrutural")

def evaluate_competency(files) -> str:
    """Avalia código usando a rubrica de competências"""
    evaluator = CompetencyEvaluator()
    return evaluate_files(files, evaluator, "Competências")

def evaluate_files(files, evaluator, evaluation_type: str) -> str:
    """Função auxiliar para avaliar arquivos com qualquer avaliador"""
    results = []
    project_files = {}
    
    try:
        if not isinstance(files, list):
            files = [files]
        
        # Primeiro, vamos ler todos os arquivos
        for file in files:
            with open(file.name, 'r', encoding='utf-8') as f:
                content = f.read()
                project_files[file.name] = content
        
        # Identificar arquivo principal
        main_file = None
        other_files = {}
        for filename, content in project_files.items():
            if "public static void main" in content:
                main_file = (filename, content)
            else:
                other_files[filename] = content
        
        # Resumo do projeto
        results.append(f"""
{'='*50}
AVALIAÇÃO {evaluation_type.upper()}
{'='*50}
Total de arquivos: {len(project_files)}
Arquivo principal: {main_file[0] if main_file else 'Não encontrado'}
Arquivos complementares: {len(other_files)}
{'='*50}
""")
        
        # Avaliar arquivo principal
        if main_file:
            result = f"\nARQUIVO PRINCIPAL: {main_file[0]}\n{'-'*30}\n"
            evaluation = evaluator.evaluate_code(main_file[1])
            
            result += f"Pontuação Total: {evaluation['total_score']:.1f}/100\n"
            result += f"Nível: {evaluation['proficiency']}\n\n"
            
            result += "Feedback Detalhado:\n"
            for category, comments in evaluation['feedback'].items():
                if comments:
                    result += f"\n{category.title()}:\n"
                    for comment in comments:
                        result += f"  {comment}\n"
            
            results.append(result)
        
        # Avaliar outros arquivos
        if other_files:
            results.append(f"\nARQUIVOS COMPLEMENTARES\n{'-'*30}")
            
            for filename, content in other_files.items():
                result = f"\nAvaliando: {filename}\n"
                evaluation = evaluator.evaluate_code(content)
                
                result += f"Pontuação: {evaluation['total_score']:.1f}/100\n"
                result += f"Nível: {evaluation['proficiency']}\n\n"
                
                result += "Feedback:\n"
                for category, comments in evaluation['feedback'].items():
                    if comments:
                        result += f"\n{category.title()}:\n"
                        for comment in comments:
                            result += f"  {comment}\n"
                
                results.append(result)
        
        return "\n".join(results)
        
    except Exception as e:
        return f"Erro ao processar arquivos: {str(e)}\nTipo do erro: {type(e)}"

# Interface Gradio com abas
with gr.Blocks(title="Java-Judge-Syntax-Competencies") as demo:
    gr.Markdown("""
    # Java-Judge-Syntax-Competencies
    
    ### [Visualizar Rubrica em PDF](rubric.pdf)
    ### [Visualizar Rubrica em PNG](rubric_table.png)
    Este avaliador analisa código Java usando duas rubricas diferentes:
    1. **Avaliação Estrutural**: Foca no uso correto de elementos da linguagem
    2. **Avaliação por Competências**: Analisa qualidade e eficiência do código
    """)
    
    with gr.Tabs():
        with gr.Tab("Avaliação Estrutural"):
            upload_structural = gr.File(
                file_count="multiple",
                label="Upload dos arquivos Java"
            )
            evaluate_btn_structural = gr.Button("Avaliar Estruturas")
            output_structural = gr.Textbox(
                label="Resultado da Avaliação",
                lines=25
            )
            evaluate_btn_structural.click(
                fn=process_java_files,
                inputs=upload_structural,
                outputs=output_structural
            )
            
        with gr.Tab("Avaliação por Competências"):
            upload_competency = gr.File(
                file_count="multiple",
                label="Upload dos arquivos Java"
            )
            evaluate_btn_competency = gr.Button("Avaliar Competências")
            output_competency = gr.Textbox(
                label="Resultado da Avaliação",
                lines=25
            )
            evaluate_btn_competency.click(
                fn=evaluate_competency,
                inputs=upload_competency,
                outputs=output_competency
            )

if __name__ == "__main__":
    demo.launch(share=True)