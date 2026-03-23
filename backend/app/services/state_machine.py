from uuid import UUID

from sqlalchemy.orm import Session

from app.models.enums import InvoiceState
from app.models.invoice import Invoice
from app.services.audit_service import write_audit_log

VALID_TRANSITIONS: dict[InvoiceState, set[InvoiceState]] = {
    InvoiceState.RAW: {InvoiceState.PARSED},
    InvoiceState.PARSED: {InvoiceState.NORMALIZED},
    InvoiceState.NORMALIZED: {InvoiceState.VALIDATED},
    InvoiceState.VALIDATED: {InvoiceState.ERROR_FOUND, InvoiceState.RECONCILED},
    InvoiceState.ERROR_FOUND: {InvoiceState.RECONCILED},
    InvoiceState.RECONCILED: {InvoiceState.REVIEWED},
    InvoiceState.REVIEWED: {InvoiceState.RESOLVED},
    InvoiceState.RESOLVED: {InvoiceState.EXPORTED},
    InvoiceState.EXPORTED: set(),
}


def transition_invoice(*, invoice: Invoice, new_state: InvoiceState, actor: UUID | str, db: Session) -> Invoice:
    old_state = invoice.state
    if new_state == old_state:
        return invoice
    if new_state not in VALID_TRANSITIONS.get(old_state, set()):
        raise ValueError(f"Invalid invoice state transition: {old_state} -> {new_state}")
    invoice.state = new_state
    write_audit_log(
        db=db,
        tenant_id=invoice.tenant_id,
        user_id=actor if isinstance(actor, UUID) else None,
        action_type="STATE_TRANSITION",
        entity_type="invoice",
        entity_id=invoice.id,
        metadata={"from": old_state.value, "to": new_state.value, "actor": str(actor)},
    )
    return invoice
