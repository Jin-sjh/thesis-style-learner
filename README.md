# thesis-style-learner

简体中文 | [English](README_EN.md)

毕业论文风格蒸馏与内容生成助手。从导师推荐的往届优秀毕业论文中学习写作风格，并生成风格一致的新内容。

## 功能特性

- **多论文风格融合** - 从多篇论文中提取共同风格特征
- **导师偏好识别** - 识别导师偏好的表达习惯
- **深度风格建模** - 句式、连接词、段落、论证全面建模
- **风格一致性检验** - 5维度评分确保生成内容风格一致
- **专属Skill生成** - 可生成独立使用的专属风格Skill

## 目录结构

```
thesis-style-learner/
├── SKILL.md                    # 主技能文件 (Claude Code)
├── README.md                   # 本文件
├── LICENSE                    # MIT许可证
├── .gitignore                # Git忽略配置
├── agents/
│   └── grading.md           # 风格评分代理
├── references/
│   └── schemas.md           # 数据结构定义
└── scripts/
    ├── __init__.py
    ├── analyze_style.py    # 风格分析脚本
    ├── check_style.py      # 风格检验脚本
    ├── generate_content.py # 内容生成脚本
    └── generate_skill.py    # 专属Skill生成脚本
```

## 快速开始

### 环境要求

- Python 3.8+

### 安装

```bash
git clone https://github.com/yourusername/thesis-style-learner.git
cd thesis-style-learner
```

### 使用方法

#### 1. 分析论文风格

```bash
python scripts/analyze_style.py path/to/paper.txt
```

#### 2. 检验生成内容的风格一致性

```bash
python scripts/check_style.py style_model.json generated_text.txt
```

#### 3. 生成专属Skill

```bash
python scripts/generate_skill.py style_model.json output_dir/
```

## 在 Claude Code 中使用

### 安装 Skill

1. 将整个文件夹复制到 Claude Code 的 Skills 目录：
   ```
   C:/Users/<username>/.claude/skills/thesis-style-learner/
   ```

2. 重启 Claude Code

### 触发方式

当用户需要生成毕业论文内容时自动触发。

### 使用流程

1. 提供往届学生的毕业论文（支持 txt、pdf、docx 格式）
2. 系统自动分析风格特征
3. 构建风格模型
4. 生成符合风格的论文内容

## 评分标准

风格一致性评分（满分50分）：

| 维度 | 分数 | 说明 |
|------|------|------|
| 句式长度 | /10 | 与模型匹配度 |
| 连接词使用 | /10 | 偏好词汇覆盖率 |
| 段落开头 | /10 | 模式匹配度 |
| 论证逻辑 | /10 | 结构匹配度 |
| 术语表述 | /10 | 习惯匹配度 |

总分 ≥ 40/50 视为风格一致

## 与 cn-master-thesis 协同

推荐工作流程：

1. **thesis-style-learner** - 学习风格，生成内容
2. **cn-master-thesis** - 规范格式，确保符合学校要求
3. **结合使用** - 风格+格式双保险

## 学术诚信提醒

- 本技能学习的是写作风格模式，不是具体内容
- 生成的内容必须基于用户自己的研究成果
- 建议使用查重工具验证原创性
- 重要章节建议在生成基础上大幅修改
- 如有疑虑，咨询导师或学术诚信部门

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 贡献

欢迎提交 Issue 和 Pull Request！"# thesis-style-learner" 
