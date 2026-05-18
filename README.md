# Mutation Testing — Roman Numeral GUI (Parallel P1)

ESPOL — Software Engineering II — Week 13.

You get a working Roman numeral converter with a live Tkinter GUI. Type a number on the left, the roman shows up on the right, and vice versa. Type `4`, you see `IV`. Type `IV`, you see `4`. Cool, ship it.

Except the test suite is bad. It tests `I`, `V`, `X`, `L`, `C`, `D`, `M` and calls it a day. None of the interesting cases — the subtractive notation that makes Roman numerals weird in the first place — are covered. A mutation testing tool will happily prove that to you: change a `-` to a `+` deep in the converter, run the tests, and the bar still goes green. Then launch the GUI, type `IV`, and watch it confidently display `6`.

That gap between "tests pass" and "program works" is the whole point of this workshop.

## What you have

- `src/roman/converter.py` — about 150 lines. Pure functions: `to_roman(n)`, `from_roman(s)`, plus a couple of helpers. Supports 1..3999, full subtractive notation (IV, IX, XL, XC, CD, CM), validates canonical form on parse.
- `src/roman/gui.py` — about 100 lines of Tkinter. Two entries, live two-way conversion, inline status messages on errors.
- `tests/test_converter.py` — 15 tests. Weak on purpose. Currently sits around 60% mutation score.
- `tests/test_gui.py` — two smoke tests that boot a real `Tk()` root.
- `pyproject.toml` / `setup.cfg` — mutmut configured to mutate the converter and run the converter tests.

## What you have to do

Push the mutation score on `src/roman/converter.py` to **>= 90%** by adding tests to `tests/test_converter.py`. The CI gate fails below 90%.

You are not allowed to:

- Modify `src/roman/converter.py` (the code is correct — your tests are not).
- Delete the existing tests. Add to them. Replace with stronger equivalents if you must, but the file should still contain at least the same number of test functions.
- Write a test function without at least one `assert` statement. The pre-commit hook will reject it. Yes, it parses your AST. No, `print` is not an assertion.

## Setup

```bash
make install         # pip installs deps + the package in editable mode
make hooks           # wires the anti-cheat pre-commit hook
make gui             # launch the desktop app — try typing "IV", "MCMXCIV", "MMMCMXCIX"
make test            # run pytest
make mutate          # run mutmut and print the results table
```

Or by hand:

```bash
pip install -r requirements.txt
pip install -e .
PYTHONPATH=src python -m roman.gui
PYTHONPATH=src python -m pytest
PYTHONPATH=src python -m mutmut run
PYTHONPATH=src python -m mutmut results
```

## Workflow we expect

1. Run `make gui` first. Play with it. Confirm it works — `4 -> IV`, `1994 -> MCMXCIV`, `MMMCMXCIX -> 3999`, `4000 -> error`.
2. Run `make mutate`. Read the results. Pick a surviving mutant: `mutmut show <id>`.
3. Read the diff. Ask yourself: what input, fed to my tests, would behave differently under this mutant than under the original? That input is the test you are missing.
4. Write the test. Run `make mutate` again. Score goes up. Repeat.
5. Stop when you hit >= 90%. Push. CI checks for you.

## Submission

- Pull request to the course repo with your branch.
- The `mutation` workflow must be green (>= 90%).
- The `tests` workflow must be green.
- Commit messages should describe which mutant family each test kills. "added tests" is not a commit message.

## Notes

The GUI is not graded. It is there because mutation testing is abstract when you only see kill/survive counts, and very obvious when you type `IV` and the screen says `6`. If a surviving mutant ever shows you something wrong in the GUI that your tests did not catch, you are looking at the exact thing this workshop is teaching.

— Natalia
