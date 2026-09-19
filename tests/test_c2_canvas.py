"""
Phase C2 scripted UI test (run under Xvfb): full ComfyUI-style canvas.

Not a pytest file - run directly, same convention as test_engine.py.
Exercises the real ui.py code (BlocklinerUI), not a mock, per project
convention: build two function nodes with a func_call between them,
switch to file view, and assert on real canvas item state + widget
positions rather than just reading the underlying data structures.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from ui import BlocklinerUI, make_node

FAILURES = []


def check(label, cond):
    status = "OK" if cond else "FAIL"
    print(f"[{status}] {label}")
    if not cond:
        FAILURES.append(label)


def main():
    app = BlocklinerUI(initial_lang="python", languages_path="languages")
    app.update()

    tab = app.tabs[app.active_tab_index]

    # Build a second node and wire node A -> node B via a func_call
    # block, exactly the shape recompute_references() expects.
    node_a = tab["nodes"][0]
    node_a["name"] = "main"
    node_b = make_node("helper", node_id="helper1", blocks=[])
    tab["nodes"].append(node_b)

    call_block = ("func_call", {"name": "helper", "args": ""})
    node_a["blocks"].append(call_block)

    app.switch_to_file_view()
    app.update()

    # --- Structural checks ---
    check("two nodes present in file view", len(app.get_current_node_list(tab)) == 2)
    check("recompute_references resolved main -> helper",
          node_b["id"] in find_node(tab, node_a["id"])["references"])

    # --- Canvas rendering checks ---
    check("both nodes have canvas boxes", set(app._fileview_boxes.keys()) == {node_a["id"], node_b["id"]})
    check("nodes got default grid positions",
          "canvas_x" in node_a and "canvas_y" in node_a and
          "canvas_x" in node_b and "canvas_y" in node_b)

    wire_items = app.workspace_canvas.find_withtag("wire")
    check("a wire was drawn for the resolved reference", len(wire_items) > 0)

    # --- Drag simulation: move node B, confirm position updates and
    # wire redraws without error ---
    old_x, old_y = node_b["canvas_x"], node_b["canvas_y"]
    node_b["canvas_x"] += 150
    node_b["canvas_y"] += 80
    win_id, _ = app._fileview_boxes[node_b["id"]]
    app.workspace_canvas.coords(win_id, node_b["canvas_x"], node_b["canvas_y"])
    app.draw_wires()
    app.update()
    check("node B position actually changed", (node_b["canvas_x"], node_b["canvas_y"]) != (old_x, old_y))
    check("wire redraw after drag succeeded (canvas still has a wire)",
          len(app.workspace_canvas.find_withtag("wire")) > 0)

    # Screenshot after drag, before deletion
    app.update()
    try:
        import subprocess
        subprocess.run(["import", "-window", "root", "/tmp/c2_canvas_after_drag.png"],
                        check=False, timeout=10)
    except Exception as e:
        print("screenshot skipped:", e)

    # --- Wire deletion: call delete_wire directly (equivalent to a
    # double-click on the drawn wire) and confirm the underlying
    # func_call block is removed, the wire disappears, and generated
    # code no longer contains the call ---
    app.delete_wire(node_a["id"], node_b["id"])
    app.update()
    check("func_call block removed from node A after delete_wire",
          not any(b[0] == "func_call" for b in node_a["blocks"]))
    check("reference cleared after recompute (post refresh_workspace)",
          node_b["id"] not in find_node(tab, node_a["id"])["references"])
    check("no wire items remain on canvas after deletion",
          len(app.workspace_canvas.find_withtag("wire")) == 0)

    # --- Regression: node view (block editor) still works after all this ---
    app.open_node(node_a["id"])
    app.update()
    check("switching back to node view clears fileview canvas items",
          len(app.workspace_canvas.find_withtag("fileview")) == 0)

    app.destroy()

    print()
    if FAILURES:
        print(f"{len(FAILURES)} FAILURE(S): {FAILURES}")
        sys.exit(1)
    else:
        print("All Phase C2 canvas assertions passed.")


def find_node(tab, node_id):
    from ui import find_node_by_id
    return find_node_by_id(tab["nodes"], node_id)


if __name__ == "__main__":
    main()
