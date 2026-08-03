# Especificación funcional — Conversor de números romanos

**Sistema:** `roman` — biblioteca de conversión entre enteros y números romanos, con GUI de escritorio.
**Versión:** 1.0
**Estado:** Aprobada.

> Este documento es la **fuente de verdad** sobre el comportamiento esperado. Cuando el código y
> esta especificación discrepan, **la especificación tiene la razón** y el código tiene un defecto.

---

## 1. Rango soportado

El sistema convierte enteros en el rango **1 a 3999 inclusive**.

- Un valor menor a 1 es inválido.
- Un valor mayor a 3999 es inválido.
- Un valor no entero es inválido (incluye booleanos: `True` no es 1).
- Todo valor inválido produce un error `RomanError`. **El sistema no debe caerse con otra excepción.**

## 2. Conversión de entero a romano — `to_roman(n)`

Devuelve la representación romana **canónica** de `n`.

Símbolos y valores:

| Símbolo | Valor | | Símbolo | Valor |
|---|---|---|---|---|
| I | 1 | | C | 100 |
| V | 5 | | D | 500 |
| X | 10 | | M | 1000 |
| L | 50 | | | |

**Notación sustractiva obligatoria.** El sistema debe usar las seis combinaciones sustractivas
cuando corresponda, y **nunca** producir cuatro símbolos iguales consecutivos:

| Valor | Representación correcta | Representación INCORRECTA |
|---|---|---|
| 4 | **IV** | IIII |
| 9 | **IX** | VIIII |
| 40 | **XL** | XXXX |
| 90 | **XC** | LXXXX |
| 400 | **CD** | CCCC |
| 900 | **CM** | DCCCC |

Ejemplos de referencia obligatorios:

| n | `to_roman(n)` |
|---|---|
| 1 | `I` |
| 4 | `IV` |
| 9 | `IX` |
| 14 | `XIV` |
| 40 | `XL` |
| 1994 | `MCMXCIV` |
| 3999 | `MMMCMXCIX` |

## 3. Conversión de romano a entero — `from_roman(s)`

Devuelve el entero correspondiente a la cadena romana `s`.

- Acepta **minúsculas y mayúsculas** indistintamente: `from_roman("iv")` = 4.
- **Tolera espacios en blanco alrededor.** El sistema **debe recortar** los espacios **al inicio y
  al final** antes de procesar: `from_roman("  IV  ")` = 4, `from_roman("X ")` = 10. Los datos
  llegan de un campo de texto de la GUI, donde el usuario deja espacios con frecuencia.
- **Los espacios internos NO se toleran**: `from_roman("X I")` es inválido → `RomanError`. Sólo se
  recortan los extremos.
- Una cadena vacía (o sólo espacios) es inválida → `RomanError`.
- Un carácter que no sea un símbolo romano es inválido → `RomanError`.
- Un valor fuera del rango 1..3999 es inválido → `RomanError`. En particular `from_roman("MMMM")`
  (4000) es inválido, aunque la cadena esté bien formada.
- Una entrada que no sea `str` es inválida → `RomanError`.

## 4. Validación de forma canónica

**El sistema sólo acepta números romanos en forma canónica.** Una cadena que representa un valor
pero no es la forma canónica de ese valor **debe rechazarse** con `RomanError`.

| Entrada | Resultado esperado | Razón |
|---|---|---|
| `IIII` | **`RomanError`** | la forma canónica de 4 es `IV` |
| `VIIII` | **`RomanError`** | la forma canónica de 9 es `IX` |
| `XXXX` | **`RomanError`** | la forma canónica de 40 es `XL` |
| `VV` | **`RomanError`** | la forma canónica de 10 es `X` |
| `IV` | `4` | canónica |
| `MCMXCIV` | `1994` | canónica |

**Criterio formal de forma canónica.** Una cadena romana es canónica si y sólo si cumple **todas**
estas reglas (definidas sobre la cadena, sin depender de la implementación):

1. `I`, `X`, `C`, `M` aparecen **como máximo tres veces consecutivas**.
2. `V`, `L`, `D` aparecen **como máximo una vez** en toda la cadena.
3. Las únicas parejas sustractivas permitidas son las seis de §2, y cada una aparece **como máximo
   una vez**.
4. Los valores de los grupos van en orden **no creciente** de izquierda a derecha.

> Ojo: **no** definas la forma canónica como "`to_roman(from_roman(s)) == s`". Esa fórmula usa el
> propio código como oráculo, y si `to_roman` tiene un defecto la fórmula lo da por bueno. La
> especificación no puede depender de la implementación que pretende validar. Las cuatro reglas de
> arriba son el criterio normativo; la tabla de ejemplos es normativa también.

## 5. Pares sustractivos inválidos

Sólo las seis combinaciones de §2 son sustractivas válidas. Cualquier otra pareja en la que un
símbolo menor precede a uno mayor es inválida → `RomanError`.

| Entrada | Resultado |
|---|---|
| `IL` | `RomanError` (49 se escribe `XLIX`) |
| `IC` | `RomanError` |
| `VX` | `RomanError` |

## 6. Validación de números romanos — `is_valid_roman(s)`

Devuelve `True` si `s` es un número romano canónico válido según §3, §4 y §5; `False` en cualquier
otro caso. **No lanza excepciones nunca**, para ningún tipo de entrada.

| Entrada | `is_valid_roman` |
|---|---|
| `IV` | `True` |
| `IIII` | **`False`** (no canónica, §4) |
| `Z` | `False` |
| `""` | `False` |
| `"  IV  "` | `True` (se recortan los extremos, §3) |
| `123` (no string) | `False` (no lanza excepción) |
| `None` | `False` (no lanza excepción) |

## 7. Aritmética romana — `add_roman(a, b)` y `subtract_roman(a, b)`

Operan sobre cadenas romanas y devuelven una cadena romana.

- `add_roman(a, b)` = representación romana de `from_roman(a) + from_roman(b)`.
- `subtract_roman(a, b)` = representación romana de `from_roman(a) - from_roman(b)`.
- **El resultado debe ser canónico y estar en el rango 1..3999.** Si el resultado queda fuera del
  rango, el sistema lanza `RomanError`.

Ejemplos obligatorios:

| Operación | Resultado |
|---|---|
| `add_roman("II", "II")` | **`IV`** |
| `add_roman("IV", "VI")` | `X` |
| `add_roman("MCMXCIV", "VI")` | `MM` |
| `subtract_roman("X", "I")` | `IX` |
| `subtract_roman("I", "I")` | `RomanError` (resultado 0, fuera de rango) |
| `add_roman("MMM", "M")` | `RomanError` (resultado 4000, fuera de rango) |

**Ambas operaciones deben ser coherentes con `to_roman` y `from_roman`:** el resultado de
`add_roman` siempre debe ser una cadena que `is_valid_roman` acepte.

## 8. Interfaz gráfica

La GUI presenta dos campos: entero y romano. Al escribir en uno, el otro se actualiza. Los errores
se muestran como mensaje en línea, sin cerrar la aplicación.

**La GUI está fuera del alcance de este taller.** No se piden pruebas de la capa Tkinter.
