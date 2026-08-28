# 🤖 Daily Problem Solver

> AI-powered system that automatically finds real-world problems and generates full-stack solutions every day.

## What It Does

Every day at 12:00 AM BDT, this system:

1. **Scrapes** trending problems from Reddit, Hacker News, Google Trends, and Twitter
2. **Extracts** real problems people are facing
3. **Checks** uniqueness against previously solved problems
4. **Generates** a complete full-stack solution using AI agents
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
│   ├── solver.py          # AI solution generator
│   └── doc_generator.py   # Auto-generates docs
├── solutions/
│   └── YYYY-MM-DD/        # Daily solutions
│       ├── README.md
│       ├── PROBLEM.md
│       ├── frontend/      # Next.js
│       ├── backend/       # Python FastAPI
│       └── docs/
├── data/
│   └── solved_problems.json
├── main.py                # Main orchestrator
└── requirements.txt
```

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Next.js (React) |
| Backend | Python (FastAPI) |
| AI Model | Ollama + Llama 3.2 |
| Workflow | GitHub Actions |
| Scraping | Reddit, HN, Google Trends, Twitter |

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
| Reddit | Programming discussions, pain points |
| Hacker News | Tech problems, startup ideas |
| Google Trends | Trending search topics |
| Twitter | Real-time complaints & needs |

### AI Agent System

```
┌─────────────────────────────────────────────┐
│              AI Agent Pipeline               │
├─────────────────────────────────────────────┤
│                                             │
│  Problem ──→ Analyzer ──→ Coder ──→ Docs    │
│                                             │
│  All running locally via Ollama             │
│  100% free, no API keys needed             │
│                                             │
└─────────────────────────────────────────────┘
```

### Deduplication

Uses a hybrid approach:
- **Text Similarity:** TF-IDF vector comparison
- **Keyword Overlap:** Custom keyword matching
- **AI Check:** Local LLM confirms uniqueness

## 📊 Daily Commit Structure

Each day creates:

```
solutions/2026-08-28/
├── README.md           # Complete documentation
├── PROBLEM.md          # Problem description
├── metadata.json       # Structured data
├── frontend/           # Next.js app
├── backend/            # Python API
└── docs/               # Architecture docs
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
      "type": "fullstack"
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

Edit `scripts/solver.py`:

```python
# Use different model
response = ollama.chat(
    model="mistral",  # Change model
    messages=[...]
)
```

### Modify Solution Type

Edit `scripts/extractor.py` to add new categories.

## 💡 Tips

1. **Run manually first** to test: `python main.py`
2. **Check GitHub Actions** for workflow status
3. **Monitor data/solved_problems.json** for history
4. **Customize scraping sources** based on your interests


## 🙏 Acknowledgments

- Built to maintain GitHub activity streak
- Powered by local AI (Ollama)
- Uses free APIs from Reddit, Hacker News, and Google Trends

