# app/main.py（修改后，基于 5.1-12 Factor Config.pdf “Runtime injection”）
import os
from collections import Counter

from dotenv import load_dotenv

# 1. 仅定义常量（不执行加载逻辑）
REQUIRED_SECRETS = ["TEXT_API_KEY"]


# 2. 新增 Secrets 加载函数（延迟到函数调用时执行）
def load_secrets():
    """加载并校验 Secrets，遵循 5.1-12 Factor Config.pdf “Fail Fast”原则"""
    load_dotenv()  # 此时执行加载，而非模块全局
    missing_secrets = [key for key in REQUIRED_SECRETS if not os.getenv(key)]
    if missing_secrets:
        raise RuntimeError(
            f"缺失关键Secrets：{', '.join(missing_secrets)}（请检查.env）"
        )
    # 返回加载的 Secrets（避免全局变量缓存）
    return {
        "TEXT_API_KEY": os.getenv("TEXT_API_KEY"),
        "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO").upper(),
    }


# 3. 核心文本统计功能（调用 load_secrets() 加载配置）
def count_text_stats(text: str) -> dict:
    secrets = load_secrets()  # 每次调用时加载，确保测试可隔离
    words = text.strip().lower().split()
    return {
        "total_words": len(words),
        "word_frequency": dict(Counter(words).most_common(3)),
        "api_key_status": "loaded",
        "log_level": secrets["LOG_LEVEL"],
    }


if __name__ == "__main__":
    # 主函数中加载 Secrets
    secrets = load_secrets()
    test_text = "DevOps combines Dev and Ops DevOps accelerates delivery"
    stats = count_text_stats(test_text)
    print(f"文本统计结果（LOG_LEVEL：{secrets['LOG_LEVEL']}）：", stats)
