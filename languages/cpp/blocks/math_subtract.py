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
