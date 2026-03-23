from enum import Enum


class Role(str, Enum):
    CA = "CA"
    CLIENT = "CLIENT"
    ADMIN = "ADMIN"


class BatchStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"


class InvoiceState(str, Enum):
    RAW = "RAW"
    PARSED = "PARSED"
    NORMALIZED = "NORMALIZED"
    VALIDATED = "VALIDATED"
    ERROR_FOUND = "ERROR_FOUND"
    RECONCILED = "RECONCILED"
    REVIEWED = "REVIEWED"
    RESOLVED = "RESOLVED"
    EXPORTED = "EXPORTED"


class Severity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class MatchType(str, Enum):
    EXACT = "EXACT"
    FUZZY = "FUZZY"
    HEURISTIC = "HEURISTIC"
    UNMATCHED = "UNMATCHED"


class GSTNVerificationStatus(str, Enum):
    ACTIVE = "ACTIVE"
    CANCELLED = "CANCELLED"
    SUSPENDED = "SUSPENDED"
    MIGRATED = "MIGRATED"
    GSTIN_UNVERIFIED = "GSTIN_UNVERIFIED"


class SuggestionDecision(str, Enum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
