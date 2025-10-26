# tests/test_main.py（修复后）
import os
import sys

import pytest

from app.main import REQUIRED_SECRETS, count_text_stats  # 所有导入移到顶部

# 确保项目根目录在 sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)


def test_count_text_stats():
    # 移除冗余的 import os（模块顶部已导入）

    # 注入所有必需的密钥（包含 TEXT_API_KEY 和 LOG_LEVEL）
    os.environ["TEXT_API_KEY"] = "test_key_123"
    os.environ["LOG_LEVEL"] = "INFO"  # 新增：注入 LOG_LEVEL，满足 REQUIRED_SECRETS 校验

    text = "DevOps DevOps Ops"
    stats = count_text_stats(text)

    # 修正键名：用 word_frequency 替代 word_count（与 main.py 保持一致）
    assert stats["total_words"] == 3
    assert (
        stats["word_frequency"]["devops"] == 2
    )  # 注意：text 被 lower() 处理，键为小写 "devops"


def test_missing_secrets(monkeypatch):
    # mock load_dotenv：不加载 .env 文件
    def mock_load_dotenv(*args, **kwargs):
        return False

    monkeypatch.setattr("app.main.load_dotenv", mock_load_dotenv)

    # 清空所有必需的密钥环境变量（包含 TEXT_API_KEY 和 LOG_LEVEL）
    for secret in REQUIRED_SECRETS:
        monkeypatch.delenv(secret, raising=False)

    # 验证缺失密钥时抛错
    with pytest.raises(RuntimeError) as excinfo:
        count_text_stats("test")

    assert "缺失关键Secrets" in str(excinfo.value)
    assert all(
        secret in str(excinfo.value) for secret in REQUIRED_SECRETS
    )  # 同时校验两个密钥
