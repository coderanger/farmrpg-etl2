from collections import defaultdict

from lxml import html
from lxml.html.clean import Cleaner

from utils.parsers import parse_page_fragment

from .models import Quest


SAFE_ATTRS = (html.defs.safe_attrs | {"style"}) - {
    "color",
    "bgcolor",
    "id",
    "class",
    "preload",
}

SAFE_STYLES = {
    "font-family",
    "font-size",
}

CLEANER = Cleaner(
    style=True,
    inline_style=False,
    safe_attrs=SAFE_ATTRS,
)


def _sanitize_style(style: str) -> str:
    rules = [r.split(":", 1) for r in style.split(";")]
    return ";".join(":".join(r) for r in rules if r[0].strip() in SAFE_STYLES)


def sanitize_quest_description(description: str) -> str:
    root = html.fragment_fromstring(description, create_parent=True)
    CLEANER(root)
    for elm in root.iterdescendants():
        style = elm.get("style")
        if style:
            clean_style = _sanitize_style(style)
            if clean_style.strip():
                elm.attrib["style"] = clean_style
            else:
                del elm.attrib["style"]
        # Remove any now-useless <fonts>.
        if elm.tag == "font" and not elm.attrib:
            elm.drop_tag()
    # Strip trailing <br>s.
    for elm in reversed(root):
        if elm.tag == "br" and (elm.tail is None or not elm.tail.strip()):
            elm.drop_tag()
        else:
            break
    inner_clean_content = "".join(html.tostring(e, encoding="unicode") for e in root)
    clean_content = f"{root.text or ' '}{inner_clean_content}"
    return clean_content


def find_all_tags():
    tags = set()
    attrs = defaultdict(set)
    css = defaultdict(set)
    for q in Quest.objects.all():
        root = parse_page_fragment(q.description)
        for elm in root.iterdescendants():
            if elm.tag not in tags:
                print(q.id, q.title, "new tag", elm.tag)
            tags.add(elm.tag)
            for key in elm.attrib:
                if key not in attrs[elm.tag]:
                    print(q.id, q.title, "new attr", elm.tag, key)
                attrs[elm.tag].add(key)
            style = elm.get("style")
            if style:
                for rule in style.split(";"):
                    spec = rule.split(":")[0].strip()
                    if spec not in css[elm.tag]:
                        print(q.id, q.title, "new style", elm.tag, spec)
                    css[elm.tag].add(spec)
    # print("attrs:")
    # for key, val in sorted(attrs.items()):
    #     print(f"{key}: {','.join(val)}")
    # print("")
    # print("css:")
    # for key, val in sorted(css.items()):
    #     print(f"{key}: {','.join(val)}")
