block_id = "go_input"
display_name = "Read Number Input"
category = "Basic"

params = [
    {"name": "variable", "type": "string", "default": "x"}
]

def default_params():
    return {"variable": "x"}

def generate_code(params, children, lang="go"):
    variable = params.get("variable", "x")
    return f"fmt.Scanln(&{variable})\n"

block_ui_description = {
    "label": "Read Number Input",
    "params": params,
    "category": "Basic",
    "description": "Reads input into an already-declared variable. Add an Import block for fmt first."
}
