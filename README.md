# roman

Roman numeral conversion library. Supports integers 1 to 3999 with subtractive notation.

## Install

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e . pytest pytest-cov
```

## Run the tests

```bash
pytest
pytest --cov=roman.converter --cov-branch --cov-report=term-missing
```

## Usage

```python
from roman.converter import to_roman, from_roman

to_roman(1994)        # 'MCMXCIV'
from_roman('MCMXCIV') # 1994
```

Command line:

```bash
python -m roman 4 IV 1994
```

## API

| Function | Description |
|---|---|
| `to_roman(n)` | Integer to roman numeral |
| `from_roman(s)` | Roman numeral to integer |
| `is_valid_roman(s)` | Whether a string is a valid roman numeral |
| `add_roman(a, b)` | Sum of two roman numerals |
| `subtract_roman(a, b)` | Difference of two roman numerals |

Invalid input raises `RomanError`.

## Layout

```
src/roman/converter.py    conversion library
src/roman/__main__.py     command line entry point
tests/test_converter.py   test suite
SPECIFICATION.md          functional specification
```
