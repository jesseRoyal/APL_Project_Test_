class Interpreter:
    def __init__(self, ast):
        self.ast = ast  # Initialize the interpreter with the AST

    def run(self):
        print("Starting interpretation...")
        result = self.evaluate(self.ast)  # Start evaluating the AST
        print(f"Final result: {result}")

    def evaluate(self, node, env=None):
        if env is None:
            env = {}  # Initialize the environment if not provided

        if isinstance(node, tuple):
            if node[0] == 'var':
                return env.get(node[1], node)  # Return variable from environment or as is
            elif node[0] == 'lambda':
                return node  # Return lambda abstraction as is
            elif node[0] == 'apply':
                func = self.evaluate(node[1], env)  # Evaluate the function part
                arg = self.evaluate(node[2], env)  # Evaluate the argument part
                if func[0] == 'lambda':
                    _, var, body = func
                    new_env = env.copy()
                    new_env[var] = arg  # Add the argument to the environment
                    return self.evaluate(self.substitute(body, var, arg), new_env)  # Substitute and evaluate
                else:
                    return ('apply', func, arg)  # Return application as is
        else:
            return node  # Return variable as is

    def substitute(self, body, var, value):
        if isinstance(body, tuple):
            if body[0] == 'var':
                return value if body[1] == var else body  # Substitute variable
            elif body[0] == 'lambda':
                return ('lambda', body[1], self.substitute(body[2], var, value))  # Substitute in lambda body
            elif body[0] == 'apply':
                return ('apply', self.substitute(body[1], var, value), self.substitute(body[2], var, value))  # Substitute in application
        return body  # Return body as is

    def beta_reduce(self, expr):
        if expr[0] == 'apply' and expr[1][0] == 'lambda':
            _, var, body = expr[1]
            value = expr[2]
            reduced_expr = self.substitute(body, var, value)  # Perform beta reduction
            print(f"Beta reduction: ({expr[1]} {expr[2]}) -> {reduced_expr}")
            return reduced_expr
        return expr  # Return expression as is

    def eta_reduce(self, expr):
        if expr[0] == 'lambda' and expr[2][0] == 'apply' and expr[2][2][0] == 'var' and expr[2][2][1] == expr[1]:
            reduced_expr = expr[2][1]  # Perform eta reduction
            print(f"Eta reduction: λ{expr[1]}.{expr[2]} -> {reduced_expr}")
            return reduced_expr
        return expr  # Return expression as is

    def alpha_convert(self, expr, new_var):
        if expr[0] == 'lambda':
            _, var, body = expr
            converted_expr = ('lambda', new_var, self.substitute(body, var, ('var', new_var)))  # Perform alpha conversion
            print(f"Alpha conversion: λ{var}.{body} -> λ{new_var}.{converted_expr[2]}")
            return converted_expr
        return expr  # Return expression as is

# Example usage
if __name__ == "__main__":
    sample_ast = ('apply', ('lambda', 'x', ('var', 'x')), ('var', 'y'))
    interpreter = Interpreter(sample_ast)
    interpreter.run()
