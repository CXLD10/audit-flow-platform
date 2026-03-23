from pathlib import Path


def test_base_repository_source_enforces_tenant_filter():
    source = Path("backend/app/repositories/base.py").read_text()
    assert "model.tenant_id == self.tenant_id" in source or "self.model.tenant_id == self.tenant_id" in source
