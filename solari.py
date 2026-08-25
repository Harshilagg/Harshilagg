import random

random.seed(7)

MESSAGES = [
    "DESTINATION PRODUCTION",
    "STATUS BUILDING BACKEND",
    "DELAY ONE MORE REFACTOR",
    "BOARDING NOW AT GATE 26",
]

CELLS = 24
CW, CH, GAP = 30, 44, 4
PAD_X, PAD_Y = 18, 16
INNER_W = CELLS * (CW + GAP) - GAP
W = INNER_W + PAD_X * 2
H = CH + PAD_Y * 2

LOOP = 16.0          # seconds
PER_MSG = LOOP / len(MESSAGES)
INTERMEDIATES = 4
ROLL_STEP = 0.12     # seconds between intermediate flaps
STAGGER = 0.035      # per-cell cascade delay

ROLL_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def centered(msg, width):
    msg = msg.upper()[:width]
    left = (width - len(msg)) // 2
    return " " * left + msg + " " * (width - len(msg) - left)


rows = [centered(m, CELLS) for m in MESSAGES]

# ---- shared keyframes: every cell steps through strip index 0,1,2,...,19 ----
kf = []
for m in range(len(MESSAGES)):
    for k in range(INTERMEDIATES + 1):
        t = m * PER_MSG + k * ROLL_STEP
        idx = m * (INTERMEDIATES + 1) + k
        kf.append((t / LOOP * 100.0, idx))
kf_body = "\n".join(
    f"  {pct:.4f}% {{ transform: translateY({-idx * CH}px); }}" for pct, idx in kf
)

parts = []
parts.append(
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
    f'role="img" aria-label="Split-flap board">'
)
parts.append(f"""<style>
  .board-bg {{ fill: #0d1117; }}
  .cell-bg  {{ fill: #16191f; }}
  .seam     {{ stroke: #0d1117; stroke-width: 2; }}
  .glyph    {{ font-family: ui-monospace, "SF Mono", SFMono-Regular, Menlo, Consolas, monospace;
               font-size: 24px; font-weight: 600; fill: #e8edf3; text-anchor: middle; }}
  .strip    {{ animation: flap {LOOP}s steps(1, end) infinite; }}
@keyframes flap {{
{kf_body}
  100% {{ transform: translateY(0px); }}
}}
@media (prefers-reduced-motion: reduce) {{ .strip {{ animation: none; }} }}
</style>""")

# clip paths (one per cell x-position)
parts.append("<defs>")
for i in range(CELLS):
    x = PAD_X + i * (CW + GAP)
    parts.append(
        f'<clipPath id="c{i}"><rect x="{x}" y="{PAD_Y}" width="{CW}" height="{CH}" rx="4"/></clipPath>'
    )
parts.append("</defs>")

parts.append(f'<rect class="board-bg" x="0" y="0" width="{W}" height="{H}" rx="10"/>')

for i in range(CELLS):
    x = PAD_X + i * (CW + GAP)
    cx = x + CW / 2
    parts.append(f'<rect class="cell-bg" x="{x}" y="{PAD_Y}" width="{CW}" height="{CH}" rx="4"/>')
    parts.append(f'<g clip-path="url(#c{i})">')
    parts.append(f'<g class="strip" style="animation-delay:{i * STAGGER:.3f}s">')
    for m in range(len(MESSAGES)):
        for k in range(INTERMEDIATES + 1):
            idx = m * (INTERMEDIATES + 1) + k
            ch = rows[m][i] if k == INTERMEDIATES else random.choice(ROLL_CHARS)
            ch = ch.replace("&", "&amp;").replace("<", "&lt;")
            y = PAD_Y + idx * CH + CH * 0.68
            parts.append(f'<text class="glyph" x="{cx:.1f}" y="{y:.1f}">{ch}</text>')
    parts.append("</g></g>")
    # split-flap seam sits above the moving strip
    parts.append(
        f'<line class="seam" x1="{x}" y1="{PAD_Y + CH / 2}" x2="{x + CW}" y2="{PAD_Y + CH / 2}"/>'
    )

parts.append("</svg>")

svg = "\n".join(parts)
open("solari-board.svg", "w").write(svg)
print("cells:", CELLS, "bytes:", len(svg))
for r in rows:
    print(repr(r))
