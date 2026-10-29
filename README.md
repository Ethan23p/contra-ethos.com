# contra-ethos.com

The home of contra-ethos, an independent studio run by Ethan Porter. Plain HTML and CSS, no build step; served by GitHub Pages from `main`.

Project pages and the card grids on both sites are written by `tools/build_pages.py` from one project list; edit the list there and rerun it rather than editing the generated HTML. It expects `ethanporter.xyz` checked out beside this repo:

    uv run --with pillow python tools/build_pages.py
