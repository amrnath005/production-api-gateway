import pytest
from fastapi import HTTPException

from app.core import settings as settings_module
from app.core.dependencies import get_api_key


@pytest.mark.asyncio
async def test_get_api_key_accepts_configured_key():
    with pytest.MonkeyPatch.context() as monkeypatch:
        monkeypatch.setattr(settings_module.settings, "API_KEY", "test-key")
        assert await get_api_key("test-key") == "test-key"


@pytest.mark.asyncio
async def test_get_api_key_rejects_invalid_key():
    with pytest.MonkeyPatch.context() as monkeypatch:
        monkeypatch.setattr(settings_module.settings, "API_KEY", "test-key")
        with pytest.raises(HTTPException) as exc_info:
            await get_api_key("wrong-key")

        assert exc_info.value.status_code == 401
