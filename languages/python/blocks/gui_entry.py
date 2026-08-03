block_id = "gui_entry"
display_name = "Add Text Input"
category = "GUI"

params = [
    {"name": "variable", "type": "variable", "default": "entry1"},
    {"name": "parent", "type": "variable", "default": "root"},
]

def default_params():
    return {"variable": "entry1", "parent": "root"}

def generate_code(params, children, lang="python"):
    var = params.get("variable", "entry1")
    parent = params.get("parent", "root")
    return (
        f"{var} = tk.Entry({parent})\n"
        f"{var}.pack(pady=5)\n"
    )

block_ui_description = {
    "label": "Add Text Input",
    "params": params,
    "category": "GUI",
    "description": "Adds a one-line text entry box. Read its value later with variable.get()."
}
