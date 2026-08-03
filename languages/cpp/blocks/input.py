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
