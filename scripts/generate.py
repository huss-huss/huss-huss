"""Generate the animated SVGs used by the profile README.

Runs daily in GitHub Actions and publishes to the `output` branch, so the README
never depends on third-party image services. Standard library only.

    GITHUB_TOKEN=... python scripts/generate.py dist/
"""

from __future__ import annotations

import json
import os
import sys
import urllib.request
from html import escape
from pathlib import Path

USER = "huss-huss"
FONT = "'Segoe UI', Ubuntu, 'Helvetica Neue', Arial, sans-serif"
MONO = "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace"
BG, PANEL, BORDER, TEXT, MUTED, ACCENT = "#0d1117", "#161b22", "#30363d", "#e6edf3", "#8b949e", "#36bcf7"

TAGLINES = [
    "I build backends that put LLMs to work",
    "FastAPI · Celery · PostgreSQL · Redis",
    "Tool-calling agents & structured outputs",
    "Resilient data extraction & automation",
]

# Featured repos, in display order. Description/language/topics come from the API.
FEATURED = [
    "ai-support-automation-system",
    "jarvis",
    "ai-job-intelligence-system",
    "table-extraction-pro",
    "n8n-ai-news2linked",
    "crawlforge",
    "llm-gateway",
]
SKIP_LANGS = {"Jupyter Notebook", "HTML", "CSS", "Shell", "Dockerfile", "Procfile", "Makefile"}
LANG_COLORS = {
    "Python": "#3572A5", "TypeScript": "#3178c6", "JavaScript": "#f1e05a", "Dart": "#00B4AB",
    "Solidity": "#AA6746", "Shell": "#89e051", "Go": "#00ADD8", "Java": "#b07219", "C++": "#f34b7d", "PLpgSQL": "#336790",
}  # fmt: skip


def api(path: str):
    token = os.environ.get("GITHUB_TOKEN", "")
    headers = {"Accept": "application/vnd.github+json", "User-Agent": USER}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(f"https://api.github.com{path}", headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return None
        raise


# --- header / footer -------------------------------------------------------------


def header() -> str:
    w, h = 1200, 300
    n = len(TAGLINES)
    period = n * 3
    lines = []
    for i, text in enumerate(TAGLINES):
        start, end = i / n * 100, (i + 1) / n * 100
        lines.append(
            f'<text class="tag t{i}" x="{w / 2}" y="214" text-anchor="middle">{escape(text)}</text>'
            f"<style>.t{i}{{animation:tag{i} {period}s infinite}}"
            f"@keyframes tag{i}{{0%,{max(start - 0.01, 0):.2f}%{{opacity:0;transform:translateY(8px)}}"
            f"{start + 3:.2f}%,{end - 4:.2f}%{{opacity:1;transform:translateY(0)}}"
            f"{end - 1:.2f}%,100%{{opacity:0;transform:translateY(-8px)}}}}</style>"
        )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#0f2027"><animate attributeName="stop-color" values="#0f2027;#13293d;#0f2027" dur="10s" repeatCount="indefinite"/></stop>
    <stop offset="55%" stop-color="#203a43"/>
    <stop offset="100%" stop-color="#2c5364"><animate attributeName="stop-color" values="#2c5364;#1b4d6b;#2c5364" dur="10s" repeatCount="indefinite"/></stop>
  </linearGradient>
  <linearGradient id="glow" x1="0" x2="1">
    <stop offset="0%" stop-color="{ACCENT}" stop-opacity="0"/><stop offset="50%" stop-color="{ACCENT}"/><stop offset="100%" stop-color="{ACCENT}" stop-opacity="0"/>
  </linearGradient>
  <clipPath id="r"><rect width="{w}" height="{h}" rx="16"/></clipPath>
</defs>
<style>
  .name {{ font: 700 58px {FONT}; fill: #fff; letter-spacing: 1px; animation: rise 1.2s ease-out both; }}
  .role {{ font: 500 24px {FONT}; fill: {ACCENT}; letter-spacing: 3px; animation: rise 1.2s .3s ease-out both; }}
  .tag {{ font: 400 22px {MONO}; fill: {TEXT}; opacity: 0; transform-box: fill-box; }}
  .dot {{ fill: {ACCENT}; opacity: .35; animation: twinkle 4s ease-in-out infinite; }}
  @keyframes rise {{ from {{ opacity: 0; transform: translateY(14px); }} to {{ opacity: 1; transform: translateY(0); }} }}
  @keyframes twinkle {{ 0%,100% {{ opacity: .15; }} 50% {{ opacity: .6; }} }}
</style>
<g clip-path="url(#r)">
  <rect width="{w}" height="{h}" fill="url(#bg)"/>
  {''.join(f'<circle class="dot" cx="{x}" cy="{y}" r="{r}" style="animation-delay:{d}s"/>' for x, y, r, d in [
      (90, 60, 2, 0), (180, 230, 1.5, 1), (300, 40, 1.5, 2), (980, 70, 2, .5), (1100, 210, 1.5, 1.5),
      (860, 250, 2, 2.5), (520, 30, 1.2, 3), (700, 270, 1.2, 1.2), (1040, 130, 1.2, 2.2), (140, 140, 1.2, .8)])}
  <path fill="{ACCENT}" fill-opacity=".08" d="M0 250 Q300 210 600 250 T1200 250 V300 H0Z">
    <animate attributeName="d" dur="8s" repeatCount="indefinite" values="M0 250 Q300 210 600 250 T1200 250 V300 H0Z;M0 245 Q300 285 600 245 T1200 245 V300 H0Z;M0 250 Q300 210 600 250 T1200 250 V300 H0Z"/>
  </path>
  <path fill="#ffffff" fill-opacity=".05" d="M0 265 Q300 295 600 265 T1200 265 V300 H0Z">
    <animate attributeName="d" dur="6s" repeatCount="indefinite" values="M0 265 Q300 295 600 265 T1200 265 V300 H0Z;M0 270 Q300 240 600 270 T1200 270 V300 H0Z;M0 265 Q300 295 600 265 T1200 265 V300 H0Z"/>
  </path>
  <text class="name" x="{w / 2}" y="118" text-anchor="middle">Hussen Mohammed</text>
  <text class="role" x="{w / 2}" y="162" text-anchor="middle">BACKEND &amp; AI SYSTEMS ENGINEER</text>
  <rect x="{w / 2 - 160}" y="180" width="320" height="2" fill="url(#glow)">
    <animate attributeName="width" values="0;320" dur="1.2s" begin=".6s" fill="freeze"/>
    <animate attributeName="x" values="{w / 2};{w / 2 - 160}" dur="1.2s" begin=".6s" fill="freeze"/>
  </rect>
  {''.join(lines)}
</g>
</svg>"""


def footer() -> str:
    w, h = 1200, 90
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<defs><linearGradient id="f" x1="0" x2="1"><stop offset="0%" stop-color="#2c5364"/><stop offset="50%" stop-color="#203a43"/><stop offset="100%" stop-color="#0f2027"/></linearGradient></defs>
<path fill="url(#f)" d="M0 40 Q300 0 600 40 T1200 40 V90 H0Z">
  <animate attributeName="d" dur="7s" repeatCount="indefinite" values="M0 40 Q300 0 600 40 T1200 40 V90 H0Z;M0 35 Q300 75 600 35 T1200 35 V90 H0Z;M0 40 Q300 0 600 40 T1200 40 V90 H0Z"/>
</path>
</svg>"""


# --- project cards ---------------------------------------------------------------


def _wrap(text: str, width: int, max_lines: int) -> list[str]:
    words, lines, line = text.split(), [], ""
    for word in words:
        if len(line) + len(word) + 1 > width:
            lines.append(line)
            line = word
            if len(lines) == max_lines:
                break
        else:
            line = f"{line} {word}".strip()
    if line and len(lines) < max_lines:
        lines.append(line)
    if len(lines) == max_lines and len(" ".join(lines)) < len(text):
        lines[-1] = lines[-1].rstrip(".,;:") + "…"
    return lines


def primary_language(repo: dict) -> str:
    """Main code language, ignoring markup/notebooks (a dashboard's HTML shouldn't label a Python project)."""
    langs = api(path=f"/repos/{USER}/{repo['name']}/languages") or {}
    code = [(k, v) for k, v in langs.items() if k not in SKIP_LANGS]
    return max(code, key=lambda kv: kv[1])[0] if code else (repo.get("language") or "")


def card(repo: dict, index: int) -> str:
    w, h = 580, 170
    lang = primary_language(repo)
    color = LANG_COLORS.get(lang, MUTED)
    desc = _wrap(repo.get("description") or "", 72, 2)
    topics = (repo.get("topics") or [])[:4]
    delay = index * 0.15
    chips, x = [], 24
    for t in topics:
        cw = 14 + len(t) * 7.2
        chips.append(
            f'<rect x="{x}" y="112" width="{cw:.0f}" height="22" rx="11" fill="{ACCENT}" fill-opacity=".12"/>'
            f'<text class="chip" x="{x + cw / 2:.0f}" y="127" text-anchor="middle">{escape(t)}</text>'
        )
        x += cw + 8
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<style>
  .c {{ animation: in .8s {delay}s ease-out both; }}
  .t {{ font: 600 19px {FONT}; fill: {ACCENT}; }}
  .d {{ font: 400 14px {FONT}; fill: {TEXT}; }}
  .chip {{ font: 500 12px {FONT}; fill: {ACCENT}; }}
  .m {{ font: 400 13px {FONT}; fill: {MUTED}; }}
  .bar {{ animation: grow 1.4s {delay + .3}s ease-out both; transform-origin: left; }}
  @keyframes in {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: none; }} }}
  @keyframes grow {{ from {{ transform: scaleX(0); }} to {{ transform: scaleX(1); }} }}
</style>
<g class="c">
  <rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="12" fill="{PANEL}" stroke="{BORDER}"/>
  <rect class="bar" x="1" y="1" width="{w - 2}" height="3" rx="1.5" fill="{color}"/>
  <text class="t" x="24" y="40">{escape(repo["name"])}</text>
  {''.join(f'<text class="d" x="24" y="{68 + i * 20}">{escape(line)}</text>' for i, line in enumerate(desc))}
  {''.join(chips)}
  <circle cx="30" cy="152" r="6" fill="{color}"/>
  <text class="m" x="42" y="157">{escape(lang or "—")}</text>
  <text class="m" x="{w - 24}" y="157" text-anchor="end">★ {repo.get("stargazers_count", 0)}</text>
</g>
</svg>"""


# --- stats -----------------------------------------------------------------------


# From the public Upwork profile; update by hand when they change.
TRACK_RECORD = [("2,500+", "hours delivered on Upwork"), ("15", "freelance projects completed"), ("100%", "job success score")]


def stats(languages: list[tuple[str, float]]) -> str:
    w, h = 1200, 210
    total = sum(v for _, v in languages) or 1
    shares = [(name, v / total) for name, v in languages]
    bar, x = [], 40.0
    for i, (name, share) in enumerate(shares):
        bw = share * (w - 80)
        bar.append(
            f'<rect class="seg" x="{x:.1f}" y="128" width="{bw:.1f}" height="12" fill="{LANG_COLORS.get(name, MUTED)}"'
            f' style="animation-delay:{0.2 + i * 0.15:.2f}s"/>'
        )
        x += bw
    legend, lx = [], 40
    for name, share in shares:
        legend.append(
            f'<circle cx="{lx + 6}" cy="172" r="6" fill="{LANG_COLORS.get(name, MUTED)}"/>'
            f'<text class="m" x="{lx + 18}" y="177">{escape(name)} {share * 100:.0f}%</text>'
        )
        lx += 40 + len(name) * 8 + 40
    figures = TRACK_RECORD
    cols = "".join(
        f'<text class="big" x="{120 + i * 380}" y="70">{escape(v)}</text>'
        f'<text class="m" x="{120 + i * 380}" y="96">{escape(label)}</text>'
        for i, (v, label) in enumerate(figures)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<style>
  .big {{ font: 700 34px {FONT}; fill: {ACCENT}; animation: in .9s ease-out both; }}
  .m {{ font: 400 14px {FONT}; fill: {MUTED}; }}
  .seg {{ animation: grow 1s ease-out both; transform-origin: left; transform-box: fill-box; }}
  @keyframes in {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: none; }} }}
  @keyframes grow {{ from {{ transform: scaleX(0); }} to {{ transform: scaleX(1); }} }}
</style>
<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="12" fill="{PANEL}" stroke="{BORDER}"/>
{cols}
<clipPath id="b"><rect x="40" y="128" width="{w - 80}" height="12" rx="6"/></clipPath>
<g clip-path="url(#b)">{''.join(bar)}</g>
{''.join(legend)}
</svg>"""


def main(out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    (out / "header.svg").write_text(header())
    (out / "footer.svg").write_text(footer())

    for i, name in enumerate(FEATURED):
        repo = api(path=f"/repos/{USER}/{name}")
        if repo and not repo.get("private"):
            (out / f"card-{name}.svg").write_text(card(repo, i % 2))

    repos = api(path=f"/users/{USER}/repos?per_page=100&type=owner") or []
    totals: dict[str, float] = {}
    for r in repos:
        if r.get("fork"):
            continue
        for lang, size in (api(path=f"/repos/{USER}/{r['name']}/languages") or {}).items():
            if lang not in SKIP_LANGS:
                totals[lang] = totals.get(lang, 0) + size
    top = sorted(totals.items(), key=lambda kv: -kv[1])[:6]
    (out / "stats.svg").write_text(stats(top))
    print(f"wrote {len(list(out.glob('*.svg')))} SVGs to {out}")


if __name__ == "__main__":
    main(Path(sys.argv[1] if len(sys.argv) > 1 else "dist"))
