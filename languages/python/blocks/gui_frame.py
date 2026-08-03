block_id = "gui_frame"
display_name = "Add Frame"
category = "GUI"

params = [
    {"name": "variable", "type": "variable", "default": "frame1"},
    {"name": "parent", "type": "variable", "default": "root"},
]

def default_params():
    return {"variable": "frame1", "parent": "root"}

def generate_code(params, children, lang="python"):
    var = params.get("variable", "frame1")
    parent = params.get("parent", "root")
    return (
        f"{var} = tk.Frame({parent})\n"
        f"{var}.pack(pady=5)\n"
    )

block_ui_description = {
    "label": "Add Frame",
    "params": params,
    "category": "GUI",
    "description": "A plain container for grouping other widgets together."
}
