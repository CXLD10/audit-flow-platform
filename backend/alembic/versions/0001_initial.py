"""initial schema

Revision ID: 0001_initial
Revises: None
Create Date: 2026-03-23 00:00:00
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "tenants",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False, unique=True),
        sa.Column("plan_tier", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tenants.id"), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False, unique=True),
        sa.Column("role", sa.Enum("CA", "CLIENT", "ADMIN", name="role_enum"), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("last_login_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "clients",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tenants.id"), nullable=False),
        sa.Column("gstin", sa.String(length=15), nullable=False),
        sa.Column("legal_name", sa.String(length=255), nullable=False),
        sa.Column("column_mapping", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("e_invoice_threshold_enabled", sa.Boolean(), nullable=False),
        sa.Column("annual_turnover", sa.Numeric(15, 2, asdecimal=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "upload_batches",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tenants.id"), nullable=False),
        sa.Column("client_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("clients.id"), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("filename", sa.String(length=255), nullable=False),
        sa.Column("file_path_s3", sa.String(length=1024), nullable=False),
        sa.Column("status", sa.Enum("PENDING", "PROCESSING", "COMPLETE", "FAILED", name="batch_status_enum"), nullable=False),
        sa.Column("return_period", sa.Date(), nullable=True),
        sa.Column("total_invoices", sa.Integer(), nullable=False),
        sa.Column("error_count", sa.Integer(), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("failed_stage", sa.String(length=50), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("last_completed_stage", sa.String(length=50), nullable=True),
        sa.Column("retry_count", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "hsn_master",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("code", sa.String(length=20), nullable=False, unique=True),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("tax_rate", sa.Numeric(5, 2, asdecimal=True), nullable=False),
        sa.Column("refreshed_at", sa.Date(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "invoices",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tenants.id"), nullable=False),
        sa.Column("batch_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("upload_batches.id"), nullable=False),
        sa.Column("client_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("clients.id"), nullable=False),
        sa.Column("invoice_number", sa.String(length=255), nullable=False),
        sa.Column("invoice_date", sa.Date(), nullable=True),
        sa.Column("supplier_name", sa.String(length=255), nullable=True),
        sa.Column("canonical_supplier_name", sa.String(length=255), nullable=True),
        sa.Column("supplier_gstin", sa.String(length=15), nullable=False),
        sa.Column("recipient_gstin", sa.String(length=15), nullable=False),
        sa.Column("hsn_sac_code", sa.String(length=20), nullable=False),
        sa.Column("taxable_value", sa.Numeric(15, 2, asdecimal=True), nullable=False),
        sa.Column("cgst_amount", sa.Numeric(15, 2, asdecimal=True), nullable=False),
        sa.Column("sgst_amount", sa.Numeric(15, 2, asdecimal=True), nullable=False),
        sa.Column("igst_amount", sa.Numeric(15, 2, asdecimal=True), nullable=False),
        sa.Column("total_invoice_value", sa.Numeric(15, 2, asdecimal=True), nullable=False),
        sa.Column("place_of_supply", sa.String(length=2), nullable=False),
        sa.Column("applicable_rate", sa.Numeric(5, 2, asdecimal=True), nullable=True),
        sa.Column("state", sa.Enum("RAW", "PARSED", "NORMALIZED", "VALIDATED", "ERROR_FOUND", "RECONCILED", "REVIEWED", "RESOLVED", "EXPORTED", name="invoice_state_enum"), nullable=False),
        sa.Column("gstn_verification_status", sa.Enum("ACTIVE", "CANCELLED", "SUSPENDED", "MIGRATED", "GSTIN_UNVERIFIED", name="gstn_verification_status_enum"), nullable=True),
        sa.Column("credit_note_flag", sa.Boolean(), nullable=False),
        sa.Column("source_row_number", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_invoices_tenant_batch", "invoices", ["tenant_id", "batch_id"])
    op.create_index("ix_invoices_tenant_state", "invoices", ["tenant_id", "state"])
    op.create_table(
        "validation_errors",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tenants.id"), nullable=False),
        sa.Column("invoice_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("invoices.id"), nullable=False),
        sa.Column("batch_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("upload_batches.id"), nullable=False),
        sa.Column("rule_id", sa.String(length=50), nullable=False),
        sa.Column("severity", sa.Enum("CRITICAL", "HIGH", "MEDIUM", "LOW", name="severity_enum"), nullable=False),
        sa.Column("field_name", sa.String(length=255), nullable=False),
        sa.Column("actual_value", sa.Text(), nullable=False),
        sa.Column("expected_value", sa.Text(), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "gstr2b_records",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tenants.id"), nullable=False),
        sa.Column("client_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("clients.id"), nullable=False),
        sa.Column("gstin", sa.String(length=15), nullable=False),
        sa.Column("invoice_number", sa.String(length=255), nullable=False),
        sa.Column("invoice_date", sa.Date(), nullable=True),
        sa.Column("supplier_gstin", sa.String(length=15), nullable=False),
        sa.Column("taxable_value", sa.Numeric(15, 2, asdecimal=True), nullable=False),
        sa.Column("tax_amount", sa.Numeric(15, 2, asdecimal=True), nullable=False),
        sa.Column("period", sa.String(length=7), nullable=False),
        sa.Column("source_file", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "reconciliation_results",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tenants.id"), nullable=False),
        sa.Column("invoice_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("invoices.id"), nullable=False, unique=True),
        sa.Column("gstr2b_record_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("gstr2b_records.id"), nullable=True),
        sa.Column("match_type", sa.Enum("EXACT", "FUZZY", "HEURISTIC", "UNMATCHED", name="match_type_enum"), nullable=False),
        sa.Column("confidence_score", sa.Integer(), nullable=False),
        sa.Column("delta_taxable_value", sa.Numeric(15, 2, asdecimal=True), nullable=False),
        sa.Column("delta_tax_amount", sa.Numeric(15, 2, asdecimal=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "entity_mappings",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tenants.id"), nullable=False),
        sa.Column("raw_name", sa.String(length=255), nullable=False),
        sa.Column("canonical_name", sa.String(length=255), nullable=False),
        sa.Column("similarity_score", sa.Numeric(5, 2, asdecimal=True), nullable=False),
        sa.Column("source_batch_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("upload_batches.id"), nullable=False),
        sa.Column("user_overridden", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "suggestions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tenants.id"), nullable=False),
        sa.Column("invoice_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("invoices.id"), nullable=False),
        sa.Column("error_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("validation_errors.id"), nullable=False),
        sa.Column("suggestion_type", sa.String(length=50), nullable=False),
        sa.Column("suggested_value", sa.Text(), nullable=False),
        sa.Column("confidence_score", sa.Integer(), nullable=False),
        sa.Column("explanation", sa.Text(), nullable=False),
        sa.Column("suppressed", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "suggestion_decisions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tenants.id"), nullable=False),
        sa.Column("suggestion_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("suggestions.id"), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("decision", sa.Enum("APPROVED", "REJECTED", name="suggestion_decision_enum"), nullable=False),
        sa.Column("comment", sa.Text(), nullable=True),
        sa.Column("decided_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "audit_log",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tenants.id"), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("action_type", sa.String(length=100), nullable=False),
        sa.Column("entity_type", sa.String(length=100), nullable=False),
        sa.Column("entity_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    for table in [
        "audit_log",
        "suggestion_decisions",
        "suggestions",
        "entity_mappings",
        "reconciliation_results",
        "gstr2b_records",
        "validation_errors",
        "invoices",
        "hsn_master",
        "upload_batches",
        "clients",
        "users",
        "tenants",
    ]:
        op.drop_table(table)
    for enum_name in [
        "suggestion_decision_enum",
        "match_type_enum",
        "severity_enum",
        "gstn_verification_status_enum",
        "invoice_state_enum",
        "batch_status_enum",
        "role_enum",
    ]:
        op.execute(f"DROP TYPE IF EXISTS {enum_name}")
