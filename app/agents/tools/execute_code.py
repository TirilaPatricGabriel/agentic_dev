from langchain_core.tools import tool
from langchain_experimental.utilities import PythonREPL

@tool
def execute_code(code: str):
    """Execute Python code and return the result. Use this to run calculations, data processing, or logic."""
    repl = PythonREPL()
    try:
        result = repl.run(code)
        return f"Execution Result:\n{result}"
    except Exception as e:
        return f"Error executing code: {repr(e)}"
        