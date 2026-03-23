import re

GSTIN_PATTERN = re.compile(r"^[0-3][0-9][A-Z]{5}[0-9]{4}[A-Z][A-Z0-9]Z[A-Z0-9]$")
PAN_PATTERN = re.compile(r"^[A-Z]{5}[0-9]{4}[A-Z]$")
GSTIN_CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
STATE_CODES = {f"{value:02d}" for value in range(1, 38)}


def normalize_gstin(value: str) -> str:
    return value.strip().upper()


def calculate_checksum(base: str) -> str:
    factor = 2
    total = 0
    for char in reversed(base):
        code_point = GSTIN_CHARS.index(char)
        addend = factor * code_point
        factor = 1 if factor == 2 else 2
        addend = (addend // len(GSTIN_CHARS)) + (addend % len(GSTIN_CHARS))
        total += addend
    remainder = total % len(GSTIN_CHARS)
    check_code_point = (len(GSTIN_CHARS) - remainder) % len(GSTIN_CHARS)
    return GSTIN_CHARS[check_code_point]


def is_valid_gstin(value: str) -> bool:
    gstin = normalize_gstin(value)
    if len(gstin) != 15 or not GSTIN_PATTERN.match(gstin):
        return False
    if gstin[:2] not in STATE_CODES:
        return False
    if not PAN_PATTERN.match(gstin[2:12]):
        return False
    return calculate_checksum(gstin[:-1]) == gstin[-1]
