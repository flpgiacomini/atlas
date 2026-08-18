#!/usr/bin/env python3
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import sys

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
BASE = "/atlas/"
errors = []

class Parser(HTMLParser):
    def __init__(self, source):
        super().__init__(); self.source = source
    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        for key in ("href", "src"):
            value = values.get(key)
            if not value or value.startswith(("#", "mailto:", "tel:", "data:")): continue
            parsed = urlparse(value)
            if parsed.scheme or parsed.netloc: continue
            if value.startswith("/") and not value.startswith(BASE):
                errors.append(f"{self.source}: root-absolute URL outside {BASE}: {value}")

for html in DIST.rglob("*.html"):
    parser = Parser(html.relative_to(DIST)); parser.feed(html.read_text(encoding="utf-8"))
print({"passed": not errors, "errors": errors, "html_files": len(list(DIST.rglob('*.html')))})
sys.exit(0 if not errors else 1)
