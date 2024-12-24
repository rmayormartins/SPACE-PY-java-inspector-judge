import javalang
from typing import Dict, List, Tuple
from dataclasses import dataclass
import re

@dataclass
class RubricCriterion:
    name: str
    description: str
    weight: int
    is_essential: bool
    levels: Dict[str, Dict[str, float]]

class EnhancedJavaStructuralEvaluator:
    """Avaliador baseado em estruturas usadas"""
    def __init__(self):
        self.rubric = {
            "declarations": RubricCriterion(
                name="Declarações",
                description="Uso de tipos e declarações",
                weight=25,
                is_essential=True,
                levels={
                    "Fraco": {"threshold": 0, "description": "Uso mínimo/incorreto"},
                    "Regular": {"threshold": 10, "description": "1-2 tipos primitivos, 1-2 variáveis"},
                    "Bom": {"threshold": 15, "description": "3 tipos primitivos, 3-4 variáveis"},
                    "Excelente": {"threshold": 20, "description": "≥4 tipos primitivos, ≥5 variáveis"}
                }
            ),
            "control_structures": RubricCriterion(
                name="Estruturas de Controle",
                description="Controle de fluxo do programa",
                weight=25,
                is_essential=True,
                levels={
                    "Fraco": {"threshold": 0, "description": "Uso mínimo/incorreto"},
                    "Regular": {"threshold": 10, "description": "1 tipo, uso básico"},
                    "Bom": {"threshold": 15, "description": "2 tipos diferentes, uso correto"},
                    "Excelente": {"threshold": 20, "description": "≥3 tipos diferentes, uso apropriado"}
                }
            ),
            "operators": RubricCriterion(
                name="Operadores",
                description="Operações e expressões",
                weight=25,
                is_essential=True,
                levels={
                    "Fraco": {"threshold": 0, "description": "Uso mínimo/incorreto"},
                    "Regular": {"threshold": 10, "description": "1-2 operadores"},
                    "Bom": {"threshold": 15, "description": "3-4 operadores"},
                    "Excelente": {"threshold": 20, "description": "≥5 operadores diferentes"}
                }
            ),
            "io_strings": RubricCriterion(
                name="I/O e Strings",
                description="Entrada/saída e manipulação de texto",
                weight=25,
                is_essential=True,
                levels={
                    "Fraco": {"threshold": 0, "description": "Uso mínimo/incorreto"},
                    "Regular": {"threshold": 10, "description": "E/S simples"},
                    "Bom": {"threshold": 15, "description": "E/S moderada, manipulação básica"},
                    "Excelente": {"threshold": 20, "description": "E/S complexa, manipulação avançada"}
                }
            )
        }

    def evaluate_declarations(self, code: str) -> Tuple[float, str, List[str]]:
        """Avalia declarações e tipos"""
        score = 0
        level = "Fraco"
        feedback = []

        try:
            tree = javalang.parse.parse(code)
            
            # Análise de tipos primitivos
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
            declarations = [node for _, node in tree.filter(javalang.tree.LocalVariableDeclaration)]
            for decl in declarations:
                type_name = decl.type.name
                used_types.add(type_name)

            num_types = len(used_types)
            num_vars = len(declarations)
            has_constants = any('final' in node.modifiers for _, node in tree.filter(javalang.tree.FieldDeclaration))

            # Determinar nível
            if num_types >= 4 and num_vars >= 5 and has_constants:
                score = 25
                level = "Excelente"
            elif num_types >= 3 and num_vars >= 3:
                score = 15
                level = "Bom"
            elif num_types >= 1 or num_vars >= 1:
                score = 10
                level = "Regular"

            feedback.append(f"✓ {num_types} tipos primitivos diferentes utilizados")
            feedback.append(f"✓ {num_vars} variáveis declaradas")
            if has_constants:
                feedback.append("✓ Uso adequado de constantes (final)")

        except Exception as e:
            feedback.append("⚠ Erro na análise de declarações")

        return score, level, feedback

    def evaluate_control_structures(self, code: str) -> Tuple[float, str, List[str]]:
        """Avalia estruturas de controle"""
        score = 0
        level = "Fraco"
        feedback = []

        try:
            tree = javalang.parse.parse(code)
            
            structures = {
                'if': len(list(tree.filter(javalang.tree.IfStatement))),
                'switch': len(list(tree.filter(javalang.tree.SwitchStatement))),
                'for': len(list(tree.filter(javalang.tree.ForStatement))),
                'while': len(list(tree.filter(javalang.tree.WhileStatement))),
                'do_while': len(list(tree.filter(javalang.tree.DoStatement)))
            }

            num_different_structures = sum(1 for count in structures.values() if count > 0)
            total_structures = sum(structures.values())

            # Determinar nível
            if num_different_structures >= 3 and total_structures >= 4:
                score = 25
                level = "Excelente"
            elif num_different_structures >= 2 and total_structures >= 2:
                score = 15
                level = "Bom"
            elif num_different_structures >= 1:
                score = 10
                level = "Regular"

            for struct, count in structures.items():
                if count > 0:
                    feedback.append(f"✓ {count} estrutura(s) {struct}")

        except Exception as e:
            feedback.append("⚠ Erro na análise de estruturas de controle")

        return score, level, feedback

    def evaluate_operators(self, code: str) -> Tuple[float, str, List[str]]:
        """Avalia operadores"""
        score = 0
        level = "Fraco"
        feedback = []

        try:
            operators = {
                'arithmetic': ['+', '-', '*', '/', '%'],
                'comparison': ['==', '!=', '>', '<', '>=', '<='],
                'logical': ['&&', '||', '!'],
                'assignment': ['+=', '-=', '*=', '/=']
            }

            used_operators = set()
            for category, ops in operators.items():
                for op in ops:
                    if op in code:
                        used_operators.add(op)
                        feedback.append(f"✓ Uso do operador {op}")

            num_operators = len(used_operators)

            # Determinar nível
            if num_operators >= 5:
                score = 25
                level = "Excelente"
            elif num_operators >= 3:
                score = 15
                level = "Bom"
            elif num_operators >= 1:
                score = 10
                level = "Regular"

        except Exception as e:
            feedback.append("⚠ Erro na análise de operadores")

        return score, level, feedback

    def evaluate_io_strings(self, code: str) -> Tuple[float, str, List[str]]:
        """Avalia entrada/saída e strings"""
        score = 0
        level = "Fraco"
        feedback = []

        try:
            features = {
                'output': 'System.out.print' in code,
                'input': 'Scanner' in code,
                'concatenation': '+' in code and '"' in code,
                'string_methods': False
            }

            # Verificar métodos de String
            string_methods = ['concat', 'substring', 'length', 'equals', 'compareTo']
            methods_used = [method for method in string_methods if f'.{method}(' in code]
            features['string_methods'] = len(methods_used) > 0

            # Contar recursos utilizados
            num_features = sum(1 for used in features.values() if used)

            # Determinar nível
            if num_features >= 3 and features['string_methods']:
                score = 25
                level = "Excelente"
            elif num_features >= 2:
                score = 15
                level = "Bom"
            elif num_features >= 1:
                score = 10
                level = "Regular"

            if features['output']:
                feedback.append("✓ Uso de saída (System.out)")
            if features['input']:
                feedback.append("✓ Uso de entrada (Scanner)")
            if features['concatenation']:
                feedback.append("✓ Concatenação de strings")
            if methods_used:
                feedback.append(f"✓ Uso de {len(methods_used)} métodos de String")

        except Exception as e:
            feedback.append("⚠ Erro na análise de I/O e strings")

        return score, level, feedback

    def evaluate_code(self, code: str) -> Dict:
        """Avalia o código Java usando todos os critérios"""
        evaluation = {
            "scores": {},
            "levels": {},
            "feedback": {},
            "summary": {
                "total_score": 0,
                "proficiency": ""
            }
        }

        # Avaliar cada critério
        criteria_evaluations = {
            "declarations": self.evaluate_declarations(code),
            "control_structures": self.evaluate_control_structures(code),
            "operators": self.evaluate_operators(code),
            "io_strings": self.evaluate_io_strings(code)
        }

        # Compilar resultados
        for criterion, (score, level, feedback) in criteria_evaluations.items():
            evaluation["scores"][criterion] = score
            evaluation["levels"][criterion] = level
            evaluation["feedback"][criterion] = feedback
            evaluation["summary"]["total_score"] += score

        # Determinar proficiência geral
        total_score = evaluation["summary"]["total_score"]
        if total_score >= 90:
            evaluation["summary"]["proficiency"] = "Excelente"
        elif total_score >= 75:
            evaluation["summary"]["proficiency"] = "Bom"
        elif total_score >= 60:
            evaluation["summary"]["proficiency"] = "Satisfatório"
        else:
            evaluation["summary"]["proficiency"] = "Necessita Melhorias"

        return evaluation

class EnhancedCompetencyEvaluator:
    """Avaliador baseado em competências"""
    def __init__(self):
        self.rubric = {
            "syntax": RubricCriterion(
                name="Corretude Sintática",
                description="Correção técnica do código",
                weight=50,
                is_essential=True,
                levels={
                    "Fraco": {"threshold": 0, "description": "Muitos erros"},
                    "Regular": {"threshold": 20, "description": "Código funcional, alguns erros"},
                    "Bom": {"threshold": 30, "description": "Código correto, erros menores"},
                    "Excelente": {"threshold": 40, "description": "Código exemplar, sem erros"}
                }
            ),
            "competencies": RubricCriterion(
                name="Competências Práticas",
                description="Qualidade da implementação",
                weight=50,
                is_essential=True,
                levels={
                    "Fraco": {"threshold": 0, "description": "Implementação pobre"},
                    "Regular": {"threshold": 20, "description": "Implementação básica"},
                    "Bom": {"threshold": 30, "description": "Boa implementação"},
                    "Excelente": {"threshold": 40, "description": "Implementação sofisticada"}
                }
            )
        }

    def evaluate_syntax(self, code: str) -> Tuple[float, str, List[str]]:
        """Avalia corretude sintática"""
        score = 0
        level = "Fraco"
        feedback = []

        try:
            tree = javalang.parse.parse(code)
            
            # 1. Estrutura básica (10 pts)
            has_class = 'class' in code
            has_main = 'public static void main' in code
            if has_class and has_main:
                score += 10
                feedback.append("✓ Estrutura básica correta (classe e main)")

            # 2. Declarações (10 pts)
            declarations = list(tree.filter(javalang.tree.LocalVariableDeclaration))
            if declarations:
                score += 10
                feedback.append(f"✓ {len(declarations)} declarações sintáticamente corretas")

            # 3. Blocos e estruturas (10 pts)
            if code.count('{') == code.count('}') and code.count('{') > 0:
                score += 10
                feedback.append("✓ Blocos corretamente delimitados")

            # 4. Expressões (10 pts)
            expressions = list(tree.filter(javalang.tree.BinaryOperation))
            if expressions:
                score += 10
                feedback.append("✓ Expressões bem formadas")

            # 5. Pontuação e formatação (10 pts)
            lines = code.split('\n')
            well_formatted = all(line.strip().endswith(';') or 
                               line.strip().endswith('{') or 
                               line.strip().endswith('}') or 
                               line.strip() == "" or 
                               line.strip().startswith('//') 
                               for line in lines if line.strip())
            if well_formatted:
                score += 10
                feedback.append("✓ Código bem formatado e pontuado")

            # Determinar nível
            if score >= 40:
                level = "Excelente"
            elif score >= 30:
                level = "Bom"
            elif score >= 20:
                level = "Regular"

        except Exception as e:
            feedback.append(f"⚠ Erro de sintaxe: {str(e)}")

        return score, level, feedback

    def evaluate_competencies(self, code: str) -> Tuple[float, str, List[str]]:
        """Avalia competências práticas"""
        score = 0
        level = "Fraco"
        feedback = []

        try:
            tree = javalang.parse.parse(code)

            # 1. Seleção de estruturas (15 pts)
            structures = {
                'if': list(tree.filter(javalang.tree.IfStatement)),
                'for': list(tree.filter(javalang.tree.ForStatement)),
                'while': list(tree.filter(javalang.tree.WhileStatement))
            }
            
            struct_score = 0
            for struct_type, instances in structures.items():
                if instances:
                    struct_score += 5
                    if struct_type == 'for' and any('length' in str(inst) for inst in instances):
                        struct_score += 2
                    elif struct_type == 'while' and any('hasNext' in str(inst) for inst in instances):
                        struct_score += 2
            
            score += min(15, struct_score)
            if struct_score > 0:
                feedback.append(f"✓ Uso apropriado de estruturas de controle")

            # 2. Manipulação de dados (15 pts)
            data_score = 0
            operations = list(tree.filter(javalang.tree.BinaryOperation))
            if operations:
                if any(op.operator in ['*', '/', '+', '-'] for op in operations):
                    data_score += 5
                if any(op.operator in ['>', '<', '>=', '<=', '=='] for op in operations):
                    data_score += 5
                if any('=' in str(op) for op in operations):
                    data_score += 5

            score += min(15, data_score)
            if data_score > 0:
                feedback.append("✓ Manipulação de dados adequada")

            # 3. Clareza e organização (10 pts)
            org_score = 0
            if all(len(decl.declarators[0].name) > 1 for _, decl in tree.filter(javalang.tree.LocalVariableDeclaration)):
                org_score += 5
            
            lines = code.split('\n')
            if any('//' in line or '/*' in line for line in lines):
                org_score += 5

            score += min(10, org_score)
            if org_score > 0:
                feedback.append("✓ Código bem organizado e documentado")

            # 4. Resolução do problema (10 pts)
            if 'Scanner' in code and 'System.out' in code and operations:
                score += 10
                feedback.append("✓ Solução completa com entrada, processamento e saída")

            # Determinar nível
            if score >= 40:
                level = "Excelente"
            elif score >= 30:
                level = "Bom"
            elif score >= 20:
                level = "Regular"

        except Exception as e:
            feedback.append(f"⚠ Erro na análise de competências: {str(e)}")

        return score, level, feedback

    def evaluate_code(self, code: str) -> Dict:
        """Avalia o código Java usando todos os critérios"""
        evaluation = {
            "scores": {},
            "levels": {},
            "feedback": {},
            "summary": {
                "total_score": 0,
                "proficiency": ""
            }
        }

        # Avaliar cada critério
        criteria_evaluations = {
            "syntax": self.evaluate_syntax(code),
            "competencies": self.evaluate_competencies(code)
        }

        # Compilar resultados
        for criterion, (score, level, feedback) in criteria_evaluations.items():
            evaluation["scores"][criterion] = score
            evaluation["levels"][criterion] = level
            evaluation["feedback"][criterion] = feedback
            evaluation["summary"]["total_score"] += score

        # Determinar proficiência geral
        total_score = evaluation["summary"]["total_score"]
        if total_score >= 90:
            evaluation["summary"]["proficiency"] = "Excelente"
        elif total_score >= 75:
            evaluation["summary"]["proficiency"] = "Bom"
        elif total_score >= 60:
            evaluation["summary"]["proficiency"] = "Satisfatório"
        else:
            evaluation["summary"]["proficiency"] = "Necessita Melhorias"

        return evaluation

# Interface Gradio
import gradio as gr

def process_java_files(files, evaluation_type: str) -> str:
    """Avalia arquivos Java usando o avaliador especificado"""
    results = []

    try:
        # Criar avaliador apropriado
        if evaluation_type == "structural":
            evaluator = EnhancedJavaStructuralEvaluator()
        else:
            evaluator = EnhancedCompetencyEvaluator()

        # Processar cada arquivo
        for file in files:
            with open(file.name, 'r', encoding='utf-8') as f:
                code = f.read()

            # Avaliar código
            evaluation = evaluator.evaluate_code(code)

            # Formatar resultado
            result = f"\n{'='*50}\n"
            result += f"Avaliação do arquivo: {file.name}\n"
            result += f"{'='*50}\n\n"

            # Pontuação e nível
            result += f"Pontuação Total: {evaluation['summary']['total_score']:.1f}/100\n"
            result += f"Nível de Proficiência: {evaluation['summary']['proficiency']}\n\n"

            # Detalhamento por critério
            result += "Avaliação Detalhada por Critério:\n"
            result += "-" * 30 + "\n\n"

            for criterion in evaluation["scores"].keys():
                result += f"• {criterion.title()}:\n"
                result += f"  Nível: {evaluation['levels'][criterion]}\n"
                result += f"  Pontuação: {evaluation['scores'][criterion]:.1f}\n"
                result += "  Feedback:\n"
                for fb in evaluation['feedback'][criterion]:
                    result += f"    - {fb}\n"
                result += "\n"

            results.append(result)

        return "\n".join(results)
    except Exception as e:
        return f"Erro ao processar arquivos: {str(e)}"

# Interface Gradio com abas 
with gr.Blocks(title="Java-Judge: Avaliador de Sintaxe e Competencia Java") as demo:
    gr.Markdown("# Java-Judge: Avaliador de Sintaxe e Competencia Java")
    # 
    gr.HTML("""
    <p>Java-Judge: Avaliador de Sintaxe e Competências em Java</p>
    <p>Ramon Mayor Martins: <a href="https://rmayormartins.github.io/" target="_blank">Website</a> | 
    <a href="https://huggingface.co/rmayormartins" target="_blank">Spaces</a></p>
    """)
    gr.Markdown("""
    Este avaliador analisa código Java em relação aos princípios de Programação Orientada a Objetos.

    Critérios avaliados:
   
    """)
    # 
    gr.HTML("""
    <p>
        <a href="https://huggingface.co/spaces/rmayormartins/java-judge-syntax-competencies/blob/main/assets/rubric.pdf" target="_blank">📄 Visualizar Rubrica PDF</a>
    </p>
    <p>
        <a href="https://huggingface.co/spaces/rmayormartins/java-judge-syntax-competencies/blob/main/assets/rubric_table.PNG" target="_blank">📊 Visualizar Tabela da Rubrica</a>
    </p>
    <p>
        <a href="https://hackmd.io/@dc5kbfmvTRSDYhAP5VRHUQ/rk_zua8j3" target="_blank">🖥️ Visualizar Markdown da Rubrica</a>
    </p>
    """)
      
    gr.Markdown("""
    # Avaliador de Código Java
    
    Este avaliador analisa código Java usando duas perspectivas diferentes:
    1. **Avaliação Estrutural**: Foca nos elementos fundamentais da linguagem
    2. **Avaliação por Competências**: Analisa a qualidade técnica e boas práticas
    """)

    with gr.Tabs():
        with gr.Tab("Avaliação Estrutural"):
            upload_structural = gr.File(
                file_count="multiple",
                label="Upload dos arquivos Java",
                file_types=[".java"]
            )
            evaluate_btn_structural = gr.Button("Avaliar Estruturas")
            output_structural = gr.Textbox(
                label="Resultado da Avaliação",
                lines=25
            )
            evaluate_btn_structural.click(
                fn=lambda x: process_java_files(x, "structural"),
                inputs=upload_structural,
                outputs=output_structural
            )

        with gr.Tab("Avaliação por Competências"):
            upload_competency = gr.File(
                file_count="multiple",
                label="Upload dos arquivos Java",
                file_types=[".java"]
            )
            evaluate_btn_competency = gr.Button("Avaliar Competências")
            output_competency = gr.Textbox(
                label="Resultado da Avaliação",
                lines=25
            )
            evaluate_btn_competency.click(
                fn=lambda x: process_java_files(x, "competency"),
                inputs=upload_competency,
                outputs=output_competency
            )

if __name__ == "__main__":
    demo.launch(debug=True)
