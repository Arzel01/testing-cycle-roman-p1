# roman — Conversor de números romanos

ESPOL · IS2 (SOFG1008) · **Taller individual: aplicación del ciclo de testing** · Paralelo 1

Heredas un proyecto que ya funciona... o eso parece. Tiene una suite de pruebas que pasa en verde.
El código tiene defectos de todas formas.

## Qué hay aquí

- `src/roman/converter.py` — la biblioteca de conversión. **Es el sistema bajo prueba.**
- `src/roman/__main__.py` — CLI mínima para inspeccionar conversiones a mano.
- `tests/test_converter.py` — la suite heredada. Pasa en verde. Es débil a propósito.
- `ESPECIFICACION.md` — **la fuente de verdad.** Lo que el sistema *debería* hacer.

## Arranque

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e . pytest pytest-cov
pytest
```

Debes ver **15 passed**.

```bash
pytest --cov=roman.converter --cov-branch --cov-report=term-missing
```

Cobertura de ramas inicial: **64%**.

## CLI

Útil para probar conversiones sin escribir una prueba:

```bash
python -m roman 4 9 1994 IV MCMXCIV
```

## Tu trabajo

Está en la guía del taller en Aula Virtual. En resumen: aplica el ciclo de testing (unidad →
integración → aceptación) para encontrar los defectos que la suite heredada no ve, clasificándolos
como faltas de **omisión** o de **comisión**.

No modifiques `src/` hasta la actividad de regresión. Añade pruebas; no borres las existentes.
