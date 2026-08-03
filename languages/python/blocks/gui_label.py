block_id = "gui_label"
display_name = "Add Label"
category = "GUI"

params = [
    {"name": "variable", "type": "variable", "default": "label1"},
    {"name": "parent", "type": "variable", "default": "root"},
    {"name": "text", "type": "text", "default": "Hello!"},
]

def default_params():
    return {"variable": "label1", "parent": "root", "text": "Hello!"}

def generate_code(params, children, lang="python"):
    var = params.get("variable", "label1")
    parent = params.get("parent", "root")
    text = params.get("text", "Hello!")
    return (
        f"{var} = tk.Label({parent}, text={text!r})\n"
        f"{var}.pack(pady=5)\n"
    )

block_ui_description = {
    "label": "Add Label",
    "params": params,
    "category": "GUI",
    "description": "Adds a text label to a window or frame."
}
