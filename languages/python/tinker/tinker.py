import tkinter as tk
from tkinter import ttk, messagebox

# This module provides the Tinker UI for creating block definitions at runtime
# No saving to disk yet – blocks exist only in memory

class BlockDefinition:
    def __init__(self, block_id, display_name, category, params, code_templates):
        self.block_id = block_id
        self.display_name = display_name
        self.category = category
        self.params = params
        self.code_templates = code_templates

    def default_params(self):
        return {p['name']: p.get('default', '') for p in self.params}

    def generate_code(self, params, children=None, lang="python"):
        template = self.code_templates.get(lang, "")
        try:
            return template.format(**params) + "\n"
        except Exception as e:
            return f"# Error generating code: {e}\n"


class TinkerUI(tk.Toplevel):
    def __init__(self, master, on_create_callback):
        super().__init__(master)
        self.title("Blockline – Tinker Block Builder")
        self.geometry("700x600")
        self.on_create_callback = on_create_callback

        self.params = []

        self._build_ui()

    def _build_ui(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        # --- Block Info Tab ---
        info_frame = ttk.Frame(notebook)
        notebook.add(info_frame, text="Block Info")

        ttk.Label(info_frame, text="Block ID:").pack(anchor="w", padx=10, pady=5)
        self.block_id_entry = ttk.Entry(info_frame)
        self.block_id_entry.pack(fill="x", padx=10)

        ttk.Label(info_frame, text="Display Name:").pack(anchor="w", padx=10, pady=5)
        self.display_name_entry = ttk.Entry(info_frame)
        self.display_name_entry.pack(fill="x", padx=10)

        ttk.Label(info_frame, text="Category:").pack(anchor="w", padx=10, pady=5)
        self.category_entry = ttk.Entry(info_frame)
        self.category_entry.pack(fill="x", padx=10)

        # --- Params Tab ---
        params_frame = ttk.Frame(notebook)
        notebook.add(params_frame, text="Inputs")

        self.params_listbox = tk.Listbox(params_frame)
        self.params_listbox.pack(fill="both", expand=True, padx=10, pady=10)

        add_param_btn = ttk.Button(params_frame, text="+ Add Input", command=self._add_param_dialog)
        add_param_btn.pack(pady=5)

        # --- Code Tab ---
        code_frame = ttk.Frame(notebook)
        notebook.add(code_frame, text="Python Code")

        ttk.Label(code_frame, text="Code Template (use {param} placeholders):").pack(anchor="w", padx=10, pady=5)
        self.code_text = tk.Text(code_frame, height=20)
        self.code_text.pack(fill="both", expand=True, padx=10, pady=5)

        # --- Bottom Buttons ---
        bottom = ttk.Frame(self)
        bottom.pack(fill="x", pady=10)

        create_btn = ttk.Button(bottom, text="Create Block", command=self._create_block)
        create_btn.pack(side="right", padx=10)

    def _add_param_dialog(self):
        dialog = tk.Toplevel(self)
        dialog.title("Add Input")
        dialog.geometry("300x200")

        ttk.Label(dialog, text="Name:").pack(anchor="w", padx=10, pady=5)
        name_entry = ttk.Entry(dialog)
        name_entry.pack(fill="x", padx=10)

        ttk.Label(dialog, text="Type:").pack(anchor="w", padx=10, pady=5)
        type_combo = ttk.Combobox(dialog, values=["string", "number", "variable", "raw"])
        type_combo.current(0)
        type_combo.pack(fill="x", padx=10)

        ttk.Label(dialog, text="Default:").pack(anchor="w", padx=10, pady=5)
        default_entry = ttk.Entry(dialog)
        default_entry.pack(fill="x", padx=10)

        def add():
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("Error", "Input name required")
                return
            param = {
                "name": name,
                "type": type_combo.get(),
                "default": default_entry.get()
            }
            self.params.append(param)
            self.params_listbox.insert(tk.END, f"{name} ({param['type']})")
            dialog.destroy()

        ttk.Button(dialog, text="Add", command=add).pack(pady=10)

    def _create_block(self):
        block_id = self.block_id_entry.get().strip()
        display_name = self.display_name_entry.get().strip()
        category = self.category_entry.get().strip() or "Custom"
        code_template = self.code_text.get("1.0", tk.END).strip()

        if not block_id or not display_name or not code_template:
            messagebox.showerror("Error", "Block ID, name, and code are required")
            return

        block = BlockDefinition(
            block_id=block_id,
            display_name=display_name,
            category=category,
            params=self.params,
            code_templates={"python": code_template}
        )

        self.on_create_callback(block)
        self.destroy()


# Helper to open the Tinker UI

def open_tinker_ui(master, on_create_callback):
    TinkerUI(master, on_create_callback)
