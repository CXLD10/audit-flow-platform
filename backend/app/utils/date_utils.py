from datetime import UTC, date, datetime

SUPPORTED_DATE_FORMATS = ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%d.%m.%Y")


def parse_date(value: object) -> date | None:
    if value in (None, ""):
        return None
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    text = str(value).strip()
    for fmt in SUPPORTED_DATE_FORMATS:
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    try:
        return datetime.fromisoformat(text).date()
    except ValueError:
        return None


def is_future(input_date: date) -> bool:
    return input_date > datetime.now(tz=UTC).date()


def financial_year_for(input_date: date) -> int:
    return input_date.year if input_date.month >= 4 else input_date.year - 1
