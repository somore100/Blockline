block_id = "raw_code"
display_name = "Custom Code"
category = "Advanced"

block_ui_description = {
    "description": "Write any Python code manually"
}

params = [
    {"name": "code", "type": "string", "default": ""}
]

def default_params():
    return {"code": ""}

def generate_code(params, children, lang="python"):
    return params["code"] + "\n"
