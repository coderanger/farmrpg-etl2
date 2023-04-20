import attrs


@attrs.define
class ParsedRecipeIngredient:
    name: str
    quantity: int


@attrs.define
class ParsedItem:
    id: int
    recipe: list[ParsedRecipeIngredient]


def parse_item(content: bytes) -> ParsedItem:
    pass
