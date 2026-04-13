#!/usr/bin/env python3
"""
论文风格分析脚本
从论文文本中提取风格特征 - 压缩版
保留所有与风格相关的特征，丢弃具体内容
"""

import re
import json
import sys
from pathlib import Path
from collections import Counter


class StyleAnalyzer:
    """论文风格分析器 - 压缩版"""

    def __init__(self):
        self.connectors = {
            "causal": [
                "因此",
                "由此可见",
                "因而",
                "所以",
                "导致",
                "使得",
                "于是",
                "故",
                "因",
            ],
            "transitional": ["然而", "但是", "不过", "尽管如此", "但", "然而", "相反"],
            "progressive": ["更进一步", "此外", "并且", "同时", "再者", "而且"],
            "conclusive": ["综上所述", "总之", "总而言之", "总的说来", "基于此"],
            "exemplary": ["例如", "以", "为例", "诸如", "如", "即", "也就是说"],
            "introductory": ["值得注意的是", "需要指出", "应当指出", "众所周知"],
            "adversative": ["虽然", "即使", "即便", "即便如此", "即便如此"],
        }

    def analyze(self, text: str) -> dict:
        """分析文本风格 - 压缩版"""
        sentences = self.split_sentences(text)
        paragraphs = self.split_paragraphs(text)

        return {
            "sentence": self.analyze_sentence(text, sentences),
            "paragraph": self.analyze_paragraph(text, paragraphs),
            "argumentation": self.analyze_argumentation(paragraphs),
            "citation": self.analyze_citation(text),
            "terminology": self.analyze_terminology(text),
            "description_patterns": self.analyze_description_patterns(text),
            "tone": self.analyze_tone(text),
        }

    def analyze_sentence(self, text: str, sentences: list) -> dict:
        """分析句式特征"""
        if not sentences:
            return {}

        lengths = [len(s) for s in sentences]
        avg_length = sum(lengths) / len(lengths)

        short = sum(1 for l in lengths if l < 25)
        medium = sum(1 for l in lengths if 25 <= l <= 50)
        long = sum(1 for l in lengths if l > 50)

        connector_usage = self.analyze_connectors(text)
        sentence_patterns = self.analyze_sentence_patterns(sentences)

        return {
            "avg_length": round(avg_length, 1),
            "min_length": min(lengths),
            "max_length": max(lengths),
            "total_sentences": len(sentences),
            "length_distribution": {
                "short": round(short / len(sentences), 3),
                "medium": round(medium / len(sentences), 3),
                "long": round(long / len(sentences), 3),
            },
            "connectors": connector_usage,
            "patterns": sentence_patterns,
        }

    def analyze_connectors(self, text: str) -> dict:
        """分析连接词使用"""
        result = {}
        total = 0
        for category, words in self.connectors.items():
            count = sum(len(re.findall(re.escape(w), text)) for w in words)
            found = [w for w in words if w in text]
            if count > 0:
                total += count
                result[category] = {"count": count, "preferred": found[:3]}

        if result:
            result["total_connector_count"] = total

        return result

    def analyze_sentence_patterns(self, sentences: list) -> dict:
        """分析常见句式模式"""
        patterns = {
            "definition": r"(?:是|指|定义|所谓)\s*[\u4e00-\u9fa5]+",
            "comparison": r"(?:相比|相对于|与.*相比|不同于)",
            "result": r"(?:结果|实验|表明|证实|证明)",
            "purpose": r"(?:为了|旨在|目的|目标是)",
            "contribution": r"(?:贡献|创新点|主要)",
            "limitation": r"(?:局限|不足|缺点|缺陷)",
        }

        result = {}
        for name, pattern in patterns.items():
            matches = len(re.findall(pattern, "".join(sentences[:50])))
            if matches > 0:
                result[name] = matches
        return result

    def analyze_paragraph(self, text: str, paragraphs: list) -> dict:
        """分析段落特征"""
        if not paragraphs:
            return {}

        lengths = [len(p) for p in paragraphs]
        avg_length = sum(lengths) / len(paragraphs)

        opening_patterns = self.analyze_opening_patterns(paragraphs)
        closing_patterns = self.analyze_closing_patterns(paragraphs)

        return {
            "avg_length": round(avg_length, 1),
            "min_length": min(lengths),
            "max_length": max(lengths),
            "total_paragraphs": len(paragraphs),
            "opening_patterns": opening_patterns,
            "closing_patterns": closing_patterns,
        }

    def analyze_opening_patterns(self, paragraphs: list) -> dict:
        """分析段落开头模式"""
        topic_sentence = 0
        question = 0
        contrast = 0
        background = 0
        reference = 0

        for p in paragraphs[:30]:
            p = p.strip()
            if not p:
                continue
            first_30 = p[:30]

            if any(
                kw in first_30
                for kw in ["本文", "本研究", "该", "本", "该方法", "本方法", "本章"]
            ):
                topic_sentence += 1
            elif p.startswith("如何") or p.startswith("为什么") or p.startswith("怎"):
                question += 1
            elif any(
                kw in first_30 for kw in ["然而", "但是", "相比", "不同于", "相反"]
            ):
                contrast += 1
            elif any(kw in first_30 for kw in ["随着", "近年来", "目前", "当今", "在"]):
                background += 1
            elif any(kw in first_30 for kw in ["文献", "研究表明", "根据", "前人"]):
                reference += 1

        total = topic_sentence + question + contrast + background + reference
        if total == 0:
            return {}

        return {
            "topic_sentence": round(topic_sentence / total, 3),
            "question": round(question / total, 3),
            "contrast": round(contrast / total, 3),
            "background": round(background / total, 3),
            "reference": round(reference / total, 3),
        }

    def analyze_closing_patterns(self, paragraphs: list) -> dict:
        """分析段落结尾模式"""
        summary = 0
        transition = 0
        conclusion = 0

        for p in paragraphs[:30]:
            p = p.strip()
            if not p or len(p) < 20:
                continue
            ending = p[-20:]

            if any(kw in ending for kw in ["综上所述", "总之", "因此"]):
                summary += 1
            elif any(kw in ending for kw in ["此外", "进一步", "下一步", "未来"]):
                transition += 1
            elif any(kw in ending for kw in ["结论", "总结", "主要贡献"]):
                conclusion += 1

        total = summary + transition + conclusion
        if total == 0:
            return {}

        return {
            "summary": round(summary / total, 3),
            "transition": round(transition / total, 3),
            "conclusion": round(conclusion / total, 3),
        }

    def analyze_argumentation(self, paragraphs: list) -> dict:
        """分析论证逻辑结构"""
        patterns = {
            "general_specific": r"^[\u4e00-\u9fa5]{0,10}(首先|第一|其一).*(其次|第二|其二).*(最后|第三|其三)",
            "cause_effect": r"(?:因此|所以|导致|由于).*(?:因此|所以|从而)",
            "comparison": r"(?:相比|与|相对于).*(?:但是|然而|而|但)",
            "problem_solution": r"(?:问题|挑战|难点).*(?:解决|方案|方法|策略)",
            "progressive": r"(?:进一步|更重要的是|此外).*?也是",
        }

        result = {}
        combined = "".join(paragraphs[:50])
        for name, pattern in patterns.items():
            matches = len(re.findall(pattern, combined))
            if matches > 0:
                result[name] = matches

        return result

    def analyze_citation(self, text: str) -> dict:
        """分析引用格式"""
        result = {}

        bracket_citation = len(re.findall(r"\[[\d,\-\s]+\]", text))
        paren_citation = len(re.findall(r"\([\u4e00-\u9fa5a-zA-Z]+,\s*\d{4}\)", text))

        result["in_text_style"] = (
            "bracket" if bracket_citation > paren_citation else "paren"
        )
        result["bracket_count"] = bracket_citation
        result["paren_count"] = paren_citation

        doi_pattern = len(re.findall(r"doi:?\s*10\.\d{4,}", text))
        if doi_pattern > 0:
            result["has_doi"] = True

        return result

    def analyze_terminology(self, text: str) -> dict:
        """分析术语使用"""
        abbreviations = re.findall(r"([A-Z]{2,})(?:\s|$|，|。)", text)
        chinese_abbrev = re.findall(
            r"([\u4e00-\u9fa5]{2,4})(?:以下|本文|该)(?:称|叫)", text
        )

        first_intro = self.analyze_term_intro(text)

        formulas = len(re.findall(r"公式[\s\d\（\(]+", text))
        figures = len(re.findall(r"图[\s\d\（\(]+", text))
        tables = len(re.findall(r"表[\s\d\（\(]+", text))

        return {
            "abbreviations_count": len(abbreviations),
            "abbreviation_examples": list(set(abbreviations))[:5],
            "chinese_abbreviations": chinese_abbrev[:3],
            "first_introduction_style": first_intro,
            "formulas_count": formulas,
            "figures_count": figures,
            "tables_count": tables,
        }

    def analyze_term_intro(self, text: str) -> str:
        """分析术语首次引入方式"""
        patterns = [
            (r"[\u4e00-\u9fa5]+是指", "定义式"),
            (r"根据[\u4e00-\u9fa5]+[\u4e00-\u9fa5]+提出", "引用式"),
            (r"通过.*实现.*[\u4e00-\u9fa5]+", "描述式"),
            (r"[\u4e00-\u9fa5]+(?:简|称)为", "简称式"),
        ]

        for pattern, name in patterns:
            if re.search(pattern, text[:5000]):
                return name
        return "unknown"

    def analyze_description_patterns(self, text: str) -> dict:
        """分析描述模式 - 图表、模型、实验"""
        result = {}

        fig_patterns = [
            (r"如图[\s\d\（\(]+所示", "如图所示"),
            (r"图[\s\d\（\(]+描述了", "图描述"),
            (r"从图[\s\d\（\(]+可以?看到", "从图可见"),
        ]
        for p, n in fig_patterns:
            if re.search(p, text):
                result[n] = True

        model_patterns = [
            (r"包括.*模块", "模块化描述"),
            (r"整体.*架构", "架构描述"),
            (r"主要.*由.*组成", "组成描述"),
        ]
        for p, n in model_patterns:
            if re.search(p, text):
                result[n] = True

        exp_patterns = [
            (r"数据集.*包括", "数据集介绍"),
            (r"实验.*环境", "实验环境"),
            (r"对比.*实验", "对比实验"),
            (r"参数.*设置", "参数设置"),
        ]
        for p, n in exp_patterns:
            if re.search(p, text):
                result[n] = True

        return result

    def analyze_tone(self, text: str) -> dict:
        """分析语气"""
        passive = len(re.findall(r"被[\u4e00-\u9fa5]+", text))
        passive += len(re.findall(r"由[\u4e00-\u9fa5]+实现", text))

        formal = [
            "提出",
            "构建",
            "实现",
            "验证",
            "分析",
            "研究",
            "方法",
            "模型",
            "系统",
            "机制",
        ]
        formal_count = sum(text.count(w) for w in formal)

        cautious = ["可能", "或许", "初步", "基本", "相对", "一定程度"]
        cautious_count = sum(text.count(w) for w in cautious)

        return {
            "passive_ratio": round(passive / max(len(text), 1) * 1000, 3),
            "formal_terms_count": formal_count,
            "cautious_terms_count": cautious_count,
            "hedge_words": [w for w in cautious if w in text][:3],
        }

    def split_sentences(self, text: str) -> list:
        """分句"""
        sentences = re.split(r"[。！？；]", text)
        return [s.strip() for s in sentences if s.strip() and len(s.strip()) > 5]

    def split_paragraphs(self, text: str) -> list:
        """分段落"""
        paragraphs = re.split(r"\n\s*\n|\n", text)
        return [p.strip() for p in paragraphs if p.strip() and len(p.strip()) > 30]


def analyze_file(file_path: str, paper_id: str = None) -> dict:
    """分析单个文件"""
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    analyzer = StyleAnalyzer()
    result = analyzer.analyze(text)

    path = Path(file_path)
    if paper_id is None:
        paper_id = path.stem

    return {
        "paper_id": paper_id,
        "source": path.name,
        "style_features": result,
        "discarded_content": [
            "完整正文",
            "实验数据",
            "图表具体内容",
            "参考文献条目",
            "代码实现细节",
        ],
    }


def analyze_batch(file_paths: list, output_dir: str = "style_extracts") -> list:
    """批量分析多篇论文"""
    import os

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    results = []
    for i, file_path in enumerate(file_paths):
        paper_id = f"paper_{i + 1}"
        result = analyze_file(file_path, paper_id)

        extract_file = output_path / f"{paper_id}.json"
        with open(extract_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        result["style_features"] = {"status": "saved", "file": str(extract_file)}
        results.append(result)

        print(f"[{i + 1}/{len(file_paths)}] 已处理: {Path(file_path).name}")

    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_style.py <paper.txt>")
        print("   or: python analyze_style.py --batch <dir>")
        sys.exit(1)

    if sys.argv[1] == "--batch" and len(sys.argv) >= 3:
        import glob

        dir_path = sys.argv[2]
        txt_files = glob.glob(f"{dir_path}/*.txt")
        if not txt_files:
            print(f"No .txt files found in {dir_path}")
            sys.exit(1)
        results = analyze_batch(txt_files, f"{dir_path}/style_extracts")
        print(f"\n完成！已处理 {len(results)} 篇论文")
    else:
        file_path = sys.argv[1]
        result = analyze_file(file_path)
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
