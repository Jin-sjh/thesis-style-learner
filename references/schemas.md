# 风格模型 schemas

## 风格分析输入 (style_analysis_input.json)

```json
{
  "papers": [
    {
      "file_path": "path/to/paper1.txt",
      "author": "学生姓名",
      "year": 2023,
      "sections": {
        "abstract_cn": "摘要内容...",
        "abstract_en": "Abstract content...",
        "introduction": "引言内容...",
        "related_work": "相关工作内容...",
        "method": "方法章节内容...",
        "experiment": "实验章节内容...",
        "conclusion": "结论内容..."
      }
    }
  ],
  "advisor": "导师姓名"
}
```

## 风格模型输出 (style_model.json)

```json
{
  "version": "1.0",
  "created_at": "2024-01-01T00:00:00Z",
  "source_papers": ["paper1", "paper2"],
  "advisor": "导师姓名",
  "features": {
    "sentence": {
      "avg_length": 35,
      "length_distribution": {
        "short_min": 10,
        "short_max": 25,
        "short_ratio": 0.2,
        "medium_min": 25,
        "medium_max": 50,
        "medium_ratio": 0.6,
        "long_min": 50,
        "long_max": 80,
        "long_ratio": 0.2
      },
      "connectors": {
        "causal": ["因此", "由此可见", "因而", "所以"],
        "transitional": ["然而", "但是", "不过", "尽管如此"],
        "progressive": ["更进一步", "此外", "并且", "同时"],
        "conclusive": ["综上所述", "总之", "总而言之"],
        "exemplary": ["例如", "以...为例", "诸如"]
      }
    },
    "paragraph": {
      "avg_length": 200,
      "min_length": 100,
      "max_length": 400,
      "opening_patterns": {
        "topic_sentence": 0.5,
        "background_intro": 0.2,
        "question引导": 0.1,
        "contrast_intro": 0.15,
        "citation_intro": 0.05
      },
      "topic_sentence_position": "段首",
      "transition_sentence_usage": "常用"
    },
    "argumentation": {
      "patterns": {
        "total_distribution": 0.35,
        "cause_effect": 0.25,
        "contrast": 0.2,
        "progressive": 0.15,
        "problem_solution": 0.05
      },
      "preferred_pattern": "总-分-总"
    },
    "terminology": {
      "intro_style": "定义式",
      "abbreviation_style": "首次全称加缩写",
      "citation_style": "序号引用"
    },
    "citation": {
      "reference_format": "gb7714",
      "in_text_format": "上标",
      "multi_citation_style": "[1,2]",
      "range_style": "[1-3]",
      "punctuation": {
        "author_separator": "和",
        "title_format": "《》",
        "journal_format": "《》",
        "year_position": "末尾"
      },
      "abbreviation_rules": {
        "single_author": "姓",
        "multi_author": "姓等",
        "et_al_threshold": 3
      }
    },
    "tone": {
      "formality": "非常正式",
      "voice": "被动语态为主",
      "certainty": {
        "definite": 0.4,
        "probable": 0.4,
        "possible": 0.2
      },
      "humble_expressions": ["本研究", "本文", "本文方法"]
    },
    "chapter_patterns": {
      "abstract": {
        "structure": "背景-问题-方法-结果-结论",
        "keywords_count": 5,
        "length_range": [300, 500]
      },
      "introduction": {
        "structure": "宏观背景 → 具体问题 → 研究意义",
        "literature_review_style": "分类评述",
        "word_count": [4000, 6000]
      },
      "related_work": {
        "organization": "按方法分类",
        "description_depth": "中等",
        "critique_style": "客观评述"
      },
      "method": {
        "description_order": "整体到局部",
        "formula_usage": "常用",
        "algorithm_detail": "详细"
      },
      "experiment": {
        "datasets_intro": "按重要性排序",
        "comparison_style": "多基线对比",
        "analysis_depth": "深入分析"
      },
      "conclusion": {
        "structure": "贡献-局限-展望",
        "contribution_count": 3,
        "future_scope": "具体"
      }
    }
  },
  "advisor_preferences": {
    "strong": [
      "句子长度在30-50字区间",
      "使用因果连接词：因此、由此可见",
      "段落主题句在段首"
    ],
    "medium": [
      "使用递进连接词：此外、更进一步",
      "采用总-分-总论证结构"
    ],
    "weak": []
  }
}
```

## 内容生成输入 (generation_input.json)

```json
{
  "style_model": {},
  "generation_request": {
    "chapter": "第三章 研究方法",
    "section": "3.1 总体框架",
    "topic": "基于深度学习的遥感影像分类方法",
    "key_elements": {
      "model_name": "RSNet",
      "backbone": "ResNet50",
      "module": "注意力机制"
    },
    "word_count": 1500,
    "must_include": ["图3.1", "公式3.1", "算法1"]
  }
}
```

## 风格检验输出 (style_check.json)

```json
{
  "consistency_score": 42,
  "max_score": 50,
  "passed": true,
  "dimensions": {
    "sentence_length": {
      "score": 8,
      "details": "85%的句子在30-50字区间"
    },
    "connectors": {
      "score": 9,
      "details": "使用了因果连接词：因此、由此可见"
    },
    "paragraph_opening": {
      "score": 8,
      "details": "60%使用主题句开头"
    },
    "argumentation": {
      "score": 9,
      "details": "采用总-分-总结构"
    },
    "terminology": {
      "score": 8,
      "details": "术语引入方式符合习惯"
    }
  },
  "warnings": [],
  "suggestions": [
    "建议增加对比论证的使用"
  ]
}
```

## 偏好强度定义

| 强度 | 覆盖率 | 要求 |
|------|--------|------|
| 强偏好 | ≥80%论文 | 必须遵循 |
| 中偏好 | 50-80%论文 | 尽量遵循 |
| 弱偏好 | <50%论文 | 参考学习 |