# Expected New Tests — Instructor Rubric

To clear 90% mutation score, students should add roughly these tests. Variants are fine as long as each surviving family from `SURVIVING-MUTANTS.md` is addressed.

1. **Subtractive 4 / IV.** `assert to_roman(4) == "IV"` and `assert from_roman("IV") == 4`.

2. **Subtractive 9 / IX.** `assert to_roman(9) == "IX"` and `assert from_roman("IX") == 9`.

3. **Subtractive 40 / XL.** `assert to_roman(40) == "XL"` and `assert from_roman("XL") == 40`.

4. **Subtractive 90 / XC.** `assert to_roman(90) == "XC"` and `assert from_roman("XC") == 90`.

5. **Subtractive 400 / CD.** `assert to_roman(400) == "CD"` and `assert from_roman("CD") == 400`.

6. **Subtractive 900 / CM.** `assert to_roman(900) == "CM"` and `assert from_roman("CM") == 900`.

7. **Compound subtractive case.** Something like `assert to_roman(1994) == "MCMXCIV"` and the inverse. Kills any remaining operator-flip survivors that hide inside multi-pair strings.

8. **Upper bound 3999 succeeds.** `assert to_roman(3999) == "MMMCMXCIX"`.

9. **Upper bound 4000 raises.** `with pytest.raises(RomanError): to_roman(4000)`.

10. **Lower bound and zero/negative raise.** `with pytest.raises(RomanError): to_roman(0)` and `to_roman(-1)`. Also `from_roman("")` raises.

Bonus (recommended for full coverage):

- Non-canonical input raises: `from_roman("IIII")` should raise.
- Invalid character raises: `from_roman("ABC")` should raise.
- Invalid subtractive raises: `from_roman("IC")` should raise.

A passing submission must keep the weak tests intact (or replace them with stronger equivalents) and reach `mutmut results` with score >= 90%.
