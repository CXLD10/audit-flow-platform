from datetime import datetime, timezone
from uuid import UUID

from app.core.database import SessionLocal
from app.core.security import get_password_hash
from app.models.client import Client
from app.models.enums import Role
from app.models.tenant import Tenant
from app.models.user import User

TENANT_ID = UUID("00000000-0000-0000-0000-000000000001")
USER_ID = UUID("00000000-0000-0000-0000-000000000010")
CLIENT_ID = UUID("00000000-0000-0000-0000-000000000020")


def main() -> None:
    db = SessionLocal()
    try:
        if db.get(Tenant, TENANT_ID):
            print("Seed data already exists.")
            return
        tenant = Tenant(id=TENANT_ID, name="Demo CA Firm", plan_tier="starter")
        user = User(
            id=USER_ID,
            tenant_id=TENANT_ID,
            email="ca@example.com",
            role=Role.CA,
            password_hash=get_password_hash("password123"),
            last_login_at=datetime.now(tz=timezone.utc),
        )
        client = Client(id=CLIENT_ID, tenant_id=TENANT_ID, gstin="27ABCDE1234F1Z5", legal_name="Demo Manufacturing Pvt Ltd", column_mapping={})
        db.add_all([tenant, user, client])
        db.commit()
        print("Seed data created.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
