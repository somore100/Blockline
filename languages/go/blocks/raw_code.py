block_id = "raw_code"
display_name = "Custom Code"
category = "Advanced"

params = [
    {"name": "code_line", "type": "code", "default": ""}
]

def default_params():
    return {"code_line": ""}

def generate_code(params, children, lang="go"):
    """Escape hatch: outputs the given line of go code as-is."""
    return params.get("code_line", "") + "\n"

block_ui_description = {
    "label": "Custom Code",
    "params": params,
    "category": "Advanced",
    "description": "Write custom go code directly (advanced users only)."
}
