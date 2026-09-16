#!/usr/bin/env python3
"""Embed the measured JSON so the deck works offline."""

import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def update():
    data = json.loads((ROOT / "presentation-data.json").read_text(encoding="utf-8"))
    path = ROOT / "presentation.html"
    if not path.exists():
        return
    pattern = r'(<script type="application/json" id="benchmark-data">)[\s\S]*?(</script>)'
    value = json.dumps(data, ensure_ascii=False, indent=2).replace("</", "<\\/")
    text, count = re.subn(pattern, lambda match: match.group(1) + "\n" + value + "\n  " + match.group(2), path.read_text(encoding="utf-8"))
    if count != 1:
        raise RuntimeError("Expected one benchmark data block")
    path.write_text(text, encoding="utf-8")
    (ROOT / "index.html").write_text(text, encoding="utf-8")


if __name__ == "__main__":
    update()
