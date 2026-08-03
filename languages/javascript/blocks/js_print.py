block_id = "js_print"
display_name = "Print"
category = "Basic"

params = [
    {"name": "value", "type": "string", "default": "Hello, World!"},
    {"name": "mode", "type": "choice", "default": "text", "choices": ["text", "variable"]}
]

def default_params():
    return {"value": "Hello, World!", "mode": "text"}

def generate_code(params, children, lang="javascript"):
    value = params.get("value", "")
    mode = params.get("mode", "text")
    if mode == "variable":
        return f"console.log({value});\n"
    return f'console.log("{value}");\n'

block_ui_description = {
    "label": "Print",
    "params": params,
    "category": "Basic",
    "description": "Logs a value or variable to the console."
}
