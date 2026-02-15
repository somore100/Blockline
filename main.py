from ui import start_ui
from engine.loader import load_blocks_from_folder
import subprocess
import platform
from pathlib import Path
from tkinter import messagebox

class PromptBuilderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Prompt Builder — Duo + Sex + Video Support")
        self.root.geometry("1300x800")

        self.script_dir = Path(__file__).parent.resolve()

        # Load logo image (replace 'logo.png' with your file name)
        try:
            logo_path = self.script_dir / "logo.png"
            self.logo_img = tk.PhotoImage(file=str(logo_path))
        except Exception as e:
            print(f"Failed to load logo: {e}")
            self.logo_img = None

        # ... [existing init code] ...

        self.build_ui()
        self.refresh_ui()

    def build_ui(self):
        # ... [existing UI code] ...

        # Add logo and author label at top-left above left_frame
        top_frame = ttk.Frame(self.root)
        top_frame.pack(side=tk.TOP, fill=tk.X)

        if self.logo_img:
            logo_label = ttk.Label(top_frame, image=self.logo_img)
            logo_label.pack(side=tk.LEFT, padx=10, pady=5)

        author_label = ttk.Label(top_frame, text="Made by domore100", font=("Arial", 10, "italic"))
        author_label.pack(side=tk.LEFT, padx=10, pady=10)

        # Main frame below top_frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0,10))

        # Replace the previous main_frame assignment with this new one
        # Left and right frame setup continues here as before...

        # [Then place your left_frame and right_frame inside main_frame as before]

        # Build the left_frame and right_frame as previously coded
        left_frame = ttk.Frame(main_frame, width=600)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, expand=False)

        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # ... rest of UI widgets building here ...

        # Add Run button + side menu next to it in right_frame or bottom-right corner
        btn_frame = ttk.Frame(right_frame)
        btn_frame.pack(fill=tk.X, pady=10)

        gen_btn = ttk.Button(btn_frame, text="Generate Prompt", command=self.generate_prompt)
        gen_btn.pack(side=tk.LEFT, padx=5)

        copy_pos_btn = ttk.Button(btn_frame, text="Copy Positive", command=self.copy_positive)
        copy_pos_btn.pack(side=tk.LEFT, padx=5)

        copy_neg_btn = ttk.Button(btn_frame, text="Copy Negative", command=self.copy_negative)
        copy_neg_btn.pack(side=tk.LEFT, padx=5)

        # Run button with menu
        self.run_btn = ttk.Menubutton(btn_frame, text="Run", direction="below")
        self.run_btn.pack(side=tk.LEFT, padx=20)

        menu = tk.Menu(self.run_btn, tearoff=False)
        menu.add_command(label="Run Locally (Terminal)", command=self.run_locally)
        menu.add_command(label="Open in VS Code", command=self.open_in_vscode)
        self.run_btn["menu"] = menu

    def run_locally(self):
        # Opens terminal in script dir and runs python main.py
        script_path = str(self.script_dir / "main.py")
        try:
            if platform.system() == "Windows":
                subprocess.Popen(["start", "cmd", "/k", f"cd /d {self.script_dir} && python {script_path}"], shell=True)
            elif platform.system() == "Darwin":  # macOS
                subprocess.Popen(["open", "-a", "Terminal", self.script_dir])
            else:  # Linux
                subprocess.Popen(["x-terminal-emulator", "-e", f"bash -c 'cd \"{self.script_dir}\"; python main.py; exec bash'"])
        except Exception as e:
            messagebox.showerror("Run Error", f"Failed to run locally: {e}")

    def open_in_vscode(self):
        # Opens this script in VS Code
        script_path = str(self.script_dir / "main.py")
        try:
            subprocess.Popen(["code", script_path])
        except Exception as e:
            messagebox.showerror("VS Code Error", f"Failed to open VS Code: {e}")

    # ... rest of your class and methods ...

def main():
    print("Starting Blockline...")

    blocks = load_blocks_from_folder("languages/python/blocks")
    print(f"Loaded {len(blocks)} blocks:")
    for block_id in blocks:
        display_name = getattr(blocks[block_id], "display_name", "Unknown")
        print(f" - {block_id} ({display_name})")

    start_ui(blocks)

if __name__ == "__main__":
    main()
