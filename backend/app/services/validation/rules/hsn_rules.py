from app.models.enums import Severity
from app.services.validation.types import RuleError


def run(invoice, hsn_tax_rates: dict):
    errors: list[RuleError] = []
    code = invoice.hsn_sac_code.strip()
    if code.isdigit() and len(code) not in {4, 6, 8}:
        errors.append(RuleError("V014", Severity.MEDIUM, invoice.id, "hsn_sac_code", code, "HSN must be 4, 6, or 8 digits", "HSN code length is invalid"))
    if code and code not in hsn_tax_rates:
        errors.append(RuleError("V023", Severity.MEDIUM, invoice.id, "hsn_sac_code", code, "code present in local HSN master", "HSN/SAC code is not present in the local HSN master"))
    return errors
