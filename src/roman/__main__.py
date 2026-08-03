import sys

from .converter import RomanError, from_roman, is_valid_roman, to_roman


def _convert(token):
    if token.lstrip("-").isdigit():
        return to_roman(int(token))
    return from_roman(token)


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if not args:
        print("usage: python -m roman <value> [value ...]")
        return 2
    status = 0
    for token in args:
        try:
            print(f"{token} -> {_convert(token)}")
        except RomanError as exc:
            print(f"{token} -> error: {exc}")
            status = 1
    return status


if __name__ == "__main__":
    raise SystemExit(main())
