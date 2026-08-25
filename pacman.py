EATEN = "IT'S PROBABLY A CACHING ISSUE"
REVEAL = "it was a caching issue"

W, H = 844, 150
CW = 13                # per-character advance
FS = 20
BASELINE = 92
PAC_R = 20
PAC_CY = 84

LOOP = 14.0
ENTER_END = 0.6        # pac starts moving
CROSS_END = 9.0        # pac exits right
PAC_X0, PAC_X1 = -40.0, 884.0

X0 = (W - len(EATEN) * CW) / 2.0


def pct(t):
    return t / LOOP * 100.0


def esc(c):
    return {"&": "&amp;", "<": "&lt;", ">": "&gt;"}.get(c, c)


# ---- per-character disappearance keyframes -------------------------------
char_kfs, char_nodes = [], []
for i, ch in enumerate(EATEN):
    cx = X0 + i * CW + CW / 2.0
    t = ENTER_END + (cx - PAC_X0) / (PAC_X1 - PAC_X0) * (CROSS_END - ENTER_END)
    p = pct(t)
    char_kfs.append(
        f"@keyframes e{i}{{0%,{p:.3f}%{{opacity:1}}{min(p + 0.25, 100):.3f}%,100%{{opacity:0}}}}"
    )
    if ch != " ":
        char_nodes.append(
            f'<text class="noise" x="{cx:.1f}" y="{BASELINE}" '
            f'style="animation-name:e{i}">{esc(ch)}</text>'
        )

pac_kf = (
    f"@keyframes drive{{"
    f"0%,{pct(ENTER_END):.3f}%{{transform:translateX({PAC_X0}px)}}"
    f"{pct(CROSS_END):.3f}%,100%{{transform:translateX({PAC_X1}px)}}}}"
)
ghost_kf = (
    f"@keyframes chase{{"
    f"0%,{pct(ENTER_END):.3f}%{{transform:translateX({PAC_X0 - 118}px)}}"
    f"{pct(CROSS_END):.3f}%,100%{{transform:translateX({PAC_X1 - 118}px)}}}}"
)
ghost2_kf = (
    f"@keyframes chase2{{"
    f"0%,{pct(ENTER_END):.3f}%{{transform:translateX({PAC_X0 - 196}px)}}"
    f"{pct(CROSS_END):.3f}%,100%{{transform:translateX({PAC_X1 - 196}px)}}}}"
)
reveal_kf = (
    f"@keyframes reveal{{"
    f"0%,{pct(9.6):.3f}%{{opacity:0}}"
    f"{pct(10.4):.3f}%,{pct(12.8):.3f}%{{opacity:1}}"
    f"{pct(13.6):.3f}%,100%{{opacity:0}}}}"
)

upper = f"M0,0 L{PAC_R},0 A{PAC_R},{PAC_R} 0 0 0 {-PAC_R},0 Z"
lower = f"M0,0 L{-PAC_R},0 A{PAC_R},{PAC_R} 0 0 0 {PAC_R},0 Z"

ghost_path = (
    "M -14 13 L -14 -2 A 14 14 0 0 1 14 -2 L 14 13 "
    "L 9.3 8.3 L 4.6 13 L 0 8.3 L -4.6 13 L -9.3 8.3 Z"
)

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Pac-Man eating buzzwords">
<style>
  .panel  {{ fill: #0d1117; }}
  .noise  {{ font-family: ui-monospace, "SF Mono", SFMono-Regular, Menlo, Consolas, monospace;
             font-size: {FS}px; fill: #6e7681; text-anchor: middle; letter-spacing: 0;
             animation-duration: {LOOP}s; animation-timing-function: steps(1,end);
             animation-iteration-count: infinite; }}
  .truth  {{ font-family: ui-monospace, "SF Mono", SFMono-Regular, Menlo, Consolas, monospace;
             font-size: {FS}px; fill: #e8edf3; text-anchor: middle;
             animation: reveal {LOOP}s linear infinite; opacity: 0; }}
  .rider  {{ animation: drive {LOOP}s linear infinite; }}
  .ghost1 {{ animation: chase {LOOP}s linear infinite; }}
  .ghost2 {{ animation: chase2 {LOOP}s linear infinite; }}
  .jaw    {{ fill: #ffd93d; }}
{pac_kf}
{ghost_kf}
{ghost2_kf}
{reveal_kf}
{chr(10).join(char_kfs)}
@media (prefers-reduced-motion: reduce) {{
  .rider,.ghost1,.ghost2,.noise {{ animation: none }}
  .truth {{ animation: none; opacity: 1 }}
}}
</style>
<rect class="panel" x="0" y="0" width="{W}" height="{H}" rx="10"/>
{chr(10).join(char_nodes)}
<text class="truth" x="{W / 2}" y="{BASELINE}">{REVEAL}</text>

<g class="ghost2"><g transform="translate(0,{PAC_CY})">
  <path d="{ghost_path}" fill="#5ad2f4"/>
  <ellipse cx="-5" cy="-2" rx="4.2" ry="5" fill="#fff"/><ellipse cx="5" cy="-2" rx="4.2" ry="5" fill="#fff"/>
  <circle cx="-3.6" cy="-2" r="2.1" fill="#0d1117"/><circle cx="6.4" cy="-2" r="2.1" fill="#0d1117"/>
</g></g>
<g class="ghost1"><g transform="translate(0,{PAC_CY})">
  <path d="{ghost_path}" fill="#ef5f5f"/>
  <ellipse cx="-5" cy="-2" rx="4.2" ry="5" fill="#fff"/><ellipse cx="5" cy="-2" rx="4.2" ry="5" fill="#fff"/>
  <circle cx="-3.6" cy="-2" r="2.1" fill="#0d1117"/><circle cx="6.4" cy="-2" r="2.1" fill="#0d1117"/>
</g></g>

<g class="rider"><g transform="translate(0,{PAC_CY})">
  <path class="jaw" d="{upper}">
    <animateTransform attributeName="transform" type="rotate"
      values="0 0 0; -34 0 0; 0 0 0" dur="0.34s" repeatCount="indefinite"
      calcMode="spline" keyTimes="0;0.5;1" keySplines="0.4 0 0.6 1; 0.4 0 0.6 1"/>
  </path>
  <path class="jaw" d="{lower}">
    <animateTransform attributeName="transform" type="rotate"
      values="0 0 0; 34 0 0; 0 0 0" dur="0.34s" repeatCount="indefinite"
      calcMode="spline" keyTimes="0;0.5;1" keySplines="0.4 0 0.6 1; 0.4 0 0.6 1"/>
  </path>
</g></g>
</svg>"""

open("pacman-eats.svg", "w").write(svg)
print("chars:", len(EATEN), "bytes:", len(svg), "X0:", X0)
