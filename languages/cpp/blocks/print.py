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
