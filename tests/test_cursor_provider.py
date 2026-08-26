"""Cursor provider: CURSOR_API_KEY, default endpoint, and CURSOR_BASE_URL override."""

from __future__ import annotations

import pytest

from tradingagents.llm_clients.api_key_env import get_api_key_env
from tradingagents.llm_clients.factory import create_llm_client
from tradingagents.llm_clients.model_catalog import get_model_options
from tradingagents.llm_clients.validators import validate_model


@pytest.mark.unit
def test_key_env_and_cli_table():
    assert get_api_key_env("cursor") == "CURSOR_API_KEY"
    from cli.utils import _llm_provider_table

    row = next(r for r in _llm_provider_table() if r[1] == "cursor")
    assert row[0] == "Cursor"
    assert row[2] == "https://api.cursor.com/v1"


@pytest.mark.unit
def test_cli_table_honors_cursor_base_url(monkeypatch):
    monkeypatch.setenv("CURSOR_BASE_URL", "http://127.0.0.1:8080/v1")
    from cli.utils import _llm_provider_table

    row = next(r for r in _llm_provider_table() if r[1] == "cursor")
    assert row[2] == "http://127.0.0.1:8080/v1"


@pytest.mark.unit
def test_client_uses_cursor_api_key_and_default_url(monkeypatch):
    monkeypatch.setenv("CURSOR_API_KEY", "crsr_test_key")
    monkeypatch.delenv("CURSOR_BASE_URL", raising=False)
    llm = create_llm_client(provider="cursor", model="composer-2.5").get_llm()
    assert str(llm.openai_api_base) == "https://api.cursor.com/v1"
    key = (
        llm.openai_api_key.get_secret_value()
        if hasattr(llm.openai_api_key, "get_secret_value")
        else llm.openai_api_key
    )
    assert key == "crsr_test_key"
    assert getattr(llm, "use_responses_api", False) in (False, None)


@pytest.mark.unit
def test_missing_key_raises(monkeypatch):
    monkeypatch.delenv("CURSOR_API_KEY", raising=False)
    with pytest.raises(ValueError, match="CURSOR_API_KEY"):
        create_llm_client(provider="cursor", model="composer-2.5").get_llm()


@pytest.mark.unit
def test_cursor_base_url_override(monkeypatch):
    monkeypatch.setenv("CURSOR_API_KEY", "crsr_test_key")
    monkeypatch.setenv("CURSOR_BASE_URL", "http://localhost:8765/v1")
    llm = create_llm_client(provider="cursor", model="composer-2.5").get_llm()
    assert str(llm.openai_api_base) == "http://localhost:8765/v1"


@pytest.mark.unit
def test_catalog_and_any_model():
    quick = {value for _, value in get_model_options("cursor", "quick")}
    deep = {value for _, value in get_model_options("cursor", "deep")}
    assert "composer-2.5" in quick
    assert "auto" in deep
    assert validate_model("cursor", "composer-2.5")
    assert validate_model("cursor", "any-account-model-id")
