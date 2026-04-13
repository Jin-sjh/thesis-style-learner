#!/usr/bin/env python3
"""
风格一致性检查脚本
检查生成内容是否符合风格模型
"""

import json
import sys
from pathlib import Path


class StyleChecker:
    """风格一致性检查器"""

    def __init__(self, style_model: dict):
        self.model = style_model
        self.features = style_model.get("features", {})

    def check(self, text: str) -> dict:
        """检查风格一致性"""
        result = {
            "sentence_length": self.check_sentence_length(text),
            "connectors": self.check_connectors(text),
            "paragraph_opening": self.check_paragraph_opening(text),
            "argumentation": self.check_argumentation(text),
            "terminology": self.check_terminology(text),
        }

        total_score = sum(d["score"] for d in result.values())
        passed = total_score >= 40

        return {
            "consistency_score": total_score,
            "max_score": 50,
            "passed": passed,
            "dimensions": result,
        }

    def check_sentence_length(self, text: str) -> dict:
        """检查句式长度"""
        sentences = text.replace("!", ".").replace("?", ".").split(".")
        lengths = [len(s.strip()) for s in sentences if s.strip()]

        if not lengths:
            return {"score": 0, "details": "无有效句子"}

        avg = sum(lengths) / len(lengths)
        in_range = sum(1 for l in lengths if 25 <= l <= 50) / len(lengths)

        if in_range >= 0.85:
            score = 10 if in_range >= 0.85 else 8
            return {
                "score": score,
                "details": f"{int(in_range * 100)}%句子在30-50字区间",
            }
        elif in_range >= 0.7:
            return {"score": 8, "details": f"{int(in_range * 100)}%句子在30-50字区间"}
        elif in_range >= 0.5:
            return {"score": 6, "details": f"{int(in_range * 100)}%句子在30-50字区间"}
        elif in_range >= 0.3:
            return {"score": 4, "details": f"{int(in_range * 100)}%句子在30-50字区间"}
        else:
            return {"score": 2, "details": f"{int(in_range * 100)}%句子在30-50字区间"}

    def check_connectors(self, text: str) -> dict:
        """检查连接词使用"""
        model_connectors = self.features.get("sentence", {}).get("connectors", {})

        found = []
        for category, words in model_connectors.items():
            count = sum(text.count(w) for w in words)
            found.append(f"{category}:{count}")

        caust = model_connectors.get("causal", [])
        used = sum(text.count(w) for w in caust)

        if used >= 3:
            return {"score": 9, "details": f"使用了{used}次因果连接词"}
        elif used >= 1:
            return {"score": 7, "details": f"使用了{used}次因果连接词"}
        else:
            return {"score": 4, "details": "缺少因果连接词"}

    def check_paragraph_opening(self, text: str) -> dict:
        """检查段落开头"""
        paragraphs = [p for p in text.split("\n\n") if p.strip()]
        if not paragraphs:
            return {"score": 0, "details": "无段落"}

        topic_count = 0
        for p in paragraphs[:10]:
            p = p.strip()[:30]
            if any(kw in p for kw in ["本文", "本研究", "该", "本方法"]):
                topic_count += 1

        ratio = topic_count / min(len(paragraphs), 10)

        if ratio >= 0.7:
            return {"score": 9, "details": f"{int(ratio * 100)}%使用主题句开头"}
        elif ratio >= 0.5:
            return {"score": 7, "details": f"{int(ratio * 100)}%使用主题句开头"}
        else:
            return {"score": 5, "details": f"{int(ratio * 100)}%使用主题句开头"}

    def check_argumentation(self, text: str) -> dict:
        """检查论证逻辑"""
        # 简单检查：是否有明显的论证结构关键词
        has_structure = any(
            kw in text for kw in ["首先", "其次", "最后", "一方面", "另一方面"]
        )

        if has_structure:
            return {"score": 8, "details": "包含论证结构标记"}
        else:
            return {"score": 5, "details": "缺少明显的论证结构标记"}

    def check_terminology(self, text: str) -> dict:
        """检查术语表述"""
        # 检查是否有图表引用
        has_figure = "图" in text
        has_table = "表" in text
        has_formula = "公式" in text

        score = sum([has_figure, has_table, has_formula]) * 3

        details = []
        if has_figure:
            details.append("图")
        if has_table:
            details.append("表")
        if has_formula:
            details.append("公式")

        if details:
            return {
                "score": min(score, 10),
                "details": f"使用了{', '.join(details)}引用",
            }
        else:
            return {"score": 4, "details": "缺少专业术语引用"}


def main():
    if len(sys.argv) < 3:
        print("Usage: python check_style.py <style_model.json> <generated_text.txt>")
        sys.exit(1)

    model_path = sys.argv[1]
    text_path = sys.argv[2]

    with open(model_path, "r", encoding="utf-8") as f:
        style_model = json.load(f)

    with open(text_path, "r", encoding="utf-8") as f:
        text = f.read()

    checker = StyleChecker(style_model)
    result = checker.check(text)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
