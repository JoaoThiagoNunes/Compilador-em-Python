from __future__ import annotations

from antlr4.Token import Token

_OPAD_ATTR = {"+": "MAIS", "-": "MENOS"}
_OPMULT_ATTR = {"*": "VEZES", "/": "DIV"}
_OPLOG_ATTR = {"OR": "OR", "AND": "AND"}
_OPREL_ATTR = {
    "<": "MENOR",
    "<=": "MENIG",
    ">": "MAIOR",
    ">=": "MAIG",
    "==": "IGUAL",
    "<>": "DIFER",
}
_OPNEG_ATTR = {"~": "NEG"}

_TOKENS_WITH_ATTR = {
    "OPAD",
    "OPMULT",
    "OPLOG",
    "OPREL",
    "OPNEG",
    "ID",
    "CTE",
    "CADEIA",
}


def token_attribute(type_name: str, text: str) -> str:
    if type_name == "OPAD":
        return _OPAD_ATTR.get(text, text)
    if type_name == "OPMULT":
        return _OPMULT_ATTR.get(text, text)
    if type_name == "OPLOG":
        return _OPLOG_ATTR.get(text.upper(), text.upper())
    if type_name == "OPREL":
        return _OPREL_ATTR.get(text, text)
    if type_name == "OPNEG":
        return _OPNEG_ATTR.get(text, "NEG")
    if type_name in ("ID", "CTE", "CADEIA"):
        return text
    return ""


def format_token_line(tok: Token, type_name: str, display_value: str | None = None) -> str:
    attr = display_value if display_value is not None else token_attribute(type_name, tok.text)
    if type_name in _TOKENS_WITH_ATTR:
        return f"{tok.line:<7} {type_name:<12} {attr}"
    label = type_name if type_name else tok.text
    return f"{tok.line:<7} {label:<12} {label}"
