block_id = "csharp_input"
display_name = "Read Line Input"
category = "Basic"

params = [
    {"name": "variable", "type": "string", "default": "input"}
]

def default_params():
    return {"variable": "input"}

def generate_code(params, children, lang="csharp"):
    variable = params.get("variable", "input")
    return f"{variable} = Console.ReadLine();\n"

block_ui_description = {
    "label": "Read Line Input",
    "params": params,
    "category": "Basic",
    "description": "Reads a line of text input from the console into an already-declared variable."
}
