#!/usr/bin/env python3
"""
从风格模型生成专属 Skill
将分析得到的风格封装为可独立使用的 Skill 文件
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime


class SkillGenerator:
    """专属 Skill 生成器"""

    def __init__(self, style_model: dict):
        self.model = style_model
        self.features = style_model.get("features", {})
        self.advisor = style_model.get("advisor", "未知导师")
        self.source_papers = style_model.get("source_papers", [])

    def generate(self, output_dir: str) -> dict:
        """生成专属 Skill"""
        advisor_dir = (
            self.advisor.replace(" ", "-").replace("教授", "").replace("老师", "")
        )
        skill_name = f"advisor-{advisor_dir}-style"

        output_path = Path(output_dir) / skill_name
        output_path.mkdir(parents=True, exist_ok=True)

        references_path = output_path / "references"
        references_path.mkdir(exist_ok=True)

        skill_md = self._generate_skill_md()
        style_model_json = json.dumps(self.model, ensure_ascii=False, indent=2)

        (output_path / "SKILL.md").write_text(skill_md, encoding="utf-8")
        (references_path / "style_model.json").write_text(
            style_model_json, encoding="utf-8"
        )

        return {
            "skill_name": skill_name,
            "skill_path": str(output_path),
            "advisor": self.advisor,
            "source_papers": self.source_papers,
        }

    def _generate_skill_md(self) -> str:
        """生成 SKILL.md"""
        features = self.features

        sentence = features.get("sentence", {})
        paragraph = features.get("paragraph", {})
        argumentation = features.get("argumentation", {})
        terminology = features.get("terminology", {})
        tone = features.get("tone", {})

        avg_len = sentence.get("avg_length", "35字")
        connectors = sentence.get("connectors", {})
        connector_str = self._format_connectors(connectors)

        opening = paragraph.get("opening_patterns", {})
        opening_pattern = list(opening.keys())[0] if opening else "主题句开头"

        argument_pattern = argumentation.get("preferred_pattern", "总-分-总")

        intro_style = terminology.get("intro_style", "定义式")

        intro_pattern = connectors.get("causal", ["因此"])[0]

        template = f"""---
name: advisor-{self._get_advisor_id()}-style
description: {self.advisor}指导论文风格。当用户需要生成符合{self.advisor}指导风格的毕业论文内容时触发。使用往届学生论文学习的写作风格：句式{avg_len}，段落{opening_pattern}，论证用{argument_pattern}。
---

# {self.advisor}论文风格

本技能用于生成符合{self.advisor}指导风格的毕业论文内容。

## 风格特征

| 维度 | 特征 |
|------|------|
| 句式长度 | {avg_len} |
| 段落开头 | {opening_pattern} |
| 常用连接词 | {connector_str[:50]}... |
| 论证结构 | {argument_pattern} |
| 术语引入 | {intro_style} |
| 学术语气 | {tone.get("formality", "正式")} |

## 使用方法

用户提供：
1. 研究方向/主题
2. 章节类型
3. 核心内容要素

系统自动生成符合该风格的论文内容。

## 章节写作范式

### 摘要
���景-问题-方法-结果-结论的五段式，关键词3-5个

### 引言
宏观背景→具体问题→研究意义，2000-3000字

### 相关工作
按方法分类，每类3-5篇文献，客观评述

### 方法
系统概述→模块详解→公式算法→复杂度分析

### 实验
数据集介绍→对比方法→结果表格→结果分析

### 结论
贡献总结(3点)→局限性→未来工作

## 风格要求

生成时严格遵循：

1. **句子长度**：{avg_len}，避免过短或过长
2. **连接词**：使用 {intro_pattern}、{connector_str.split("、")[0]} 等因果递进连接词
3. **段落开头**：段首使用主题句或{opening_pattern}
4. **论证**：采用{argument_pattern}结构
5. **术语**：首次出现时给出定义

## 示例

**输入**："帮我写第三章方法的第一节，总体框架"

**输出**：
```
## 3.1 总体框架

如图3.1所示，本文提出的{模型名称}主要由三个部分组成：特征提取模块、关系建模模块和预测输出模块。

{intro_pattern}，特征提取模块采用...实现...。该模块的输出作为关系建模模块的输入。

更进一步，关系建模模块通过...机制建模...。
```

## 输出格式

生成内容包含：
- 章节标题
- 正文（符合风格）
- 图表占位符 [图X]、[表X]
- 参考文献占位 [1]、[2]

用户需填充：真实实验数据、文献引用、个人见解。

## 学术提醒

- 仅学习写作风格，不复制具体内容
- 生成内容基于用户自己的研究
- 建议使用查重工具验证原创性
"""
        return template

    def _format_connectors(self, connectors: dict) -> str:
        """格式化连接词"""
        result = []
        for category in ["causal", "transitional", "progressive"]:
            words = connectors.get(category, [])
            if words:
                result.extend(words[:2])
        return "、".join(result)

    def _get_advisor_id(self) -> str:
        """获取导师ID"""
        return self.advisor.replace(" ", "").replace("教授", "").replace("老师", "")[:3]


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_skill.py <style_model.json> [output_dir]")
        sys.exit(1)

    model_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "."

    with open(model_path, "r", encoding="utf-8") as f:
        style_model = json.load(f)

    generator = SkillGenerator(style_model)
    result = generator.generate(output_dir)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
