#!/usr/bin/env python3
"""
rebuild_pages.py — replaces ALL <style> blocks in every lekciq*.html with
one clean, unified CSS.  Also fixes the Revolut bar so it shows by default.

Replaces / supersedes:
  fix_mobile.py, fix_tablet.py, fix_js_and_center.py,
  fix_fullscreen.py, fix_topbar.py
"""
import os, re

DOCS = os.path.join(os.path.dirname(__file__), "docs")

# ─────────────────────────────────────────────────────────────────────────────
# UNIFIED CSS  (single block, no !important cascade wars)
# Key choices:
#   • overflow-x: clip on html/body  → doesn't break position:sticky
#   • #topbar position:sticky; top:0 → stays at top while scrolling
#   • sidebar position:fixed always  → out of flex flow on all screens
#   • no backdrop-filter blur        → overlay doesn't blur content
#   • z-index: sidebar 100 > topbar 99 > overlay 98
# ─────────────────────────────────────────────────────────────────────────────
UNIFIED_CSS = """\
<style>
/* ══════════════════════════════════════════════════════════════
   ДАА 2026 — unified lecture page stylesheet
   ══════════════════════════════════════════════════════════════ */

/* ── Variables ─────────────────────────────────────────────── */
:root {
  --bg:#0f1117; --bg2:#1a1d27; --bg3:#242838;
  --accent:#4f8ef7; --accent2:#7c5cbf; --green:#2ecc71;
  --yellow:#f39c12; --red:#e74c3c; --text:#e8eaf0;
  --text2:#9ca3af; --border:#2d3148;
  --def-bg:#0d2137; --def-border:#1e5799;
  --ex-bg:#0d2d1a;  --ex-border:#1e7d3e;
  --key-bg:#2d2100; --key-border:#7d5c00;
  --code-bg:#141822;
}
[data-theme="light"] {
  --bg:#f0f2f8; --bg2:#ffffff; --bg3:#e8ecf5;
  --accent:#2563eb; --accent2:#7c3aed; --green:#16a34a;
  --yellow:#d97706; --red:#dc2626; --text:#1e293b;
  --text2:#64748b; --border:#cbd5e1;
  --def-bg:#eff6ff; --def-border:#3b82f6;
  --ex-bg:#f0fdf4;  --ex-border:#22c55e;
  --key-bg:#fffbeb; --key-border:#f59e0b;
  --code-bg:#1e293b;
}

/* ── Reset ─────────────────────────────────────────────────── */
* { box-sizing: border-box; margin: 0; padding: 0; }
/* clip: prevents horizontal scroll WITHOUT breaking position:sticky */
html { overflow-x: clip; }
body {
  font-family: 'Segoe UI', system-ui, sans-serif;
  background: var(--bg); color: var(--text); line-height: 1.7;
  overflow-x: clip; width: 100%;
}
img { max-width: 100%; height: auto; }

/* ── Page layout ───────────────────────────────────────────── */
#layout { display: flex; min-height: 100vh; width: 100%; }

/* ── Sidebar ───────────────────────────────────────────────── */
#sidebar {
  width: 280px; background: var(--bg2);
  border-right: 1px solid var(--border);
  position: fixed; top: 0; left: 0;
  height: 100vh; overflow-y: auto;
  transition: transform .3s; z-index: 100; padding: 20px 0;
}
#sidebar h2 {
  color: var(--accent); font-size: .85rem; text-transform: uppercase;
  letter-spacing: 1px; padding: 0 20px 10px;
  border-bottom: 1px solid var(--border);
}
#sidebar ul { list-style: none; padding: 10px 0; }
#sidebar li a {
  display: block; padding: 8px 20px; color: var(--text2);
  text-decoration: none; font-size: .88rem;
  border-left: 3px solid transparent; transition: all .2s;
}
#sidebar li a:hover,
#sidebar li a.active {
  color: var(--accent); border-left-color: var(--accent);
  background: rgba(79,142,247,.08);
}
.sidebar-back-link {
  display: flex; align-items: center; gap: 8px;
  padding: 10px 20px 14px; color: var(--accent);
  text-decoration: none; font-size: .88rem; font-weight: 600;
  border-bottom: 1px solid var(--border); margin-bottom: 4px;
  transition: background .18s;
}
.sidebar-back-link:hover { background: rgba(79,142,247,.08); }
.sidebar-close {
  display: none;
  position: absolute; top: 14px; right: 14px;
  background: none; border: none; color: var(--text2);
  font-size: 1.1rem; cursor: pointer;
  padding: 4px 8px; border-radius: 6px; line-height: 1;
  transition: color .18s, background .18s;
}
.sidebar-close:hover { color: var(--text); background: var(--bg3); }

/* ── Overlay (no blur) ─────────────────────────────────────── */
#sidebar-overlay {
  display: none; position: fixed; inset: 0;
  background: rgba(0,0,0,.52); z-index: 98;
}
#sidebar-overlay.active { display: block; }

/* ── Main area (desktop default: 280px offset) ─────────────── */
#main {
  margin-left: 280px; flex: 1;
  padding: 40px; max-width: 1000px;
}

/* ── Topbar (sticky so it stays visible while scrolling) ───── */
#topbar {
  position: sticky; top: 0; z-index: 99;
  background: var(--bg2); border-bottom: 1px solid var(--border);
  display: flex; align-items: center; justify-content: space-between;
  padding: 12px 40px; margin: -40px -40px 40px;
}
#topbar h1 { font-size: 1.1rem; color: var(--accent); }
.topbar-left { display: flex; align-items: center; gap: 8px; flex-shrink: 0; }
.btn-back {
  display: inline-flex; align-items: center; gap: 5px;
  font-size: .82rem; padding: 6px 12px; white-space: nowrap;
}
.btn-icon { padding: 6px 10px; font-size: 1rem; }
#menu-toggle { display: none; }

/* ── Buttons ───────────────────────────────────────────────── */
.btn {
  padding: 6px 14px; border-radius: 6px;
  border: 1px solid var(--border);
  background: var(--bg3); color: var(--text);
  cursor: pointer; font-size: .85rem;
}
.btn:hover { background: var(--accent); color: #fff; border-color: var(--accent); }

/* ── Progress bar ──────────────────────────────────────────── */
#progress-wrap {
  background: var(--bg3); border-radius: 8px;
  padding: 16px 20px; margin-bottom: 32px;
  border: 1px solid var(--border);
}
#progress-wrap h3 { font-size: .9rem; color: var(--text2); margin-bottom: 10px; }
#progress-bar-outer { background: var(--bg); border-radius: 99px; height: 8px; overflow: hidden; }
#progress-bar-inner {
  height: 100%;
  background: linear-gradient(90deg, var(--accent), var(--green));
  border-radius: 99px; transition: width .5s;
}
#progress-label { font-size: .85rem; color: var(--text2); margin-top: 6px; }

/* ── Topic sections ────────────────────────────────────────── */
.topic {
  background: var(--bg2); border: 1px solid var(--border);
  border-radius: 12px; margin-bottom: 40px;
  overflow: hidden; scroll-margin-top: 80px;
}
.topic-header {
  padding: 20px 24px;
  background: linear-gradient(135deg, var(--accent2), var(--accent));
  display: flex; align-items: center; justify-content: space-between;
}
.topic-header h2 { color: #fff; font-size: 1.15rem; }
.topic-num {
  background: rgba(255,255,255,.2); color: #fff; border-radius: 50%;
  width: 32px; height: 32px;
  display: flex; align-items: center; justify-content: center; font-weight: 700;
}
.topic-body { padding: 24px; }

/* ── Cards ─────────────────────────────────────────────────── */
.card { border-radius: 8px; padding: 16px 20px; margin: 16px 0; }
.card-label {
  font-weight: 700; font-size: .8rem;
  text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;
}
.card.def { background: var(--def-bg); border-left: 4px solid var(--def-border); }
.card.def .card-label { color: var(--accent); }
.card.ex  { background: var(--ex-bg);  border-left: 4px solid var(--ex-border); }
.card.ex  .card-label { color: var(--green); }
.card.key { background: var(--key-bg); border-left: 4px solid var(--key-border); }
.card.key .card-label { color: var(--yellow); }
.card.warn { background: rgba(231,76,60,.07); border-left: 4px solid var(--red); }

/* ── Section headers ───────────────────────────────────────── */
.sec-h {
  font-size: .95rem; font-weight: 700; color: var(--accent);
  margin: 20px 0 8px; display: flex; align-items: center; gap: 8px;
}
.sec-h::before {
  content: ''; display: inline-block;
  width: 3px; height: 16px; background: var(--accent); border-radius: 2px;
}

/* ── Code ──────────────────────────────────────────────────── */
pre {
  background: var(--code-bg); color: #cdd6f4; border-radius: 8px;
  padding: 16px 20px; overflow-x: auto;
  font-family: 'Cascadia Code','Fira Code',monospace; font-size: .88rem;
  line-height: 1.6; margin: 12px 0; border: 1px solid var(--border);
  max-width: 100%; box-sizing: border-box;
}
code {
  font-family: 'Cascadia Code','Fira Code',monospace;
  font-size: .88rem; word-break: break-all;
}
.kw{color:#cba6f7} .cm{color:#6c7086;font-style:italic}
.nm{color:#89dceb} .op{color:#89b4fa} .str{color:#a6e3a1} .num{color:#fab387}

/* ── Visualization ─────────────────────────────────────────── */
.viz {
  background: var(--code-bg); border: 1px solid var(--border);
  border-radius: 8px; padding: 16px 20px; font-family: monospace;
  font-size: .85rem; color: #cdd6f4; white-space: pre;
  overflow-x: auto; margin: 12px 0; max-width: 100%; box-sizing: border-box;
}

/* ── Tables ────────────────────────────────────────────────── */
table { width: 100%; border-collapse: collapse; margin: 12px 0; font-size: .9rem; }
th {
  background: var(--bg3); color: var(--accent);
  padding: 10px 12px; text-align: left; border-bottom: 2px solid var(--accent);
}
td { padding: 9px 12px; border-bottom: 1px solid var(--border); }
tr:hover td { background: rgba(79,142,247,.05); }

/* ── Lists ─────────────────────────────────────────────────── */
ul.bullet { list-style: none; padding: 0; }
ul.bullet li { padding: 6px 0 6px 24px; position: relative; }
ul.bullet li::before { content: '▸'; position: absolute; left: 0; color: var(--accent); }

/* ── Boxes ─────────────────────────────────────────────────── */
.exam-box {
  background: linear-gradient(135deg,rgba(231,76,60,.1),rgba(231,76,60,.05));
  border: 1px solid var(--red); border-radius: 8px;
  padding: 16px 20px; margin: 16px 0;
}
.exam-box .card-label { color: var(--red); }
.conn-box {
  background: rgba(124,92,191,.1); border: 1px solid var(--accent2);
  border-radius: 8px; padding: 16px 20px; margin: 16px 0;
}
.conn-box .card-label { color: var(--accent2); }
.thm {
  background: rgba(79,142,247,.07); border: 1px solid var(--accent);
  border-radius: 8px; padding: 16px 20px; margin: 12px 0;
}
.thm-title { color: var(--accent); font-weight: 700; margin-bottom: 8px; }

/* ── Typography ────────────────────────────────────────────── */
p { margin: 10px 0; }
b, strong { color: var(--accent); }
hr { border: none; border-top: 1px solid var(--border); margin: 20px 0; }

/* ── MathJax ───────────────────────────────────────────────── */
mjx-container { max-width: 100%; overflow-x: auto; display: block; }
mjx-container svg { max-width: 100%; }

/* ═══════════════════════════════════════════════════════════
   REVOLUT TOP BAR
   ═══════════════════════════════════════════════════════════ */
#rbar {
  width: 100%;
  background: linear-gradient(90deg,#070c1a 0%,#0c1628 50%,#070c1a 100%);
  border-bottom: 1px solid rgba(0,117,235,.22);
}
.rbar-inner {
  max-width: 1200px; margin: 0 auto;
  display: flex; align-items: center; gap: 14px; padding: 8px 20px;
}
.rbar-emoji { font-size: 1rem; flex-shrink: 0; line-height: 1; }
.rbar-text {
  font-size: .84rem; color: rgba(232,234,240,.68);
  flex: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.rbar-btn {
  display: inline-flex; align-items: center; gap: 7px;
  background: linear-gradient(135deg,#0075eb,#00a8ff);
  color: #fff; text-decoration: none; padding: 6px 16px;
  border-radius: 20px; font-weight: 700; font-size: .79rem;
  white-space: nowrap; flex-shrink: 0;
  box-shadow: 0 2px 12px rgba(0,117,235,.32);
  transition: opacity .18s, transform .18s;
}
.rbar-btn:hover { opacity: .88; transform: translateY(-1px); }
.rbar-close {
  background: none; border: none; color: rgba(255,255,255,.32);
  cursor: pointer; font-size: .88rem; padding: 4px 8px;
  border-radius: 4px; flex-shrink: 0; line-height: 1; transition: color .18s;
}
.rbar-close:hover { color: rgba(255,255,255,.7); }

/* ═══════════════════════════════════════════════════════════
   RESPONSIVE
   ═══════════════════════════════════════════════════════════ */

/* Desktop (> 1100px): sidebar always visible */
@media (min-width: 1101px) {
  #sidebar    { transform: none; }
  #menu-toggle { display: none; }
  .btn-back   { display: inline-flex; }
  .sidebar-close { display: none; }
}

/* Tablet + phone (≤ 1100px): hamburger drawer */
@media (max-width: 1100px) {
  /* Sidebar slides off-screen by default */
  #sidebar     { transform: translateX(-100%); }
  #sidebar.open { transform: translateX(0); }
  .sidebar-close { display: block; }

  /* Hamburger visible; back button lives in sidebar */
  #menu-toggle { display: inline-flex; }
  .btn-back    { display: none; }

  /* Main: full width */
  #main {
    margin-left: 0; width: 100%; max-width: 100%;
    box-sizing: border-box; padding: 16px;
  }

  /* Topbar: sticky still works because we use overflow-x:clip not hidden */
  #topbar {
    padding: 10px 16px; margin: -16px -16px 16px; gap: 8px;
  }
  #topbar h1 {
    font-size: .82rem; overflow: hidden;
    text-overflow: ellipsis; white-space: nowrap; flex: 1;
  }

  /* Content tweaks */
  .topic-body   { padding: 16px; }
  .topic-header { padding: 14px 16px; }
  .topic-header h2 { font-size: 1rem; }
  .topic { scroll-margin-top: 60px; }
  pre   { font-size: .78rem; }
  table { font-size: .8rem; display: block; overflow-x: auto; }
  #progress-wrap { padding: 12px 14px; }
  #progress-wrap label { font-size: .78rem; }
  #progress-wrap > div { flex-wrap: wrap; }
  .card, .exam-box, .conn-box, .thm { word-break: break-word; }
  code  { word-break: break-all; }
  img   { max-width: 100%; }
}

/* Revolut bar: hide text on very small screens */
@media (max-width: 540px) {
  .rbar-text  { display: none; }
  .rbar-inner { gap: 10px; }
}
</style>"""

# ─────────────────────────────────────────────────────────────────────────────
# Updated rbar script: bar shows by default (CSS sets display:block),
# JS only hides it if the user already dismissed it.
# ─────────────────────────────────────────────────────────────────────────────
OLD_RBAR_SCRIPT = """\
<script>
(function(){
  if (!localStorage.getItem('rbar4_gone')) {
    document.getElementById('rbar').style.display = 'block';
  }
  window.dismissRBar = function() {
    document.getElementById('rbar').style.display = 'none';
    localStorage.setItem('rbar4_gone', '1');
  };
})();
</script>"""

NEW_RBAR_SCRIPT = """\
<script>
(function(){
  if (localStorage.getItem('rbar4_gone')) {
    document.getElementById('rbar').style.display = 'none';
  }
  window.dismissRBar = function() {
    document.getElementById('rbar').style.display = 'none';
    localStorage.setItem('rbar4_gone', '1');
  };
})();
</script>"""


def rebuild_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # 1. Remove ALL existing <style>...</style> blocks
    content = re.sub(r'<style>.*?</style>\n?', '', content, flags=re.DOTALL)

    # 2. Inject unified CSS right before </head>
    content = content.replace('</head>', UNIFIED_CSS + '\n</head>', 1)

    # 3. Update rbar script (show by default; hide only if dismissed)
    content = content.replace(OLD_RBAR_SCRIPT, NEW_RBAR_SCRIPT)

    return content, content != original


lecture_files = sorted(
    f for f in os.listdir(DOCS) if re.match(r'lekciq\d+\.html', f)
)

for fname in lecture_files:
    path = os.path.join(DOCS, fname)
    content, changed = rebuild_file(path)
    if changed:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'✓  Rebuilt: {fname}')
    else:
        print(f'–  No change: {fname}')

print('\nDone.')
