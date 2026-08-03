block_id = "math_multiply_cpp"
display_name = "Multiply (x)"
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
