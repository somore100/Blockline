"""
C++ Core Blocks for Blockline
Save each block as a separate file in languages/cpp/blocks/

These blocks generate C++ code instead of Python code.
"""

# ============================================================
# languages/cpp/blocks/print.py
# ============================================================
"""
block_id = "print_cpp"
display_name = "Print"
category = "Basic"

params = [
    {"name": "value", "type": "string", "default": "Hello, World!"},
    {"name": "mode", "type": "choice", "default": "text", "choices": ["text", "variable"]}
]

def default_params():
    return {"value": "Hello, World!", "mode": "text"}

def generate_code(params, children, lang="cpp"):
    value = params.get("value", "Hello, World!")
    mode = params.get("mode", "text")
    
    if mode == "variable":
        return f'std::cout << {value} << std::endl;\n'
    else:
        return f'std::cout << "{value}" << std::endl;\n'

block_ui_description = {
    "label": "Print",
    "params": params,
    "category": "Basic",
    "description": "Prints output to console. Use 'text' for strings, 'variable' for variables."
}
"""

# ============================================================
# languages/cpp/blocks/input.py
# ============================================================
"""
block_id = "input_cpp"
display_name = "Input"
category = "Basic"

params = [
    {"name": "variable", "type": "string", "default": "userInput"},
    {"name": "type", "type": "choice", "default": "string", "choices": ["string", "int", "double"]}
]

def default_params():
    return {"variable": "userInput", "type": "string"}

def generate_code(params, children, lang="cpp"):
    var = params.get("variable", "userInput")
    var_type = params.get("type", "string")
    
    if var_type == "string":
        return f'std::string {var};\nstd::getline(std::cin, {var});\n'
    else:
        return f'{var_type} {var};\nstd::cin >> {var};\n'

block_ui_description = {
    "label": "Input",
    "params": params,
    "category": "Basic",
    "description": "Gets user input and stores it in a variable"
}
"""

# ============================================================
# languages/cpp/blocks/assign.py
# ============================================================
"""
block_id = "assign_cpp"
display_name = "Set Variable"
category = "Basic"

params = [
    {"name": "type", "type": "choice", "default": "int", "choices": ["int", "double", "string", "bool", "auto"]},
    {"name": "variable", "type": "string", "default": "x"},
    {"name": "value", "type": "string", "default": "0"}
]

def default_params():
    return {"type": "int", "variable": "x", "value": "0"}

def generate_code(params, children, lang="cpp"):
    var_type = params.get("type", "int")
    var = params.get("variable", "x")
    val = params.get("value", "0")
    
    # Add quotes for string type if not already quoted
    if var_type == "string" and not (val.startswith('"') or val.startswith("'")):
        val = f'"{val}"'
    
    return f'{var_type} {var} = {val};\n'

block_ui_description = {
    "label": "Set Variable",
    "params": params,
    "category": "Basic",
    "description": "Creates and assigns a value to a variable"
}
"""

# ============================================================
# languages/cpp/blocks/comment.py
# ============================================================
"""
block_id = "comment_cpp"
display_name = "Comment"
category = "Basic"

params = [
    {"name": "text", "type": "string", "default": "This is a comment"}
]

def default_params():
    return {"text": "This is a comment"}

def generate_code(params, children, lang="cpp"):
    text = params.get("text", "")
    return f'// {text}\n'

block_ui_description = {
    "label": "Comment",
    "params": params,
    "category": "Basic",
    "description": "Adds a comment to the code"
}
"""

# ============================================================
# languages/cpp/blocks/math_add.py
# ============================================================
"""
block_id = "math_add_cpp"
display_name = "Add (+)"
category = "Math"

params = [
    {"name": "result", "type": "string", "default": "result"},
    {"name": "a", "type": "string", "default": "0"},
    {"name": "b", "type": "string", "default": "0"}
]

def default_params():
    return {"result": "result", "a": "0", "b": "0"}

def generate_code(params, children, lang="cpp"):
    result = params.get("result", "result")
    a = params.get("a", "0")
    b = params.get("b", "0")
    return f'{result} = {a} + {b};\n'

block_ui_description = {
    "label": "Add",
    "params": params,
    "category": "Math",
    "description": "Adds two numbers"
}
"""

# ============================================================
# languages/cpp/blocks/math_subtract.py
# ============================================================
"""
block_id = "math_subtract_cpp"
display_name = "Subtract (-)"
category = "Math"

params = [
    {"name": "result", "type": "string", "default": "result"},
    {"name": "a", "type": "string", "default": "0"},
    {"name": "b", "type": "string", "default": "0"}
]

def default_params():
    return {"result": "result", "a": "0", "b": "0"}

def generate_code(params, children, lang="cpp"):
    result = params.get("result", "result")
    a = params.get("a", "0")
    b = params.get("b", "0")
    return f'{result} = {a} - {b};\n'

block_ui_description = {
    "label": "Subtract",
    "params": params,
    "category": "Math",
    "description": "Subtracts two numbers"
}
"""

# ============================================================
# languages/cpp/blocks/math_multiply.py
# ============================================================
"""
block_id = "math_multiply_cpp"
display_name = "Multiply (×)"
category = "Math"

params = [
    {"name": "result", "type": "string", "default": "result"},
    {"name": "a", "type": "string", "default": "1"},
    {"name": "b", "type": "string", "default": "1"}
]

def default_params():
    return {"result": "result", "a": "1", "b": "1"}

def generate_code(params, children, lang="cpp"):
    result = params.get("result", "result")
    a = params.get("a", "1")
    b = params.get("b", "1")
    return f'{result} = {a} * {b};\n'

block_ui_description = {
    "label": "Multiply",
    "params": params,
    "category": "Math",
    "description": "Multiplies two numbers"
}
"""

# ============================================================
# languages/cpp/blocks/math_divide.py
# ============================================================
"""
block_id = "math_divide_cpp"
display_name = "Divide (÷)"
category = "Math"

params = [
    {"name": "result", "type": "string", "default": "result"},
    {"name": "a", "type": "string", "default": "1"},
    {"name": "b", "type": "string", "default": "1"}
]

def default_params():
    return {"result": "result", "a": "1", "b": "1"}

def generate_code(params, children, lang="cpp"):
    result = params.get("result", "result")
    a = params.get("a", "1")
    b = params.get("b", "1")
    return f'{result} = {a} / {b};\n'

block_ui_description = {
    "label": "Divide",
    "params": params,
    "category": "Math",
    "description": "Divides two numbers"
}
"""

# ============================================================
# languages/cpp/blocks/include.py
# ============================================================
"""
block_id = "include_cpp"
display_name = "Include Header"
category = "Modules"

params = [
    {"name": "header", "type": "string", "default": "iostream"}
]

def default_params():
    return {"header": "iostream"}

def generate_code(params, children, lang="cpp"):
    header = params.get("header", "iostream")
    return f'#include <{header}>\n'

block_ui_description = {
    "label": "Include Header",
    "params": params,
    "category": "Modules",
    "description": "Includes a C++ header file (e.g., iostream, string, vector)"
}
"""

# ============================================================
# languages/cpp/blocks/raw_code.py
# ============================================================
"""
block_id = "raw_code_cpp"
display_name = "Custom Code"
category = "Advanced"

params = [
    {"name": "code_line", "type": "code", "default": ""}
]

def default_params():
    return {"code_line": ""}

def generate_code(params, children, lang="cpp"):
    return params.get("code_line", "") + "\n"

block_ui_description = {
    "label": "Custom Code",
    "params": params,
    "category": "Advanced",
    "description": "Write custom C++ code (advanced users only)"
}
"""