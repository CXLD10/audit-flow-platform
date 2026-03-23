from datetime import date

from app.models.hsn_master import HSNMaster


class HSNRepository:
    def __init__(self, db):
        self.db = db

    def get_by_code(self, code: str) -> HSNMaster | None:
        return self.db.query(HSNMaster).filter(HSNMaster.code == code).one_or_none()

    def last_refresh_date(self) -> date | None:
        record = self.db.query(HSNMaster).order_by(HSNMaster.refreshed_at.desc()).first()
        return record.refreshed_at if record else None
