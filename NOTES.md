# Blockliner V2 - skeleton status

## What's real and tested here (not stubs)

- `concepts.json` - master universal concept list (Phase 1, points 1-2), 11 concepts.
- `engine/renderer.py` - pure `[[slotname]]` string-substitution engine (Phase 1, point 4).
  No `eval`/`exec` anywhere. `tests/test_engine.py` proves it renders a real nested
  project (assign, list_create, an `if` containing a `print` + `list_append`, and a
  `raw_code` block) byte-for-byte correctly. Run it: `python tests/test_engine.py`.
- `engine/schema.py` + `engine/loader.py` - JSON pack loading + validation (Phase 2,
  points 6-7). Verified a malformed pack (bad manifest, block missing `template`) gets
  skipped with a warning instead of crashing the app (Phase 4, point 14).
- `languages/python/` - a real, working language pack: `manifest.json` +
  `concepts.json` (block templates) + `includes.json` (empty starter). Covers the
  concept-mapped blocks (`print`→`output`, `assign`, `comment`, `if_statement`→`if`,
  `loop_for`, `loop_while`, `func_def`, `func_call`, `return_statement`→`return`,
  `list_create`, `list_append`) plus two intentionally non-translatable examples
  (`raw_code`, `import_module`) with no `concept_id`, per Phase 3 points 9-10.
- `engine/model.py` - carried over from V1 byte-for-byte, per your own Phase 6 point 17
  (it was already just data).
- `main.py` - keeps the AppImage/persistent-data-path fix from V1 exactly as-is, but
  swaps `load_blocks_from_folder` for `load_all_language_packs` + `load_master_concepts`.
- `build.py` - kept the Windows UTF-8 `reconfigure()` fix. Updated `EXTRA_DATA_DIRS`
  (dropped the now-gone top-level `blocks/` folder) and added `EXTRA_DATA_FILES` so
  root `concepts.json` actually ships in the built binary (Phase 6, point 19).
- `.gitignore` - fixed filename (was `gitignore`, missing the leading dot, which is why
  `venv/` and `__pycache__/` were getting tracked in V1).

## The one real gap: `ui.py`

`ui.py` was copied over **unchanged** (4076 lines - not rewritten). It turns out this
is mostly fine already: it has a `get_block_attr()` helper that already normalizes
dict-vs-module access (built for the custom-block builder), so most of `ui.py`'s
*reads* of a block (category, description, is_container, params) work against a
JSON-loaded block dict with zero changes.

The one thing `ui.py` needs that a plain JSON dict doesn't have is a callable
`generate_code(params, children, lang)`. `engine/renderer.py` has
`with_generate_code(blocks)` for exactly this - it wraps every loaded block with a
`generate_code` function backed by `render_block()` (not exec'd code), so `ui.py` keeps
calling blocks the same way it always did. `main.py` already calls this before handing
blocks to `start_ui()`.

**What I have not done:** actually run `ui.py` against this. It's 4076 lines I haven't
read in full, and language *switching* (loading a different pack when the user changes
tabs/language) isn't wired up yet in `main.py` - only the default language pack is
passed to `start_ui()` at startup. If `ui.py` has its own logic elsewhere that reloads
blocks per-tab/per-language, that call site will need to call
`load_all_language_packs()` + `with_generate_code()` the same way `main.py` does now.

## Update: all 8 target languages + HTML now exist

`languages/` now has working packs for Python, C++, C, C#, Java, JavaScript, Rust, Go,
and HTML - all validated with `check_pack.py` and render-tested (see below). Each
covers the same 13 blocks as Python (11 concept-mapped + `raw_code` + `import_module`),
except HTML which has its own smaller, mostly non-translatable set (page structure,
headings, links, etc. - per Phase 3 point 9) since general-purpose programming
concepts don't really apply to markup.

**Real semantic caveats worth knowing before relying on these** (not just syntax -
these are actual language behavior differences a user could get bitten by):

- **Rust `assign_variable`** always creates a new binding via `let` (shadowing) rather
  than mutating an existing variable - reassigning the same name needs `let mut` once
  then a bare `=` after, which this simple block doesn't cover.
- **Go `assign_variable`** uses `:=`, which the Go compiler rejects on a variable
  that's already declared in the same scope ("no new variables on left side of :=").
- **C's `list_append`** deliberately does NOT generate real code - C's fixed-size
  arrays can't grow at runtime, so this block outputs an honest TODO comment instead
  of code that looks like it works but doesn't compile/behave correctly.
- **`func_def` across C, C++, C#, Java, Go, Rust** all default to a void/no-return-value
  signature, and C#/Java's version assumes it will be placed inside a class (they have
  no free-standing top-level functions).
- A few blocks (C's `loop_for`, using start/end instead of a single `iterable`) don't
  match the universal concept's slot names exactly - this is a deliberate, documented
  trade-off for correctness in that specific language, flagged in that block's own
  `description` field rather than forced into a bad translation. It just means that
  one block won't be cleanly auto-translatable later (Phase 5) without a manual mapping
  step - most other blocks across all 9 languages DO match slot names correctly.

All of the above trade-offs are recorded in-line in each block's own `"description"`
field, not just here - so anyone browsing blocks in the UI later sees the caveat right
where they'd use it.

**Render-tested, not just schema-valid**: `list_create`/`vec!`/`[]type{}`/array-literal
templates were specifically checked for a subtle bug risk - literal `[`/`]` characters
sitting directly next to a `[[placeholder]]` (e.g. Rust's `vec![[[items]]];`) could in
theory confuse the placeholder regex. Confirmed working correctly for Python, JS, Go,
and Rust.

## Phase A2 - `match`, `node_types.json`, `comment_token` (node/wire hierarchy foundation)

**`match` backfilled for Python only (12 of 13 blocks; `raw_code` deliberately excluded,
same reasoning as its missing `concept_id` - it's the non-translatable escape hatch).
The other 8 languages are intentionally left matchless for now** - see the phased
implementation plan's own reasoning: match patterns can't be validated against real
code until Phase E's tree-sitter matcher exists, so backfilling all 117 blind was
judged speculative/risky work. A missing `match` is not an error state - it's the same
graceful "stays raw, isn't recognized yet" fallback as `raw_code` today.

**Known grammar ambiguities baked into Python's `match` data itself** (not fixable by
schema alone - Phase E3's matcher will need a secondary check on top of `node_kind`):
- `print(...)` and `func_call` are both tree-sitter `call` nodes. Disambiguation needs
  a literal check on the function name ("is it literally `print`?").
- `list_create` (`x = [1, 2, 3]`) and `assign` (`x = 5`) are both tree-sitter
  `assignment` nodes. Disambiguation needs a check on the right-hand side's node type
  (is it a `list` literal or not?).

**`slot_map` conventions used (documented here since JSON has no comments)**:
- A plain field name (`"left"`, `"body"`) means a direct named child field access on
  the tree-sitter CST node - the common case.
- `"self"` (used by `comment`) means the whole matched node's own text, not a child.
- `"child:N"` (used by `return_statement`, which has no named field in tree-sitter's
  Python grammar) means the Nth positional child.
- Dot-notation (`"function.object"`, used by `list_append`) means a nested field
  access - `my_list.append(x)` is a `call` node whose `function` field is itself an
  `attribute` node with an `object` field.

**`node_types.json` added for all 9 packs, not just Python** - unlike `match`, this is
structural data (what node kinds a language *has*, and whether an entry point is
mandatory), not something that needs a matcher to validate, so there's no reason to
defer it language-by-language.
- **`required: true`** (must auto-create + protect a `start` node, Phase B3):
  C, C++, C#, Java, Go, Rust - all need a `main`/`Main` entry point to produce a
  runnable executable.
- **`required: false`**: Python, JavaScript (script-style, runs top-to-bottom, no
  wrapper needed), and HTML (no function/entry-point concept exists for markup at
  all - HTML gets a single `document` node type instead of `function`/`start`).
- **Known gap, not yet solved**: C#'s and Java's `start` node's `header_template`
  (`static void Main(string[] args)` / `public static void main(String[] args)`)
  assumes it's sitting inside a class - same simplification already called out in
  those languages' `func_def` block description. Auto-creating a bare `start` node
  for C#/Java in isolation won't actually compile without a wrapping class. This is a
  Phase B concern (node hierarchy needs a "class" node type too for these two
  languages, or file-level wrapping), left open rather than papered over here.
- `node_kind` values for `function`/`method`/`start` are **best-effort placeholders**
  against each language's well-known tree-sitter grammar node kind names - none of
  this has been checked against an actual installed grammar yet, since Phase E hasn't
  started. Treat as "probably right, not yet verified."

**`comment_token` added to all 9 manifests** (`"//"`, `"#"`, or a `["<!--", "-->"]`
pair for HTML) for Phase A3's marker-comment export. Validated but deliberately
non-fatal to load - a broken `comment_token` gets warned-and-stripped, same as a
broken `match` rule, rather than taking the whole pack down. (This one actually
shipped with a bug during development: it was first wired into the same fatal
`validate_manifest` path as required fields like `name`/`version`, so a bad
`comment_token` killed the entire pack load - caught by an adversarial test before
being fixed. `tests/test_engine.py`'s `test_a2_warn_and_strip_contract()` now checks
this specific failure mode permanently.)

## Phase A3 - marker-comment round-trip

**Deliberate deviation from the plan's file placement**: the plan said "renderer.py
wraps each node's rendered block", and the wrapping side (`render_node_with_marker`,
`render_file`) does live in `engine/renderer.py`. But the *parsing/reconciliation* side
(`parse_marked_file`, `reconcile_file`) was put in a new `engine/markers.py` instead of
also cramming it into `renderer.py` - text parsing and diffing against an in-memory
model is a genuinely different concern from template substitution, and renderer.py's
own docstring promises it stays pure substitution. No functional difference, just
organizational.

**What "reopen" actually means here, since it's easy to read the plan's test gate too
literally**: the marker tag only ever carries a bare `node_id`, never the node's
`node_type`/`name`/`category`. That's not an oversight - it means marker-comment
round-trip is NOT a way to reconstruct a file's full node structure from nothing (that
full cold-reconstruction job belongs to Phase E, for files Blockliner has never seen).
What this phase actually does: Blockliner keeps the authoritative Node objects in
memory (eventually backed by a project save file, not built yet), and when reopening,
cross-checks the *source file on disk* against what Blockliner already knows per node,
using the markers purely as an alignment key. A marker whose node_id isn't in the
in-memory project becomes an "orphaned raw" node (metadata-less, by necessity) rather
than something reconstructed - same honest-degradation philosophy as everywhere else.

**Marker tag is comment-syntax-agnostic on purpose**: `parse_marked_file()` searches
only for the literal `$$$blockliner:node:N$$$ start/end` text, never the surrounding
comment characters. Parsing therefore works even for a pack with a missing/invalid
`comment_token` (A2's warn-and-strip already handles that gracefully) - only
*rendering* the marker needs to know the language's comment syntax, not detecting one.

**Reconciliation cases handled, all non-fatal, all return diagnostics rather than
raising**: unchanged node -> the ORIGINAL Node object is reattached (same Python
object, not rebuilt - `render_file` on the result is byte-identical, gate 1);
hand-edited node -> demoted to `node_type="raw"` with exact byte content, no attempt
to guess blocks back (gate 2); node marker present in the file but unknown to the
in-memory project -> orphaned raw node; node known in-memory but its marker missing
from the file -> left unchanged (no signal either way, so no action is safer than a
guess); unclosed/mismatched/duplicate markers -> best-effort segment recovery plus a
diagnostic explaining the judgment call. Verified against a real pack too, not just
synthetic test data - HTML's `["<!--", "-->"]` two-token comment_token round-trips
correctly (`<!-- $$$blockliner:node:1$$$ start -->`). Marker delimiter switched from
an initial Unicode block character (`▓`) to plain ASCII `$$$` after review - `▓` isn't
on any keyboard and isn't something a human or an AI coding assistant can reliably
type, whereas `$$$` is plain ASCII, easy to reproduce exactly, and survives
copy-paste through any terminal/editor without risk of mangling.

## Blocks-as-JSON: per-block files replace concepts.json

Each language pack's single `concepts.json` was split into one JSON file per block:
`languages/<lang>/blocks/<block_id>.json`, filename (minus `.json`) = block id. This
is about per-language block *templates* only - the project-root `concepts.json` (the
small, fixed universal concept-id vocabulary loaded by `load_master_concepts`) is a
different thing entirely and is untouched by this change.

**Why**: easier to add/remove/hand-edit a single block without touching or diffing a
big shared file - directly useful for extension authors and for feeding individual
blocks to coder-model output one at a time.

**What actually changed**: only `engine/loader.py`'s file-discovery step - it now
globs `blocks/*.json` and assembles the same `{block_id: block_def}` dict that used
to come from one `json.load()` call, then hands that dict to `validate_concepts()`
completely unchanged. Nothing in Phase A2 (`match`, `node_types.json`) or A3 (marker
round-trip) needed to change at all - both already operate at the individual-block or
individual-node level, they just happened to read from one merged dict before. A
malformed block file is now skipped at read time, one file earlier than before, with
zero effect on its sibling files.

**Known gap**: if you keep a standalone `check_pack.py` validator locally (used to
pre-check coder-model JSON output before it's added to a pack) it is NOT part of this
codebase and was not updated here - it almost certainly still assumes the old
single-concepts.json-per-language shape and will need updating separately to validate
one block file at a time.

