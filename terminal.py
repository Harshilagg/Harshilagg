LINE1 = "> I like problems where the hard part is the design, not the syntax."
LINE2 = "> I take vague requirements and turn them into schemas that hold up."

FS = 20
CW = 13                 # per-character advance (matches pacman.py at the same font size)
PAD_X, PAD_TOP, PAD_BOTTOM = 24, 40, 36
LINE_GAP = 34

W = max(len(LINE1), len(LINE2)) * CW + PAD_X * 2
H = PAD_TOP + LINE_GAP + PAD_BOTTOM
BASE1 = PAD_TOP
BASE2 = PAD_TOP + LINE_GAP

CHAR_STEP = 0.045        # seconds between characters appearing
TYPE_START1 = 0.5
LINE_PAUSE = 0.5
TYPE_START2 = TYPE_START1 + len(LINE1) * CHAR_STEP + LINE_PAUSE
END_TYPE2 = TYPE_START2 + len(LINE2) * CHAR_STEP
HOLD = 2.0
RESET_GAP = 0.3
LOOP = END_TYPE2 + HOLD + RESET_GAP

HIDE_X, HIDE_Y = -999.0, -999.0


def pct(t):
    return t / LOOP * 100.0


def esc(c):
    return {"&": "&amp;", "<": "&lt;", ">": "&gt;"}.get(c, c)


def char_reveal_kfs(line, start, prefix, y):
    kfs, nodes = [], []
    for i, ch in enumerate(line):
        t = start + i * CHAR_STEP
        p = pct(t)
        name = f"{prefix}{i}"
        kfs.append(f"@keyframes {name}{{0%,{p:.3f}%{{opacity:0}}{min(p + 0.25, 100):.3f}%,100%{{opacity:1}}}}")
        if ch != " ":
            x = PAD_X + i * CW
            nodes.append(
                f'<text class="char" x="{x:.1f}" y="{y}" style="animation-name:{name}">{esc(ch)}</text>'
            )
    return kfs, nodes


kf1, nodes1 = char_reveal_kfs(LINE1, TYPE_START1, "a", BASE1)
kf2, nodes2 = char_reveal_kfs(LINE2, TYPE_START2, "b", BASE2)

# ---- cursor: discrete position steps, independent continuous blink ----
cursor_stops = [(0.0, HIDE_X, HIDE_Y)]
cursor_stops.append((TYPE_START1, PAD_X, BASE1))
for i in range(len(LINE1)):
    cursor_stops.append((TYPE_START1 + i * CHAR_STEP, PAD_X + (i + 1) * CW, BASE1))
cursor_stops.append((TYPE_START2, PAD_X, BASE2))
for i in range(len(LINE2)):
    cursor_stops.append((TYPE_START2 + i * CHAR_STEP, PAD_X + (i + 1) * CW, BASE2))
cursor_stops.append((END_TYPE2 + HOLD, HIDE_X, HIDE_Y))
cursor_stops.append((LOOP, HIDE_X, HIDE_Y))

cursor_kf_body = "\n".join(
    f"  {pct(t):.4f}% {{ transform: translate({x:.1f}px,{y:.1f}px); }}" for t, x, y in cursor_stops
)

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Terminal: about me">
<style>
  .panel  {{ fill: #0d1117; }}
  .char   {{ font-family: ui-monospace, "SF Mono", SFMono-Regular, Menlo, Consolas, monospace;
             font-size: {FS}px; fill: #e8edf3;
             animation-duration: {LOOP}s; animation-timing-function: steps(1,end);
             animation-iteration-count: infinite; }}
  .cursor {{ fill: #e8edf3;
             animation: blink 0.9s steps(1,end) infinite,
                        movecursor {LOOP}s steps(1,end) infinite; }}
@keyframes blink {{ 0%,49% {{ opacity: 1; }} 50%,100% {{ opacity: 0; }} }}
@keyframes movecursor {{
{cursor_kf_body}
}}
{chr(10).join(kf1)}
{chr(10).join(kf2)}
@media (prefers-reduced-motion: reduce) {{
  .char   {{ animation: none; opacity: 1; }}
  .cursor {{ animation: none; opacity: 0; }}
}}
</style>
<rect class="panel" x="0" y="0" width="{W}" height="{H}" rx="10"/>
{chr(10).join(nodes1)}
{chr(10).join(nodes2)}
<rect class="cursor" x="0" y="{-FS * 0.78:.1f}" width="2" height="{FS * 0.9:.1f}"/>
</svg>"""

open("assests/terminal.svg", "w").write(svg)
print("loop:", round(LOOP, 2), "bytes:", len(svg), "W:", W, "H:", H)
