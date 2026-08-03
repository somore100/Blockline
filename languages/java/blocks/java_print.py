block_id = "java_print"
display_name = "Print"
category = "Basic"

params = [
    {"name": "value", "type": "string", "default": "Hello, World!"},
    {"name": "mode", "type": "choice", "default": "text", "choices": ["text", "variable"]}
]

def default_params():
    return {"value": "Hello, World!", "mode": "text"}

def generate_code(params, children, lang="java"):
    value = params.get("value", "")
    mode = params.get("mode", "text")
    if mode == "variable":
        return f"System.out.println({value});\n"
    return f'System.out.println("{value}");\n'

block_ui_description = {
    "label": "Print",
    "params": params,
    "category": "Basic",
    "description": "Prints a value or variable to the console."
}
