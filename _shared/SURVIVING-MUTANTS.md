# Surviving Mutants — Instructor Notes

This file is NOT shipped to students in their starter. It lists the specific mutants the weak baseline suite is designed to leave alive. Use it to grade and to write the "expected new tests" set.

Baseline weak suite hits the obvious single-symbol conversions (I, V, X, L, C, D, M) plus a couple of roundtrips. That kills enough additive-rule mutants to land around ~60% kill rate, while leaving the subtractive pairs and the range guards completely unexamined.

## The 6 target survivors

1. **Boundary at 4 (IV).** Mutating the pair `(4, "IV")` — e.g. flipping the value to `3` or `5`, or deleting the entry — survives because nothing asserts `to_roman(4) == "IV"` or `from_roman("IV") == 4`.

2. **Boundary at 9 (IX).** Same shape: mutate `(9, "IX")` value or string. No test exercises 9 or "IX".

3. **Boundary at 40 / 90 (XL, XC).** Mutating either tuple in `_PAIRS` (value or symbol) survives. Suite never touches 40, 90, "XL", or "XC".

4. **Boundary at 400 / 900 (CD, CM).** Same: no test for 400, 900, "CD", "CM".

5. **Operator flip on the subtractive rule.** In `from_roman`, the line `total += _SINGLE[pair[1]] - _SINGLE[pair[0]]` — flipping `-` to `+`, or swapping the operand order — survives because the suite never parses a string containing a subtractive pair like "IV", "IX", "XL", "XC", "CD", "CM".

6. **Relational operator on the upper bound 3999.** In `to_roman`, `if n > _MAX_VALUE` mutated to `>=` (or `_MAX_VALUE` mutated to `3998` / `4000`) survives. No test asserts that 3999 succeeds and 4000 raises.

Bonus survivors the weak suite also leaves alive (cheap to kill, useful for partial credit):

- `_MIN_VALUE` boundary: `n < 1` flipped to `<= 1` or `< 0`.
- Empty-string guard in `from_roman`.
- Canonical-form check (`_roundtrip_differs`): non-canonical inputs like "IIII" should raise but the suite never tries.
- Invalid characters: "Z" should raise.

## Approximate score math

15 tests, ~60% kill rate ≈ 18-22 surviving mutants out of ~50 generated. Exact number depends on mutmut version; the six families above are the conceptual targets.
