block_id = "js_input_prompt"
display_name = "Prompt Input (Browser)"
category = "Basic"

params = [
    {"name": "variable", "type": "string", "default": "answer"},
    {"name": "message", "type": "string", "default": "Enter a value:"}
]

def default_params():
    return {"variable": "answer", "message": "Enter a value:"}

def generate_code(params, children, lang="javascript"):
    variable = params.get("variable", "answer")
    message = params.get("message", "Enter a value:")
    return f'{variable} = prompt("{message}");\n'

block_ui_description = {
    "label": "Prompt Input (Browser)",
    "params": params,
    "category": "Basic",
    "description": "Browser-only: shows a popup asking the user for input. Won't work in Node.js."
}
