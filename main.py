import argparse
from lexer import lexer
from parser_1 import parser as main_parser
from semantic_analyzer import SemanticAnalyzer
from interpreter import Interpreter
from llm_interface import LLMInterface

def main():
    """
    Entry point of the program.
    Prompts the user for input and performs semantic analysis, interpretation, and optional transformation info retrieval.
    """
    # Parse command line arguments
    arg_parser = argparse.ArgumentParser(description="Lambda Calculus Interpreter")
    arg_parser.add_argument('--api_key', type=str, help="OpenAI API key")
    args = arg_parser.parse_args()

    # Prompt user for input
    source_code = input("Enter your Lambda Calculus code: ")

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
        print("Error: Failed to parse the source code.")
        return

    # Semantic analysis
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)

    # Evaluate the AST
    interpreter = Interpreter(ast)
    interpreter.run()

    # If API key is provided, get transformation info from LLM
    if args.api_key:
        llm = LLMInterface(args.api_key)
        transformation_info = llm.get_transformation_info(source_code)
        print("Transformation Info from LLM:", transformation_info)

if __name__ == "__main__":
    main()
()