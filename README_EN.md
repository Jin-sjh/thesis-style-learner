# thesis-style-learner

[简体中文](README.md) | English

Thesis Style Distiller and Content Generator. Learn writing style from previous graduate theses recommended by your advisor, and generate new content with consistent style.

## How to Trigger

Automatically triggered when user needs to generate thesis content. Trigger keywords:
- "imitate the writing style" / "模仿风格写作"
- "generate content in same style as advisor's thesis"
- "extract writing style from this paper"
- "write XX chapter in this paper's format"

## Features

- **Multi-Paper Style Fusion** - Extract common style features from multiple papers
- **Advisor Preference Recognition** - Identify advisor's expression preferences
- **Deep Style Modeling** - Model sentences, connectors, paragraphs, argumentation
- **6-Dimension Style Analysis** - Sentence structure, paragraph logic, academic tone, terminology, format, chapter paradigms
- **Style Consistency Check** - 5-dimension scoring for style consistency
- **Dedicated Skill Generation** - Generate standalone skill for specific advisor

## Directory Structure

```
thesis-style-learner/
├── SKILL.md                    # Main skill file (Claude Code)
├── README.md                   # Chinese README
├── README_EN.md              # English README
├── LICENSE                  # MIT License
├── .gitignore             # Git ignore config
├── references/
│   ├── style-analysis-prompts.md  # Style analysis prompt templates
│   └── chapter-templates.md      # Chapter writing frame templates
```

## Quick Start

### Requirements

- Python 3.8+

### Workflow

1. User provides previous graduate theses (supports txt, pdf, docx)
2. System analyzes style features (6 dimensions)
3. Builds style profile
4. Generates thesis content with consistent style

### Core Principles

1. **Learn Style, Not Content** - Extract writing patterns, never copy original text
2. **Complete Style Profile** - Analyze 6 dimensions (sentence, paragraph, tone, terminology, format, chapter paradigm)
3. **Actionable Output** - Generated content directly usable for academic writing
4. **Large File Strategy** - Use layered reading for PDF to avoid token limits

## 6-Dimension Style Analysis

| Dimension | Description |
|-----------|-------------|
| Sentence Structure | Avg sentence length, active/passive voice, connector usage |
| Paragraph Logic | Topic sentence position, support style, development pattern |
| Academic Tone | Self-reference, emphasis phrases, conclusion language |
| Terminology Habits | Abbreviation handling, citation format, technical terms |
| Chapter Format | Title hierarchy, figure/table numbering, summary sections |
| Chapter Paradigm | Chapter opening-middle-ending templates |

## Style Profile Output

```
📄 Style Profile
【Sentence Style】...
【Paragraph Logic】...
【Academic Tone】...
【Terminology Habits】...
【Format Standards】...
【Chapter Paradigm】 Abstract/Intro/Related Work/Experiment/Conclusion templates
【Typical Expression Patterns】 Reusable sentence frames
```

## Collaboration with cn-master-thesis

Recommended workflow:

1. **thesis-style-learner** - Learn style, generate content
2. **cn-master-thesis** - Format compliance, ensure school requirements
3. **Combined Use** - Style + Format double guarantee

## Academic Integrity Reminder

- This skill learns writing style patterns, not specific content
- Generated content must be based on user's own research
- Use plagiarism checker to verify originality
- Important sections should be substantially modified
- Consult advisor if in doubt
- Do not generate fake experimental data (use placeholder if data not provided)
- Reference format templates provided, user responsible for accuracy

## Reference Files

- `references/style-analysis-prompts.md` - Detailed prompt templates for each dimension
- `references/chapter-templates.md` - Common chapter writing frame templates

## License

MIT License - See [LICENSE](LICENSE) file

## Contributing

Issues and Pull Requests are welcome!