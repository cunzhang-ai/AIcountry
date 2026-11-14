"""Build the public reading site from canonical Markdown."""

import html
import json
import posixpath
import re
import shutil
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit, urlunsplit

from markdown_it import MarkdownIt


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "_site"
REPO = "https://github.com/cunzhang-ai/AIcountry"
HAN = re.compile(r"[\u3400-\u9fff\uf900-\ufaff\U00020000-\U000323af]")
HOMEPAGE = [
    ("National settlement", "research/NATIONAL-SETTLEMENT.md", "The institutions the project chooses and why."),
    ("Opening programme", "research/settlement/first-round-mandate/01-decisions-and-conditions.md", "Democratic authority, continuity supply, and documented repairs."),
    ("Fourteen chapters", "research/country/README.md", "The detailed design, from rights and elections to finance, ecology, and AI."),
    ("Edition 1", "research/edition/README.md", "The frozen research design and its publication record."),
    ("Evidence and limitations", "research/status/current/06-national-choices-and-evidence.md", "What supports the design, and where evidence is incomplete."),
    ("Contribute", "CONTRIBUTING.md", "A short guide for people and AI tools."),
]
MARKDOWN = MarkdownIt("commonmark", {"html": False}).enable("table")


def relative(source, destination):
    path = posixpath.relpath(destination, posixpath.dirname(source) or ".")
    return quote(path, safe="/-._~")


def title_for(path, body):
    heading = next((line[2:].strip() for line in body.splitlines() if line.startswith("# ")), None)
    return heading or Path(path).stem.replace("-", " ").title()


def rewrite_links(tokens, source, pages):
    for token in tokens:
        if token.type in ("link_open", "image"):
            attribute = "href" if token.type == "link_open" else "src"
            parsed = urlsplit(token.attrGet(attribute) or "")
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            target = posixpath.normpath(posixpath.join(posixpath.dirname(source), unquote(parsed.path)))
            if target not in pages and target + "/README.md" in pages:
                target += "/README.md"
            if target in pages:
                href = relative(source, pages[target])
            elif (ROOT / target).is_file() and not target.startswith("../"):
                kind = "raw" if attribute == "src" else "blob"
                href = f"{REPO}/{kind}/main/{quote(target)}"
            elif (ROOT / target).is_dir() and not target.startswith("../"):
                href = f"{REPO}/tree/main/{quote(target)}"
            else:
                continue
            destination = urlsplit(href)
            token.attrSet(attribute, urlunsplit(destination._replace(query=parsed.query, fragment=parsed.fragment)))
        if token.children:
            rewrite_links(token.children, source, pages)


def render(source, body, pages):
    environment = {}
    tokens = MARKDOWN.parse(body, environment)
    rewrite_links(tokens, source, pages)
    ids = set()
    for index, token in enumerate(tokens):
        if token.type != "heading_open":
            continue
        heading = "".join(child.content for child in tokens[index + 1].children or [] if child.type in ("text", "code_inline"))
        base = re.sub(r"[^\w -]", "", heading.lower()).replace(" ", "-")
        slug = base
        sequence = 1
        while slug in ids:
            slug = f"{base}-{sequence}"
            sequence += 1
        ids.add(slug)
        token.attrSet("id", slug)
    return MARKDOWN.renderer.render(tokens, MARKDOWN.options, environment)


def layout(path, title, body, extra=""):
    url = lambda destination: relative(path, destination)
    name = html.escape(title)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{name} · AIcountry</title>
<meta name="description" content="A research design for a democratic future country, with essential services and accountable AI assistance.">
<link rel="stylesheet" href="{url('assets/style.css')}">
</head>
<body>
<header class="masthead"><nav aria-label="Main navigation">
<a class="brand" href="{url('index.html')}">AIcountry</a>
<a href="{url('research/NATIONAL-SETTLEMENT.html')}">Design</a>
<a href="{url('research/country/README.html')}">Chapters</a>
<a href="{url('search.html')}">Search</a>
<a href="{url('CONTRIBUTING.html')}">Contribute</a>
</nav></header>
<main>{body}</main>
<footer><a href="{REPO}">GitHub</a><a href="{url('llms.txt')}">AI guide</a><a href="{url('index.json')}">Document index</a></footer>
{extra}
</body></html>
"""


def write(path, contents):
    target = OUT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(contents, encoding="utf-8")


def home(pages):
    cards = [
        f'<a class="card" href="{quote(pages[path])}"><h2>{title}</h2><p>{description}</p></a>'
        for title, path, description in HOMEPAGE
    ]
    chapters = []
    for source in sorted(pages):
        if re.fullmatch(r"research/country/C\d\d-[^/]+\.md", source):
            title = title_for(source, (ROOT / source).read_text(encoding="utf-8"))
            chapters.append(f'<li><a href="{quote(pages[source])}">{html.escape(title)}</a></li>')
    assert len(chapters) == 14
    return f"""
<section class="hero">
<p class="edition">Edition 1</p>
<h1>Designing a future country</h1>
<p>A constitutional democracy with enforceable rights, dependable public services, local self-government, and AI under accountable public authority.</p>
<a class="primary" href="research/NATIONAL-SETTLEMENT.html">Read the national settlement</a>
</section>
<section class="cards" aria-label="Start reading">{''.join(cards)}</section>
<section class="chapter-list"><h2>Explore the fourteen chapters</h2><ul>{''.join(chapters)}</ul></section>
"""


def main():
    sources = [ROOT / name for name in ("README.md", "CONTRIBUTING.md", "AGENTS.md")]
    sources.extend((ROOT / "research").rglob("*.md"))
    sources.extend((ROOT / "public" / "research").glob("*.md"))
    pages = {p.relative_to(ROOT).as_posix(): p.relative_to(ROOT).with_suffix(".html").as_posix() for p in sorted(sources)}
    if OUT.exists():
        shutil.rmtree(OUT)

    index = []
    for source, page in pages.items():
        path = ROOT / source
        content = path.read_text(encoding="utf-8")
        if HAN.search(source) or HAN.search(content):
            raise ValueError(f"Non-English public text in {source}")
        title = title_for(source, content)
        body = render(source, content, pages)
        toolbar = f'<p class="source"><a href="{relative(page, source)}">Markdown</a> · <a href="{REPO}/blob/main/{quote(source)}">Source on GitHub</a></p>'
        write(page, layout(page, title, f"<article>{toolbar}{body}</article>"))
        write(source, content)
        index.append({"title": title, "url": page, "markdown": source})

    write("index.html", layout("index.html", "Designing a future country", home(pages)))
    write("search.html", layout("search.html", "Search the design", """
<section class="chapter-list">
<h1>Search the design</h1>
<label for="query">Search by title or document path</label>
<input id="query" type="search" placeholder="Try housing, elections, or C11" autocomplete="off">
<p id="result-count" role="status"></p>
<ul id="results"></ul>
<noscript><a href="research/country/README.html">Browse the chapter map</a></noscript>
</section>
""", '<script src="assets/search.js" defer></script>'))
    write("index.json", json.dumps(index, ensure_ascii=False, indent=2) + "\n")
    write("llms.txt", (ROOT / "site/llms.txt").read_text(encoding="utf-8"))
    write(".nojekyll", "")
    for asset in ("style.css", "search.js"):
        write(f"assets/{asset}", (ROOT / "site" / asset).read_text(encoding="utf-8"))
    assert all((OUT / item[key]).is_file() for item in index for key in ("url", "markdown"))
    print(f"Built {len(pages)} reading pages and indexed {len(index)} documents.")


if __name__ == "__main__":
    main()
