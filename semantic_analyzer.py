class SemanticAnalyzer:
    def analyze(self, node):
        if node is None:
            print("Error: Received None node for analysis.")
            return

        print(f"Analyzing node: {node}")  # Debugging: Print node
        if isinstance(node, tuple):
            if node[0] == 'lambda':
                _, var, body = node
                self.analyze(body)
            elif node[0] == 'apply':
                _, func, arg = node
                self.analyze(func)
                self.analyze(arg)
        elif isinstance(node, str):
            # Process variable node
            pass
        else:
            print("Error: Invalid node type.")

# Example usage
if __name__ == "__main__":
    analyzer = SemanticAnalyzer()
    sample_ast = ('lambda', 'x', ('apply', 'x', 'y'))
    analyzer.analyze(sample_ast)
