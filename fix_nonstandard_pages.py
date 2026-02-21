#!/usr/bin/env python3
"""
fix_nonstandard_pages.py

lekciq4, lekciq7, lekciq10, lekciq13 were created with custom CSS classes
(card-blue, card-green, topic-title, info-box, etc.) that differ from the
unified stylesheet.  The rebuild removed their original <style> blocks,
losing all card/section coloring.

This script adds a SUPPLEMENT <style> block after the unified one for each
affected page.  The supplement contains ONLY the content-specific classes
(no body / #sidebar / #main / @media layout rules, which are handled by the
unified CSS).
"""
import os, re

DOCS = os.path.join(os.path.dirname(__file__), "docs")

# ─── lekciq4 ────────────────────────────────────────────────────────────────
SUPP_4 = """\
<style>
/* ── lekciq4 content-specific classes ── */
:root {
  --l4-blue:#1f6feb; --l4-blue-l:#388bfd; --l4-blue-bg:#0d2140;
  --l4-green-l:#56d364; --l4-green-bg:#0d3020;
  --l4-yellow:#d29922; --l4-yellow-l:#e3b341; --l4-yellow-bg:#2d2000;
  --l4-purple:#8957e5; --l4-purple-l:#bc8cff; --l4-purple-bg:#1c1040;
  --l4-red:#da3633; --l4-red-l:#f85149; --l4-red-bg:#2d0606;
  --l4-muted:#8b949e; --l4-card:#1c2128; --l4-border:#30363d;
}
.page-header { border-bottom:1px solid var(--l4-border); margin-bottom:40px; padding-bottom:24px; }
.page-header .lecture-badge { background:var(--l4-blue-bg); color:var(--l4-blue-l); border:1px solid var(--l4-blue); padding:4px 12px; border-radius:20px; font-size:13px; display:inline-block; margin-bottom:12px; }
.page-header h1 { font-size:2rem; font-weight:700; margin-bottom:8px; }
.page-header .subtitle { color:var(--l4-muted); font-size:15px; }
.page-header .meta { margin-top:12px; font-size:13px; color:var(--l4-muted); }
.topic-title { font-size:1.5rem; font-weight:700; margin-bottom:24px; color:var(--text); display:flex; align-items:center; gap:12px; }
.topic-title .icon { font-size:1.2rem; }
.card-blue   { background:var(--l4-blue-bg);   border-color:var(--l4-blue)!important; }
.card-green  { background:var(--l4-green-bg);  border-color:var(--l4-green-l)!important; }
.card-yellow { background:var(--l4-yellow-bg); border-color:var(--l4-yellow)!important; }
.card-purple { background:var(--l4-purple-bg); border-color:var(--l4-purple)!important; }
.card-red    { background:var(--l4-red-bg);    border-color:var(--l4-red)!important; }
.card-gray   { background:var(--bg3);          border-color:var(--border)!important; }
.card-blue   .card-label { color:var(--l4-blue-l); }
.card-green  .card-label { color:var(--l4-green-l); }
.card-yellow .card-label { color:var(--l4-yellow-l); }
.card-purple .card-label { color:var(--l4-purple-l); }
.card-red    .card-label { color:var(--l4-red-l); }
.card-gray   .card-label { color:var(--l4-muted); }
.ascii-box { background:var(--bg3); border:1px solid var(--border); border-radius:8px; padding:16px; font-family:monospace; font-size:13px; white-space:pre; overflow-x:auto; color:var(--l4-green-l); margin:12px 0; }
.steps { counter-reset:step; }
.step { display:flex; gap:14px; margin-bottom:14px; align-items:flex-start; }
.step-num { background:var(--l4-blue); color:#fff; width:26px; height:26px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:13px; font-weight:700; flex-shrink:0; margin-top:2px; }
.step-content { flex:1; }
.hl-blue   { color:var(--l4-blue-l);   font-weight:600; }
.hl-green  { color:var(--l4-green-l);  font-weight:600; }
.hl-yellow { color:var(--l4-yellow-l); font-weight:600; }
.hl-purple { color:var(--l4-purple-l); font-weight:600; }
.hl-red    { color:var(--l4-red-l);    font-weight:600; }
.proof-block { border-left:4px solid var(--l4-purple); padding-left:16px; margin:12px 0; }
.proof-block .proof-label { font-size:12px; text-transform:uppercase; color:var(--l4-purple-l); font-weight:700; margin-bottom:8px; }
code:not(pre code) { background:var(--bg3); border:1px solid var(--border); padding:2px 6px; border-radius:4px; font-size:13px; }
#sidebar .section-header { padding:10px 16px 4px; font-size:11px; text-transform:uppercase; color:var(--l4-blue-l); letter-spacing:1px; margin-top:8px; }
</style>"""

# ─── lekciq7 ────────────────────────────────────────────────────────────────
SUPP_7 = """\
<style>
/* ── lekciq7 content-specific classes ── */
:root {
  --l7-c1:#58a6ff; --l7-c2:#3fb950; --l7-c3:#f0883e;
  --l7-c4:#bc8cff; --l7-c5:#ff7b72;
  --l7-dim:#8b949e; --l7-card:#1c2128; --l7-border:#30363d;
}
.subtitle { color:var(--l7-dim); font-size:.9rem; margin-bottom:2.5rem; }
#main h1 { font-size:2rem; color:var(--l7-c1); border-bottom:2px solid var(--l7-border); padding-bottom:.8rem; margin-bottom:.4rem; }
#main h2 { font-size:1.35rem; color:var(--l7-c3); margin:2.5rem 0 1rem; padding-left:.8rem; border-left:4px solid var(--l7-c3); }
#main h3 { font-size:1.05rem; color:var(--l7-c2); margin:1.5rem 0 .6rem; }
.card-definition { border-left:4px solid var(--l7-c1)!important; }
.card-intuition  { border-left:4px solid var(--l7-c2)!important; }
.card-visual     { border-left:4px solid var(--l7-c4)!important; }
.card-example    { border-left:4px solid var(--l7-c3)!important; }
.card-key        { border-left:4px solid var(--l7-c5)!important; }
.card-exam       { border-left:4px solid #f0e68c!important; background:#1a1a0a!important; }
.lbl-def  { color:var(--l7-c1); }
.lbl-int  { color:var(--l7-c2); }
.lbl-vis  { color:var(--l7-c4); }
.lbl-ex   { color:var(--l7-c3); }
.lbl-key  { color:var(--l7-c5); }
.lbl-exam { color:#f0e68c; }
.ascii { font-family:'Courier New',monospace; background:#0d1117; padding:1rem 1.2rem; border-radius:6px; border:1px solid var(--l7-border); color:var(--l7-c2); font-size:.82rem; overflow-x:auto; white-space:pre; line-height:1.4; }
code.inline { background:#21262d; padding:.1rem .4rem; border-radius:4px; font-size:.85rem; color:var(--l7-c2); }
.badge { display:inline-block; background:var(--l7-c4); color:#000; border-radius:4px; padding:.1rem .5rem; font-size:.75rem; font-weight:700; margin-right:.4rem; }
.tag-lec { background:#1f3a5f; color:var(--l7-c1); border:1px solid var(--l7-c1); }
.link-row { display:flex; gap:.6rem; flex-wrap:wrap; margin-top:.6rem; }
.link-badge { background:#21262d; border:1px solid var(--l7-border); border-radius:20px; padding:.2rem .7rem; font-size:.78rem; color:var(--l7-c4); }
.nav-section { color:var(--l7-c3); font-weight:700; margin-top:1rem; font-size:.75rem; padding:.3rem 1.2rem; text-transform:uppercase; display:block; }
li::marker { color:var(--l7-c1); }
</style>"""

# ─── lekciq10 ───────────────────────────────────────────────────────────────
SUPP_10 = """\
<style>
/* ── lekciq10 content-specific classes ── */
:root {
  --l10-c1:#58a6ff; --l10-c2:#3fb950; --l10-c3:#f0883e;
  --l10-c4:#ff7b72; --l10-c5:#d2a8ff; --l10-hl:#ffa657;
  --l10-dim:#8b949e; --l10-s2:#21262d; --l10-border:#30363d;
}
.page-title { background:linear-gradient(135deg,var(--l10-c1),var(--l10-c5)); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; font-size:2.2rem; font-weight:700; margin-bottom:.5rem; }
.page-subtitle { color:var(--l10-dim); font-size:1rem; margin-bottom:2.5rem; }
.topic-title { color:var(--l10-c1); font-size:1.4rem; font-weight:700; margin-bottom:1.2rem; padding-bottom:.6rem; border-bottom:2px solid var(--l10-border); display:flex; align-items:center; gap:.6rem; }
.topic-title::before { content:''; display:inline-block; width:4px; height:1.4rem; background:var(--l10-c1); border-radius:2px; }
.subsection { margin:1.2rem 0; }
.section-label { display:inline-block; background:var(--l10-s2); border:1px solid var(--l10-border); border-radius:6px; padding:.2rem .6rem; font-size:.75rem; font-weight:600; text-transform:uppercase; letter-spacing:.08em; margin-bottom:.5rem; margin-right:.4rem; }
.label-def   { color:var(--l10-c5); border-color:var(--l10-c5)!important; }
.label-explain { color:var(--l10-c2); border-color:var(--l10-c2)!important; }
.label-viz   { color:var(--l10-c3); border-color:var(--l10-c3)!important; }
.label-example { color:var(--l10-hl); border-color:var(--l10-hl)!important; }
.label-key   { color:var(--l10-c4); border-color:var(--l10-c4)!important; }
.label-link  { color:var(--l10-c1); border-color:var(--l10-c1)!important; }
.label-exam  { color:var(--l10-c2); border-color:var(--l10-c2)!important; background:rgba(63,185,80,.08); }
.info-box { border-radius:8px; padding:1rem 1.2rem; margin:1rem 0; border-left:4px solid; }
.info-box.definition { background:rgba(88,166,255,.08); border-color:var(--l10-c1); }
.info-box.theorem    { background:rgba(210,168,255,.08); border-color:var(--l10-c5); }
.info-box.warning    { background:rgba(255,123,114,.08); border-color:var(--l10-c4); }
.info-box.success    { background:rgba(63,185,80,.08);  border-color:var(--l10-c2); }
.info-box.note       { background:rgba(240,136,62,.08); border-color:var(--l10-c3); }
.info-box strong { display:block; margin-bottom:.4rem; font-size:.85rem; text-transform:uppercase; letter-spacing:.06em; }
.key-list { list-style:none; }
.key-list li { padding:.4rem 0; padding-left:1.4rem; position:relative; }
.key-list li::before { content:'▸'; color:var(--l10-c3); position:absolute; left:0; font-size:.8rem; top:.5rem; }
.mermaid { background:var(--l10-s2); border-radius:8px; padding:1rem; margin:1rem 0; text-align:center; border:1px solid var(--l10-border); }
.exam-question { background:linear-gradient(135deg,rgba(63,185,80,.06),rgba(88,166,255,.06)); border:1px solid var(--l10-c2); border-radius:8px; padding:1.2rem; margin-top:1.2rem; }
.exam-question strong { color:var(--l10-c2); display:block; margin-bottom:.4rem; }
.step-table { font-size:.85rem; }
.step-table td.highlight { background:rgba(88,166,255,.15); color:var(--l10-c1); font-weight:600; }
.step-table td.done { background:rgba(63,185,80,.1); color:var(--l10-c2); }
code:not(pre code) { background:var(--l10-s2); color:var(--l10-c5); padding:.1em .35em; border-radius:4px; font-size:.9em; }
#sidebar li.section-header a { color:var(--text); font-weight:600; font-size:.9rem; margin-top:.8rem; }
</style>"""

# ─── lekciq13 ───────────────────────────────────────────────────────────────
SUPP_13 = """\
<style>
/* ── lekciq13 content-specific classes ── */
:root {
  --l13-c1:#58a6ff; --l13-c2:#3fb950; --l13-c3:#f78166;
  --l13-c4:#d2a679; --l13-c5:#bc8cff;
  --l13-border:#30363d; --l13-t3:#cdd9e5;
  --l13-thm-bg:#1a2332; --l13-def-bg:#1a2a1a; --l13-warn-bg:#2a1f10;
}
#main h1 { font-size:2.2rem; color:var(--l13-c1); margin-bottom:8px; border-bottom:2px solid var(--l13-border); padding-bottom:16px; }
.subtitle { color:var(--text2); font-size:1rem; margin-bottom:36px; }
h2.section-title { font-size:1.5rem; color:var(--l13-c4); margin:48px 0 16px; padding-left:14px; border-left:4px solid var(--l13-c4); }
h3.sub-title   { font-size:1.15rem; color:var(--l13-c2); margin:28px 0 12px; }
h4.sub-sub     { font-size:1rem; color:var(--l13-c5); margin:20px 0 8px; }
.box { background:var(--bg2); border:1px solid var(--border); border-radius:10px; padding:22px 26px; margin:18px 0; }
.theorem-box { background:var(--l13-thm-bg); border-left:4px solid var(--l13-c1); border-radius:0 10px 10px 0; padding:18px 22px; margin:18px 0; }
.theorem-box .label { font-size:11px; color:var(--l13-c1); text-transform:uppercase; letter-spacing:1px; font-weight:700; margin-bottom:8px; }
.theorem-box .title { font-size:1.05rem; font-weight:700; color:var(--l13-t3); margin-bottom:10px; }
.def-box { background:var(--l13-def-bg); border-left:4px solid var(--l13-c2); border-radius:0 10px 10px 0; padding:18px 22px; margin:18px 0; }
.def-box .label { font-size:11px; color:var(--l13-c2); text-transform:uppercase; letter-spacing:1px; font-weight:700; margin-bottom:8px; }
.warn-box { background:var(--l13-warn-bg); border-left:4px solid var(--l13-c3); border-radius:0 10px 10px 0; padding:18px 22px; margin:18px 0; }
.warn-box .label { font-size:11px; color:var(--l13-c3); text-transform:uppercase; letter-spacing:1px; font-weight:700; margin-bottom:8px; }
.grid-2 { display:grid; grid-template-columns:1fr 1fr; gap:16px; margin:16px 0; }
.tree-vis { background:var(--bg3); border:1px solid var(--border); border-radius:10px; padding:20px; margin:18px 0; font-family:monospace; font-size:13px; overflow-x:auto; }
.tree-vis pre { color:var(--l13-t3); }
.diagram-box { background:var(--bg3); border:1px solid var(--border); border-radius:10px; padding:20px; margin:18px 0; }
.diagram-box .mermaid { display:flex; justify-content:center; }
.exam-box .label { font-size:11px; color:var(--l13-c5); text-transform:uppercase; letter-spacing:1px; font-weight:700; margin-bottom:10px; }
.key-points { background:var(--bg3); border-radius:10px; padding:18px 22px; margin:16px 0; }
.key-points ul { padding-left:20px; }
.key-points li { color:var(--l13-t3); margin-bottom:6px; }
.key-points li strong { color:var(--l13-c2); }
.badge-blue   { background:#1c3a5c; color:var(--l13-c1); }
.badge-green  { background:#1a3a1a; color:var(--l13-c2); }
.badge-red    { background:#3a1a1a; color:var(--l13-c3); }
.badge-purple { background:#2a1a3a; color:var(--l13-c5); }
.badge { display:inline-block; padding:2px 8px; border-radius:4px; font-size:12px; font-weight:700; margin-right:6px; }
.step-num { background:var(--l13-c1); color:#000; }
.connect-box { background:var(--bg3); border:1px dashed var(--l13-c4); border-radius:8px; padding:14px 18px; margin:14px 0; font-size:14px; color:var(--text2); }
.connect-box strong { color:var(--l13-c4); }
.adv-table { background:var(--bg3); border-radius:8px; overflow:hidden; margin:16px 0; }
code.inline { background:var(--bg3); padding:2px 6px; border-radius:4px; font-family:monospace; font-size:14px; color:var(--l13-c4); }
hr.section-divider { border:none; border-top:1px solid var(--border); margin:40px 0; }
#sidebar .section-label { padding:12px 20px 4px; color:var(--l13-c4); font-size:11px; text-transform:uppercase; letter-spacing:.8px; font-weight:700; display:block; }
</style>"""

SUPPLEMENTS = {
    "lekciq4.html":  SUPP_4,
    "lekciq7.html":  SUPP_7,
    "lekciq10.html": SUPP_10,
    "lekciq13.html": SUPP_13,
}

# Marker to detect if already applied
MARKER = "content-specific classes"

for fname, supplement in SUPPLEMENTS.items():
    path = os.path.join(DOCS, fname)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    if MARKER in content:
        print(f"–  Skipped (already applied): {fname}")
        continue

    # Insert supplement right before </head>
    content = content.replace('</head>', supplement + '\n</head>', 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓  Fixed: {fname}")

print("\nDone.")
