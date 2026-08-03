block_id = "c_print_text"
display_name = "Print Text"
category = "Basic"

params = [
    {"name": "value", "type": "string", "default": "Hello, World!"}
]

def default_params():
    return {"value": "Hello, World!"}

def generate_code(params, children, lang="c"):
    value = params.get("value", "")
    return f'puts("{value}");\n'

block_ui_description = {
    "label": "Print Text",
    "params": params,
    "category": "Basic",
    "description": "Prints a fixed line of text to the console (adds a newline automatically)."
}
