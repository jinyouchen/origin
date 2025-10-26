# app/main.py（修复后）
import os
from collections import Counter
from dotenv import load_dotenv

# 1. 定义所有必需的密钥（包含 LOG_LEVEL，避免 KeyError）
REQUIRED_SECRETS = ["TEXT_API_KEY", "LOG_LEVEL"]  # 新增 LOG_LEVEL 到必需列表


def load_secrets():
    """加载并校验 Secrets，显式指定 .env 路径"""
    # 移除重复导入（已在模块顶部导入 os 和 load_dotenv）

    # 计算 .env 路径：main.py 在 app/ 目录，.env 在项目根目录
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dotenv_path = os.path.join(project_root, ".env")

    # 强制加载指定路径的 .env 文件
    load_dotenv(dotenv_path=dotenv_path)

    # 校验所有必需密钥（包括 LOG_LEVEL）
    missing_secrets = [key for key in REQUIRED_SECRETS if not os.getenv(key)]
    if missing_secrets:
        raise RuntimeError(
            f"缺失关键Secrets：{', '.join(missing_secrets)}（请检查.env）"
        )
    return {key: os.getenv(key) for key in REQUIRED_SECRETS}


# 3. 核心文本统计功能
def count_text_stats(text: str) -> dict:
    secrets = load_secrets()  # 加载包含 LOG_LEVEL 的密钥
    words = text.strip().lower().split()
    return {
        "total_words": len(words),
        "word_frequency": dict(Counter(words).most_common(3)),
        "api_key_status": "loaded",
        "log_level": secrets["LOG_LEVEL"],  # 现在 LOG_LEVEL 已被校验，安全访问
    }


if __name__ == "__main__":
    secrets = load_secrets()
    test_text = "DevOps combines Dev and Ops DevOps accelerates delivery"
    stats = count_text_stats(test_text)
    print(f"文本统计结果（LOG_LEVEL：{secrets['LOG_LEVEL']}）：", stats)
