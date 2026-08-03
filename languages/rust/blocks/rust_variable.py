block_id = "rust_variable"
display_name = "Set Variable"
category = "Basic"

params = [
    {"name": "mutable", "type": "boolean", "default": "false"},
    {"name": "variable", "type": "string", "default": "x"},
    {"name": "value", "type": "string", "default": "0"}
]

def default_params():
    return {"mutable": "false", "variable": "x", "value": "0"}

def generate_code(params, children, lang="rust"):
    mutable = str(params.get("mutable", "false")).strip().lower() in ("true", "1", "yes")
    var = params.get("variable", "x")
    val = params.get("value", "0")
    mut_kw = "mut " if mutable else ""
    return f"let {mut_kw}{var} = {val};\n"

block_ui_description = {
    "label": "Set Variable",
    "params": params,
    "category": "Basic",
    "description": "Declares a variable. Set 'mutable' to true if you need to change it later - Rust variables are immutable by default."
}
