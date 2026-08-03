block_id = "gui_import"
display_name = "Import Tkinter"
category = "GUI"

params = []

def default_params():
    return {}

def generate_code(params, children, lang="python"):
    return "import tkinter as tk\n"

block_ui_description = {
    "label": "Import Tkinter",
    "params": params,
    "category": "GUI",
    "description": "Imports Tkinter. Add this once, at the very top of any GUI program."
}
