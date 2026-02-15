block_id = "sleep"
display_name = "Sleep (Delay)"
category = "Control"
params = [
    {"name": "seconds", "type": "number", "default": "1"}
]

def default_params():
    return {"seconds": "1"}

def generate_code(params, children, lang="python"):
    if lang.lower().startswith("py"):
        seconds = params.get("seconds", "1")
        return f'time.sleep({seconds})\n'
    return ""

block_ui_description = {
    "label": "Sleep",
    "params": params,
    "category": "Control",
    "description": "Pauses execution for specified seconds (requires 'import time')"
}
