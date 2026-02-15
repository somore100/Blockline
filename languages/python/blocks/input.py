block_id = "input"
display_name = "Input"
category = "Basic"
params = [
    {"name": "prompt", "type": "string", "default": "Enter value: "},
    {"name": "variable", "type": "string", "default": "user_input"}
]

def default_params():
    return {"prompt": "Enter value: ", "variable": "user_input"}

def generate_code(params, children, lang="python"):
    if lang.lower().startswith("py"):
        prompt = params.get("prompt", "")
        var = params.get("variable", "user_input")
        return f'{var} = input({repr(prompt)})\n'
    return ""

block_ui_description = {
    "label": "Input",
    "params": params,
    "category": "Basic",
    "description": "Gets user input and stores it in a variable"
}