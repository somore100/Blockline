block_id = "gui_button"
display_name = "Add Button"
category = "GUI"

params = [
    {"name": "variable", "type": "variable", "default": "button1"},
    {"name": "parent", "type": "variable", "default": "root"},
    {"name": "text", "type": "text", "default": "Click Me"},
    {"name": "command", "type": "variable", "default": "None"},
]

def default_params():
    return {"variable": "button1", "parent": "root", "text": "Click Me", "command": "None"}

def generate_code(params, children, lang="python"):
    var = params.get("variable", "button1")
    parent = params.get("parent", "root")
    text = params.get("text", "Click Me")
    command = params.get("command", "None")
    return (
        f"{var} = tk.Button({parent}, text={text!r}, command={command})\n"
        f"{var}.pack(pady=5)\n"
    )

block_ui_description = {
    "label": "Add Button",
    "params": params,
    "category": "GUI",
    "description": "Adds a clickable button. Set 'command' to the name of a function to call it on click."
}
