block_id = "range_function"
display_name = "Range"
category = "Functions"
params = [
    {"name": "result", "type": "string", "default": "numbers"},
    {"name": "start", "type": "number", "default": "0"},
    {"name": "stop", "type": "number", "default": "10"},
    {"name": "step", "type": "number", "default": "1"}
]

def default_params():
    return {"result": "numbers", "start": "0", "stop": "10", "step": "1"}

def generate_code(params, children, lang="python"):
    if lang.lower().startswith("py"):
        result = params.get("result", "numbers")
        start = params.get("start", "0")
        stop = params.get("stop", "10")
        step = params.get("step", "1")
        if step == "1":
            return f'{result} = range({start}, {stop})\n'
        return f'{result} = range({start}, {stop}, {step})\n'
    return ""

block_ui_description = {
    "label": "Range",
    "params": params,
    "category": "Functions",
    "description": "Creates a range of numbers"
}


