block_id = "csharp_using"
display_name = "Using Directive"
category = "Modules"

params = [
    {"name": "namespace", "type": "string", "default": "System"}
]

def default_params():
    return {"namespace": "System"}

def generate_code(params, children, lang="csharp"):
    return f"using {params.get('namespace', 'System')};\n"

block_ui_description = {
    "label": "Using Directive",
    "params": params,
    "category": "Modules",
    "description": "Imports a namespace (e.g. System, System.Collections.Generic)."
}
