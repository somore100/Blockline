block_id = "gui_window"
display_name = "Create Window"
category = "GUI"

params = [
    {"name": "variable", "type": "variable", "default": "root"},
    {"name": "title", "type": "text", "default": "My App"},
    {"name": "width", "type": "number", "default": "400"},
    {"name": "height", "type": "number", "default": "300"},
]

def default_params():
    return {"variable": "root", "title": "My App", "width": "400", "height": "300"}

def generate_code(params, children, lang="python"):
    var = params.get("variable", "root")
    title = params.get("title", "My App")
    width = params.get("width", "400")
    height = params.get("height", "300")
    return (
        f"{var} = tk.Tk()\n"
        f"{var}.title({title!r})\n"
        f"{var}.geometry(\"{width}x{height}\")\n"
    )

block_ui_description = {
    "label": "Create Window",
    "params": params,
    "category": "GUI",
    "description": "Creates the main Tkinter window. Add this first, before any other GUI blocks."
}
