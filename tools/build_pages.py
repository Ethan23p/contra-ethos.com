"""Generate project pages for both sites and their card sections.

Each project lives on one site ('ce' = contra-ethos.com, 'ep' = ethanporter.xyz).
contra-ethos shows cards for its own projects; ethanporter.xyz shows all of them.
Pages that moved to ethanporter.xyz leave a redirect stub on contra-ethos.
Expects ethanporter.xyz checked out beside this repo.

    uv run --with pillow python tools/build_pages.py
"""
import html, os, re
from pathlib import Path
from PIL import Image

CE = Path(__file__).resolve().parents[1].as_posix()
EP = (Path(CE).parent / 'ethanporter.xyz').as_posix()
ROOT = {'ce': CE, 'ep': EP}
URL = {'ce': 'https://contra-ethos.com', 'ep': 'https://ethanporter.xyz'}
GH = 'https://github.com/Ethan23p/'
MOVED = ['dkb-library', 'ai-kassandra', 'agent-dashboard']  # once on contra-ethos

GAMES_LINE = 'An attempt at a game with Tetris-like purity: one screen, a few fundamental elements, mechanics that come naturally, difficulty you can feel, room for skill, and actual fun.'

P = [
    dict(slug='dkb-library', site='ep', title='DKB Library', meta='Bun, TypeScript, SQLite, Claude Agent SDK · alpha · archived', layout='full', image=False,
         line="I didn't trust modern AI models to capture the full nuance of a given article or whitepaper, let alone a body of research, so I made an agentic system that sits atop my research and serves as my librarian, subject-matter expert, and data scientist.",
         note="This project was first shipped as my entry to a competition hosted by the Future of Life Foundation; now I've archived it as I develop a more general solution.",
         links=[('Code', GH + 'dkb-library')]),
    dict(slug='ai-kassandra', site='ep', title='AI Kassandra', meta='Gemini, Hono, TypeScript, SQLite · beta · archived', layout='half',
         line='I wanted an app that provided insight, validation, and confidence, like horoscopes do for some people, but based on data and personality psychology, instead of constellations.',
         alt='An AI Kassandra assessment question: a road trip hits a snag, with four ways to respond.',
         links=[('Code', GH + 'AI_Kassandra')],
         gallery=[('ai-kassandra-profile', 'A user profile showing Big Five scores as bars.')]),
    dict(slug='agent-dashboard', site='ep', title='Agent Dashboard', meta='MCP, Python, Textual · alpha · archived', layout='half', pos='20% 50%',
         line="Before I knew what a \"harness\" was, I needed a testbed for my crazy hypotheses about AI. Claude Code eventually stepped in, but this project is still in the back of my mind; I'll be returning to those hypotheses.",
         alt='Agent Dashboard running in a terminal: an agent list on the left, a conversation with the active agent on the right, and a prompt box below.',
         links=[('Code', GH + 'agent-dashboard')]),
    dict(slug='phosphor-sand', site='ce', title='Phosphor Sand', meta='Rust, WebGPU · alpha · active', layout='full', pos='50% 45%',
         line="I wanted to explore cellular automata and see if I could surprise myself - I managed to: today it has plants that transport energy, and soap that interacts with water and oil to create isolated bubbles much larger than a single cell. I'm still actively iterating on the concept.",
         alt='Phosphor Sand on a phone: a basin of water between sand slopes, with stone drawn into it and dark air bubbles scattered through the water, under a CRT scanline look.',
         links=[('Play', 'https://sand.contra-ethos.com'), ('Code', GH + 'Phosphor-Sand')]),
    dict(slug='gravity-blobs', site='ce', title='Gravity Blobs', meta='Rust, WebGPU · alpha · active', layout='half', pos='50% 62%',
         line=GAMES_LINE,
         alt='Gravity Blobs on a phone: numbered blobs clustered at the center of a circular arena, with the next blob aimed from the rim.',
         links=[('Play', 'https://play.contra-ethos.com/blob/'), ('Code', GH + 'contra-ethos-games'), ('Original prototype', GH + 'Blob-Merge-Game')]),
    dict(slug='dice-merge', site='ce', title='Dice Merge Game', meta='Rust, WebGPU · alpha · active', layout='half', pos='50% 42%',
         line=GAMES_LINE,
         alt='Dice Merge Game: a five-by-five board holding dice valued one to four, a score of 90, and the next die below.',
         links=[('Play', 'https://play.contra-ethos.com/dice/'), ('Code', GH + 'contra-ethos-games'), ('Original prototype', GH + 'Dice-Merge-Testbed')]),
    dict(slug='claude-code-plugins', site='ce', title='Claude Code plugins', meta='Claude Code, Claude Agent SDK, Logseq CLI', layout='full', image=False,
         line='These are simply the various things that were worth extending Claude Code with for my setup - they are not much, but a good demonstration of my working philosophy in agentic AI.',
         items=[('logseq-interface', 'agent access to my Logseq graph through its CLI'),
                ('bounded-graph-access', "limits that access to the parts of the graph I've chosen to share"),
                ('tacit-frames', 'skills that load a source text verbatim as framing, rather than distilling it into procedures'),
                ('design-patterns', 'how to construct those tacit-knowledge skills'),
                ('eval-harness', 'evaluate a system by having a real Claude instance operate it'),
                ('mp-skills', "Matt Pocock's workflow skills, kept apart and credited to him")],
         links=[('Code', GH + 'ethans-plugins_Claude-Code'), ("Matt Pocock's skills", 'https://github.com/mattpocock/skills')]),
]

e = html.escape


def t(s):
    """Escape prose; keep a spaced hyphen from starting a line."""
    return e(s).replace(' - ', '&nbsp;- ')


def size(path):
    with Image.open(path) as im:
        return im.size


FONTS = {
    'ce': 'family=IBM+Plex+Mono:wght@400&family=Schibsted+Grotesk:wght@700&family=Source+Sans+3:wght@400;600',
    'ep': 'family=Jost:wght@300;400;600',
}
WORDMARK = {'ce': 'contra-ethos', 'ep': 'Ethan Porter'}
FOOT = {
    'ce': '''<footer>
<span>contra-ethos © 2026</span>
<a href="https://ethanporter.xyz">[ethanporter.xyz]</a>
</footer>
''',
    'ep': '<footer>Ethan Porter © 2026</footer>\n',
}
CRUMB = {'ce': '[projects]', 'ep': 'Projects'}


def head(site, title, desc):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="color-scheme" content="dark">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{FONTS[site]}&display=swap">
<link rel="stylesheet" href="/style.css">
</head>
<body>
<header>
<a class="wordmark" href="/">{WORDMARK[site]}</a>
</header>
'''


def img(root, rel, alt, lazy=False):
    w, h = size(f'{root}/{rel}')
    l = ' loading="lazy"' if lazy else ''
    return f'<img src="/{rel}" alt="{e(alt)}" width="{w}" height="{h}"{l}>'


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)


def page(p):
    site, root = p['site'], ROOT[p['site']]
    out = [head(site, f"{p['title']} · {WORDMARK[site]}", p['line']), '\n<main>\n<article class="project">\n']
    out.append(f'<p class="crumb"><a href="/#projects">{CRUMB[site]}</a></p>\n')
    out.append(f"<h1>{e(p['title'])}</h1>\n<p class=\"meta\">{e(p['meta'])}</p>\n")
    label = (lambda x: f'[{e(x)}]') if site == 'ce' else e
    out.append('<ul class="links">\n' + ''.join(f'<li><a href="{u}">{label(x)}</a></li>\n' for x, u in p['links']) + '</ul>\n')
    if p.get('image', True):
        out.append(f'<figure class="hero">{img(root, "images/projects/" + p["slug"] + ".webp", p["alt"])}</figure>\n')
    out.append(f"<blockquote>\n<p>{t(p['line'])}</p>\n</blockquote>\n")
    if p.get('note'):
        out.append(f"<p>{t(p['note'])}</p>\n")
    if p.get('items'):
        out.append('<ul class="outline">\n' + ''.join(f'<li><code>{e(n)}</code>: {t(d)}</li>\n' for n, d in p['items']) + '</ul>\n')
    if p.get('gallery'):
        out.append('<div class="gallery">\n' + ''.join(
            f'<figure>{img(root, "images/projects/" + s + ".webp", a, lazy=True)}</figure>\n' for s, a in p['gallery']) + '</div>\n')
    out.append('</article>\n</main>\n\n' + FOOT[site] + '</body>\n</html>\n')
    write(f"{root}/projects/{p['slug']}/index.html", ''.join(out))


def stub(slug):
    to = f"{URL['ep']}/projects/{slug}/"
    write(f'{CE}/projects/{slug}/index.html', f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Moved</title>
<link rel="canonical" href="{to}">
<meta http-equiv="refresh" content="0; url={to}">
</head>
<body>
<p>This page moved to <a href="{to}">{to}</a>.</p>
</body>
</html>
''')


def card(p, root, href):
    cls = f"card card--{p['layout']}" + ('' if p.get('image', True) else ' card--text')
    out = [f'<a class="{cls}" href="{href}">\n']
    if p.get('image', True):
        rel = f"images/projects/{p['slug']}-card.webp"
        w, h = size(f'{root}/{rel}')
        style = []
        if p.get('fit'): style.append(f"object-fit:{p['fit']}")
        if p.get('pos'): style.append(f"object-position:{p['pos']}")
        st = f' style="{";".join(style)}"' if style else ''
        out.append(f'<img src="/{rel}" alt="" width="{w}" height="{h}" loading="lazy"{st}>\n')
    out.append(f'<span class="card-title">{e(p["title"])}</span>\n<span class="card-meta">{e(p["meta"])}</span>\n')
    if not p.get('image', True):
        out.append(f'<span class="card-line">{t(p["line"])}</span>\n')
    out.append('</a>\n')
    return ''.join(out)


def href(p, from_site):
    path = f"/projects/{p['slug']}/"
    return path if p['site'] == from_site else URL[p['site']] + path


def cards(site, ps):
    return '<div class="cards">\n' + ''.join(card(p, ROOT[site], href(p, site)) for p in ps) + '</div>\n'


def put_cards(site, block):
    path = f'{ROOT[site]}/index.html'
    s = open(path, encoding='utf-8').read()
    s, n = re.subn(r'<div class="cards">\n.*?</div>\n', lambda m: block, s, count=1, flags=re.S)
    assert n == 1, path
    write(path, s)


for p in P:
    page(p)
for slug in MOVED:
    stub(slug)

put_cards('ce', cards('ce', [p for p in P if p['site'] == 'ce']))
put_cards('ep', cards('ep', P))
print('ok')
