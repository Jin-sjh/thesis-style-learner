# thesis-style-learner

[简体中文](README.md) | English

Thesis Style Distiller and Content Generator. Learn writing style from previous graduate theses recommended by your advisor, and generate new content with consistent style.

## Features

- **Multi-Paper Style Fusion** - Extract common style features from multiple papers
- **Advisor Preference Recognition** - Identify advisor's expression preferences
- **Deep Style Modeling** - Model sentences, connectors, paragraphs, argumentation
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
├── agents/
│   └── grading.md        # Style grading agent
├── references/
│   └── schemas.md       # Data structure definitions
└── scripts/
    ├── __init__.py
    ├── analyze_style.py    # Style analysis script
    ├── check_style.py      # Style check script
    ├── generate_content.py # Content generation script
    └── generate_skill.py    # Dedicated skill generation script
```

## Quick Start

### Requirements

- Python 3.8+

### Installation

```bash
git clone https://github.com/yourusername/thesis-style-learner.git
cd thesis-style-learner
```

### Usage

#### 1. Analyze Paper Style

```bash
python scripts/analyze_style.py path/to/paper.txt
```

#### 2. Check Style Consistency

```bash
python scripts/check_style.py style_model.json generated_text.txt
```

#### 3. Generate Dedicated Skill

```bash
python scripts/generate_skill.py style_model.json output_dir/
```

## Usage in Claude Code

### Install Skill

1. Copy the entire folder to Claude Code's Skills directory:
   ```
   C:/Users/<username>/.claude/skills/thesis-style-learner/
   ```

2. Restart Claude Code

### How to Trigger

Automatically triggered when user needs to generate thesis content.

### Workflow

1. Provide previous graduate theses (supports txt, pdf, docx)
2. System analyzes style features
3. Builds style model
4. Generates thesis content with consistent style

## Scoring Standard

Style consistency scoring (max 50 points):

| Dimension | Score | Description |
|-----------|-------|------------|
| Sentence Length | /10 | Model matching |
| Connector Usage | /10 | Preference vocabulary coverage |
| Paragraph Opening | /10 | Pattern matching |
| Argumentation | /10 | Structure matching |
| Terminology | /10 | Habit matching |

Total ≥ 40/50 = style consistent

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

## License

MIT License - See [LICENSE](LICENSE) file

## Contributing

Issues and Pull Requests are welcome!