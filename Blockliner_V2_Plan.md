# Blockliner V2 — Node/Wire Redesign: Implementation Plan (handoff v4)

**Status: Phases A, B, and C1 complete and tested (unchanged from v3).
Phase C2 (full ComfyUI-style node canvas) is now also complete and
tested this session. Starting C3 next (manual wire-drag).**

This is a continuation document - the previous handoff (v3) is superseded
in place. Sections marked ✅ are done and tested (either on real hardware,
or via a headless Xvfb + scripted-Tkinter harness that exercises the real
UI code and, where relevant, takes real screenshots - noted per item
below). Everything else is unchanged from the plan and not yet started.

---

## Phase C — Wires as a derived call graph

### C1. Derived call graph ✅ COMPLETE (unchanged from v3)

See v3 for full detail.

### C2. Draw wires on the file canvas ✅ COMPLETE

Full ComfyUI-style freeform canvas, as decided at the end of the last
session - not the lighter text-label interim that was also on the table.

- **`render_file_view()` rewritten**: node boxes are no longer
  `.pack()`-stacked into `workspace_frame`. They're now drawn directly on
  `workspace_canvas` via `canvas.create_window(x, y, anchor="nw", ...)` at
  each node's explicit `canvas_x`/`canvas_y` position, so they can sit
  anywhere rather than in a single vertical stack. Visual appearance
  (icon, lock glyph, color, block/child count, Open button) is unchanged
  from B2/B3 - only placement and mouse behavior changed.
- **`assign_default_canvas_positions(nodes)`**: any node missing
  `canvas_x`/`canvas_y` gets a default 3-per-row grid slot
  (260×150 spacing). Never overwrites a position the user already dragged
  a node to. Positions are in-memory only, same as everything else in
  Phase B/C (still no real save format - see carry-forward item 4).
- **Dragging**: grabbed from a node box's header only (so the Open button
  and double-click-to-open both still work). A ~4px movement threshold
  distinguishes an actual drag from a click, since Tkinter fires
  `<ButtonPress-1>`/`<B1-Motion>`/`<ButtonRelease-1>` and
  `<Double-Button-1>` independently and a plain click never crosses the
  threshold. During a drag, only `draw_wires()` runs on every
  `<B1-Motion>` (not a full `refresh_workspace()`) for responsiveness;
  the position is committed to the node dict live, and
  `mark_active_tab_dirty()` + scrollregion update happen on release.
- **`draw_wires()` / `_draw_one_wire()` / `_bezier_points()`**: renders
  every edge in the current file-view depth's `references` as a cubic
  Bézier curve (right-center of the source box to left-center of the
  target box, with horizontally-pulled control points so curves leave/
  arrive roughly perpendicular to the box edge regardless of relative
  position - the ComfyUI look). Tkinter has no native bezier canvas item,
  so the curve is flattened to a 24-segment polyline and drawn with
  `smooth=True`. A small dot is drawn at the target end as a lightweight
  direction indicator. Only draws an edge when **both** endpoints are
  boxes actually shown at the current depth (a class's internal nodes
  don't draw wires out past their own canvas).
- **Click-to-select / double-click-to-delete**: single-click a wire
  (`select_wire`) highlights it (orange, thicker) via a redraw; the
  target/source ids are stored in `self._fileview_selected_wire`.
  Double-click a wire (`delete_wire`) removes the underlying `func_call`
  block from the *source* node via `remove_first_func_call_targeting()`
  (recursive, same traversal order as `iter_all_blocks_recursive`) and
  triggers a full `refresh_workspace()` - the wire disappears because
  `recompute_references()` naturally stops finding that call, never
  because the wire itself was deleted directly. Matches the C2/C3 test
  gate from the plan: *deleting a wire removes the block, never the
  reverse.* If a node calls another one more than once, one
  double-click removes one call; the wire stays until all calls to that
  target are gone.
- **Scrollregion**: `_update_fileview_scrollregion()` sizes
  `workspace_canvas`'s scrollregion to the bounding box of everything
  tagged `"fileview"` (boxes + wires), so dragging a node far out still
  keeps it reachable via the existing scrollbar. Pan/zoom proper was
  explicitly deferred, not attempted this round - first pass just reuses
  the plain scrollbar already in place for the block editor.

**A real, non-obvious bug found and fixed this session (would have sunk
C2 silently):** Tkinter canvas *window* items (used both for the boxes
and for the pre-existing `workspace_frame` embedding that holds the block
editor) **always paint on top of drawn items** (lines/ovals) **regardless
of creation order or `tag_raise`/`tag_lower`** - this is a real Tk
behavior, not a bug in the sense of being fixable via z-order calls.
Separately, an empty `tk.Frame` under `pack_propagate` does **not**
reliably shrink its own requested size back down after its last child is
destroyed - `workspace_frame` was retaining its old ~324px requested
height from the last time `show_empty_state()`'s big padded label was
packed into it, even with zero children and after `update_idletasks()`.
Combined, this meant `workspace_frame`'s embedded window - though
visually empty - silently occluded every wire drawn beneath it on the
same canvas. Diagnosed by: (1) confirming a bare `create_line` call was
invisible even far from any node box, (2) ruling out Xvfb/ImageMagick
screenshot capture itself via a minimal standalone Tk+Canvas+`import`
repro (that one worked fine), (3) enumerating every canvas item's real
`bbox()` via `canvas.find_all()`, which showed the `workspace_frame`
window's bbox as `(0, 0, 600, 324)` - fully covering the wire's bbox.
**Fix**: `workspace_frame`'s window item id is now saved
(`self.workspace_frame_window_id`) at creation. `refresh_workspace()`
explicitly pins its height to `1` whenever `view_mode == "file"` (nothing
is meant to be inside `workspace_frame` in file view anymore - see next
paragraph) and reverts it to natural sizing (`height=0`, which is Tk's
canvas-window convention for "use the widget's requested size") whenever
`view_mode == "node"`. Also relevant: the "← Back" button used to be
packed into `workspace_frame` inside `render_file_view()` - now pinned to
1px, that would've hidden it - so it was moved into `refresh_node_nav()`
(the workspace header, alongside the existing "+ New Node" button),
which is a more consistent home for it anyway (same place "Nodes"/"+ New
Node" already live).

- **Verified (scripted, `tests/test_c2_canvas.py`, run under Xvfb)**: two
  function nodes with a `func_call` between them get canvas boxes at
  default grid positions; a wire is drawn for the resolved reference;
  simulating a drag (updating `canvas_x`/`canvas_y` + calling
  `draw_wires()`) moves the box and the wire follows; calling
  `delete_wire()` directly (equivalent to double-clicking the drawn wire)
  removes the `func_call` block, clears the reference on next recompute,
  and leaves no wire canvas items behind; switching back to node view
  clears every `"fileview"`-tagged canvas item. **Screenshot-verified**
  at each stage, including the specific occlusion bug above (before/after
  comparison - a plain 8px red test line was completely invisible before
  the fix, fully visible after) and a 3-node scenario (`main` calling
  both `helper_one` and `helper_two`, `helper_one` also calling
  `helper_two`) showing three simultaneous curved wires, confirming
  multi-edge rendering and the expected/acceptable Tk limitation that a
  long wire passing behind an intermediate node box is occluded by that
  box's window for the segment underneath it (visible again on both
  sides - a routing/z-order refinement, not a correctness bug, and worth
  a note for C3/D if it becomes visually confusing with denser graphs).
  Full Phase A engine regression (`tests/test_engine.py`) re-run clean
  after all changes - zero regression.

### C3. Manual wire-drag — NOT STARTED, unchanged from plan

Drag from node A to node B inserts a `func_call` block into whichever
node is currently open, targeting B - the reverse of C1, so both
directions of authoring (typing a call vs. dragging a wire) stay
consistent through the same underlying block data. C2's box dragging
code (press/motion/release with a movement threshold, grabbed from the
header) is the template to adapt: C3 needs an equivalent drag gesture
started from a box's *edge* (an output "port" region, conventionally the
right side) rather than its header, ending on another box, with a
temporary rubber-band line drawn during the drag for feedback.

**C2/C3 test gate (unchanged from plan, C2's half now verified)**: call a
function by typing it → wire appears automatically (✅ C1 does the data
side, C2 the rendering side - verified together this session). Delete
the wire visually → the underlying `func_call` block is removed and the
call disappears from generated code (✅ verified this session - see
above; never the other way around).

---

## Everything else (Phases A, B, D, E, F; carry-forward items)

Unchanged from v3 - see that document for full detail. Repeating only
what's now stale or newly relevant:

1. **Node position storage** (`canvas_x`/`canvas_y`, added this session)
   joins the existing carry-forward item about no real persistence format
   existing yet (v3 item 4) - it's in-memory only, same status as
   `nodes`/`kind`/`child_nodes`/`locked`/`references`. Closing the app
   still loses all of this.
2. **`engine.model.Node` vs. UI's tuple-based node shape**: still not
   reconciled (v3 item 2), still most relevant once real persistence is
   designed.
3. **C#/Java entry-point header rendering** still intentionally minimal
   (v3 item 3) - unaffected by C2.
4. **Wire routing behind intermediate boxes** (new, minor, noted above):
   not a correctness problem today (only 3 nodes tested), but worth
   revisiting once graphs get denser - either accept it (ComfyUI itself
   has the same visual layering in practice) or add simple curve routing
   away from intervening boxes in a later pass.
5. `check_pack.py`, stale `concepts.json` files, and the Python-only
   `match` backfill question (v3 items 5-7) - all still open, still
   untouched this round.

## Suggested build order (unchanged)

```
A (done) → B (done) → C1 (done) → C2 (done) → C3 (next) → D (sections) → F (slot parsing) → E (cold import)
