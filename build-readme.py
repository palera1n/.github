import datetime
import operator
import pathlib
import re
import typing
import json

import feedparser
import httpx
import jinja2

ROOT_DIR = pathlib.Path(__file__).parent.resolve()
README_FILE = ROOT_DIR / "README.md"
TEMPLATE_FILE = ROOT_DIR / "TEMPLATE.md"
CREDITS_JSON_URL = "https://palera.in/credits.json"

class ContentPiece(typing.NamedTuple):
    name: str
    github: str
    desc: str


ContentPieces = list[ContentPiece]


def parse_credits_json() -> list[ContentPiece]:
    """
    Parse credits.json to retrieve the contents inside the 'credits' key.
    """
    resp = httpx.get(CREDITS_JSON_URL)
    credits_json = resp.json()
    credits = credits_json.get("credits", [])

    content_pieces = []
    for credit in credits:
        name = credit.get("name", "")
        github = credit.get("github", "")
        desc = credit.get("desc", "")

        content_pieces.append(ContentPiece(github=github, name=name, desc=desc))

    return content_pieces



def generate_readme(content: dict[str, list[ContentPiece]]) -> None:
    """
    Generate Readme file from template file
    """
    template_content = TEMPLATE_FILE.read_text()
    jinja_template = jinja2.Template(template_content)
    updated_content = jinja_template.render(**content)
    README_FILE.write_text(updated_content)


if __name__ == "__main__":
    content = dict(
        credits=parse_credits_json()
    )
    generate_readme(content)
