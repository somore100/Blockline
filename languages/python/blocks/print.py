# blocks/core/print.py or languages/python/blocks/print.py

block_id = "print"
display_name = "Print"
category = "Basic"

params = [
    {"name": "value", "type": "string", "default": "Hello, World!"},
    {"name": "mode", "type": "choice", "default": "text", "choices": ["text", "variable"]}
]

def default_params():
    return {"value": "Hello, World!", "mode": "text"}

def generate_code(params, children, lang="python"):
    if lang.lower().startswith("py"):
        value = params.get("value", "Hello, World!")
        mode = params.get("mode", "text")
        
        if mode == "variable":
            # Print variable without quotes
            return f'print({value})\n'
        else:
            # Print as text string with quotes
            return f'print({repr(value)})\n'
    elif lang.lower().startswith("c"):
        value = params.get("value", "Hello, World!")
        mode = params.get("mode", "text")
        
        if mode == "variable":
            return f'std::cout << {value} << std::endl;\n'
        else:
            return f'std::cout << "{value}" << std::endl;\n'
    return ""

block_ui_description = {
    "label": "Print",
    "params": params,
    "category": "Basic",
    "description": "Prints a value or variable to the console. Use 'text' mode for strings, 'variable' mode for variables."
}