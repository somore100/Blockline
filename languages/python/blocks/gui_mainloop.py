block_id = "gui_mainloop"
display_name = "Run Window"
category = "GUI"

params = [
    {"name": "variable", "type": "variable", "default": "root"},
]

def default_params():
    return {"variable": "root"}

def generate_code(params, children, lang="python"):
    var = params.get("variable", "root")
    return f"{var}.mainloop()\n"

block_ui_description = {
    "label": "Run Window",
    "params": params,
    "category": "GUI",
    "description": "Starts the window's event loop. Add this last, after all other GUI blocks."
}
