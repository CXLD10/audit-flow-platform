from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]


def test_base_repository_source_enforces_tenant_filter():
    source = (REPO_ROOT / "backend/app/repositories/base.py").read_text()
    assert "model.tenant_id == self.tenant_id" in source or "self.model.tenant_id == self.tenant_id" in source
