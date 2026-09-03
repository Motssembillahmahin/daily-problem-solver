# 🤖 Daily Problem Solver

> System that automatically finds real-world problems and ships a matching Python CLI solution from a curated template library every day - or ships nothing when no template fits.

## What It Does

Every day at 12:00 AM BDT, this system:

1. **Scrapes** real problems from Stack Overflow, Ask HN, GitHub issues, Hacker News, Reddit, and Google Trends
2. **Extracts** real problems people are facing
3. **Checks** uniqueness against previously solved problems
4. **Selects** a matching template from the library by keyword fit and generates its files - or skips the day if nothing fits well enough
5. **Pushes** everything to GitHub automatically

## 🎯 Goal

Maintain an active GitHub streak while building useful AI-powered solutions to real problems.

## 📁 Project Structure

```
daily-problem-solver/
├── .github/workflows/
│   └── daily.yml          # Automated daily workflow
├── scripts/
│   ├── scraper.py         # Scrapes multiple sources
│   ├── extractor.py       # Extracts problems
│   ├── dedup.py           # Deduplication (local AI)
│   ├── smart_solver.py    # Solution generator (template based)
│   ├── dates.py           # Pipeline date helpers (Asia/Dhaka)
│   └── doc_generator.py   # Auto-generates docs
├── solutions/
│   └── YYYY-MM-DD/        # Daily solutions (BDT date)
│       ├── README.md          # Usage docs for the generated tool
│       ├── PROBLEM.md         # Problem statement and provenance
│       ├── metadata.json
│       ├── <solution>.py      # The generated tool
│       ├── requirements.txt
│       └── docs/
│           └── SOLUTION.md    # How the problem was picked and solved
├── data/
│   └── solved_problems.json
├── tests/
├── main.py                # Main orchestrator
├── requirements.txt
└── requirements-dev.txt
```

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Next.js (React) |
| Backend | Python (FastAPI) |
| AI Model | Ollama + Llama 3.2 |
| Workflow | GitHub Actions |
| Scraping | Stack Overflow, Ask HN, GitHub issues, HN, Reddit, Google Trends |

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- Ollama

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/Motssembillahmahin/daily-problem-solver.git
cd daily-problem-solver

# 2. Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 3. Pull AI model
ollama pull llama3.2

# 4. Install Python dependencies
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 5. Run manually
python main.py
```

## 🤖 How It Works

### Scraping Sources

| Source | What It Captures |
|--------|------------------|
| Stack Overflow | Tagged questions - every item is a stated problem |
| Ask HN | Questions from HN with self-text |
| GitHub Issues | Reported bugs with discussion |
| Hacker News | Top stories (link posts rarely qualify as problems) |
| Reddit | Subreddit discussions (unreliable from CI; non-fatal) |
| Google Trends | Trending searches (low weight) |

Product announcements ("Show HN", "Launch HN", "Introducing") are rejected: they
describe something that was built, not a problem to solve. If no scraped problem
matches any template in the library, the run ships nothing rather than an unrelated
tool.

### Pipeline Stages

No LLM writes code in this pipeline. Each day's run moves through fixed,
deterministic stages:

1. **Scrape** - pull raw posts/questions/issues from the sources above
2. **Extract** - keep only items with real problem indicators and score them
3. **Deduplicate** - reject anything too similar to a previously solved problem
   (see below - this is the only stage that optionally uses a local LLM)
4. **Template fit** - score the problem against every template's keywords
5. **Generate or skip** - if a template clears the fit threshold, its files are
   written; otherwise the day ships nothing rather than an unrelated tool

### Deduplication

Uses a hybrid approach:
- **Text Similarity:** TF-IDF vector comparison
- **Keyword Overlap:** Custom keyword matching
- **AI Check:** Local LLM confirms uniqueness

## 📊 Daily Commit Structure

Each day creates:

```
solutions/2026-08-28/
├── README.md           # Usage docs for the generated tool
├── PROBLEM.md          # Problem description and provenance
├── metadata.json       # Structured data
├── <solution>.py       # The generated tool
├── requirements.txt    # Its dependencies
└── docs/
    └── SOLUTION.md     # How the problem was picked and solved
```

## ⚙️ Configuration

### Environment Variables

Create `.env` file:

```bash
# GitHub (for pushing)
GITHUB_TOKEN=your_token_here

# Reddit (optional, for higher limits)
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret

# AI Model (optional)
OLLAMA_MODEL=llama3.2
```

### GitHub Secrets

Add to repository Settings → Secrets:

| Secret | Description |
|--------|-------------|
| `GITHUB_TOKEN` | Already provided by GitHub |

## 🕐 Schedule

- **Time:** 12:00 AM BDT (18:00 UTC)
- **Frequency:** Daily
- **Manual Trigger:** Available via GitHub Actions

## 📈 Tracking Progress

The system maintains `data/solved_problems.json`:

```json
{
  "problems": [
    {
      "date": "2026-08-28",
      "title": "AI File Organizer",
      "keywords": ["files", "organize", "automation"],
      "type": "file_organizer"
    }
  ]
}
```

## 🔧 Customization

### Add New Scraping Source

Edit `scripts/scraper.py`:

```python
def scrape_my_source():
    # Your scraping logic
    return posts
```

### Change AI Model

Ollama is used only for the optional deduplication check. Edit
`scripts/dedup.py`:

```python
# Use different model
response = ollama.chat(
    model="mistral",  # Change model
    messages=[...]
)
```

### Add a Solution Type

Solutions come from templates in `scripts/smart_solver.py`. Add a generator
method, register it in `SolutionGenerator.solution_templates`, and add its
keywords to `SolutionGenerator.TEMPLATE_KEYWORDS`.

### Add a Problem Category

Edit `CATEGORIES` in `scripts/extractor.py`.

## 💡 Tips

1. **Run manually first** to test: `python main.py`
2. **Check GitHub Actions** for workflow status
3. **Monitor data/solved_problems.json** for history
4. **Customize scraping sources** based on your interests


## 🙏 Acknowledgments

- Built to maintain GitHub activity streak
- Deduplication optionally checked by local AI (Ollama)
- Uses free APIs from Stack Overflow, Ask HN, GitHub Issues, Hacker News,
  Reddit, and Google Trends

