# test suite
import pytest
from roman.converter import (to_roman, from_roman, is_valid_roman, add_roman, subtract_roman, _roundtrip_differs, _count_char, RomanError)

def test_one():
    assert to_roman(1) == "I"


def test_two():
    assert to_roman(2) == "II"


def test_three():
    assert to_roman(3) == "III"


def test_five():
    assert to_roman(5) == "V"


def test_ten():
    assert to_roman(10) == "X"


def test_fifty():
    assert to_roman(50) == "L"


def test_hundred():
    assert to_roman(100) == "C"


def test_five_hundred():
    assert to_roman(500) == "D"


def test_thousand():
    assert to_roman(1000) == "M"


def test_from_one():
    assert from_roman("I") == 1


def test_from_five():
    assert from_roman("V") == 5


def test_from_two():
    assert from_roman("II") == 2


def test_roundtrip_small():
    assert from_roman(to_roman(7)) == 7


def test_roundtrip_medium():
    assert from_roman(to_roman(58)) == 58


def test_lowercase_input():
    assert from_roman("xi") == 11


def test_to_roman_float_raises():
    with pytest.raises(RomanError):
        to_roman(3.5)


def test_to_roman_bool_raises():
    with pytest.raises(RomanError):
        to_roman(True)


def test_to_roman_zero_raises():
    with pytest.raises(RomanError):
        to_roman(0)


def test_to_roman_negative_raises():
    with pytest.raises(RomanError):
        to_roman(-1)


def test_to_roman_too_large_raises():
    with pytest.raises(RomanError):
        to_roman(4000)


def test_from_roman_non_string_raises():
    with pytest.raises(RomanError):
        from_roman(42)


def test_from_roman_empty_raises():
    with pytest.raises(RomanError):
        from_roman("")


def test_from_roman_invalid_char_raises():
    with pytest.raises(RomanError):
        from_roman("ABC")


def test_from_roman_invalid_subtractive_pair_raises():
    with pytest.raises(RomanError):
        from_roman("IL")


def test_from_roman_out_of_range_raises():
    with pytest.raises(RomanError):
        from_roman("MMMM")


def test_from_roman_iv():
    assert from_roman("IV") == 4


def test_from_roman_ix():
    assert from_roman("IX") == 9


def test_from_roman_xl():
    assert from_roman("XL") == 40


def test_from_roman_xc():
    assert from_roman("XC") == 90


def test_from_roman_cd():
    assert from_roman("CD") == 400


def test_from_roman_cm():
    assert from_roman("CM") == 900


def test_is_valid_roman_true():
    assert is_valid_roman("XIV") is True


def test_is_valid_roman_false_empty():
    assert is_valid_roman("") is False


def test_is_valid_roman_false_invalid_char():
    assert is_valid_roman("Z") is False


def test_add_roman_basic():
    assert add_roman("I", "II") == "III"


def test_add_roman_subtractive():
    assert add_roman("IV", "I") == "V"


def test_subtract_roman_basic():
    assert subtract_roman("V", "II") == "III"


def test_subtract_roman_to_one():
    assert subtract_roman("II", "I") == "I"


def test_roundtrip_differs_same():
    assert _roundtrip_differs(4, "IV") is False


def test_roundtrip_differs_different():
    assert _roundtrip_differs(4, "IIII") is True


def test_count_char_present():
    assert _count_char("III", "I") == 3


def test_count_char_absent():
    assert _count_char("XIV", "Z") == 0


def test_count_char_mixed():
    assert _count_char("MMXIV", "M") == 2


# ---------------------------------------------------------------------------
# Part 4 – Integration tests: add_roman / subtract_roman collaborate with
#           from_roman, to_roman, and is_valid_roman (Spec §7)
# ---------------------------------------------------------------------------

# The spec mandates specific outputs for the arithmetic functions AND states:
# "the result of add_roman is always a string that is_valid_roman accepts."
# These tests exercise the full pipeline, not a single function in isolation.

def test_integration_add_roman_result_is_valid():
    # Collaboration: add_roman calls from_roman twice, then to_roman, and the
    # output must be accepted by is_valid_roman.
    result = add_roman("IV", "VI")
    assert is_valid_roman(result), f"add_roman result '{result}' not accepted by is_valid_roman"

def test_integration_subtract_roman_result_is_valid():
    result = subtract_roman("X", "I")
    assert is_valid_roman(result), f"subtract_roman result '{result}' not accepted by is_valid_roman"

def test_integration_add_roman_spec_example_ii_plus_ii():
    # Spec §7 mandatory example: add_roman("II", "II") == "IV"
    # Exercises from_roman("II")+from_roman("II")=4, then to_roman(4) must
    # produce "IV" (subtractive notation), and is_valid_roman must accept it.
    result = add_roman("II", "II")
    assert result == "IV"
    assert is_valid_roman(result)

def test_integration_add_roman_spec_example_mcmxciv():
    # Spec §7: add_roman("MCMXCIV", "VI") == "MM"
    result = add_roman("MCMXCIV", "VI")
    assert result == "MM"
    assert is_valid_roman(result)

def test_integration_subtract_roman_spec_example_x_minus_i():
    # Spec §7: subtract_roman("X", "I") == "IX"
    result = subtract_roman("X", "I")
    assert result == "IX"
    assert is_valid_roman(result)

def test_integration_add_roman_overflow_raises():
    # Spec §7: add_roman("MMM", "M") -> RomanError (result 4000, out of range)
    with pytest.raises(RomanError):
        add_roman("MMM", "M")

def test_integration_subtract_roman_underflow_raises():
    # Spec §7: subtract_roman("I", "I") -> RomanError (result 0, out of range)
    with pytest.raises(RomanError):
        subtract_roman("I", "I")


# ---------------------------------------------------------------------------
# Part 5 – Acceptance tests (derived from SPECIFICATION.md, not from the code)
# ---------------------------------------------------------------------------

# AC-1  Subtractive notation is mandatory for to_roman (Spec §2)
#
# Given  the integer 4
# When   to_roman(4) is called
# Then   the result is "IV" (never "IIII")
def test_ac1_to_roman_4_uses_subtractive_notation():
    assert to_roman(4) == "IV"


# AC-2  Leading and trailing whitespace is tolerated by from_roman (Spec §3)
#
# Given  a roman string that has leading and/or trailing spaces
# When   from_roman is called with that string
# Then   the whitespace is stripped and the correct integer is returned
def test_ac2_from_roman_strips_surrounding_whitespace():
    assert from_roman("  IV  ") == 4
    assert from_roman("X ") == 10


# AC-3  from_roman rejects non-canonical strings (Spec §4)
#
# Given  the string "IIII", which encodes 4 but is not in canonical form
# When   from_roman("IIII") is called
# Then   RomanError is raised (the canonical form of 4 is "IV")
def test_ac3_from_roman_rejects_non_canonical_string():
    with pytest.raises(RomanError):
        from_roman("IIII")
