# Functional specification: Roman numeral converter

**System:** `roman`, a conversion library between integers and roman numerals.
**Version:** 1.0
**Status:** Approved.

> This document states the expected behaviour. When the code and this specification disagree, the
> specification is right and the code has a defect.

---

## 1. Supported range

The system converts integers in the range **1 to 3999 inclusive**.

- A value below 1 is invalid.
- A value above 3999 is invalid.
- A non-integer value is invalid, including booleans: `True` is not 1.
- Every invalid value raises `RomanError`. The system must not fail with any other exception.

## 2. Integer to roman: `to_roman(n)`

Returns the **canonical** roman representation of `n`.

Symbols and values:

| Symbol | Value | | Symbol | Value |
|---|---|---|---|---|
| I | 1 | | C | 100 |
| V | 5 | | D | 500 |
| X | 10 | | M | 1000 |
| L | 50 | | | |

**Subtractive notation is mandatory.** The system uses the six subtractive combinations where they
apply, and never produces four identical symbols in a row:

| Value | Correct | Incorrect |
|---|---|---|
| 4 | **IV** | IIII |
| 9 | **IX** | VIIII |
| 40 | **XL** | XXXX |
| 90 | **XC** | LXXXX |
| 400 | **CD** | CCCC |
| 900 | **CM** | DCCCC |

Mandatory reference values:

| n | `to_roman(n)` |
|---|---|
| 1 | `I` |
| 4 | `IV` |
| 9 | `IX` |
| 14 | `XIV` |
| 40 | `XL` |
| 1994 | `MCMXCIV` |
| 3999 | `MMMCMXCIX` |

## 3. Roman to integer: `from_roman(s)`

Returns the integer that corresponds to the roman string `s`.

- Accepts lowercase and uppercase interchangeably: `from_roman("iv")` is 4.
- **Leading and trailing whitespace is tolerated.** The system trims it before processing:
  `from_roman("  IV  ")` is 4, and `from_roman("X ")` is 10. Input arrives from a user-facing field,
  where stray blanks are common.
- **Internal whitespace is not tolerated.** `from_roman("X I")` is invalid and raises `RomanError`.
  Only the ends are trimmed.
- An empty string, or a string of blanks only, is invalid and raises `RomanError`.
- Any character that is not a roman symbol is invalid and raises `RomanError`.
- A value outside 1 to 3999 is invalid and raises `RomanError`. In particular `from_roman("MMMM")`,
  which is 4000, is invalid even though the string is well formed.
- An input that is not a `str` is invalid and raises `RomanError`.

## 4. Canonical form validation

**The system accepts roman numerals in canonical form only.** A string that represents a value but is
not the canonical form of that value **is rejected** with `RomanError`.

| Input | Expected result | Reason |
|---|---|---|
| `IIII` | **`RomanError`** | the canonical form of 4 is `IV` |
| `VIIII` | **`RomanError`** | the canonical form of 9 is `IX` |
| `XXXX` | **`RomanError`** | the canonical form of 40 is `XL` |
| `VV` | **`RomanError`** | the canonical form of 10 is `X` |
| `IV` | `4` | canonical |
| `MCMXCIV` | `1994` | canonical |

**Formal criterion.** Read the string as a sequence of **groups**, where a group is one of the six
subtractive pairs of section 2 or a single symbol. A string is canonical if and only if all of these
rules hold:

1. `I`, `X`, `C` and `M` appear **at most three times in a row**.
2. `V`, `L` and `D` appear **at most once** in the whole string.
3. The only subtractive pairs allowed are the six of section 2, each **at most once**. Outside those
   six, no symbol may be followed by one of greater value.
4. Group values are **non-increasing** from left to right.
5. **After a subtractive pair**, for example `IV`, every following group must be worth **less than the
   subtracted symbol**, so less than `I` in the case of `IV`. This is why `IVI` is not canonical:
   4 + 1 = 5 is written `V`.

> Do not define canonical form as `to_roman(from_roman(s)) == s`. That formula uses the code as its
> own oracle, so a defect in `to_roman` would make the formula accept it. A specification cannot
> depend on the implementation it is meant to validate. The five rules above are the normative
> criterion, and the table of examples is normative as well.

## 5. Invalid subtractive pairs

Only the six combinations of section 2 are valid subtractive pairs. Any other pair in which a smaller
symbol precedes a larger one is invalid and raises `RomanError`.

| Input | Result |
|---|---|
| `IL` | `RomanError`, since 49 is written `XLIX` |
| `IC` | `RomanError` |
| `VX` | `RomanError` |

## 6. Roman numeral validation: `is_valid_roman(s)`

Returns `True` when `s` is a valid canonical roman numeral under sections 3, 4 and 5, and `False`
otherwise. **It never raises**, for any type of input.

| Input | `is_valid_roman` |
|---|---|
| `IV` | `True` |
| `IIII` | **`False`**, not canonical, section 4 |
| `Z` | `False` |
| `""` | `False` |
| `"  IV  "` | `True`, the ends are trimmed, section 3 |
| `123`, not a string | `False`, and it does not raise |
| `None` | `False`, and it does not raise |

## 7. Roman arithmetic: `add_roman(a, b)` and `subtract_roman(a, b)`

Both operate on roman strings and return a roman string.

- `add_roman(a, b)` is the roman representation of `from_roman(a) + from_roman(b)`.
- `subtract_roman(a, b)` is the roman representation of `from_roman(a) - from_roman(b)`.
- **The result must be canonical and within 1 to 3999.** When the result falls outside that range the
  system raises `RomanError`.

Mandatory examples:

| Operation | Result |
|---|---|
| `add_roman("II", "II")` | **`IV`** |
| `add_roman("IV", "VI")` | `X` |
| `add_roman("MCMXCIV", "VI")` | `MM` |
| `subtract_roman("X", "I")` | `IX` |
| `subtract_roman("I", "I")` | `RomanError`, result 0, outside the range |
| `add_roman("MMM", "M")` | `RomanError`, result 4000, outside the range |

**Both operations must be consistent with `to_roman` and `from_roman`:** the result of `add_roman` is
always a string that `is_valid_roman` accepts.
