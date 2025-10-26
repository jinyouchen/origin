# tests/test_main.py（优化后，基于 testing-with-docker.pdf）
import pytest
import os
import sys

# 确保项目根目录在 sys.path（若已通过 pytest.ini 配置可省略）
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

# 导入依赖（此时 app.main 导入时无全局 Secrets 加载）
from app.main import count_text_stats, load_secrets, REQUIRED_SECRETS
from dotenv import load_dotenv


def test_count_text_stats():
    # 正常场景测试（依赖 .env 存在，或手动注入环境变量）
    text = "DevOps DevOps Ops"
    stats = count_text_stats(text)
    assert stats["total_words"] == 3
    assert stats["word_frequency"]["devops"] == 2
    assert stats["api_key_status"] == "loaded"


def test_missing_secrets(monkeypatch):
    # 1. mock load_dotenv：使其不加载 .env（参考 testing-with-docker.pdf 模拟逻辑）
    def mock_load_dotenv(*args, **kwargs):
        return False  # 不加载任何文件

    monkeypatch.setattr("app.main.load_dotenv", mock_load_dotenv)

    # 2. 清空所有 REQUIRED_SECRETS 的环境变量（参考 5.1-12 Factor Config.pdf）
    for secret in REQUIRED_SECRETS:
        monkeypatch.delenv(secret, raising=False)  # 删除系统/虚拟环境变量

    # 3. 执行测试：调用 count_text_stats 时会触发 load_secrets()，进而抛错
    with pytest.raises(RuntimeError) as excinfo:
        count_text_stats("test")

    # 校验错误信息（符合 6-Software testing.pdf “精准测试结果”要求）
    assert "缺失关键Secrets" in str(excinfo.value)
    assert all(secret in str(excinfo.value) for secret in REQUIRED_SECRETS)
