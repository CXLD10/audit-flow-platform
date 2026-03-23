from decimal import Decimal

from rapidfuzz.fuzz import WRatio

from app.models.enums import MatchType
from app.utils.decimal_utils import ONE_RUPEE, within_tolerance


def exact_match(invoice, candidates):
    for candidate in candidates:
        if (
            candidate.invoice_number == invoice.invoice_number
            and candidate.invoice_date == invoice.invoice_date
            and within_tolerance(candidate.taxable_value + candidate.tax_amount, invoice.total_invoice_value, ONE_RUPEE)
        ):
            return MatchType.EXACT, 100, candidate
    return None


def fuzzy_match(invoice, candidates):
    for candidate in candidates:
        score = WRatio(candidate.invoice_number, invoice.invoice_number)
        if score >= 85:
            return MatchType.FUZZY, max(75, min(90, int(score))), candidate
    return None


def heuristic_match(invoice, candidates):
    for candidate in candidates:
        if invoice.invoice_date and candidate.invoice_date and candidate.invoice_date.month == invoice.invoice_date.month:
            return MatchType.HEURISTIC, 60, candidate
    return None
