block_id = "go_print"
display_name = "Print"
category = "Basic"

params = [
    {"name": "value", "type": "string", "default": "Hello, World!"},
    {"name": "mode", "type": "choice", "default": "text", "choices": ["text", "variable"]}
]

def default_params():
    return {"value": "Hello, World!", "mode": "text"}

def generate_code(params, children, lang="go"):
    value = params.get("value", "")
    mode = params.get("mode", "text")
    if mode == "variable":
        return f"fmt.Println({value})\n"
    return f'fmt.Println("{value}")\n'

block_ui_description = {
    "label": "Print",
    "params": params,
    "category": "Basic",
    "description": "Prints a value or variable to the console. Add an Import block for fmt first."
}
