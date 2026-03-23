from decimal import Decimal, ROUND_HALF_UP

TWOPLACES = Decimal("0.01")
ZERO = Decimal("0.00")
ONE_RUPEE = Decimal("1.00")


def to_decimal(value: object) -> Decimal:
    if value is None or value == "":
        return ZERO
    if isinstance(value, Decimal):
        return value.quantize(TWOPLACES, rounding=ROUND_HALF_UP)
    normalized = str(value).replace(",", "").replace("₹", "").strip()
    return Decimal(normalized or "0").quantize(TWOPLACES, rounding=ROUND_HALF_UP)


def within_tolerance(actual: Decimal, expected: Decimal, tolerance: Decimal = ONE_RUPEE) -> bool:
    return abs(actual - expected) <= tolerance
