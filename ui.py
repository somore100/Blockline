import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import importlib.util
import os
import json
import threading
import uuid
import subprocess
import sys
from PIL import Image, ImageTk  # For logo support

# Dark mode color scheme
DARK_BG = "#1e1e1e"
DARK_FG = "#d4d4d4"
DARK_PANEL = "#252526"
DARK_ACCENT = "#007acc"
DARK_HOVER = "#2d2d30"
DARK_BORDER = "#3e3e42"
BLOCK_BG = "#2d2d30"
BLOCK_HOVER = "#3e3e42"
BLOCK_SELECTED = "#094771"

# Block category colors
CATEGORY_COLORS = {
    "Basic": "#4ec9b0",
    "Math": "#ce9178",
    "Control": "#c586c0",
    "Functions": "#dcdcaa",
    "Data Structures": "#569cd6",
    "String Operations": "#9cdcfe",
    "Modules": "#4fc1ff",
    "GUI": "#b5cea8",
    "Advanced": "#f48771",
    "Custom Blocks": "#ff6b9d"
}

CUSTOM_BLOCKS_PATH = os.path.join("user_data", "custom_blocks.json")

def load_blocks_from_folder(folder_path):
    """Dynamically load blocks from folder structure"""
    blocks = {}
    if not os.path.exists(folder_path):
        return blocks
        
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith(".py") and not filename.startswith("__"):
                file_path = os.path.join(root, filename)
                rel_path = os.path.relpath(file_path, folder_path)
                module_name = rel_path.replace(os.sep, ".")[:-3]

                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                try:
                    spec.loader.exec_module(module)
                except Exception as e:
                    print(f"Failed to load block '{module_name}': {e}")
                    continue

                if hasattr(module, "block_id"):
                    blocks[module.block_id] = module
    return blocks

class PaletteBlockItem(tk.Frame):
    """Block item in palette - click to add"""
    def __init__(self, parent, block_module, on_add):
        super().__init__(parent, bg=DARK_PANEL, cursor="hand2", relief=tk.FLAT)
        self.block_module = block_module
        self.on_add = on_add
        
        # Handle both dict (custom blocks) and module objects
        if isinstance(block_module, dict):
            category = block_module.get("category", "Basic")
            display_name = block_module.get("display_name", "Unknown")
            description = block_module.get("description", "")
        else:
            category = getattr(block_module, "category", "Basic")
            display_name = getattr(block_module, "display_name", "Unknown")
            description = getattr(block_module, "block_ui_description", {}).get("description", "")
        
        self.color = CATEGORY_COLORS.get(category, "#ffffff")
        
        # Color indicator
        indicator = tk.Frame(self, bg=self.color, width=4)
        indicator.pack(side=tk.LEFT, fill=tk.Y)
        
        # Block info
        info_frame = tk.Frame(self, bg=DARK_PANEL)
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=6)
        
        self.name_label = tk.Label(
            info_frame,
            text=display_name,
            bg=DARK_PANEL,
            fg=DARK_FG,
            font=("Segoe UI", 9, "bold"),
            anchor="w"
        )
        self.name_label.pack(anchor="w")
        
        if description:
            self.desc_label = tk.Label(
                info_frame,
                text=description[:50] + "..." if len(description) > 50 else description,
                bg=DARK_PANEL,
                fg="#888888",
                font=("Segoe UI", 8),
                anchor="w",
                wraplength=180
            )
            self.desc_label.pack(anchor="w")
        
        # Add button
        add_btn = tk.Label(
            self,
            text="＋",
            bg=DARK_PANEL,
            fg=self.color,
            font=("Segoe UI", 14, "bold"),
            cursor="hand2"
        )
        add_btn.pack(side=tk.RIGHT, padx=8)
        
        # Bind events
        self.bind("<Button-1>", lambda e: self.on_add(self.block_module))
        add_btn.bind("<Button-1>", lambda e: self.on_add(self.block_module))
        self.name_label.bind("<Button-1>", lambda e: self.on_add(self.block_module))
        
        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)
    
    def on_hover(self, event):
        self.configure(bg=DARK_HOVER, relief=tk.RAISED)
        for child in self.winfo_children():
            if isinstance(child, (tk.Frame, tk.Label)) and child.winfo_width() > 4:
                child.configure(bg=DARK_HOVER)
    
    def on_leave(self, event):
        self.configure(bg=DARK_PANEL, relief=tk.FLAT)
        for child in self.winfo_children():
            if isinstance(child, (tk.Frame, tk.Label)) and child.winfo_width() > 4:
                child.configure(bg=DARK_PANEL)

class BlockWidget(tk.Frame):
    """Visual representation of a block in the workspace"""
    def __init__(self, parent, block_id, block_module, params, index, on_delete, on_edit, on_move_up, on_move_down):
        super().__init__(parent, bg=BLOCK_BG, highlightthickness=2, highlightbackground=DARK_BORDER, relief=tk.RAISED)
        self.block_id = block_id
        self.block_module = block_module
        self.params = params
        self.index = index
        self.on_delete = on_delete
        self.on_edit = on_edit
        self.on_move_up = on_move_up
        self.on_move_down = on_move_down
        
        # Get category color
        category = getattr(block_module, "category", "Basic")
        self.category_color = CATEGORY_COLORS.get(category, "#ffffff")
        
        self.create_widgets()
        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)
        
    def create_widgets(self):
        # Header with block name and buttons
        header = tk.Frame(self, bg=self.category_color, height=32)
        header.pack(fill=tk.X, padx=2, pady=2)
        header.pack_propagate(False)
        
        # Block index number
        tk.Label(
            header,
            text=f"{self.index + 1}",
            bg=self.category_color,
            fg="#000000",
            font=("Segoe UI", 9, "bold"),
            width=3
        ).pack(side=tk.LEFT, padx=(8, 4))
        
        # Block name
        name_label = tk.Label(
            header,
            text=self.block_module.display_name,
            bg=self.category_color,
            fg="#000000",
            font=("Segoe UI", 10, "bold"),
            anchor="w"
        )
        name_label.pack(side=tk.LEFT, padx=4, fill=tk.X, expand=True)
        
        # Control buttons
        btn_config = {
            "bg": self.category_color,
            "fg": "#000000",
            "relief": tk.FLAT,
            "width": 2,
            "cursor": "hand2"
        }
        
        tk.Button(header, text="▲", font=("Segoe UI", 8), command=lambda: self.on_move_up(self.index), **btn_config).pack(side=tk.RIGHT, padx=1)
        tk.Button(header, text="▼", font=("Segoe UI", 8), command=lambda: self.on_move_down(self.index), **btn_config).pack(side=tk.RIGHT, padx=1)
        tk.Button(header, text="✎", font=("Segoe UI", 10), command=lambda: self.on_edit(self.index), **btn_config).pack(side=tk.RIGHT, padx=2)
        tk.Button(header, text="✕", font=("Segoe UI", 10, "bold"), command=lambda: self.on_delete(self.index), **btn_config).pack(side=tk.RIGHT, padx=2)
        
        # Parameters display
        if self.params:
            params_frame = tk.Frame(self, bg=BLOCK_BG)
            params_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=6)
            
            for name, value in self.params.items():
                param_row = tk.Frame(params_frame, bg=BLOCK_BG)
                param_row.pack(fill=tk.X, pady=2)
                
                tk.Label(
                    param_row,
                    text=f"{name}:",
                    bg=BLOCK_BG,
                    fg="#888888",
                    font=("Consolas", 9),
                    anchor="w",
                    width=15
                ).pack(side=tk.LEFT)
                
                # Truncate long values
                display_value = str(value)
                if len(display_value) > 40:
                    display_value = display_value[:37] + "..."
                
                tk.Label(
                    param_row,
                    text=display_value,
                    bg=BLOCK_BG,
                    fg=DARK_FG,
                    font=("Consolas", 9, "bold"),
                    anchor="w"
                ).pack(side=tk.LEFT, padx=4)
    
    def on_hover(self, event):
        self.configure(bg=BLOCK_HOVER, highlightbackground=self.category_color, highlightthickness=3)
    
    def on_leave(self, event):
        self.configure(bg=BLOCK_BG, highlightbackground=DARK_BORDER, highlightthickness=2)

class BlocklineUI(tk.Tk):
    def __init__(self, initial_lang="python", languages_path="languages"):
        super().__init__()
        self.title("Blockline - Visual Code Builder")
        self.geometry("1400x800")
        self.configure(bg=DARK_BG)
        
        self.languages_path = languages_path
        self.current_language = initial_lang
        self.blocks = {}
        self.project_blocks = []
        self.blocks_by_category = {}
        self.custom_blocks = []
        
        # Create languages folder structure if it doesn't exist
        os.makedirs(os.path.join(languages_path, "python", "blocks"), exist_ok=True)
        os.makedirs(os.path.join(languages_path, "cpp", "blocks"), exist_ok=True)
        
        self.load_blocks_for_language(self.current_language)
        self.load_and_merge_custom_blocks()
        self.create_widgets()
        self.update_generated_code()
    
    def load_blocks_for_language(self, lang):
        """Load blocks from language folder"""
        lang_blocks_path = os.path.join(self.languages_path, lang, "blocks")
        if not os.path.isdir(lang_blocks_path):
            os.makedirs(lang_blocks_path, exist_ok=True)
            self.blocks = {}
        else:
            self.blocks = load_blocks_from_folder(lang_blocks_path)
        
        # Group blocks by category
        self.blocks_by_category = {}
        for block_id, module in self.blocks.items():
            category = getattr(module, "category", "Basic")
            self.blocks_by_category.setdefault(category, []).append(module)
    
    def load_custom_blocks_data(self):
        """Load custom blocks from JSON file"""
        if not os.path.exists("user_data"):
            os.makedirs("user_data")
        if os.path.exists(CUSTOM_BLOCKS_PATH):
            try:
                with open(CUSTOM_BLOCKS_PATH, "r") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Failed to load custom blocks: {e}")
                return []
        return []
    
    def save_custom_blocks_data(self, custom_blocks):
        """Save custom blocks to JSON file"""
        if not os.path.exists("user_data"):
            os.makedirs("user_data")
        try:
            with open(CUSTOM_BLOCKS_PATH, "w") as f:
                json.dump(custom_blocks, f, indent=2)
        except Exception as e:
            print(f"Failed to save custom blocks: {e}")
    
    def load_and_merge_custom_blocks(self):
        """Load custom blocks and merge them into blocks dictionary"""
        self.custom_blocks = self.load_custom_blocks_data()
        
        # Convert custom blocks JSON to module-like objects
        for cblock in self.custom_blocks:
            # Create generate_code function with closure
            def make_generate_code(template):
                def gen_code(params, children=None, lang=None):
                    code = template
                    for k, v in params.items():
                        code = code.replace(f"{{{{{k}}}}}", str(v))
                    return code + "\n"
                return gen_code
            
            # Ensure block has all required attributes
            if "block_id" not in cblock:
                cblock["block_id"] = "custom_" + str(uuid.uuid4())[:8]
            
            cblock["generate_code"] = make_generate_code(cblock["code_template"])
            cblock["category"] = "Custom Blocks"
            cblock["display_name"] = cblock.get("display_name", "Unnamed Custom Block")
            cblock["params"] = cblock.get("params", [])
            
            # Add to blocks dict and category
            self.blocks[cblock["block_id"]] = cblock
            self.blocks_by_category.setdefault("Custom Blocks", []).append(cblock)
    
    def _on_mousewheel(self, event, canvas):
        """Handle mousewheel scrolling"""
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def create_widgets(self):
        # Top toolbar
        toolbar = tk.Frame(self, bg=DARK_PANEL, height=50)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        toolbar.pack_propagate(False)
        
        # Logo and branding
        logo_frame = tk.Frame(toolbar, bg=DARK_PANEL)
        logo_frame.pack(side=tk.LEFT, padx=15)
        
        # Try to load logo
        try:
            logo_path = "logo.png"  # Assumes logo.png is in the same folder as main.py
            if os.path.exists(logo_path):
                logo_img = Image.open(logo_path)
                logo_img = logo_img.resize((32, 32), Image.Resampling.LANCZOS)
                self.logo_photo = ImageTk.PhotoImage(logo_img)
                tk.Label(
                    logo_frame,
                    image=self.logo_photo,
                    bg=DARK_PANEL
                ).pack(side=tk.LEFT, padx=(0, 8))
        except Exception as e:
            print(f"Could not load logo: {e}")
        
        tk.Label(
            logo_frame,
            text="⬢ Blockline",
            bg=DARK_PANEL,
            fg=DARK_ACCENT,
            font=("Segoe UI", 16, "bold")
        ).pack(side=tk.LEFT)
        
        tk.Label(
            logo_frame,
            text="by domore100",
            bg=DARK_PANEL,
            fg="#888888",
            font=("Segoe UI", 8, "italic")
        ).pack(side=tk.LEFT, padx=(5, 0))
        
        # Toolbar buttons
        btn_style = {"style": "Toolbar.TButton"}
        
        ttk.Button(toolbar, text="💾 Save", command=self.save_project, **btn_style).pack(side=tk.LEFT, padx=3)
        ttk.Button(toolbar, text="📂 Load", command=self.load_project, **btn_style).pack(side=tk.LEFT, padx=3)
        ttk.Button(toolbar, text="📤 Export", command=self.export_code, **btn_style).pack(side=tk.LEFT, padx=3)
        
        tk.Frame(toolbar, bg=DARK_BORDER, width=2).pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=8)
        
        ttk.Button(toolbar, text="🔧 Manage Custom Blocks", command=self.manage_custom_blocks_dialog, **btn_style).pack(side=tk.LEFT, padx=3)
        
        tk.Frame(toolbar, bg=DARK_BORDER, width=2).pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=8)
        
        # Run button with dropdown
        run_frame = tk.Frame(toolbar, bg=DARK_PANEL)
        run_frame.pack(side=tk.LEFT, padx=3)
        
        run_btn = ttk.Button(run_frame, text="▶ Run", command=self.run_code, **btn_style)
        run_btn.pack(side=tk.LEFT)
        
        # Dropdown for run options
        run_menu_btn = tk.Label(
            run_frame,
            text="▼",
            bg=DARK_PANEL,
            fg=DARK_FG,
            font=("Segoe UI", 8),
            cursor="hand2"
        )
        run_menu_btn.pack(side=tk.LEFT, padx=(2, 0))
        
        def show_run_menu(event):
            menu = tk.Menu(self, tearoff=0, bg=DARK_PANEL, fg=DARK_FG, activebackground=DARK_HOVER)
            menu.add_command(label="▶ Run in Blockline", command=self.run_code)
            menu.add_command(label="🖥️ Run in Terminal", command=self.run_in_terminal)
            menu.add_command(label="📝 Open in VS Code", command=self.open_in_vscode)
            menu.add_separator()
            menu.add_command(label="💾 Export & Run...", command=self.export_and_run)
            menu.post(event.x_root, event.y_root)
        
        run_menu_btn.bind("<Button-1>", show_run_menu)
        
        ttk.Button(toolbar, text="🗑 Clear", command=self.clear_all, **btn_style).pack(side=tk.LEFT, padx=3)
        
        # Main container
        main_container = tk.Frame(self, bg=DARK_BG)
        main_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel: Block Palette
        left_panel = tk.Frame(main_container, bg=DARK_PANEL, width=280)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 3))
        left_panel.pack_propagate(False)
        
        palette_header = tk.Frame(left_panel, bg=DARK_PANEL, height=50)
        palette_header.pack(fill=tk.X)
        palette_header.pack_propagate(False)
        
        tk.Label(
            palette_header,
            text="📦 Block Palette",
            bg=DARK_PANEL,
            fg=DARK_FG,
            font=("Segoe UI", 11, "bold")
        ).pack(pady=5)
        
        tk.Label(
            palette_header,
            text="Click to add block →",
            bg=DARK_PANEL,
            fg="#888888",
            font=("Segoe UI", 8, "italic")
        ).pack()
        
        # Search box
        search_frame = tk.Frame(left_panel, bg=DARK_PANEL)
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_palette)
        
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            bg=DARK_BG,
            fg=DARK_FG,
            font=("Segoe UI", 9),
            insertbackground=DARK_FG
        )
        search_entry.pack(fill=tk.X, ipady=3)
        
        tk.Label(
            search_frame,
            text="🔍 Search blocks...",
            bg=DARK_PANEL,
            fg="#555555",
            font=("Segoe UI", 8)
        ).pack(anchor="w", pady=(2, 0))
        
        # Scrollable palette - FIXED
        self.palette_canvas = tk.Canvas(left_panel, bg=DARK_PANEL, highlightthickness=0)
        palette_scrollbar = ttk.Scrollbar(left_panel, orient="vertical", command=self.palette_canvas.yview)
        self.palette_frame = tk.Frame(self.palette_canvas, bg=DARK_PANEL)
        
        self.palette_frame.bind(
            "<Configure>",
            lambda e: self.palette_canvas.configure(scrollregion=self.palette_canvas.bbox("all"))
        )
        
        self.palette_canvas.create_window((0, 0), window=self.palette_frame, anchor="nw", width=260)
        self.palette_canvas.configure(yscrollcommand=palette_scrollbar.set)
        
        # Bind mousewheel ONLY to palette canvas
        self.palette_canvas.bind("<Enter>", lambda e: self.palette_canvas.bind_all("<MouseWheel>", lambda ev: self._on_mousewheel(ev, self.palette_canvas)))
        self.palette_canvas.bind("<Leave>", lambda e: self.palette_canvas.unbind_all("<MouseWheel>"))
        
        self.palette_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        palette_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Build palette
        self.build_palette()
        
        # Middle panel: Workspace
        middle_panel = tk.Frame(main_container, bg=DARK_BG)
        middle_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=3)
        
        workspace_header = tk.Frame(middle_panel, bg=DARK_BG, height=50)
        workspace_header.pack(fill=tk.X)
        workspace_header.pack_propagate(False)
        
        tk.Label(
            workspace_header,
            text="🎨 Workspace",
            bg=DARK_BG,
            fg=DARK_FG,
            font=("Segoe UI", 11, "bold")
        ).pack(side=tk.LEFT, padx=10, pady=5)
        
        self.block_count_label = tk.Label(
            workspace_header,
            text="0 blocks",
            bg=DARK_BG,
            fg="#888888",
            font=("Segoe UI", 9)
        )
        self.block_count_label.pack(side=tk.LEFT, padx=5)
        
        # Workspace canvas - FIXED
        self.workspace_canvas = tk.Canvas(middle_panel, bg=DARK_BG, highlightthickness=1, highlightbackground=DARK_BORDER)
        workspace_scrollbar = ttk.Scrollbar(middle_panel, orient="vertical", command=self.workspace_canvas.yview)
        self.workspace_frame = tk.Frame(self.workspace_canvas, bg=DARK_BG)
        
        self.workspace_frame.bind(
            "<Configure>",
            lambda e: self.workspace_canvas.configure(scrollregion=self.workspace_canvas.bbox("all"))
        )
        
        self.workspace_canvas.create_window((0, 0), window=self.workspace_frame, anchor="nw", width=600)
        self.workspace_canvas.configure(yscrollcommand=workspace_scrollbar.set)
        
        # Bind mousewheel ONLY to workspace canvas
        self.workspace_canvas.bind("<Enter>", lambda e: self.workspace_canvas.bind_all("<MouseWheel>", lambda ev: self._on_mousewheel(ev, self.workspace_canvas)))
        self.workspace_canvas.bind("<Leave>", lambda e: self.workspace_canvas.unbind_all("<MouseWheel>"))
        
        self.workspace_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        workspace_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Empty state
        self.show_empty_state()
        
        # Right panel: Code Preview
        right_panel = tk.Frame(main_container, bg=DARK_PANEL, width=400)
        right_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(3, 0))
        right_panel.pack_propagate(False)
        
        code_header = tk.Frame(right_panel, bg=DARK_PANEL, height=50)
        code_header.pack(fill=tk.X)
        code_header.pack_propagate(False)
        
        tk.Label(
            code_header,
            text="📝 Generated Code",
            bg=DARK_PANEL,
            fg=DARK_FG,
            font=("Segoe UI", 11, "bold")
        ).pack(pady=5)
        
        # Language selector with Add Language button
        lang_frame = tk.Frame(right_panel, bg=DARK_PANEL)
        lang_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(
            lang_frame,
            text="Language:",
            bg=DARK_PANEL,
            fg=DARK_FG,
            font=("Segoe UI", 9)
        ).pack(side=tk.LEFT, padx=5)
        
        # Get available languages
        available_langs = self.get_available_languages()
        
        self.lang_var = tk.StringVar(value=self.current_language)
        self.lang_combo = ttk.Combobox(
            lang_frame,
            textvariable=self.lang_var,
            values=available_langs,
            state="readonly",
            width=10
        )
        self.lang_combo.pack(side=tk.LEFT, padx=5)
        self.lang_combo.bind("<<ComboboxSelected>>", self.on_language_change)
        
        # Add Language button
        ttk.Button(
            lang_frame,
            text="+ Lang",
            command=self.add_language_dialog,
            style="Toolbar.TButton"
        ).pack(side=tk.LEFT, padx=2)
        
        self.line_count_label = tk.Label(
            lang_frame,
            text="0 lines",
            bg=DARK_PANEL,
            fg="#888888",
            font=("Segoe UI", 8)
        )
        self.line_count_label.pack(side=tk.RIGHT, padx=5)
        
        # Code display
        self.code_text = tk.Text(
            right_panel,
            bg="#1e1e1e",
            fg=DARK_FG,
            font=("Consolas", 9),
            insertbackground=DARK_FG,
            selectbackground=BLOCK_SELECTED,
            relief=tk.FLAT,
            padx=12,
            pady=12,
            wrap=tk.NONE
        )
        self.code_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Apply dark theme
        self.apply_theme()
        
        # Footer with credits
        footer = tk.Frame(self, bg=DARK_PANEL, height=25)
        footer.pack(side=tk.BOTTOM, fill=tk.X)
        footer.pack_propagate(False)
        
        tk.Label(
            footer,
            text="Made with ❤️ by domore100  |  Blockline Visual Code Builder",
            bg=DARK_PANEL,
            fg="#666666",
            font=("Segoe UI", 8)
        ).pack(side=tk.LEFT, padx=15, pady=5)
        
        version_label = tk.Label(
            footer,
            text="v1.0",
            bg=DARK_PANEL,
            fg="#444444",
            font=("Segoe UI", 7)
        )
        version_label.pack(side=tk.RIGHT, padx=15, pady=5)
    
    def apply_theme(self):
        """Apply dark theme to ttk widgets"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure("Toolbar.TButton",
                       background=DARK_PANEL,
                       foreground=DARK_FG,
                       borderwidth=1,
                       focuscolor=DARK_ACCENT,
                       padding=8)
        style.map("Toolbar.TButton",
                 background=[('active', DARK_HOVER), ('pressed', DARK_ACCENT)])
        
        style.configure("TCombobox",
                       fieldbackground=DARK_BG,
                       background=DARK_PANEL,
                       foreground=DARK_FG,
                       arrowcolor=DARK_FG)
        style.map("TCombobox",
                 fieldbackground=[('readonly', DARK_BG)],
                 selectbackground=[('readonly', DARK_BG)])
    
    def get_available_languages(self):
        """Get list of available languages"""
        if not os.path.exists(self.languages_path):
            return ["python"]
        return sorted([d for d in os.listdir(self.languages_path) 
                      if os.path.isdir(os.path.join(self.languages_path, d))])
    
    def build_palette(self):
        """Build the block palette"""
        for widget in self.palette_frame.winfo_children():
            widget.destroy()
        
        search_term = self.search_var.get().lower()
        
        if not self.blocks_by_category:
            tk.Label(
                self.palette_frame,
                text=f"No blocks for '{self.current_language}'\n\nAdd blocks to:\nlanguages/{self.current_language}/blocks/",
                bg=DARK_PANEL,
                fg="#888888",
                font=("Segoe UI", 9),
                justify=tk.CENTER
            ).pack(pady=50)
            return
        
        for category in sorted(self.blocks_by_category.keys()):
            blocks_in_category = [
                b for b in self.blocks_by_category[category]
                if not search_term or search_term in b.display_name.lower() or 
                   search_term in getattr(b, "block_ui_description", {}).get("description", "").lower()
            ]
            
            if not blocks_in_category:
                continue
            
            # Category header
            category_header = tk.Frame(self.palette_frame, bg=DARK_PANEL)
            category_header.pack(fill=tk.X, pady=(10, 2))
            
            color = CATEGORY_COLORS.get(category, "#ffffff")
            
            tk.Label(
                category_header,
                text="▼",
                bg=DARK_PANEL,
                fg=color,
                font=("Segoe UI", 8)
            ).pack(side=tk.LEFT, padx=5)
            
            tk.Label(
                category_header,
                text=category.upper(),
                bg=DARK_PANEL,
                fg=color,
                font=("Segoe UI", 9, "bold")
            ).pack(side=tk.LEFT)
            
            tk.Label(
                category_header,
                text=f"({len(blocks_in_category)})",
                bg=DARK_PANEL,
                fg="#666666",
                font=("Segoe UI", 8)
            ).pack(side=tk.LEFT, padx=3)
            
            # Category blocks
            for block_module in sorted(blocks_in_category, key=lambda x: x.get("display_name", "") if isinstance(x, dict) else x.display_name):
                item = PaletteBlockItem(self.palette_frame, block_module, self.add_block_to_workspace)
                item.pack(fill=tk.X, pady=1)
    
    def refresh_palette(self):
        """Refresh the palette when language or search changes"""
        self.build_palette()
    
    def filter_palette(self, *args):
        """Filter palette based on search"""
        self.refresh_palette()
    
    def on_language_change(self, event=None):
        """Handle language change"""
        self.current_language = self.lang_var.get()
        self.load_blocks_for_language(self.current_language)
        self.load_and_merge_custom_blocks()  # Re-merge custom blocks
        self.refresh_palette()
        self.project_blocks.clear()
        self.refresh_workspace()
        self.update_generated_code()
    
    def add_language_dialog(self):
        """Prompt user to add a new language folder"""
        def create_language():
            new_lang = entry.get().strip().lower()
            if not new_lang:
                messagebox.showwarning("Invalid", "Language name cannot be empty.")
                return
            new_path = os.path.join(self.languages_path, new_lang)
            if os.path.exists(new_path):
                messagebox.showwarning("Exists", f"Language '{new_lang}' already exists.")
                return
            os.makedirs(os.path.join(new_path, "blocks"))
            messagebox.showinfo("Created", f"Language '{new_lang}' created.")
            dialog.destroy()
            
            # Refresh language list and select new language
            langs = list(self.lang_combo['values'])
            langs.append(new_lang)
            langs.sort()
            self.lang_combo['values'] = langs
            self.lang_var.set(new_lang)
            self.on_language_change()
        
        dialog = tk.Toplevel(self)
        dialog.title("Add New Language")
        dialog.geometry("300x120")
        dialog.configure(bg=DARK_PANEL)
        dialog.transient(self)
        dialog.grab_set()
        
        tk.Label(
            dialog,
            text="Enter language name:",
            bg=DARK_PANEL,
            fg=DARK_FG,
            font=("Segoe UI", 10)
        ).pack(pady=10)
        
        entry = tk.Entry(dialog, bg=DARK_BG, fg=DARK_FG, font=("Segoe UI", 10))
        entry.pack(pady=5, padx=10)
        entry.focus()
        
        btn_frame = tk.Frame(dialog, bg=DARK_PANEL)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Create", command=create_language).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        dialog.bind("<Return>", lambda e: create_language())
        dialog.bind("<Escape>", lambda e: dialog.destroy())
    
    def manage_custom_blocks_dialog(self):
        """Dialog to view, edit, and delete custom blocks"""
        dialog = tk.Toplevel(self)
        dialog.title("Manage Custom Blocks")
        dialog.geometry("700x600")
        dialog.configure(bg=DARK_PANEL)
        dialog.transient(self)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Header
        header = tk.Frame(dialog, bg="#ff6b9d", height=50)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="🔧 Manage Custom Blocks",
            bg="#ff6b9d",
            fg="#000000",
            font=("Segoe UI", 13, "bold")
        ).pack(side=tk.LEFT, padx=20, pady=15)
        
        tk.Label(
            header,
            text=f"{len(self.custom_blocks)} blocks",
            bg="#ff6b9d",
            fg="#000000",
            font=("Segoe UI", 9)
        ).pack(side=tk.RIGHT, padx=20)
        
        # Block list
        list_frame = tk.Frame(dialog, bg=DARK_PANEL)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        canvas = tk.Canvas(list_frame, bg=DARK_PANEL, highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        blocks_container = tk.Frame(canvas, bg=DARK_PANEL)
        
        blocks_container.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=blocks_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        def refresh_list():
            for widget in blocks_container.winfo_children():
                widget.destroy()
            
            if not self.custom_blocks:
                tk.Label(
                    blocks_container,
                    text="No custom blocks yet\n\nClick 'Create New Block' to get started",
                    bg=DARK_PANEL,
                    fg="#888888",
                    font=("Segoe UI", 10),
                    justify=tk.CENTER
                ).pack(pady=50)
                return
            
            for i, cblock in enumerate(self.custom_blocks):
                block_frame = tk.Frame(blocks_container, bg=DARK_BG, relief=tk.RAISED, borderwidth=1)
                block_frame.pack(fill=tk.X, pady=5, padx=5)
                
                # Block info
                info_frame = tk.Frame(block_frame, bg=DARK_BG)
                info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=8)
                
                tk.Label(
                    info_frame,
                    text=cblock.get("display_name", "Unnamed"),
                    bg=DARK_BG,
                    fg=DARK_FG,
                    font=("Segoe UI", 10, "bold"),
                    anchor="w"
                ).pack(anchor="w")
                
                params_text = ", ".join([p["name"] for p in cblock.get("params", [])])
                if params_text:
                    tk.Label(
                        info_frame,
                        text=f"Parameters: {params_text}",
                        bg=DARK_BG,
                        fg="#888888",
                        font=("Segoe UI", 8),
                        anchor="w"
                    ).pack(anchor="w")
                
                # Buttons
                btn_frame = tk.Frame(block_frame, bg=DARK_BG)
                btn_frame.pack(side=tk.RIGHT, padx=10, pady=8)
                
                def make_edit(idx):
                    return lambda: self.edit_custom_block(idx, dialog, refresh_list)
                
                def make_delete(idx):
                    return lambda: self.delete_custom_block(idx, refresh_list)
                
                tk.Button(
                    btn_frame,
                    text="✎ Edit",
                    bg="#4a9eff",
                    fg="white",
                    font=("Segoe UI", 9),
                    relief=tk.FLAT,
                    cursor="hand2",
                    command=make_edit(i)
                ).pack(side=tk.LEFT, padx=3)
                
                tk.Button(
                    btn_frame,
                    text="✕ Delete",
                    bg="#ff4757",
                    fg="white",
                    font=("Segoe UI", 9),
                    relief=tk.FLAT,
                    cursor="hand2",
                    command=make_delete(i)
                ).pack(side=tk.LEFT, padx=3)
        
        refresh_list()
        
        # Bottom buttons
        bottom_frame = tk.Frame(dialog, bg=DARK_PANEL)
        bottom_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        ttk.Button(
            bottom_frame,
            text="➕ Create New Block",
            command=lambda: [dialog.destroy(), self.create_custom_block_dialog()],
            style="Toolbar.TButton"
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            bottom_frame,
            text="Close",
            command=dialog.destroy,
            style="Toolbar.TButton"
        ).pack(side=tk.RIGHT, padx=5)
    
    def edit_custom_block(self, index, parent_dialog, refresh_callback):
        """Edit an existing custom block"""
        if index >= len(self.custom_blocks):
            return
        
        cblock = self.custom_blocks[index]
        
        edit_dialog = tk.Toplevel(parent_dialog)
        edit_dialog.title(f"Edit {cblock.get('display_name', 'Block')}")
        edit_dialog.geometry("650x550")
        edit_dialog.configure(bg=DARK_PANEL)
        edit_dialog.transient(parent_dialog)
        edit_dialog.grab_set()
        
        # Center dialog
        edit_dialog.update_idletasks()
        x = (edit_dialog.winfo_screenwidth() // 2) - (edit_dialog.winfo_width() // 2)
        y = (edit_dialog.winfo_screenheight() // 2) - (edit_dialog.winfo_height() // 2)
        edit_dialog.geometry(f"+{x}+{y}")
        
        # Header
        header = tk.Frame(edit_dialog, bg="#4a9eff", height=50)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="✎ Edit Custom Block",
            bg="#4a9eff",
            fg="white",
            font=("Segoe UI", 13, "bold")
        ).pack(side=tk.LEFT, padx=20, pady=15)
        
        # Form (same as create dialog)
        form_frame = tk.Frame(edit_dialog, bg=DARK_PANEL)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Block name
        tk.Label(
            form_frame,
            text="Block Name:",
            bg=DARK_PANEL,
            fg=DARK_FG,
            font=("Segoe UI", 9, "bold")
        ).grid(row=0, column=0, sticky="w", pady=8, padx=5)
        
        name_entry = tk.Entry(
            form_frame,
            bg=DARK_BG,
            fg=DARK_FG,
            font=("Segoe UI", 10),
            width=50
        )
        name_entry.grid(row=0, column=1, sticky="ew", pady=8, padx=5)
        name_entry.insert(0, cblock.get("display_name", ""))
        
        # Parameters
        tk.Label(
            form_frame,
            text="Parameters:",
            bg=DARK_PANEL,
            fg=DARK_FG,
            font=("Segoe UI", 9, "bold")
        ).grid(row=1, column=0, sticky="nw", pady=8, padx=5)
        
        params_text = tk.Text(
            form_frame,
            height=6,
            bg=DARK_BG,
            fg=DARK_FG,
            font=("Consolas", 9),
            relief=tk.FLAT,
            padx=8,
            pady=8
        )
        params_text.grid(row=1, column=1, sticky="ew", pady=8, padx=5)
        
        # Load existing params
        existing_params = "\n".join([f"{p['name']}:{p['type']}" for p in cblock.get("params", [])])
        params_text.insert("1.0", existing_params)
        
        # Code template
        tk.Label(
            form_frame,
            text="Code Template:",
            bg=DARK_PANEL,
            fg=DARK_FG,
            font=("Segoe UI", 9, "bold")
        ).grid(row=2, column=0, sticky="nw", pady=8, padx=5)
        
        template_text = tk.Text(
            form_frame,
            height=10,
            bg=DARK_BG,
            fg=DARK_FG,
            font=("Consolas", 9),
            relief=tk.FLAT,
            padx=8,
            pady=8
        )
        template_text.grid(row=2, column=1, sticky="ew", pady=8, padx=5)
        template_text.insert("1.0", cblock.get("code_template", ""))
        
        form_frame.columnconfigure(1, weight=1)
        
        # Buttons
        btn_frame = tk.Frame(edit_dialog, bg=DARK_PANEL)
        btn_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        def on_save():
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("Error", "Block name cannot be empty.")
                return
            
            # Parse parameters
            raw_params = params_text.get("1.0", tk.END).strip()
            params_list = []
            if raw_params:
                for line in raw_params.splitlines():
                    line = line.strip()
                    if not line:
                        continue
                    if ':' in line:
                        pname, ptype = line.split(':', 1)
                        params_list.append({
                            "name": pname.strip(),
                            "type": ptype.strip(),
                            "default": ""
                        })
            
            code_template = template_text.get("1.0", tk.END).strip()
            if not code_template:
                messagebox.showerror("Error", "Code template cannot be empty.")
                return
            
            # Update block
            self.custom_blocks[index]["display_name"] = name
            self.custom_blocks[index]["params"] = params_list
            self.custom_blocks[index]["code_template"] = code_template
            
            # Save and reload
            self.save_custom_blocks_data(self.custom_blocks)
            self.load_blocks_for_language(self.current_language)
            self.load_and_merge_custom_blocks()
            self.refresh_palette()
            
            refresh_callback()
            edit_dialog.destroy()
            messagebox.showinfo("Success", f"Block '{name}' updated!")
        
        ttk.Button(
            btn_frame,
            text="✓ Save Changes",
            command=on_save,
            style="Toolbar.TButton"
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame,
            text="✕ Cancel",
            command=edit_dialog.destroy,
            style="Toolbar.TButton"
        ).pack(side=tk.LEFT, padx=5)
    
    def delete_custom_block(self, index, refresh_callback):
        """Delete a custom block"""
        if index >= len(self.custom_blocks):
            return
        
        cblock = self.custom_blocks[index]
        block_name = cblock.get("display_name", "Unnamed")
        
        if messagebox.askyesno("Delete Block", f"Delete custom block '{block_name}'?\n\nThis cannot be undone."):
            self.custom_blocks.pop(index)
            self.save_custom_blocks_data(self.custom_blocks)
            
            # Reload blocks
            self.load_blocks_for_language(self.current_language)
            self.load_and_merge_custom_blocks()
            self.refresh_palette()
            
            refresh_callback()
            messagebox.showinfo("Deleted", f"Block '{block_name}' deleted.")
    
    def create_custom_block_dialog(self):
        """Dialog to create a custom block - simplified and user-friendly"""
        dialog = tk.Toplevel(self)
        dialog.title("Create Custom Block - Easy Guide")
        dialog.geometry("800x650")
        dialog.configure(bg=DARK_PANEL)
        dialog.transient(self)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Header
        header = tk.Frame(dialog, bg="#ff6b9d", height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="➕ Create Your Own Custom Block",
            bg="#ff6b9d",
            fg="#000000",
            font=("Segoe UI", 14, "bold")
        ).pack(side=tk.LEFT, padx=20, pady=10)
        
        tk.Label(
            header,
            text="✨ Make blocks for tasks you do often!",
            bg="#ff6b9d",
            fg="#000000",
            font=("Segoe UI", 9)
        ).pack(side=tk.LEFT, padx=10)
        
        # Main container with tabs
        main_frame = tk.Frame(dialog, bg=DARK_PANEL)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Left side - Form
        left_frame = tk.Frame(main_frame, bg=DARK_PANEL)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Step 1: Block Name
        step1 = tk.LabelFrame(
            left_frame,
            text="📝 Step 1: Give Your Block a Name",
            bg=DARK_PANEL,
            fg="#4ec9b0",
            font=("Segoe UI", 10, "bold"),
            labelanchor="n"
        )
        step1.pack(fill=tk.X, pady=10)
        
        tk.Label(
            step1,
            text="Example: 'Greet User', 'Draw Square', 'Calculate Total'",
            bg=DARK_PANEL,
            fg="#888888",
            font=("Segoe UI", 8, "italic")
        ).pack(anchor="w", padx=10, pady=(5, 0))
        
        name_entry = tk.Entry(
            step1,
            bg=DARK_BG,
            fg=DARK_FG,
            font=("Segoe UI", 11),
            relief=tk.FLAT,
            highlightthickness=2,
            highlightbackground="#4ec9b0",
            highlightcolor="#4ec9b0"
        )
        name_entry.pack(fill=tk.X, padx=10, pady=10, ipady=5)
        name_entry.insert(0, "My Custom Block")
        
        # Step 2: Parameters
        step2 = tk.LabelFrame(
            left_frame,
            text="🎯 Step 2: Add Inputs (Parameters) - Optional",
            bg=DARK_PANEL,
            fg="#ce9178",
            font=("Segoe UI", 10, "bold"),
            labelanchor="n"
        )
        step2.pack(fill=tk.X, pady=10)
        
        tk.Label(
            step2,
            text="One per line. Format: name:type\nLeave empty if your block doesn't need inputs!",
            bg=DARK_PANEL,
            fg="#888888",
            font=("Segoe UI", 8, "italic"),
            justify=tk.LEFT
        ).pack(anchor="w", padx=10, pady=(5, 0))
        
        # Quick add buttons
        quick_params_frame = tk.Frame(step2, bg=DARK_PANEL)
        quick_params_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(
            quick_params_frame,
            text="Quick add:",
            bg=DARK_PANEL,
            fg=DARK_FG,
            font=("Segoe UI", 8)
        ).pack(side=tk.LEFT, padx=5)
        
        params_text = tk.Text(
            step2,
            height=4,
            bg=DARK_BG,
            fg=DARK_FG,
            font=("Consolas", 10),
            relief=tk.FLAT,
            highlightthickness=2,
            highlightbackground="#ce9178",
            highlightcolor="#ce9178",
            padx=8,
            pady=8
        )
        params_text.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        def add_param_template(template):
            params_text.insert(tk.END, template + "\n")
        
        for template, label in [("message:string", "Text"), ("count:number", "Number"), ("enabled:boolean", "Yes/No")]:
            tk.Button(
                quick_params_frame,
                text=f"+ {label}",
                bg="#3a3a3a",
                fg=DARK_FG,
                font=("Segoe UI", 8),
                relief=tk.FLAT,
                cursor="hand2",
                command=lambda t=template: add_param_template(t)
            ).pack(side=tk.LEFT, padx=2)
        
        # Step 3: Code Template
        step3 = tk.LabelFrame(
            left_frame,
            text="💻 Step 3: Write Your Code Template",
            bg=DARK_PANEL,
            fg="#569cd6",
            font=("Segoe UI", 10, "bold"),
            labelanchor="n"
        )
        step3.pack(fill=tk.BOTH, expand=True, pady=10)
        
        tk.Label(
            step3,
            text="Use {{name}} to insert your parameters. Example: print({{message}})",
            bg=DARK_PANEL,
            fg="#888888",
            font=("Segoe UI", 8, "italic")
        ).pack(anchor="w", padx=10, pady=(5, 0))
        
        template_text = tk.Text(
            step3,
            bg=DARK_BG,
            fg=DARK_FG,
            font=("Consolas", 10),
            relief=tk.FLAT,
            highlightthickness=2,
            highlightbackground="#569cd6",
            highlightcolor="#569cd6",
            padx=8,
            pady=8,
            wrap=tk.WORD
        )
        template_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Right side - Examples and Help
        right_frame = tk.Frame(main_frame, bg=DARK_BG, width=300, relief=tk.RAISED, borderwidth=2)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        right_frame.pack_propagate(False)
        
        tk.Label(
            right_frame,
            text="📚 Examples & Help",
            bg=DARK_BG,
            fg="#dcdcaa",
            font=("Segoe UI", 11, "bold")
        ).pack(pady=10)
        
        examples_canvas = tk.Canvas(right_frame, bg=DARK_BG, highlightthickness=0)
        examples_scroll = ttk.Scrollbar(right_frame, orient="vertical", command=examples_canvas.yview)
        examples_container = tk.Frame(examples_canvas, bg=DARK_BG)
        
        examples_container.bind(
            "<Configure>",
            lambda e: examples_canvas.configure(scrollregion=examples_canvas.bbox("all"))
        )
        
        examples_canvas.create_window((0, 0), window=examples_container, anchor="nw")
        examples_canvas.configure(yscrollcommand=examples_scroll.set)
        
        examples_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        examples_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Example 1
        ex1_frame = tk.Frame(examples_container, bg="#2d2d30", relief=tk.RAISED, borderwidth=1)
        ex1_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(
            ex1_frame,
            text="Example 1: Simple Greeting",
            bg="#2d2d30",
            fg="#4ec9b0",
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", padx=8, pady=(5, 2))
        
        tk.Label(
            ex1_frame,
            text="Name: Greet User\n\nParameter:\nname:string\n\nCode:\nprint('Hello, {{name}}!')",
            bg="#2d2d30",
            fg="#cccccc",
            font=("Consolas", 8),
            justify=tk.LEFT
        ).pack(anchor="w", padx=8, pady=(0, 5))
        
        def load_example_1():
            name_entry.delete(0, tk.END)
            name_entry.insert(0, "Greet User")
            params_text.delete("1.0", tk.END)
            params_text.insert("1.0", "name:string")
            template_text.delete("1.0", tk.END)
            template_text.insert("1.0", "print('Hello, {{name}}!')")
        
        tk.Button(
            ex1_frame,
            text="📋 Load This Example",
            bg="#4ec9b0",
            fg="#000000",
            font=("Segoe UI", 8, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            command=load_example_1
        ).pack(pady=5)
        
        # Example 2
        ex2_frame = tk.Frame(examples_container, bg="#2d2d30", relief=tk.RAISED, borderwidth=1)
        ex2_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(
            ex2_frame,
            text="Example 2: Repeat Message",
            bg="#2d2d30",
            fg="#ce9178",
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", padx=8, pady=(5, 2))
        
        tk.Label(
            ex2_frame,
            text="Name: Repeat Print\n\nParameters:\nmsg:string\ntimes:number\n\nCode:\nfor i in range({{times}}):\n    print({{msg}})",
            bg="#2d2d30",
            fg="#cccccc",
            font=("Consolas", 8),
            justify=tk.LEFT
        ).pack(anchor="w", padx=8, pady=(0, 5))
        
        def load_example_2():
            name_entry.delete(0, tk.END)
            name_entry.insert(0, "Repeat Print")
            params_text.delete("1.0", tk.END)
            params_text.insert("1.0", "msg:string\ntimes:number")
            template_text.delete("1.0", tk.END)
            template_text.insert("1.0", "for i in range({{times}}):\n    print({{msg}})")
        
        tk.Button(
            ex2_frame,
            text="📋 Load This Example",
            bg="#ce9178",
            fg="#000000",
            font=("Segoe UI", 8, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            command=load_example_2
        ).pack(pady=5)
        
        # Example 3
        ex3_frame = tk.Frame(examples_container, bg="#2d2d30", relief=tk.RAISED, borderwidth=1)
        ex3_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(
            ex3_frame,
            text="Example 3: No Parameters",
            bg="#2d2d30",
            fg="#569cd6",
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", padx=8, pady=(5, 2))
        
        tk.Label(
            ex3_frame,
            text="Name: Draw Line\n\nParameters:\n(leave empty)\n\nCode:\nprint('=' * 50)",
            bg="#2d2d30",
            fg="#cccccc",
            font=("Consolas", 8),
            justify=tk.LEFT
        ).pack(anchor="w", padx=8, pady=(0, 5))
        
        def load_example_3():
            name_entry.delete(0, tk.END)
            name_entry.insert(0, "Draw Line")
            params_text.delete("1.0", tk.END)
            template_text.delete("1.0", tk.END)
            template_text.insert("1.0", "print('=' * 50)")
        
        tk.Button(
            ex3_frame,
            text="📋 Load This Example",
            bg="#569cd6",
            fg="#000000",
            font=("Segoe UI", 8, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            command=load_example_3
        ).pack(pady=5)
        
        # Tips
        tips_frame = tk.Frame(examples_container, bg="#3a3a3a", relief=tk.RAISED, borderwidth=1)
        tips_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(
            tips_frame,
            text="💡 Quick Tips",
            bg="#3a3a3a",
            fg="#dcdcaa",
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", padx=8, pady=(5, 2))
        
        tk.Label(
            tips_frame,
            text="• Use {{}} for parameters\n• Keep it simple at first\n• Test with examples\n• No parameters? Leave blank!",
            bg="#3a3a3a",
            fg="#aaaaaa",
            font=("Segoe UI", 8),
            justify=tk.LEFT
        ).pack(anchor="w", padx=8, pady=(0, 8))
        
        # Buttons
        btn_frame = tk.Frame(dialog, bg=DARK_PANEL)
        btn_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        def on_save():
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("Oops!", "Please give your block a name! 😊")
                return
            
            # Parse parameters
            raw_params = params_text.get("1.0", tk.END).strip()
            params_list = []
            if raw_params:
                for line in raw_params.splitlines():
                    line = line.strip()
                    if not line:
                        continue
                    if ':' in line:
                        pname, ptype = line.split(':', 1)
                        params_list.append({
                            "name": pname.strip(),
                            "type": ptype.strip(),
                            "default": ""
                        })
                    else:
                        # Default to string if no type specified
                        params_list.append({
                            "name": line.strip(),
                            "type": "string",
                            "default": ""
                        })
            
            code_template = template_text.get("1.0", tk.END).strip()
            if not code_template:
                messagebox.showerror("Oops!", "Please add some code for your block! 💻")
                return
            
            # Create new custom block
            new_block = {
                "block_id": "custom_" + str(uuid.uuid4())[:8],
                "display_name": name,
                "category": "Custom Blocks",
                "params": params_list,
                "code_template": code_template,
                "language": "all"
            }
            
            # Add to custom blocks list and save
            self.custom_blocks.append(new_block)
            self.save_custom_blocks_data(self.custom_blocks)
            
            # Create generate_code function
            def make_generate_code(template):
                def gen_code(params, children=None, lang=None):
                    code = template
                    for k, v in params.items():
                        code = code.replace(f"{{{{{k}}}}}", str(v))
                    return code + "\n"
                return gen_code
            
            new_block["generate_code"] = make_generate_code(new_block["code_template"])
            
            # Add to blocks dict and category
            self.blocks[new_block["block_id"]] = new_block
            self.blocks_by_category.setdefault("Custom Blocks", []).append(new_block)
            
            self.refresh_palette()
            messagebox.showinfo("Success! 🎉", f"Custom block '{name}' created!\n\nFind it in the 'Custom Blocks' category.")
            dialog.destroy()
        
        def on_cancel():
            dialog.destroy()
        
        tk.Button(
            btn_frame,
            text="✓ Create My Block!",
            bg="#4ec9b0",
            fg="#000000",
            font=("Segoe UI", 11, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            command=on_save,
            padx=20,
            pady=8
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="✕ Cancel",
            bg="#888888",
            fg="white",
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            cursor="hand2",
            command=on_cancel,
            padx=15,
            pady=8
        ).pack(side=tk.LEFT, padx=5)
        
        dialog.bind("<Escape>", lambda e: on_cancel())
        name_entry.focus_set()
        name_entry.select_range(0, tk.END)
    
    def add_block_to_workspace(self, block_module):
        """Add a block to the workspace"""
        # Check for special action blocks (like custom block creator)
        if isinstance(block_module, dict):
            special_action = block_module.get("special_action")
        else:
            special_action = getattr(block_module, "block_ui_description", {}).get("special_action")
        
        # Handle special blocks
        if special_action == "create_custom_block":
            self.create_custom_block_dialog()
            return
        elif special_action == "manage_custom_blocks":
            self.manage_custom_blocks_dialog()
            return
        
        # Normal block adding
        if isinstance(block_module, dict):
            default_params_func = lambda: {p["name"]: p.get("default", "") for p in block_module.get("params", [])}
        else:
            default_params_func = getattr(block_module, "default_params", None)
        
        params = default_params_func() if (default_params_func and callable(default_params_func)) else {}
        self.edit_block_params(block_module, params, add_mode=True)
    
    def edit_block_params(self, block_module, current_params, add_mode=True, index=None):
        """Show dialog to edit block parameters"""
        # Handle both dict (custom blocks) and module objects
        if isinstance(block_module, dict):
            block_id = block_module.get("block_id", "unknown")
            display_name = block_module.get("display_name", "Unknown")
            category = block_module.get("category", "Basic")
            description = block_module.get("description", "")
            block_params = block_module.get("params", [])
        else:
            block_id = getattr(block_module, "block_id", "unknown")
            display_name = getattr(block_module, "display_name", "Unknown")
            category = getattr(block_module, "category", "Basic")
            description = getattr(block_module, "block_ui_description", {}).get("description", "")
            block_params = getattr(block_module, "params", [])
        
        dialog = tk.Toplevel(self)
        dialog.title(f"{'Add' if add_mode else 'Edit'} {display_name}")
        dialog.geometry("500x450")
        dialog.configure(bg=DARK_PANEL)
        dialog.transient(self)
        dialog.grab_set()
        
        # Header
        header_color = CATEGORY_COLORS.get(category, DARK_ACCENT)
        
        header = tk.Frame(dialog, bg=header_color, height=50)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text=f"⚙ {display_name}",
            bg=header_color,
            fg="#000000",
            font=("Segoe UI", 13, "bold")
        ).pack(side=tk.LEFT, padx=20, pady=15)
        
        tk.Label(
            header,
            text=category,
            bg=header_color,
            fg="#000000",
            font=("Segoe UI", 9)
        ).pack(side=tk.RIGHT, padx=20)
        
        # Description
        if description:
            desc_frame = tk.Frame(dialog, bg=DARK_BG)
            desc_frame.pack(fill=tk.X, padx=20, pady=10)
            
            tk.Label(
                desc_frame,
                text=description,
                bg=DARK_BG,
                fg="#aaaaaa",
                font=("Segoe UI", 9),
                wraplength=450,
                justify=tk.LEFT
            ).pack(anchor="w")
        
        # Parameters
        params_container = tk.Frame(dialog, bg=DARK_PANEL)
        params_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        params_canvas = tk.Canvas(params_container, bg=DARK_PANEL, highlightthickness=0)
        params_scroll = ttk.Scrollbar(params_container, orient="vertical", command=params_canvas.yview)
        params_frame = tk.Frame(params_canvas, bg=DARK_PANEL)
        
        params_frame.bind(
            "<Configure>",
            lambda e: params_canvas.configure(scrollregion=params_canvas.bbox("all"))
        )
        
        params_canvas.create_window((0, 0), window=params_frame, anchor="nw")
        params_canvas.configure(yscrollcommand=params_scroll.set)
        
        params_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        params_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        param_widgets = {}
        
        for i, param in enumerate(block_params):
            name = param["name"]
            param_type = param.get("type", "string")
            
            row_frame = tk.Frame(params_frame, bg=DARK_PANEL)
            row_frame.pack(fill=tk.X, pady=6)
            
            label_frame = tk.Frame(row_frame, bg=DARK_PANEL)
            label_frame.pack(fill=tk.X)
            
            tk.Label(
                label_frame,
                text=f"{name}:",
                bg=DARK_PANEL,
                fg=DARK_FG,
                font=("Segoe UI", 9, "bold")
            ).pack(side=tk.LEFT)
            
            tk.Label(
                label_frame,
                text=f"({param_type})",
                bg=DARK_PANEL,
                fg="#888888",
                font=("Segoe UI", 8)
            ).pack(side=tk.LEFT, padx=5)
            
            entry = tk.Entry(
                row_frame,
                bg=DARK_BG,
                fg=DARK_FG,
                insertbackground=DARK_FG,
                font=("Consolas", 10),
                relief=tk.FLAT,
                highlightthickness=1,
                highlightbackground=DARK_BORDER,
                highlightcolor=header_color
            )
            entry.pack(fill=tk.X, pady=(3, 0), ipady=4)
            entry.insert(0, current_params.get(name, param.get("default", "")))
            param_widgets[name] = entry
        
        # Buttons
        btn_frame = tk.Frame(dialog, bg=DARK_PANEL)
        btn_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        def on_save():
            new_params = {name: w.get() for name, w in param_widgets.items()}
            if add_mode:
                self.project_blocks.append((block_id, new_params))
            else:
                self.project_blocks[index] = (block_id, new_params)
            self.refresh_workspace()
            dialog.destroy()
        
        def on_cancel():
            dialog.destroy()
        
        ttk.Button(btn_frame, text="✓ Save & Add" if add_mode else "✓ Save Changes", 
                  command=on_save, style="Toolbar.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="✕ Cancel", command=on_cancel, 
                  style="Toolbar.TButton").pack(side=tk.LEFT, padx=5)
        
        dialog.bind("<Return>", lambda e: on_save())
        dialog.bind("<Escape>", lambda e: on_cancel())
        
        if param_widgets:
            list(param_widgets.values())[0].focus_set()
    
    def delete_block(self, index):
        """Delete a block from the workspace"""
        if 0 <= index < len(self.project_blocks):
            block_id, _ = self.project_blocks[index]
            block_name = self.blocks.get(block_id).display_name if self.blocks.get(block_id) else "Block"
            if messagebox.askyesno("Delete Block", f"Remove '{block_name}' from workspace?"):
                self.project_blocks.pop(index)
                self.refresh_workspace()
    
    def edit_block(self, index):
        """Edit an existing block"""
        if 0 <= index < len(self.project_blocks):
            block_id, params = self.project_blocks[index]
            block_module = self.blocks.get(block_id)
            if block_module:
                self.edit_block_params(block_module, params, add_mode=False, index=index)
    
    def move_block_up(self, index):
        """Move block up in sequence"""
        if index > 0:
            self.project_blocks[index], self.project_blocks[index-1] = \
                self.project_blocks[index-1], self.project_blocks[index]
            self.refresh_workspace()
    
    def move_block_down(self, index):
        """Move block down in sequence"""
        if index < len(self.project_blocks) - 1:
            self.project_blocks[index], self.project_blocks[index+1] = \
                self.project_blocks[index+1], self.project_blocks[index]
            self.refresh_workspace()
    
    def show_empty_state(self):
        """Show empty workspace message"""
        self.empty_label = tk.Label(
            self.workspace_frame,
            text="👈 Click blocks in palette to add them here",
            bg=DARK_BG,
            fg="#555555",
            font=("Segoe UI", 12, "italic")
        )
        self.empty_label.pack(expand=True, pady=150)
    
    def refresh_workspace(self):
        """Refresh the visual workspace"""
        for widget in self.workspace_frame.winfo_children():
            widget.destroy()
        
        if not self.project_blocks:
            self.show_empty_state()
        else:
            for i, (block_id, params) in enumerate(self.project_blocks):
                block_module = self.blocks.get(block_id)
                if block_module:
                    block_widget = BlockWidget(
                        self.workspace_frame,
                        block_id,
                        block_module,
                        params,
                        i,
                        self.delete_block,
                        self.edit_block,
                        self.move_block_up,
                        self.move_block_down
                    )
                    block_widget.pack(fill=tk.X, pady=4, padx=10)
        
        count = len(self.project_blocks)
        self.block_count_label.config(text=f"{count} block{'s' if count != 1 else ''}")
        self.update_generated_code()
    
    def update_generated_code(self):
        """Generate code from current project blocks"""
        lang = self.lang_var.get()
        code = ""
        
        for block_id, params in self.project_blocks:
            module = self.blocks.get(block_id)
            if not module:
                code += f"# ERROR: Block '{block_id}' not found\n"
                continue
            
            try:
                code += module.generate_code(params, [], lang=lang)
            except Exception as e:
                code += f"# ERROR generating block '{block_id}': {e}\n"
        
        self.code_text.delete(1.0, tk.END)
        if code:
            self.code_text.insert(tk.END, code)
        else:
            self.code_text.insert(tk.END, "# No code generated yet\n# Add blocks from the palette!")
        
        line_count = len([l for l in code.split('\n') if l.strip()])
        self.line_count_label.config(text=f"{line_count} lines")
    
    def save_project(self):
        """Save project to JSON"""
        if not self.project_blocks:
            messagebox.showinfo("Nothing to Save", "Add some blocks first!")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("Blockline Project", "*.json"), ("All Files", "*.*")],
            title="Save Blockline Project"
        )
        if filename:
            try:
                project_data = {
                    "language": self.current_language,
                    "blocks": self.project_blocks
                }
                with open(filename, 'w') as f:
                    json.dump(project_data, f, indent=2)
                messagebox.showinfo("Saved", f"Project saved to:\n{filename}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save: {e}")
    
    def load_project(self):
        """Load project from JSON"""
        filename = filedialog.askopenfilename(
            filetypes=[("Blockline Project", "*.json"), ("All Files", "*.*")],
            title="Load Blockline Project"
        )
        if filename:
            try:
                with open(filename, 'r') as f:
                    project_data = json.load(f)
                
                # Handle old format (just blocks array) or new format (with language)
                if isinstance(project_data, list):
                    self.project_blocks = project_data
                else:
                    saved_lang = project_data.get("language", "python")
                    if saved_lang != self.current_language:
                        self.lang_var.set(saved_lang)
                        self.on_language_change()
                    self.project_blocks = project_data.get("blocks", [])
                
                self.refresh_workspace()
                messagebox.showinfo("Loaded", f"Project loaded from:\n{filename}")
            except Exception as e:
                messagebox.showerror("Load Error", f"Failed to load: {e}")
    
    def export_code(self):
        """Export generated code to file"""
        code = self.code_text.get(1.0, tk.END).strip()
        if not code or code.startswith("# No code"):
            messagebox.showinfo("Nothing to Export", "Generate some code first!")
            return
        
        lang = self.lang_var.get()
        ext_map = {"python": ".py", "cpp": ".cpp", "javascript": ".js", "rust": ".rs"}
        ext = ext_map.get(lang, ".txt")
        
        filename = filedialog.asksaveasfilename(
            defaultextension=ext,
            filetypes=[("Source Code", f"*{ext}"), ("All Files", "*.*")],
            title=f"Export {lang.title()} Code"
        )
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(code)
                messagebox.showinfo("Exported", f"Code exported to:\n{filename}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export: {e}")
    
    def run_in_terminal(self):
        """Run code in external terminal"""
        code = self.code_text.get(1.0, tk.END).strip()
        if not code or code.startswith("# No code"):
            messagebox.showwarning("No Code", "Generate some code first!")
            return
        
        if self.lang_var.get() != "python":
            messagebox.showinfo("Python Only", "Terminal execution only supports Python.\nUse 'Export & Run' for other languages.")
            return
        
        try:
            # Create temp file
            temp_file = os.path.join(os.getcwd(), "temp_blockline_script.py")
            with open(temp_file, 'w') as f:
                f.write(code)
            
            # Run in terminal based on OS
            if os.name == 'nt':  # Windows
                subprocess.Popen(['cmd', '/K', 'python', temp_file])
            else:  # macOS/Linux
                subprocess.Popen(['gnome-terminal', '--', 'python3', temp_file])
            
            messagebox.showinfo("Running", "Script is running in terminal!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open terminal:\n{e}")
    
    def open_in_vscode(self):
        """Open generated code in VS Code"""
        code = self.code_text.get(1.0, tk.END).strip()
        if not code or code.startswith("# No code"):
            messagebox.showwarning("No Code", "Generate some code first!")
            return
        
        try:
            lang = self.lang_var.get()
            ext_map = {"python": ".py", "cpp": ".cpp", "javascript": ".js", "rust": ".rs"}
            ext = ext_map.get(lang, ".txt")
            
            # Create a temp file
            temp_file = os.path.join(os.getcwd(), f"blockline_script{ext}")
            with open(temp_file, 'w') as f:
                # Add header comment
                f.write(f"# Generated by Blockline - by domore100\n")
                f.write(f"# Language: {lang}\n")
                f.write(f"# Project blocks: {len(self.project_blocks)}\n\n")
                f.write(code)
            
            # Try to open in VS Code
            try:
                subprocess.Popen(['code', temp_file])
                messagebox.showinfo("VS Code", f"Opening in VS Code!\n\nFile: {temp_file}")
            except FileNotFoundError:
                # VS Code not in PATH, try full path
                if os.name == 'nt':  # Windows
                    vscode_path = os.path.expandvars(r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe")
                    if os.path.exists(vscode_path):
                        subprocess.Popen([vscode_path, temp_file])
                        messagebox.showinfo("VS Code", f"Opening in VS Code!\n\nFile: {temp_file}")
                    else:
                        raise FileNotFoundError("VS Code not found")
                else:
                    raise FileNotFoundError("VS Code not found")
        except FileNotFoundError:
            messagebox.showerror(
                "VS Code Not Found",
                "Could not find VS Code.\n\nPlease install VS Code or add it to your PATH.\n\nAlternatively, use 'Export Code' to save the file manually."
            )
        except Exception as e:
            messagebox.showerror("Error", f"Could not open VS Code:\n{e}")
    
    def export_and_run(self):
        """Export code and provide run instructions"""
        code = self.code_text.get(1.0, tk.END).strip()
        if not code or code.startswith("# No code"):
            messagebox.showwarning("No Code", "Generate some code first!")
            return
        
        lang = self.lang_var.get()
        ext_map = {"python": ".py", "cpp": ".cpp", "javascript": ".js", "rust": ".rs"}
        ext = ext_map.get(lang, ".txt")
        
        filename = filedialog.asksaveasfilename(
            defaultextension=ext,
            filetypes=[("Source Code", f"*{ext}"), ("All Files", "*.*")],
            title=f"Export {lang.title()} Code"
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(f"# Generated by Blockline - by domore100\n")
                    f.write(f"# Language: {lang}\n\n")
                    f.write(code)
                
                # Provide run instructions
                run_instructions = {
                    "python": f"python {os.path.basename(filename)}",
                    "cpp": f"g++ {os.path.basename(filename)} -o output && ./output",
                    "javascript": f"node {os.path.basename(filename)}",
                    "rust": f"rustc {os.path.basename(filename)} && ./output"
                }
                
                instruction = run_instructions.get(lang, f"Run with appropriate compiler/interpreter")
                
                messagebox.showinfo(
                    "Exported!",
                    f"Code exported to:\n{filename}\n\nTo run:\n{instruction}"
                )
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export: {e}")
        """Execute generated Python code in a thread to prevent freezing"""
        code = self.code_text.get(1.0, tk.END).strip()
        if not code or code.startswith("# No code"):
            messagebox.showwarning("No Code", "Generate some code first!")
            return
        
        if self.lang_var.get() != "python":
            messagebox.showinfo("Python Only", "Only Python code can be run directly.\nExport and compile/run externally.")
            return
        
        # Create output window
        output_window = tk.Toplevel(self)
        output_window.title("Program Output")
        output_window.geometry("700x500")
        output_window.configure(bg=DARK_BG)
        
        # Header
        header = tk.Frame(output_window, bg=DARK_ACCENT, height=40)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="▶ Program Output",
            bg=DARK_ACCENT,
            fg="white",
            font=("Segoe UI", 12, "bold")
        ).pack(side=tk.LEFT, padx=15, pady=10)
        
        # Output text
        output_text = tk.Text(
            output_window,
            bg="#1e1e1e",
            fg="#00ff00",
            font=("Consolas", 10),
            padx=15,
            pady=15,
            wrap=tk.WORD
        )
        output_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Run in thread to prevent UI freezing
        def execute_code():
            import sys
            from io import StringIO
            
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            old_stdin = sys.stdin
            
            sys.stdout = StringIO()
            sys.stderr = StringIO()
            
            # Create a custom input handler
            input_buffer = []
            
            def custom_input(prompt=""):
                # Schedule input dialog on main thread
                result = []
                def show_input():
                    user_input = tk.simpledialog.askstring("Input", prompt, parent=output_window)
                    result.append(user_input if user_input is not None else "")
                
                output_window.after(0, show_input)
                # Wait for result
                while not result:
                    import time
                    time.sleep(0.1)
                return result[0]
            
            # Replace built-in input
            import builtins
            old_input = builtins.input
            builtins.input = custom_input
            
            try:
                exec(code, {"__builtins__": builtins})
                stdout_output = sys.stdout.getvalue()
                stderr_output = sys.stderr.getvalue()
                
                def update_output():
                    if stdout_output:
                        output_text.insert(tk.END, stdout_output)
                    if stderr_output:
                        output_text.insert(tk.END, f"\n--- Errors ---\n{stderr_output}", "error")
                        output_text.tag_config("error", foreground="#ff5555")
                    if not stdout_output and not stderr_output:
                        output_text.insert(tk.END, "✓ Program executed successfully (no output)")
                
                output_window.after(0, update_output)
                
            except Exception as e:
                def show_error():
                    output_text.insert(tk.END, f"❌ Runtime Error:\n{str(e)}", "error")
                    output_text.tag_config("error", foreground="#ff5555")
                
                output_window.after(0, show_error)
                
            finally:
                sys.stdout = old_stdout
                sys.stderr = old_stderr
                sys.stdin = old_stdin
                builtins.input = old_input
        
        # Start execution in thread
        thread = threading.Thread(target=execute_code, daemon=True)
        thread.start()
    
    def run_code(self):
        """Execute generated Python code in a thread to prevent freezing - runs in Blockline"""
        code = self.code_text.get(1.0, tk.END).strip()
        if not code or code.startswith("# No code"):
            messagebox.showwarning("No Code", "Generate some code first!")
            return
        
        if self.lang_var.get() != "python":
            messagebox.showinfo("Python Only", "Blockline can only run Python code directly.\n\nFor other languages:\n• Use '🖥️ Run in Terminal'\n• Or '📝 Open in VS Code'")
            return
        
        # Create output window
        output_window = tk.Toplevel(self)
        output_window.title("Program Output")
        output_window.geometry("700x500")
        output_window.configure(bg=DARK_BG)
        
        # Header
        header = tk.Frame(output_window, bg=DARK_ACCENT, height=40)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="▶ Program Output",
            bg=DARK_ACCENT,
            fg="white",
            font=("Segoe UI", 12, "bold")
        ).pack(side=tk.LEFT, padx=15, pady=10)
        
        # Output text
        output_text = tk.Text(
            output_window,
            bg="#1e1e1e",
            fg="#00ff00",
            font=("Consolas", 10),
            padx=15,
            pady=15,
            wrap=tk.WORD
        )
        output_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Run in thread to prevent UI freezing
        def execute_code():
            import sys
            from io import StringIO
            
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            old_stdin = sys.stdin
            
            sys.stdout = StringIO()
            sys.stderr = StringIO()
            
            # Create a custom input handler
            input_buffer = []
            
            def custom_input(prompt=""):
                # Schedule input dialog on main thread
                result = []
                def show_input():
                    user_input = tk.simpledialog.askstring("Input", prompt, parent=output_window)
                    result.append(user_input if user_input is not None else "")
                
                output_window.after(0, show_input)
                # Wait for result
                while not result:
                    import time
                    time.sleep(0.1)
                return result[0]
            
            # Replace built-in input
            import builtins
            old_input = builtins.input
            builtins.input = custom_input
            
            try:
                exec(code, {"__builtins__": builtins})
                stdout_output = sys.stdout.getvalue()
                stderr_output = sys.stderr.getvalue()
                
                def update_output():
                    if stdout_output:
                        output_text.insert(tk.END, stdout_output)
                    if stderr_output:
                        output_text.insert(tk.END, f"\n--- Errors ---\n{stderr_output}", "error")
                        output_text.tag_config("error", foreground="#ff5555")
                    if not stdout_output and not stderr_output:
                        output_text.insert(tk.END, "✓ Program executed successfully (no output)")
                
                output_window.after(0, update_output)
                
            except Exception as e:
                def show_error():
                    output_text.insert(tk.END, f"❌ Runtime Error:\n{str(e)}", "error")
                    output_text.tag_config("error", foreground="#ff5555")
                
                output_window.after(0, show_error)
                
            finally:
                sys.stdout = old_stdout
                sys.stderr = old_stderr
                sys.stdin = old_stdin
                builtins.input = old_input
        
        # Start execution in thread
        thread = threading.Thread(target=execute_code, daemon=True)
        thread.start()
    
    def clear_all(self):
        """Clear all blocks"""
        if not self.project_blocks:
            return
        if messagebox.askyesno("Clear Workspace", f"Remove all {len(self.project_blocks)} blocks?"):
            self.project_blocks.clear()
            self.refresh_workspace()

def start_ui(blocks=None, initial_lang="python", languages_path="languages"):
    """Start the Blockline UI"""
    app = BlocklineUI(initial_lang=initial_lang, languages_path=languages_path)
    app.mainloop()