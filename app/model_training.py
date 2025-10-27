# app/model_training.py（参考15-MLFlow.pdf的“Experiments”章节）
import mlflow
import mlflow.sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
import yaml
from app.data_processing import extract_text_from_pdf  # 复用之前的PDF提取功能

# 加载参数（与DVC共享params.yaml，实现参数统一管理）
with open("params.yaml", "r") as f:
    params = yaml.safe_load(f)["model"]

def train_keyword_model(pdf_paths: list):
    """训练关键词提取模型，用MLFlow跟踪实验"""
    # 初始化MLFlow
    mlflow.set_experiment(experiment_name=params["experiment_name"])
    
    with mlflow.start_run():
        # 1. 提取PDF文本（输入数据）
        texts = [extract_text_from_pdf(path) for path in pdf_paths]
        
        # 2. 记录参数（15-MLFlow.pdf的“Parameters”跟踪）
        mlflow.log_param("max_features", params["max_features"])
        mlflow.log_param("ngram_range", params["ngram_range"])
        
        # 3. 训练模型（示例：TF-IDF关键词提取）
        vectorizer = TfidfVectorizer(
            max_features=params["max_features"],
            ngram_range=params["ngram_range"]
        )
        X = vectorizer.fit_transform(texts)
        
        # 4. 记录指标（假设用虚拟准确率，实际可替换为真实评估）
        dummy_accuracy = 0.85  # 实际应基于测试集计算
        mlflow.log_metric("accuracy", dummy_accuracy)
        
        # 5. 保存模型（15-MLFlow.pdf的“Models”管理）
        mlflow.sklearn.log_model(vectorizer, "keyword-model")
        
        print(f"实验完成：Run ID = {mlflow.active_run().info.run_id}")
        return vectorizer

if __name__ == "__main__":
    # 用DVC管理的PDF作为训练数据
    pdf_files = [
        "data/raw/14-DVC.pdf",
        "data/raw/15-MLFlow.pdf"
    ]
    train_keyword_model(pdf_files)