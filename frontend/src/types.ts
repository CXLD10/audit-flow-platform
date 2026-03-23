export type UserRole = "CA" | "CLIENT" | "ADMIN";
export type Severity = "CRITICAL" | "HIGH" | "MEDIUM" | "LOW";
export type InvoiceState = "RAW" | "PARSED" | "NORMALIZED" | "VALIDATED" | "ERROR_FOUND" | "RECONCILED" | "REVIEWED" | "RESOLVED" | "EXPORTED";
export type MatchType = "EXACT" | "FUZZY" | "HEURISTIC" | "UNMATCHED";

export type BatchStatus = "QUEUED" | "PENDING" | "PROCESSING" | "COMPLETE" | "FAILED";

export type AuthUser = {
  id: string;
  tenant_id: string;
  email: string;
  role: UserRole;
  created_at: string;
};

export type ClientRecord = {
  id: string;
  tenant_id: string;
  gstin: string;
  legal_name: string;
  created_at: string;
};

export type ValidationErrorRecord = {
  id: string;
  invoice_id: string;
  rule_id: string;
  severity: Severity;
  field_name: string;
  actual_value: string;
  expected_value: string;
  message: string;
};

export type ReconciliationRecord = {
  id: string;
  invoice_id: string;
  gstr2b_record_id: string | null;
  match_type: MatchType;
  confidence_score: number;
  delta_taxable_value: string;
  delta_tax_amount: string;
  created_at: string;
};

export type InvoiceRecord = {
  id: string;
  tenant_id: string;
  batch_id: string;
  client_id: string;
  invoice_number: string;
  invoice_date: string | null;
  supplier_name?: string | null;
  canonical_supplier_name?: string | null;
  supplier_gstin: string;
  recipient_gstin: string;
  hsn_sac_code: string;
  taxable_value: string;
  cgst_amount: string;
  sgst_amount: string;
  igst_amount: string;
  total_invoice_value: string;
  place_of_supply: string;
  applicable_rate?: string | null;
  credit_note_flag: boolean;
  state: InvoiceState;
  gstn_verification_status?: string | null;
  created_at: string;
  errors: ValidationErrorRecord[];
  reconciliation_result?: ReconciliationRecord | null;
};

export type BatchRecord = {
  id: string;
  tenant_id: string;
  client_id: string;
  user_id: string;
  filename: string;
  file_path_s3: string;
  status: BatchStatus;
  return_period: string | null;
  total_invoices: number;
  error_count: number;
  created_at: string;
  completed_at: string | null;
  failed_stage: string | null;
  error_message: string | null;
  last_completed_stage: string | null;
};

export type BatchResultsResponse = {
  batch: BatchRecord;
  invoices: InvoiceRecord[];
  errors: ValidationErrorRecord[];
  degraded_messages: string[];
};

export type BatchProgress = {
  stage: string;
  pct: number;
  processed: number;
  total: number;
  status: BatchStatus;
  error_message?: string | null;
  degraded?: boolean;
};

export type PaginatedInvoices = {
  items: InvoiceRecord[];
  total: number;
};

export type AuditLogRecord = {
  id: string;
  action_type: string;
  entity_type: string;
  entity_id: string;
  created_at: string;
  metadata: Record<string, string | number | boolean | null>;
};
