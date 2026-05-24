# humanint

Parse and format human-readable integers in Python. Zero dependencies.

```python
from humanint import parse, format

parse("1.5k")        # 1500
parse("2M")          # 2_000_000
parse("-3.2B")       # -3_200_000_000
parse("1,000,000")   # 1_000_000

format(1500)             # "1.5K"
format(2_000_000_000)    # "2.0B"
format(1234, precision=3)  # "1.234K"
```

## Install

```bash
python -m pip install -e .
```

From source:

```bash
git clone https://github.com/nripankadas07/humanint.git
cd humanint
pip install -e .[dev]
```

## API

### `parse(text: str) -> int`

Parse a human-readable number string into an integer. Accepts plain digits,
optional sign, optional thousands separator (`,` or `_`), and an optional
case-insensitive suffix from `K`, `M`, `B`, `T`. Raises `HumanIntError` on
invalid input or when the suffix expansion would not yield an exact integer.

### `format(value: int, precision: int = 1) -> str`

Format an integer using the largest applicable suffix from `K`, `M`, `B`, `T`.
`precision` is the number of decimal places (default `1`, must be `>= 0`).
Returns a plain digit string for values smaller than 1,000.

### `HumanIntError`

Subclass of `ValueError` raised by all parse/format errors.

## Running tests

```bash
pip install -e .[dev]
pytest
```

## License

MIT
