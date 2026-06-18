import sys
from pathlib import Path

# Permite imports dos pacotes lexica, parse, semantica e codegen
sys.path.insert(0, str(Path(__file__).resolve().parent))

from codegen.codegen import gerar_codigo
from lexica.analisador_lexico import run_lexical
from parse.parser import analisar, mostrar_arvore
from semantica.semantic import analisar_semantica


def _cabecalho(titulo, arquivo):
    sep = "-" * 60
    print(f"\n{sep}")
    print(f"  {titulo} - {arquivo}")
    print(sep)


def run_parse(source_file):
    try:
        arvore, parser, erros = analisar(source_file)
    except FileNotFoundError:
        print(f"Arquivo nao encontrado: {source_file}")
        return 1

    _cabecalho("ANALISE SINTATICA", source_file)

    if erros.mensagem:
        print(f"ERRO SINTATICO: {erros.mensagem}")
        return 1

    print("Programa sintaticamente valido.\n")
    print("Arvore sintatica:")
    print(mostrar_arvore(arvore, parser))
    print()
    return 0


def run_semantic(source_file):
    try:
        arvore, parser, erros = analisar(source_file)
    except FileNotFoundError:
        print(f"Arquivo nao encontrado: {source_file}")
        return 1

    _cabecalho("ANALISE SEMANTICA", source_file)

    if erros.mensagem:
        print(f"ERRO SINTATICO: {erros.mensagem}")
        return 1

    sem = analisar_semantica(arvore)
    if sem.erros:
        print("ERROS SEMANTICOS:")
        for e in sem.erros:
            print(f"  {e}")
        return 1

    print("Programa semanticamente valido.\n")
    print("Tabela de simbolos:")
    for nome, tipo in sem.tabela.items():
        print(f"  {nome}: {tipo}")
    print()
    return 0


def run_code(source_file):
    try:
        arvore, parser, erros = analisar(source_file)
    except FileNotFoundError:
        print(f"Arquivo nao encontrado: {source_file}")
        return 1

    _cabecalho("GERACAO DE CODIGO", source_file)

    if erros.mensagem:
        print(f"ERRO SINTATICO: {erros.mensagem}")
        return 1

    sem = analisar_semantica(arvore)
    if sem.erros:
        print("ERROS SEMANTICOS:")
        for e in sem.erros:
            print(f"  {e}")
        return 1

    gen = gerar_codigo(arvore)
    print("Codigo gerado:\n")
    for linha in gen.instrucoes:
        print(linha)
    print()
    return 0


def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <arquivo.sl> [--parse | --semantic | --code]")
        sys.exit(1)

    arquivo = sys.argv[1]
    if len(sys.argv) > 2:
        op = sys.argv[2]
        if op == "--parse":
            sys.exit(run_parse(arquivo))
        if op == "--semantic":
            sys.exit(run_semantic(arquivo))
        if op == "--code":
            sys.exit(run_code(arquivo))

    sys.exit(run_lexical(arquivo))


if __name__ == "__main__":
    main()
