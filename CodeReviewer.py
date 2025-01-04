import ast
import pycodestyle


class CodeReviewer:
    def __init__(self):
        self.feedback = []

    def analyze_python_code(self, code):
        try:
            # Parse the Python code into an Abstract Syntax Tree (AST)
            tree = ast.parse(code)
        except SyntaxError as e:
            self.feedback.append(f"Syntax Error: {e}")
            return

        # Perform checks
        self._check_indentation(tree)
        self._check_undefined_vars(tree)
        self._check_code_style(code)
        self._check_comments(code)

    def _check_indentation(self, tree):
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if node.body and not isinstance(node.body[0], ast.Expr):
                    self.feedback.append(
                        f"Function '{node.name}' should have a docstring or 'pass' statement."
                    )
            elif isinstance(node, (ast.For, ast.While, ast.If, ast.With)):
                if node.body and not isinstance(node.body[0], ast.Expr):
                    self.feedback.append(
                        f"Indentation Error: Missing 'pass' statement for '{node.__class__.__name__}'."
                    )

    def _check_undefined_vars(self, tree):
        defined_vars = set()
        used_vars = set()

        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                if isinstance(node.ctx, ast.Store):
                    defined_vars.add(node.id)
                elif isinstance(node.ctx, ast.Load):
                    used_vars.add(node.id)

        undefined_vars = used_vars - defined_vars
        for var in undefined_vars:
            self.feedback.append(f"Variable '{var}' is used but not defined.")

    def _check_code_style(self, code):
        style_guide = pycodestyle.StyleGuide(quiet=True)
        result = style_guide.check_code(code)
        if result.total_errors > 0:
            self.feedback.append(
                f"Code style issues found: {result.total_errors} issue(s). Please fix them."
            )

    def _check_comments(self, code):
        lines = code.split('\n')
        for i, line in enumerate(lines):
            if line.strip().startswith('#'):
                # Check for empty comments or comments without space after '#'
                if len(line.strip()) == 1 or line.strip()[1] != ' ':
                    self.feedback.append(
                        f"Improve comment style in line {i + 1}: '{line.strip()}'"
                    )

    def get_feedback(self):
        return self.feedback


if __name__ == "__main__":
    # Example Python code to analyze
    python_code = """
    def add(a, b):
        #Add two numbers
        result = a + b
        print(result)
    """

    code_reviewer = CodeReviewer()
    code_reviewer.analyze_python_code(python_code)

    feedback = code_reviewer.get_feedback()

    if feedback:
        print("Code Review Feedback:")
        for msg in feedback:
            print(f"- {msg}")
    else:
        print("No coding issues found. Code looks great!")
