import importlib.util
import pathlib

def load_blocks_from_folder(folder_path):
    """
    Discover and load all Python block modules from the given folder path.
    Returns a dictionary mapping block_id to the loaded module.
    """
    registry = {}
    folder_path = pathlib.Path(folder_path)

    for path in folder_path.rglob("*.py"):
        if path.name.startswith("__"):
            continue  # skip __init__.py and other special files

        spec = importlib.util.spec_from_file_location(path.stem, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if hasattr(module, "block_id"):
            registry[module.block_id] = module
        else:
            print(f"Warning: module {path} missing 'block_id', skipped.")

    return registry

def load_blocks_from_folder(folder_path):
    registry = {}
    folder_path = pathlib.Path(folder_path)
    print(f"Loading blocks from: {folder_path.resolve()}")

    for path in folder_path.rglob("*.py"):
        print(f"Checking file: {path}")
        if path.name.startswith("__"):
            continue

        spec = importlib.util.spec_from_file_location(path.stem, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if hasattr(module, "block_id"):
            print(f"Loaded block: {module.block_id}")
            registry[module.block_id] = module
        else:
            print(f"Warning: module {path} missing 'block_id', skipped.")

    return registry
