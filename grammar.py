from flask import Flask, render_template, request, jsonify
from lark import Lark, Tree, Transformer
from graphviz import Digraph
import os
import time

app = Flask(__name__)

grammar = """
?start: expr

?expr: expr"+"term    -> suma
     | expr"-"term    -> resta
     | term

?term: term"*"factor  -> mul
     | term"/"factor  -> div
     | factor

?factor: "("expr")"   -> grupo
       | NUMBER       -> numero

NUMBER: /[0-9]+(\.[0-9]+)?/

%import common.WS
%ignore WS
"""

parser = Lark(grammar, parser="lalr")

class createTree(Transformer):
    def suma(self, items):
        return items[0] + items[1]

    def resta(self, items):
        return items[0] - items[1]

    def mul(self, items):
        return items[0] * items[1]

    def div(self, items):
        return float(items[0]) / float(items[1])

    def numero(self, items):
        value = float(items[0])  
        return value

    def grupo(self, items):
        return items[0]

evaluator = createTree()

def generateTree(tree):
    dot = Digraph()
    node_count = 0

    def add_nodes_edges(node, parent=None):
        nonlocal node_count
        current_id = str(node_count)
        label = node.data if isinstance(node, Tree) else str(node)
        dot.node(current_id, label)
        if parent is not None:
            dot.edge(parent, current_id)
        node_count += 1

        if isinstance(node, Tree):
            for child in node.children:
                add_nodes_edges(child, current_id)

    add_nodes_edges(tree)
    
    timestamp = str(int(time.time() * 1000))  
    file_name = f"tree_{timestamp}"  
    file_path = os.path.join("static", file_name)
    
    dot.format = "svg"
    dot.render(file_path, cleanup=True)
    
    return f"{file_name}.svg"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calcular", methods=["POST"])
def calcular():
    data = request.json
    expression = data.get("expression")

    try:
        tree = parser.parse(expression)
        print(tree)
        result = evaluator.transform(tree)
        tree_image = generateTree(tree)
        return jsonify({"valid": True, "result": result, "tree": tree_image})
    except Exception as e:
        return jsonify({"valid": False, "error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
