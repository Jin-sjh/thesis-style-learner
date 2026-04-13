#!/usr/bin/env python3
"""
论文风格分析脚本
从论文文本中提取风格特征
"""

import re
import json
import sys
from pathlib import Path


class StyleAnalyzer:
    """论文风格分析器"""

    def __init__(self):
        self.connectors = {
            "causal": ["因此", "由此可见", "因而", "所以", "导致", "使得"],
            "transitional": ["然而", "但是", "不过", "尽管如此", "但", "然而"],
            "progressive": ["更进一步", "此外", "并且", "同时", "此外", "再者"],
            "conclusive": ["综上所述", "总之", "总而言之", "总的说来"],
            "exemplary": ["例如", "以", "为例", "诸如", "如"],
        }

    def analyze(self, text: str) -> dict:
        """分析文本风格"""
        return {
            "sentence": self.analyze_sentence(text),
            "paragraph": self.analyze_paragraph(text),
            "terminology": self.analyze_terminology(text),
            "tone": self.analyze_tone(text),
        }

    def analyze_sentence(self, text: str) -> dict:
        """分析句式特征"""
        sentences = self.split_sentences(text)
        if not sentences:
            return {}

        lengths = [len(s) for s in sentences]
        avg_length = sum(lengths) / len(lengths)

        short = sum(1 for l in lengths if l < 25)
        medium = sum(1 for l in lengths if 25 <= l <= 50)
        long = sum(1 for l in lengths if l > 50)

        return {
            "avg_length": round(avg_length, 1),
            "total_sentences": len(sentences),
            "length_distribution": {
                "short": short / len(sentences),
                "medium": medium / len(sentences),
                "long": long / len(sentences),
            },
            "connectors": self.analyze_connectors(text),
        }

    def analyze_connectors(self, text: str) -> dict:
        """分析连接词使用"""
        result = {}
        for category, words in self.connectors.items():
            count = sum(text.count(w) for w in words)
            found = [w for w in words if w in text]
            result[category] = {"count": count, "examples": found[:3]}
        return result

    def analyze_paragraph(self, text: str) -> dict:
        """分析段落特征"""
        paragraphs = self.split_paragraphs(text)
        if not paragraphs:
            return {}

        lengths = [len(p) for p in paragraphs]
        avg_length = sum(lengths) / len(paragraphs)

        # 分析段落开头
        opening_patterns = self.analyze_opening_patterns(paragraphs)

        return {
            "avg_length": round(avg_length, 1),
            "total_paragraphs": len(paragraphs),
            "opening_patterns": opening_patterns,
        }

    def analyze_opening_patterns(self, paragraphs: list) -> dict:
        """分析段落开头模式"""
        topic_sentence = 0
        question = 0
        contrast = 0

        for p in paragraphs[:20]:
            p = p.strip()
            if not p:
                continue
            if any(kw in p[:20] for kw in ["本文", "本研究", "该", "本"]):
                topic_sentence += 1
            elif p.startswith("如何") or p.startswith("为什么"):
                question += 1
            elif any(kw in p[:30] for kw in ["然而", "但是", "相比", "不同于"]):
                contrast += 1

        total = topic_sentence + question + contrast
        if total == 0:
            return {}

        return {
            "topic_sentence": topic_sentence / total,
            "question": question / total,
            "contrast": contrast / total,
        }

    def analyze_terminology(self, text: str) -> dict:
        """分析术语使用"""
        # 检测缩写词
        abbreviations = re.findall(r"([A-Z]{2,})(?:\s|$|，|。)", text)
        # 检测公式引用
        formulas = re.findall(r"公式[\s\d]+", text)
        # 检测图表引用
        figures = re.findall(r"图[\s\d]+", text)
        tables = re.findall(r"表[\s\d]+", text)

        return {
            "abbreviations_count": len(abbreviations),
            "formulas_count": len(formulas),
            "figures_count": len(figures),
            "tables_count": len(tables),
        }

    def analyze_tone(self, text: str) -> dict:
        """分析语气"""
        # 被动语态检测
        passive_count = len(re.findall(r"被|由|所|为", text))

        # 学术词汇统计
        academic_words = [
            "提出",
            "构建",
            "实现",
            "验证",
            "分析",
            "研究",
            "方法",
            "模型",
        ]
        academic_count = sum(text.count(w) for w in academic_words)

        return {"passive_indicators": passive_count, "academic_terms": academic_count}

    def split_sentences(self, text: str) -> list:
        """分句"""
        # 按句号、问号、感叹号分句
        sentences = re.split(r"[。！？]", text)
        return [s.strip() for s in sentences if s.strip()]

    def split_paragraphs(self, text: str) -> list:
        """分段落"""
        return [p.strip() for p in text.split("\n\n") if p.strip()]


def analyze_file(file_path: str) -> dict:
    """分析单个文件"""
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    analyzer = StyleAnalyzer()
    return analyzer.analyze(text)


def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_style.py <paper.txt>")
        sys.exit(1)

    file_path = sys.argv[1]
    result = analyze_file(file_path)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
