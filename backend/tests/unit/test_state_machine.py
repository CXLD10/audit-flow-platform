from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]


def test_state_machine_disallows_normalized_to_error_found_direct_transition():
    source = (REPO_ROOT / "backend/app/services/state_machine.py").read_text()
    assert "InvoiceState.NORMALIZED: {InvoiceState.VALIDATED}" in source
    assert "InvoiceState.ERROR_FOUND" not in source.split("InvoiceState.NORMALIZED:", 1)[1].split("}", 1)[0]


def test_state_machine_allows_validated_to_error_found_transition():
    source = (REPO_ROOT / "backend/app/services/state_machine.py").read_text()
    assert "InvoiceState.VALIDATED: {InvoiceState.ERROR_FOUND, InvoiceState.RECONCILED}" in source
