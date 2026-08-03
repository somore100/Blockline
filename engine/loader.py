import importlib.util
import pathlib


def load_blocks_from_folder(folder_path, verbose=False):
    """
    Discover and load all Python block modules from the given folder path
    (recursively). Returns a dict mapping block_id -> loaded module.
    """
    registry = {}
    folder_path = pathlib.Path(folder_path)

    if not folder_path.exists():
        if verbose:
            print(f"⚠ Blocks folder does not exist: {folder_path.resolve()}")
        return registry

    if verbose:
        print(f"Loading blocks from: {folder_path.resolve()}")

    for path in sorted(folder_path.rglob("*.py")):
        if path.name.startswith("__"):
            continue  # skip __init__.py and other special files

        if verbose:
            print(f"Checking file: {path}")

        spec = importlib.util.spec_from_file_location(path.stem, path)
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
        except Exception as e:
            print(f"✗ Failed to load block file '{path}': {e}")
            continue

        if hasattr(module, "block_id"):
            if verbose:
                print(f"Loaded block: {module.block_id}")
            registry[module.block_id] = module
        else:
            print(f"⚠ Module {path} missing 'block_id', skipped.")

    return registry


def load_blocks_for_language(lang, languages_root="languages", core_folder=None):
    """
    Load blocks for a specific language, following the fallback rule from
    the spec: language-specific blocks (languages/<lang>/blocks/) take
    priority; anything not overridden there falls back to the shared
    core blocks folder, if one is given.
    """
    registry = {}

    if core_folder:
        registry.update(load_blocks_from_folder(core_folder))

    lang_folder = pathlib.Path(languages_root) / lang / "blocks"
    registry.update(load_blocks_from_folder(lang_folder))

    return registry
