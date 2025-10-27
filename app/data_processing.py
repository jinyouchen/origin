# app/data_processing.py（参考14-DVC.pdf第6章“Data Transformation”）
import os
import argparse
from pathlib import Path
from PyPDF2 import PdfReader  # 依赖PyPDF2，已在requirements.txt中

def extract_text_from_pdf(pdf_path: str) -> str:
    """从PDF文件提取文本（复用之前的逻辑，适配14-DVC.pdf的数据处理要求）"""
    if not Path(pdf_path).exists():
        raise FileNotFoundError(f"原始PDF不存在：{pdf_path}")
    
    text = []
    with open(pdf_path, "rb") as f:
        reader = PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text.strip())
    return "\n".join(text)

def process_all_pdfs(raw_dir: str, processed_dir: str):
    """处理raw目录下所有PDF，保存到processed目录（DVC输出目录）"""
    # 创建processed目录（若不存在）
    Path(processed_dir).mkdir(parents=True, exist_ok=True)
    
    # 遍历raw目录下的PDF文件
    for pdf_file in Path(raw_dir).glob("*.pdf"):
        if pdf_file.name in ["14- DVC.pdf", "15-MLFlow.pdf"]:  # 只处理目标文件
            # 提取文本
            pdf_text = extract_text_from_pdf(str(pdf_file))
            
            # 保存到processed目录（文件名保持一致，后缀改为.txt）
            output_path = Path(processed_dir) / f"{pdf_file.stem}.txt"
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(pdf_text)
            print(f"已处理：{pdf_file.name} → {output_path}")

if __name__ == "__main__":
    # 解析命令行参数（DVC流水线传递的输入/输出路径，参考dvc.yaml配置）
    parser = argparse.ArgumentParser(description="处理PDF数据（DVC阶段）")
    parser.add_argument("--input", required=True, help="原始PDF目录（data/raw）")
    parser.add_argument("--output", required=True, help="处理后文本目录（data/processed）")
    args = parser.parse_args()
    
    # 执行处理
    process_all_pdfs(raw_dir=args.input, processed_dir=args.output)