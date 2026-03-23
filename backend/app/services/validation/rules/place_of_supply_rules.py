from app.models.enums import Severity
from app.services.validation.types import RuleError
from app.utils.gstin_utils import STATE_CODES


def run(invoice):
    if invoice.place_of_supply not in STATE_CODES:
        return [
            RuleError(
                "V015",
                Severity.MEDIUM,
                invoice.id,
                "place_of_supply",
                invoice.place_of_supply,
                "valid 2-digit Indian state code",
                "Place of supply is not a valid Indian state code",
            )
        ]
    return []
