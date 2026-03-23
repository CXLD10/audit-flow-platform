from decimal import Decimal

from app.utils.decimal_utils import to_decimal, within_tolerance


def test_to_decimal_strips_currency_symbols_and_commas():
    assert to_decimal("₹12,500.50") == Decimal("12500.50")


def test_within_tolerance_allows_one_rupee_difference():
    assert within_tolerance(Decimal("100.00"), Decimal("100.90"), Decimal("1.00")) is True
