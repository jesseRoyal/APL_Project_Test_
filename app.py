from flask import Flask, request, jsonify
from lexer import lexer
from parser_1 import parser as main_parser
from semantic_analyzer import SemanticAnalyzer
from interpreter import Interpreter
from llm_interface import LLMInterface

app = Flask(__name__)

@app.route('/evaluate', methods=['POST'])
def evaluate():
    """
    API endpoint to evaluate Lambda Calculus expressions.

    Args:
        data (dict): JSON object containing the source code and optional API key.

    Returns:
        dict: JSON object containing the evaluation result and optional
              transformation info.
    """
    # Parse the request data
    data = request.json
    source_code = data['source_code']
    api_key = data.get('api_key')

    # Lex the source code
    lexer.input(source_code)
    tokens = list(lexer)
    # Print tokens (debugging)
    print("Tokens:", tokens) 

    # Parse the source code
    ast = main_parser.parse(source_code)
    # Print the abstract syntax tree (debugging)
    print("AST:", ast) 

    # If parsing fails, return an error response
    if ast is None:
        return jsonify(error="Error: Failed to parse the source code."), 400

    # Semantic analysis
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)

    # Evaluate the AST
    interpreter = Interpreter(ast)
    result = interpreter.run()

    # Construct the final result
    final_result = {"result": result}

    # If API key is provided, get transformation info from LLM
    if api_key:
        llm = LLMInterface(api_key)
        transformation_info = llm.get_transformation_info(source_code)
        final_result["transformation_info"] = transformation_info

    return jsonify(result=final_result)

if __name__ == '__main__':
    app.run(debug=True)
