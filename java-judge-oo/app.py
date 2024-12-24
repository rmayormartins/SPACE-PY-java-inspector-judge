import javalang
from typing import Dict, List, Tuple
from dataclasses import dataclass
import gradio as gr

@dataclass
class RubricCriterion:
    name: str
    description: str
    weight: int
    is_essential: bool
    levels: Dict[str, Dict[str, float]]

class EnhancedJavaPOOEvaluator:
    """Avaliador POO com rubrica detalhada"""

    def __init__(self):
        self.rubric = {
            "classes_objects": RubricCriterion(
                name="Classes e Objetos",
                description="Avalia a definição e uso de classes e objetos",
                weight=20,
                is_essential=True,
                levels={
                    "Fraco": {"threshold": 0, "description": "Nenhuma ou poucas classes/objetos"},
                    "Regular": {"threshold": 10, "description": "Classes básicas sem organização clara"},
                    "Bom": {"threshold": 15, "description": "Classes bem estruturadas e objetos adequados"},
                    "Excelente": {"threshold": 20, "description": "Excelente uso de classes e objetos"}
                }
            ),
            "methods": RubricCriterion(
                name="Métodos",
                description="Avalia métodos e sua organização",
                weight=20,
                is_essential=True,
                levels={
                    "Fraco": {"threshold": 0, "description": "Poucos métodos ou mal estruturados"},
                    "Regular": {"threshold": 10, "description": "Métodos básicos sem sobrecarga"},
                    "Bom": {"threshold": 15, "description": "Boa organização e alguns métodos sobrecarregados"},
                    "Excelente": {"threshold": 20, "description": "Excelente organização e uso de sobrecarga"}
                }
            ),
            "attributes": RubricCriterion(
                name="Atributos",
                description="Avalia atributos e sua organização",
                weight=20,
                is_essential=True,
                levels={
                    "Fraco": {"threshold": 0, "description": "Poucos atributos ou mal organizados"},
                    "Regular": {"threshold": 10, "description": "Atributos básicos sem encapsulamento"},
                    "Bom": {"threshold": 15, "description": "Boa organização de atributos"},
                    "Excelente": {"threshold": 20, "description": "Excelente organização e encapsulamento"}
                }
            ),
            "encapsulation": RubricCriterion(
                name="Encapsulamento",
                description="Avalia uso de modificadores e getters/setters",
                weight=10,
                is_essential=False,
                levels={
                    "Ausente": {"threshold": 0, "description": "Sem encapsulamento"},
                    "Parcial": {"threshold": 5, "description": "Encapsulamento básico"},
                    "Bom": {"threshold": 7.5, "description": "Bom uso de encapsulamento"},
                    "Excelente": {"threshold": 10, "description": "Encapsulamento completo e correto"}
                }
            ),
            "inheritance": RubricCriterion(
                name="Herança",
                description="Avalia uso de herança",
                weight=10,
                is_essential=False,
                levels={
                    "Ausente": {"threshold": 0, "description": "Sem uso de herança"},
                    "Parcial": {"threshold": 5, "description": "Uso básico de herança"},
                    "Bom": {"threshold": 7.5, "description": "Bom uso de herança"},
                    "Excelente": {"threshold": 10, "description": "Uso avançado e apropriado de herança"}
                }
            ),
            "polymorphism": RubricCriterion(
                name="Polimorfismo",
                description="Avalia uso de polimorfismo",
                weight=10,
                is_essential=False,
                levels={
                    "Ausente": {"threshold": 0, "description": "Sem uso de polimorfismo"},
                    "Parcial": {"threshold": 5, "description": "Uso básico de sobrescrita"},
                    "Bom": {"threshold": 7.5, "description": "Bom uso de polimorfismo"},
                    "Excelente": {"threshold": 10, "description": "Uso avançado de polimorfismo"}
                }
            ),
            "abstraction": RubricCriterion(
                name="Abstração",
                description="Avalia uso de abstrações",
                weight=10,
                is_essential=False,
                levels={
                    "Ausente": {"threshold": 0, "description": "Sem uso de abstração"},
                    "Parcial": {"threshold": 5, "description": "Uso básico de interfaces/classes abstratas"},
                    "Bom": {"threshold": 7.5, "description": "Bom uso de abstração"},
                    "Excelente": {"threshold": 10, "description": "Uso completo de abstrações"}
                }
            )
        }

    def evaluate_criterion(self, criterion: RubricCriterion, analysis_result: Dict) -> Tuple[float, str, str]:
        """Avalia um critério específico baseado nos resultados da análise"""
        score = 0
        level = list(criterion.levels.keys())[0]  # Nível mais baixo por padrão
        feedback = []

        if criterion.name == "Classes e Objetos":
            num_classes = len(analysis_result.get("classes", []))
            num_objects = len(analysis_result.get("objects", []))

            if num_classes >= 3 and num_objects >= 5:
                score = criterion.weight
                level = "Excelente"
            elif num_classes >= 2 and num_objects >= 3:
                score = criterion.weight * 0.75
                level = "Bom"
            elif num_classes >= 1 and num_objects >= 1:
                score = criterion.weight * 0.5
                level = "Regular"

            feedback.append(f"Encontradas {num_classes} classes e {num_objects} objetos")

        elif criterion.name == "Métodos":
            methods = analysis_result.get("methods", [])
            method_names = [m.name for m in methods]
            overloaded = len([name for name in method_names if method_names.count(name) > 1])

            if len(methods) >= 5 and overloaded >= 2:
                score = criterion.weight
                level = "Excelente"
            elif len(methods) >= 3 and overloaded >= 1:
                score = criterion.weight * 0.75
                level = "Bom"
            elif len(methods) >= 1:
                score = criterion.weight * 0.5
                level = "Regular"

            feedback.append(f"Encontrados {len(methods)} métodos, sendo {overloaded} sobrecarregados")

        elif criterion.name == "Atributos":
            attributes = analysis_result.get("attributes", [])
            num_private = analysis_result["encapsulation"]["private_count"]

            if len(attributes) >= 5 and num_private >= 3:
                score = criterion.weight
                level = "Excelente"
            elif len(attributes) >= 3 and num_private >= 1:
                score = criterion.weight * 0.75
                level = "Bom"
            elif len(attributes) >= 1:
                score = criterion.weight * 0.5
                level = "Regular"

            feedback.append(f"Encontrados {len(attributes)} atributos, sendo {num_private} privados")

        elif criterion.name == "Encapsulamento":
            num_private = analysis_result["encapsulation"]["private_count"]
            num_getters_setters = analysis_result["encapsulation"]["getters_setters"]

            if num_private >= 3 and num_getters_setters >= 4:
                score = criterion.weight
                level = "Excelente"
            elif num_private >= 2 and num_getters_setters >= 3:
                score = criterion.weight * 0.75
                level = "Bom"
            elif num_private >= 1 and num_getters_setters >= 2:
                score = criterion.weight * 0.5
                level = "Parcial"

            feedback.append(f"Encontrados {num_private} atributos privados e {num_getters_setters} getters/setters")

        elif criterion.name == "Herança":
            subclasses = analysis_result["inheritance"]["subclasses"]

            if len(subclasses) >= 3:
                score = criterion.weight
                level = "Excelente"
            elif len(subclasses) >= 2:
                score = criterion.weight * 0.75
                level = "Bom"
            elif len(subclasses) >= 1:
                score = criterion.weight * 0.5
                level = "Parcial"

            feedback.append(f"Encontradas {len(subclasses)} classes que usam herança")

        elif criterion.name == "Polimorfismo":
            overridden = len(analysis_result["polymorphism"]["overridden_methods"])

            if overridden >= 3:
                score = criterion.weight
                level = "Excelente"
            elif overridden >= 2:
                score = criterion.weight * 0.75
                level = "Bom"
            elif overridden >= 1:
                score = criterion.weight * 0.5
                level = "Parcial"

            feedback.append(f"Encontrados {overridden} métodos sobrescritos")

        elif criterion.name == "Abstração":
            abstract_classes = len(analysis_result["abstraction"]["abstract_classes"])
            interfaces = len(analysis_result["abstraction"]["interfaces"])

            if abstract_classes >= 1 and interfaces >= 1:
                score = criterion.weight
                level = "Excelente"
            elif abstract_classes >= 1 and interfaces >= 0:
                score = criterion.weight * 0.75
                level = "Bom"
            elif abstract_classes >= 1 or interfaces >= 1:
                score = criterion.weight * 0.5
                level = "Parcial"

            feedback.append(f"Encontradas {abstract_classes} classes abstratas e {interfaces} interfaces")

        return score, level, ". ".join(feedback)

    def analyze_code(self, code: str) -> Dict:
        """Analisa o código Java e retorna dados brutos"""
        analysis = {
            "classes": [],
            "objects": [],
            "methods": [],
            "attributes": [],
            "encapsulation": {"private_count": 0, "getters_setters": 0},
            "inheritance": {"subclasses": []},
            "polymorphism": {"overridden_methods": []},
            "abstraction": {"abstract_classes": [], "interfaces": []}
        }

        try:
            tree = javalang.parse.parse(code)

            # Análise de classes e objetos
            analysis["classes"] = [node for _, node in tree.filter(javalang.tree.ClassDeclaration)]
            analysis["objects"] = [node for _, node in tree.filter(javalang.tree.VariableDeclarator)
                                 if isinstance(node.initializer, javalang.tree.ClassCreator)]

            # Análise de métodos
            analysis["methods"] = [node for _, node in tree.filter(javalang.tree.MethodDeclaration)]

            # Análise de atributos e encapsulamento
            fields = [node for _, node in tree.filter(javalang.tree.FieldDeclaration)]
            analysis["attributes"] = fields
            analysis["encapsulation"]["private_count"] = sum(1 for field in fields
                                                           if "private" in field.modifiers)

            # Contagem de getters e setters
            methods = analysis["methods"]
            getters_setters = sum(1 for method in methods
                                if method.name.startswith('get') or method.name.startswith('set'))
            analysis["encapsulation"]["getters_setters"] = getters_setters

            # Análise de herança
            analysis["inheritance"]["subclasses"] = [cls for cls in analysis["classes"]
                                                   if cls.extends is not None]

            # Análise de polimorfismo
            analysis["polymorphism"]["overridden_methods"] = [method for method in methods
                                                            if any(ann.name == "Override"
                                                                  for ann in (method.annotations or []))]

            # Análise de abstração
            analysis["abstraction"]["abstract_classes"] = [cls for cls in analysis["classes"]
                                                         if "abstract" in cls.modifiers]
            analysis["abstraction"]["interfaces"] = [node for _, node in tree.filter(javalang.tree.InterfaceDeclaration)]

        except Exception as e:
            print(f"Erro na análise: {str(e)}")

        return analysis

    def evaluate_code(self, code: str) -> Dict:
        """Avalia o código Java usando a rubrica detalhada"""
        analysis = self.analyze_code(code)
        evaluation = {
            "scores": {},
            "levels": {},
            "feedback": {},
            "summary": {
                "essential_score": 0,
                "bonus_score": 0,
                "total_score": 0
            }
        }

        # Avalia cada critério
        for criterion_key, criterion in self.rubric.items():
            score, level, feedback = self.evaluate_criterion(criterion, analysis)

            evaluation["scores"][criterion_key] = score
            evaluation["levels"][criterion_key] = level
            evaluation["feedback"][criterion_key] = feedback

            if criterion.is_essential:
                evaluation["summary"]["essential_score"] += score
            else:
                evaluation["summary"]["bonus_score"] += score

        evaluation["summary"]["total_score"] = min(100,
            evaluation["summary"]["essential_score"] +
            evaluation["summary"]["bonus_score"])

        # Determina nível geral
        if evaluation["summary"]["total_score"] >= 90:
            evaluation["summary"]["proficiency"] = "Excelente"
        elif evaluation["summary"]["total_score"] >= 75:
            evaluation["summary"]["proficiency"] = "Bom"
        elif evaluation["summary"]["total_score"] >= 60:
            evaluation["summary"]["proficiency"] = "Satisfatório"
        else:
            evaluation["summary"]["proficiency"] = "Necessita Melhorias"

        return evaluation

# Interface Gradio
with gr.Blocks(title="Avaliador de POO em Java") as demo:
    gr.Markdown("# Avaliador de POO em Java")
    gr.Markdown("""
    Este avaliador analisa código Java em relação aos princípios de Programação Orientada a Objetos.

    Critérios avaliados:
   
    """)
    # Links usando caminho completo do Hugging Face
    gr.HTML(f"""
    <h3>
        <a href="https://huggingface.co/spaces/rmayormartins/java-judge-oo/resolve/main/assets/rubric.pdf" target="_blank">📄 Visualizar Rubrica PDF</a>
    </h3>
    <h3>
        <a href="https://huggingface.co/spaces/rmayormartins/java-judge-oo/resolve/main/assets/rubric_table.PNG" target="_blank">📊 Visualizar Tabela da Rubrica</a>
    </h3>
    """)

    upload = gr.File(label="Carregue arquivos Java para avaliação", file_types=[".java"], file_count="multiple")
    evaluate_button = gr.Button("Avaliar Código")
    output = gr.Textbox(label="Resultado da Avaliação", lines=25)

    def evaluate_code_files(files) -> str:
        """Função para avaliar múltiplos arquivos Java"""
        evaluator = EnhancedJavaPOOEvaluator()
        results = []

        for file in files:
            with open(file.name, 'r', encoding='utf-8') as f:
                code = f.read()
            evaluation = evaluator.evaluate_code(code)

            # Formatar resultado por arquivo
            result = f"\n{'='*50}\nAvaliação do arquivo: {file.name}\n{'='*50}\n\n"

            # Pontuação e nível geral
            result += f"Pontuação Total: {evaluation['summary']['total_score']:.1f}/100\n"
            result += f"Nível de Proficiência: {evaluation['summary']['proficiency']}\n"
            result += f"Pontuação Essencial: {evaluation['summary']['essential_score']:.1f}/60\n"
            result += f"Pontuação Bônus: {evaluation['summary']['bonus_score']:.1f}/40\n\n"

            # Detalhamento por critério
            result += "Avaliação Detalhada por Critério:\n"
            result += "-" * 30 + "\n\n"

            for criterion_key, criterion in evaluator.rubric.items():
                result += f"• {criterion.name}:\n"
                result += f"  Nível: {evaluation['levels'][criterion_key]}\n"
                result += f"  Pontuação: {evaluation['scores'][criterion_key]:.1f}/{criterion.weight}\n"
                if evaluation['feedback'][criterion_key]:
                    result += f"  Feedback: {evaluation['feedback'][criterion_key]}\n"
                result += "\n"

            results.append(result)

        return "\n".join(results)

    evaluate_button.click(fn=evaluate_code_files, inputs=upload, outputs=output)

if __name__ == "__main__":
    demo.launch(debug=True)
