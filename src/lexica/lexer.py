MAX_ID_LEN = 16
INT_MIN = -32768
INT_MAX = 32767


def nome_id(text: str) -> str:
    return text[:MAX_ID_LEN]


class LexerValidator:
    MAX_ID_LEN = MAX_ID_LEN

    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def validate_identifier(self, token_text: str, line: int, column: int) -> str:
        if len(token_text) > self.MAX_ID_LEN:
            truncated = token_text[: self.MAX_ID_LEN]
            self.warnings.append(
                f"Linha {line}:{column}: identificador '{token_text}' truncado para "
                f"'{truncated}' (maximo {self.MAX_ID_LEN} caracteres)."
            )
            return truncated
        return token_text

    def validate_integer(self, token_text: str, line: int, column: int) -> bool:
        try:
            value = int(token_text)
        except ValueError:
            self.errors.append(
                f"Linha {line}:{column}: '{token_text}' nao e um inteiro valido."
            )
            return False

        if value < INT_MIN or value > INT_MAX:
            self.errors.append(
                f"Linha {line}:{column}: inteiro {value} fora do intervalo "
                f"[{INT_MIN}, {INT_MAX}]."
            )
            return False
        return True

    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def report(self) -> str:
        lines: list[str] = []
        for w in self.warnings:
            lines.append(f"[AVISO]  {w}")
        for e in self.errors:
            lines.append(f"[ERRO]   {e}")
        return "\n".join(lines) if lines else "Analise lexica concluida sem problemas."
