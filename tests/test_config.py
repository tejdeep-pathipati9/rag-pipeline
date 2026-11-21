"""Check shared settings without loading models or contacting services."""

from unittest.mock import Mock

import pytest

from src import config


def test_environment_settings_are_loaded_and_keys_are_hidden(monkeypatch):
    monkeypatch.setattr(config, "load_dotenv", Mock())
    settings = {
        "EMBEDDING_MODEL": "local-model", "EMBEDDING_REVISION": "pinned",
        "MODEL_CACHE_DIR": "local-cache", "PINECONE_INDEX_NAME": "policies",
        "PINECONE_API_KEY": "pinecone-secret", "LLM_API_KEY": "model-secret",
        "LLM_MODEL": "deployment", "LLM_BASE_URL": "https://example.test/anthropic",
    }
    for name, value in settings.items():
        monkeypatch.setenv(name, value)

    loaded = config.AppConfig.from_env()

    assert (loaded.embedding_model, loaded.embedding_revision, loaded.cache_dir) == (
        "local-model", "pinned", "local-cache"
    )
    assert loaded.pinecone_index_name == "policies"
    assert loaded.pinecone_api_key == "pinecone-secret"
    assert loaded.llm_api_key == "model-secret"
    assert loaded.llm_model == "deployment"
    assert loaded.llm_base_url == "https://example.test/anthropic"
    assert "pinecone-secret" not in repr(loaded)
    assert "model-secret" not in repr(loaded)
    loaded.validate(require_index=True, require_llm=True)


def test_validation_requires_only_the_services_in_use():
    loaded = config.AppConfig()
    loaded.validate(require_index=False, require_llm=False)
    with pytest.raises(ValueError, match="PINECONE_API_KEY"):
        loaded.validate(require_index=True, require_llm=False)
    loaded.pinecone_api_key = "test"
    loaded.pinecone_index_name = "policies"
    loaded.validate(require_index=True, require_llm=False)
    with pytest.raises(ValueError, match="LLM_API_KEY"):
        loaded.validate(require_index=True, require_llm=True)
