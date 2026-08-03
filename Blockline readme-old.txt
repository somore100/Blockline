📘 README.md

# 🚀 Blockline Blockline is a visual block-based programming environment made by domore100. It allows users to create programs using draggable blocks and generate real code (Python, C++, and more in the future). --- ## ✨ Features - 🧱 Block-based programming system - 🐍 Python support (runs inside computer 💻 C++ language structure support - ➕ Custom blocks (per language) - 🗂 Automatic block loading system - 💾 Save system - 🖼 Built-in logo and branding - ▶ Run options: - Run inside app (Python) - Run locally (terminal) - Open in VS Code --- ## 📂 Project Structure 

blockline/ │ ├── main.py ├── ui.py ├── logo.jpg ├── README.md │ ├── engine/ │ └── loader.py │ ├── languages/ │ ├── python/ │ └── cpp/ │ ├── user_data/ │ └── (custom blocks stored here)

--- ## ▶ Running From Source Make sure Python 3.10+ is installed. Install required libraries: 

pip install pillow

Run: 

python main.py

--- ## 🏗 Building EXE Inside project folder: 

pyinstaller --onefile --windowed ^ --add-data "logo.jpg;." ^ --add-data "engine;engine" ^ --add-data "languages;languages" ^ --add-data "user_data;user_data" ^ main.py

The executable will be created in: 

dist/main.exe

--- ## 🧠 Custom Blocks Custom blocks: - Are saved per language - Are stored inside `user_data/` - Allow raw code definition - Support input variables --- ## 🛠 Requirements - Python 3.10+ - Pillow - PyInstaller (for building exe) - VS Code (optional for editor feature) --- ## 👨‍💻 Author Made by **domore100** --- ## 📌 Future Plans - More languages - Block marketplace - Better UI - Export as standalone scripts - Installer version - Auto-updater ---
