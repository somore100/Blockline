block_id = "rust_input_line"
display_name = "Read Line Input"
category = "Basic"

params = [
    {"name": "variable", "type": "string", "default": "input"}
]

def default_params():
    return {"variable": "input"}

def generate_code(params, children, lang="rust"):
    var = params.get("variable", "input")
    return (
        f"let mut {var} = String::new();\n"
        f'std::io::stdin().read_line(&mut {var}).expect("Failed to read line");\n'
    )

block_ui_description = {
    "label": "Read Line Input",
    "params": params,
    "category": "Basic",
    "description": "Reads a line of text input from the console into a new String variable."
}
