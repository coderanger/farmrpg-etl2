from lxml import html
from lxml.etree import _Element
from lxml.html.clean import Cleaner


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


def _is_br(elm: _Element | None, no_tail=True) -> bool:
    return (
        elm is not None
        and elm.tag == "br"
        and ((not no_tail) or elm.tail is None or not elm.tail.strip())
    )


def sanitize_quest_description(description: str) -> str:
    description = description.replace("{mycabbages}", "")
    root: _Element = html.fragment_fromstring(description, create_parent=True)
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
        # Remove more than two <br>s in a row.
        if (
            _is_br(elm)
            and _is_br(elm.getnext())
            and _is_br(elm.getnext().getnext(), no_tail=False)
        ):
            elm.drop_tag()
    # Strip trailing <br>s.
    for elm in reversed(root):
        if _is_br(elm):
            elm.drop_tag()
        else:
            break
    inner_clean_content = "".join(html.tostring(e, encoding="unicode") for e in root)
    clean_content = f"{root.text or ' '}{inner_clean_content}"
    return clean_content
