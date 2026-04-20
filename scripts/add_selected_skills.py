#!/usr/bin/env python3
"""
从精选候选中创建 SKILL.md 文件并写入仓库
手工精选的高质量 skills，按分类分组
"""
import json
import os
import re
from pathlib import Path

REPO_ROOT = Path("d:/pyworkplace/github/learning-open-source")
ALL_SKILLS_DIR = REPO_ROOT / "all-skills" / "skills"

# =========================================================
# 手工精选：每个 skill 包含 slug、分类、中文名、描述、SKILL.md 内容
# 覆盖 8 个领域，共 30 个高质量 skill
# =========================================================
SELECTED_SKILLS = [

    # ===== 搜索 & 研究工具 =====
    {
        "slug": "tavily-search",
        "category": "superpowers",
        "zh_name": "Tavily 智能搜索",
        "description": "Tavily AI 搜索引擎集成，专为 AI Agent 优化，支持实时网页搜索、摘要提取和来源引用。",
        "content": """# Tavily Search

Use this skill when the agent needs to **search the web with AI-optimized results** — real-time information, source citations, and clean summaries designed for LLM consumption.

## When to Use

- User asks for up-to-date facts, news, or recent events
- Need to verify claims or find current data
- Research tasks requiring multiple sources
- Any question where training data may be outdated

## How to Use

```
Search for: [your query]
Source: Tavily API
```

Tavily is purpose-built for AI agents — it returns structured results with:
- **Answer**: Direct answer to the query
- **Sources**: Cited URLs with relevance scores
- **Raw content**: Full page text for deep analysis

## Setup

```bash
export TAVILY_API_KEY=your_key_here
```

Get your key at: https://tavily.com

## Best Practices

1. Use specific queries — "Python 3.12 new features 2024" beats "Python features"
2. Set `search_depth=advanced` for research tasks
3. Use `include_domains` to restrict to trusted sources
4. Chain multiple searches for comprehensive research

## Example Queries

- `"latest GPT-4o capabilities 2025"`
- `"React 19 breaking changes"`
- `"competitor analysis [company name] 2025"`
"""
    },
    {
        "slug": "web-search-pro",
        "category": "superpowers",
        "zh_name": "专业网页搜索",
        "description": "多引擎聚合网页搜索技能，支持 DuckDuckGo/Bing/Google，无需 API key 即可使用，适合快速信息检索。",
        "content": """# Web Search Pro

Multi-engine web search skill. Use when you need **fast, free web search** without API keys — falls back across DuckDuckGo → Bing → Google automatically.

## When to Use

- Quick factual lookups
- Finding documentation, GitHub repos, or articles
- No Tavily API key available
- Broad topic exploration

## Engines Supported

| Engine | API Key Required | Notes |
|--------|-----------------|-------|
| DuckDuckGo | No | Default, privacy-focused |
| Bing | No (limited) | Good for recent news |
| Google | Yes (Custom Search) | Most comprehensive |

## Usage

```
Search: [query]
Engine: duckduckgo | bing | google
Max results: 5-20
```

## Tips

- Wrap multi-word queries in quotes for exact matches: `"sprint planning template"`
- Use `-term` to exclude: `python tutorial -beginner`
- Use `site:github.com` to search specific domains
- For code: add `site:stackoverflow.com` or `site:github.com`

## Output Format

Returns structured results:
```json
{
  "results": [
    {"title": "...", "url": "...", "snippet": "...", "score": 0.9}
  ]
}
```
"""
    },
    {
        "slug": "deep-research",
        "category": "superpowers",
        "zh_name": "深度研究助手",
        "description": "自动化深度研究工具，针对任意主题进行多轮搜索、信息聚合、去重和结构化报告生成。",
        "content": """# Deep Research

Automated deep research skill. Use when you need **comprehensive, multi-source research** on any topic — goes beyond a single search to synthesize knowledge from dozens of sources.

## When to Use

- Market research and competitive analysis
- Technical deep-dives (architecture choices, library comparisons)
- Academic or professional research reports
- Due diligence on companies, technologies, or people

## Process

```
1. Query Decomposition  → Break topic into 5-10 sub-questions
2. Parallel Search      → Search each sub-question across multiple engines
3. Content Extraction   → Scrape and clean full page content
4. Deduplication        → Remove overlapping information
5. Synthesis            → Merge findings into coherent narrative
6. Citation             → Track all sources with relevance scores
7. Report Generation    → Structured markdown report
```

## Usage

```
Research: [topic]
Depth: quick (5 min) | standard (15 min) | thorough (30 min)
Format: executive summary | full report | bullet points
```

## Output Structure

```markdown
# Research Report: [Topic]

## Executive Summary
[2-3 paragraph overview]

## Key Findings
### Finding 1: [Title]
[Details with citations]

## Sources
[Numbered source list]
```

## Tips

- Be specific: "React vs Vue for enterprise SaaS 2025" > "frontend frameworks"
- Use `depth=thorough` for high-stakes decisions
- Specify output format based on audience
"""
    },

    # ===== 开发工具 =====
    {
        "slug": "github-api",
        "category": "dev-workflow",
        "zh_name": "GitHub API 集成",
        "description": "完整的 GitHub API 集成技能，支持 Issues、PR、仓库管理、搜索和 GitHub Actions 操作。",
        "content": """# GitHub API

Full GitHub API integration skill. Use for **managing repos, issues, PRs, and workflows** programmatically.

## When to Use

- Create, update, or close GitHub issues
- Review and merge pull requests
- Search repositories or code
- Trigger or monitor GitHub Actions
- Manage releases and tags
- Bulk operations across repos

## Key Operations

### Issues
```python
# Create issue
POST /repos/{owner}/{repo}/issues
{
  "title": "Bug: ...",
  "body": "Description...",
  "labels": ["bug", "high-priority"]
}

# List open issues
GET /repos/{owner}/{repo}/issues?state=open&sort=created
```

### Pull Requests
```python
# List PRs awaiting review
GET /repos/{owner}/{repo}/pulls?state=open

# Merge PR
PUT /repos/{owner}/{repo}/pulls/{pull_number}/merge
{"merge_method": "squash"}
```

### Code Search
```python
# Search code across GitHub
GET /search/code?q=function+repo:{owner}/{repo}

# Search issues
GET /search/issues?q=is:issue+is:open+label:bug+repo:{owner}/{repo}
```

## Setup

```bash
export GITHUB_TOKEN=ghp_your_token_here
```

Scopes needed: `repo`, `read:org` (for org repos)

## Best Practices

1. Use `per_page=100` to reduce API calls
2. Cache responses — GitHub has rate limits (5000 req/hour with auth)
3. Use `If-None-Match` header with ETags for conditional requests
4. For bulk ops, use GraphQL API — 1 call vs many REST calls
"""
    },
    {
        "slug": "git-commit-automation",
        "category": "dev-workflow",
        "zh_name": "Git 提交自动化",
        "description": "智能 Git 提交助手，自动分析代码变更、生成规范的 Conventional Commits 提交消息并执行提交。",
        "content": """# Git Commit Automation

Intelligent git commit skill. Use to **automatically generate conventional commit messages** from staged changes.

## When to Use

- After making code changes, need a clean commit message
- Enforcing conventional commits across team
- Generating changelogs from commit history
- Code review automation

## Conventional Commits Format

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types
| Type | When to Use |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no logic change |
| `refactor` | Code restructure, no behavior change |
| `perf` | Performance improvement |
| `test` | Adding tests |
| `chore` | Build process, dependencies |
| `ci` | CI/CD changes |

## Auto-Generation Process

```
1. Run: git diff --staged
2. Analyze: changed files, function names, added/removed lines
3. Classify: determine commit type from changes
4. Generate: craft message following conventional commits spec
5. Confirm: show message for approval before committing
6. Commit: git commit -m "generated message"
```

## Example Output

```bash
# Input: staged changes to auth middleware
feat(auth): add JWT refresh token support

Implements sliding session tokens with configurable expiry.
Token refresh endpoint: POST /api/auth/refresh

Closes #234
```

## Integration

Works with: husky, commitlint, semantic-release, changelogithub
"""
    },
    {
        "slug": "copilot-cli",
        "category": "dev-workflow",
        "zh_name": "Copilot CLI 代码分析",
        "description": "通过 GitHub Copilot CLI 分析代码、探索项目结构、生成文档和自动化开发任务，提高开发效率。",
        "content": """# Copilot CLI

Code analysis and automation via GitHub Copilot CLI. Use for **AI-assisted code exploration, documentation generation, and dev task automation**.

## When to Use

- Understand unfamiliar codebases quickly
- Generate README or API docs from code
- Find bugs or security issues via AI review
- Automate repetitive dev tasks with AI suggestions

## Core Commands

### Code Explanation
```bash
# Explain what a file does
gh copilot explain "$(cat src/auth/middleware.py)"

# Explain a git diff
git diff HEAD~1 | gh copilot explain
```

### Command Suggestions
```bash
# Get shell command suggestions
gh copilot suggest "find all TODO comments in Python files"
# → find . -name "*.py" -exec grep -n "TODO" {} +

gh copilot suggest "docker command to clean up stopped containers"
# → docker container prune -f
```

### Code Review
```bash
# Review staged changes
git diff --staged | gh copilot explain --target=review
```

## Workflow Integration

```yaml
# .github/workflows/ai-review.yml
- name: AI Code Review
  run: |
    git diff ${{ github.base_ref }}..HEAD > changes.diff
    gh copilot explain < changes.diff
```

## Best Practices

1. Pipe specific files, not entire repos
2. Ask for explanations before asking for fixes
3. Use `--target=shell` for CLI help, `--target=git` for git ops
4. Verify all AI suggestions before executing
"""
    },
    {
        "slug": "security-audit-toolkit",
        "category": "dev-workflow",
        "zh_name": "安全审计工具包",
        "description": "代码安全审计工具，自动扫描 SQL 注入、XSS、硬编码密钥、不安全依赖等常见安全漏洞。",
        "content": """# Security Audit Toolkit

Code security audit skill. Use to **scan codebases for vulnerabilities** — SQL injection, XSS, hardcoded secrets, insecure deps, and OWASP Top 10.

## When to Use

- Pre-release security review
- Pull request security checks
- Onboarding to legacy codebase
- Compliance audits (SOC2, ISO 27001)

## Vulnerability Categories

### OWASP Top 10 Coverage
| Vuln | Detection Method |
|------|-----------------|
| SQL Injection | Pattern matching + AST analysis |
| XSS | Template/HTML output analysis |
| Broken Auth | JWT/session config review |
| Sensitive Data | Regex for keys, passwords, tokens |
| XXE | XML parser config check |
| Broken Access | Permission check coverage |
| Security Misconfig | Config file analysis |
| Insecure Deserialization | pickle/eval/exec detection |
| Outdated Components | dependency version audit |
| Insufficient Logging | log statement coverage |

## Tools Integration

```bash
# Python: bandit
bandit -r ./src -ll -f json

# JavaScript: npm audit
npm audit --json

# Secrets: truffleHog
trufflehog git file://. --json

# Dependencies: safety
safety check --json
```

## Output Format

```markdown
## Security Audit Report

### Critical (must fix before deploy)
- [SQLI-001] src/db/queries.py:45 - String concatenation in SQL query
  Fix: Use parameterized queries

### High
- [SECRET-003] config/settings.py:12 - Hardcoded API key
  Fix: Move to environment variable

### Summary
Critical: 1 | High: 3 | Medium: 7 | Low: 12
```
"""
    },
    {
        "slug": "web-deploy-github",
        "category": "dev-workflow",
        "zh_name": "GitHub Pages 部署",
        "description": "一键部署静态网站到 GitHub Pages，支持自定义域名、HTTPS 配置和自动化 CI/CD 流水线。",
        "content": """# Web Deploy GitHub Pages

Deploy static sites to GitHub Pages. Use for **quick, free hosting** of documentation, portfolio sites, or static web apps.

## When to Use

- Deploy React/Vue/Next.js static exports
- Host project documentation (Docusaurus, MkDocs)
- Personal portfolio or landing pages
- Demo deployments for PRs

## Quick Deploy

```bash
# Option 1: gh-pages package (Node.js)
npm install -D gh-pages
# package.json:
"scripts": {
  "deploy": "gh-pages -d dist"
}
npm run build && npm run deploy

# Option 2: GitHub Actions (recommended)
# See workflow below
```

## GitHub Actions Workflow

```yaml
# .github/workflows/deploy.yml
name: Deploy to GitHub Pages
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci && npm run build
      - uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./dist
```

## Custom Domain Setup

```
1. Add CNAME file to public/ folder:
   echo "yourdomain.com" > public/CNAME

2. DNS Settings (at your registrar):
   A     @    185.199.108.153
   A     @    185.199.109.153
   CNAME www  yourusername.github.io

3. Enable HTTPS in repo Settings > Pages
```
"""
    },
    {
        "slug": "n8n-workflow",
        "category": "dev-workflow",
        "zh_name": "n8n 工作流自动化",
        "description": "n8n 无代码工作流自动化集成，支持 400+ 应用连接，构建自动化流水线，替代 Zapier/Make。",
        "content": """# n8n Workflow Automation

n8n integration skill. Use to **build and manage automation workflows** connecting any apps without writing code — or with code when needed.

## When to Use

- Automate repetitive cross-app tasks
- Webhook-triggered workflows
- Data sync between tools (CRM, Slack, DB, etc.)
- Scheduled jobs and cron tasks
- Replace Zapier/Make with self-hosted solution

## Core Concepts

```
Trigger → Nodes → Actions
```

### Node Types
| Type | Examples |
|------|---------|
| Triggers | Webhook, Cron, Email, GitHub |
| Apps | Slack, Notion, Jira, GitHub, Gmail |
| Logic | IF, Switch, Merge, Loop |
| Data | JSON, Code, Set, Filter |
| AI | OpenAI, Anthropic, LangChain |

## Common Workflows

### Slack → GitHub Issue
```json
{
  "trigger": "Slack message with /bug command",
  "steps": [
    "Parse command arguments",
    "Create GitHub issue via API",
    "Reply to Slack with issue link"
  ]
}
```

### Daily Report Generator
```json
{
  "trigger": "Cron: 0 9 * * 1-5",
  "steps": [
    "Fetch Jira open tickets",
    "Get GitHub PRs pending review",
    "Format as Markdown report",
    "Send to Slack #daily-standup"
  ]
}
```

## Self-Hosting

```bash
# Docker Compose
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v n8n_data:/home/node/.n8n \
  n8nio/n8n
```

Access at: http://localhost:5678
"""
    },
    {
        "slug": "sqlite-agent",
        "category": "dev-workflow",
        "zh_name": "SQLite 数据分析助手",
        "description": "SQLite 数据库操作技能，支持自然语言转 SQL 查询、数据分析、表结构探索和结果可视化。",
        "content": """# SQLite Agent

Natural language SQLite interface. Use to **query and analyze SQLite databases** using plain language — no SQL knowledge required.

## When to Use

- Explore an unknown database schema
- Answer data questions without writing SQL
- Generate reports from local data
- Debug data issues

## Natural Language → SQL

```
User: "Show me the top 10 customers by total order value last month"

→ SQL:
SELECT c.name, SUM(o.amount) as total
FROM customers c
JOIN orders o ON c.id = o.customer_id
WHERE o.created_at >= date('now', '-1 month')
GROUP BY c.id
ORDER BY total DESC
LIMIT 10
```

## Schema Exploration

```python
# Auto-discover tables and columns
import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# List tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

# For each table, get schema
for table in tables:
    cursor.execute(f"PRAGMA table_info({table[0]})")
    columns = cursor.fetchall()
```

## Supported Operations

- `SELECT` with complex JOINs, aggregations, window functions
- `INSERT`, `UPDATE`, `DELETE` with confirmation prompts
- Schema analysis: `EXPLAIN QUERY PLAN`, index usage
- Export to CSV, JSON, Markdown tables
- Visual charts via matplotlib/plotly

## Safety Rules

1. Always show SQL before executing
2. Require confirmation for writes
3. Never DELETE without WHERE clause
4. Backup before schema changes
"""
    },

    # ===== AI / LLM 工具 =====
    {
        "slug": "prompt-optimizer",
        "category": "ai-product",
        "zh_name": "Prompt 优化器",
        "description": "分析和优化 AI Prompt，识别模糊表达、角色缺失、约束不足等问题，输出经过验证的高质量提示词。",
        "content": """# Prompt Optimizer

Prompt engineering skill. Use to **diagnose and improve AI prompts** — transforms vague instructions into precise, effective prompts.

## When to Use

- Your prompt gives inconsistent results
- Output doesn't match expectations
- Preparing prompts for production use
- Teaching prompt engineering best practices

## Diagnosis Framework

### Common Issues
| Issue | Example | Fix |
|-------|---------|-----|
| Vague role | "You are helpful" | "You are a senior backend engineer specializing in Python and distributed systems" |
| Missing context | "Fix this bug" | "Fix this bug in our FastAPI auth middleware. We use JWT tokens, Python 3.11, and must maintain backward compatibility" |
| Unclear format | "Summarize this" | "Summarize in 3 bullet points, each under 20 words, for a non-technical executive audience" |
| No constraints | "Write code" | "Write Python code: PEP 8 compliant, with type hints, docstrings, and error handling" |
| Missing examples | "Extract dates" | Provide 3 examples with expected output |

## Optimization Process

```
1. ANALYZE  → Identify the core task and success criteria
2. ROLE     → Define expert persona with specific background
3. CONTEXT  → Add relevant constraints and environment
4. TASK     → Clarify exactly what to do (action verb)
5. FORMAT   → Specify output format, length, structure
6. EXAMPLES → Add few-shot examples if needed
7. VALIDATE → Test with edge cases
```

## Before / After

**Before:**
```
Summarize the meeting notes.
```

**After:**
```
You are an executive assistant. Summarize the following meeting notes into:
1. Decision made (1 sentence each)
2. Action items (owner + deadline format)
3. Open questions needing follow-up

Be concise. Use bullet points. Maximum 200 words total.

Meeting notes:
[NOTES]
```

## Prompt Templates

- System prompt template
- Chain-of-thought template
- Few-shot learning template
- JSON output template
- Code generation template
"""
    },
    {
        "slug": "rag-search",
        "category": "ai-product",
        "zh_name": "RAG 本地知识搜索",
        "description": "基于向量检索的本地知识库搜索技能，支持文档嵌入、语义搜索、混合检索和答案生成。",
        "content": """# RAG Search

Local knowledge base search via RAG (Retrieval-Augmented Generation). Use to **search and query your own documents** with semantic understanding.

## When to Use

- Q&A over internal documentation
- Search across large codebases or wikis
- Customer support from knowledge base
- Private data that can't go to cloud APIs

## Architecture

```
Documents → Chunking → Embedding → Vector Store
                                       ↓
Query → Embedding → Similarity Search → Context → LLM → Answer
```

## Setup

```python
# 1. Install dependencies
pip install langchain chromadb sentence-transformers

# 2. Index documents
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

loader = DirectoryLoader('./docs', glob="**/*.md")
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_db")
```

## Hybrid Search

```python
# Combine semantic + keyword search
from langchain.retrievers import EnsembleRetriever
from langchain.retrievers import BM25Retriever

bm25 = BM25Retriever.from_documents(chunks)
semantic = vectorstore.as_retriever(search_kwargs={"k": 5})

hybrid = EnsembleRetriever(
    retrievers=[bm25, semantic],
    weights=[0.3, 0.7]
)
```

## Best Practices

1. Chunk size: 200-500 tokens for factual Q&A, 500-1000 for synthesis
2. Overlap: 10-20% to avoid cutting mid-sentence
3. Metadata filtering: tag docs by type, date, source
4. Reranking: use cross-encoder to rerank top-20 → top-5
"""
    },
    {
        "slug": "ai-code-review",
        "category": "ai-product",
        "zh_name": "AI 代码审查",
        "description": "AI 驱动的代码审查技能，自动检测代码质量、性能瓶颈、安全漏洞和架构问题，给出可执行的改进建议。",
        "content": """# AI Code Review

AI-powered code review skill. Use to **get deep, actionable code reviews** covering quality, performance, security, and architecture.

## When to Use

- Pre-merge code review
- Onboarding review of legacy code
- Personal learning and improvement
- Checking AI-generated code before shipping

## Review Dimensions

### 1. Correctness
- Logic errors and edge cases
- Null pointer / undefined access
- Off-by-one errors
- Race conditions (async code)

### 2. Performance
- O(n²) algorithms that should be O(n log n)
- Unnecessary database queries in loops (N+1)
- Memory leaks
- Missing caching opportunities

### 3. Security
- SQL injection, XSS vulnerabilities
- Hardcoded secrets
- Insecure direct object reference
- Missing input validation

### 4. Maintainability
- Function length > 50 lines
- Duplicate code (DRY violations)
- Missing error handling
- Unclear variable names

## Review Format

```markdown
## Code Review: [filename]

### Summary
[2-sentence overall assessment]

### Issues Found

#### 🔴 Critical: SQL Injection Risk
**Line 47:** `query = f"SELECT * FROM users WHERE id = {user_id}"`
**Fix:** Use parameterized query:
```python
query = "SELECT * FROM users WHERE id = ?"
cursor.execute(query, (user_id,))
```

#### 🟡 Performance: N+1 Query
**Lines 23-31:** Loading user's posts in a loop
**Fix:** Use `prefetch_related` or single JOIN query

### Positive Patterns
- ✅ Good use of type hints throughout
- ✅ Error handling is comprehensive
```

## Usage

```
Review the following code for: [correctness | performance | security | all]
Focus on: [specific concern]
Context: [language, framework, deployment environment]

[paste code]
```
"""
    },

    # ===== 数据分析 =====
    {
        "slug": "bilibili-analytics",
        "category": "superpowers",
        "zh_name": "B站数据分析",
        "description": "Bilibili 视频搜索与数据分析，抓取关键词搜索结果，生成统计报告，支持多页抓取和可视化。",
        "content": """# Bilibili Analytics

Bilibili (B站) video analytics skill. Use to **research content trends, analyze creator performance**, and gather competitive intelligence on Chinese video platforms.

## When to Use

- Content strategy research for Chinese market
- Competitor analysis on B站
- Trending topic discovery
- Influencer research and outreach

## Key Metrics

| Metric | Chinese | Description |
|--------|---------|-------------|
| 播放量 | plays | View count |
| 弹幕数 | danmaku | Bullet comment count |
| 点赞数 | likes | Like count |
| 投币数 | coins | Coin count (deeper engagement) |
| 收藏数 | favorites | Bookmark count |
| 分享数 | shares | Share count |

## Engagement Score Formula

```python
# Weighted engagement score
score = (
    plays * 0.1 +
    danmaku * 3 +
    likes * 2 +
    coins * 4 +
    favorites * 3 +
    shares * 5
) / plays * 100
```

## Usage Pattern

```
Analyze: [keyword / channel / video]
Metrics: engagement | growth | trending
Time range: last 7 days | 30 days | 3 months
Output: summary | detailed report | CSV
```

## Data Sources

- B站搜索 API: `https://api.bilibili.com/x/web-interface/search/all`
- 视频详情: `https://api.bilibili.com/x/web-interface/view`
- UP主信息: `https://api.bilibili.com/x/space/acc/info`

## Output Example

```markdown
## B站关键词分析报告：AI绘画

分析时间：2025-04-12
关键词搜索结果：1,247 个视频

### TOP 10 视频（按综合分）
1. 【完全免费】AI绘画零基础教程 - 播放量 234万，综合分 89.2
2. ...

### 趋势分析
- 本月新增：+312 个相关视频
- 平均播放量：4.7万（↑23% vs 上月）
```
"""
    },
    {
        "slug": "google-search-console",
        "category": "superpowers",
        "zh_name": "Google Search Console 分析",
        "description": "Google Search Console API 集成，获取网站搜索表现数据、关键词排名、点击率分析和 SEO 优化建议。",
        "content": """# Google Search Console

Google Search Console (GSC) API skill. Use to **analyze website search performance**, keyword rankings, CTR, and get data-driven SEO recommendations.

## When to Use

- Weekly/monthly SEO performance review
- Identify top-performing content to double down on
- Find keywords with high impressions but low CTR
- Monitor for manual actions or technical issues

## Key Metrics

| Metric | What it Means |
|--------|--------------|
| Clicks | Users who clicked your result |
| Impressions | Times your result was shown |
| CTR | Click-through rate (clicks/impressions) |
| Position | Average ranking position |

## High-Impact Analysis

### Quick Win Keywords
```python
# Keywords with top 20 position but CTR < 3% (title optimization opportunity)
df[
    (df['position'] <= 20) &
    (df['ctr'] < 0.03) &
    (df['impressions'] > 100)
].sort_values('impressions', ascending=False)
```

### Position 4-10 Keywords (page 1 upgrade targets)
```python
df[(df['position'] >= 4) & (df['position'] <= 10)]\
    .sort_values('impressions', ascending=False)\
    .head(20)
```

## API Setup

```python
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

service = build('searchconsole', 'v1', credentials=creds)

response = service.searchanalytics().query(
    siteUrl='https://yoursite.com',
    body={
        'startDate': '2025-01-01',
        'endDate': '2025-04-12',
        'dimensions': ['query', 'page'],
        'rowLimit': 1000
    }
).execute()
```

## Automated Reports

Weekly report template:
- Top 10 keywords by clicks
- Top 10 pages by impressions
- Keywords that gained/lost >5 positions
- Pages with CTR below 2%
"""
    },
    {
        "slug": "excel-analyzer",
        "category": "superpowers",
        "zh_name": "Excel 智能分析",
        "description": "Excel/CSV 数据智能分析技能，支持自然语言查询、自动图表生成、数据清洗和透视表操作。",
        "content": """# Excel Analyzer

Excel and CSV intelligent analysis skill. Use to **analyze spreadsheet data with natural language** — pivot tables, charts, statistical summaries, all without formulas.

## When to Use

- Business data analysis without BI tools
- Quick insights from exported reports
- Data cleaning and transformation
- Generating charts for presentations

## Natural Language Interface

```
Analyze: [filename.xlsx]
Question: "What's the monthly revenue trend for 2024?"
Output: line chart + summary table

---

"Find all rows where profit margin < 10%"
→ Filtered table with conditional highlighting

---

"Compare Q1 vs Q2 sales by region"
→ Pivot table + comparison chart
```

## Supported Operations

### Data Exploration
```python
import pandas as pd

df = pd.read_excel('data.xlsx')

# Auto-summary
print(df.describe())
print(df.dtypes)
print(df.isnull().sum())  # missing value report
```

### Data Cleaning
```python
# Auto-detect and fix common issues
df = df.dropna(subset=['revenue'])  # required fields
df['date'] = pd.to_datetime(df['date'])  # fix date parsing
df['amount'] = df['amount'].str.replace(',', '').astype(float)  # fix numbers
df = df.drop_duplicates()  # remove duplicates
```

### Visualization
```python
import plotly.express as px

# Monthly trend
monthly = df.groupby(df['date'].dt.month)['revenue'].sum()
fig = px.line(monthly, title='Monthly Revenue 2024')
fig.show()
```

## Output Formats

- Markdown tables
- Excel with formatting
- PNG/HTML charts
- Summary bullet points
"""
    },

    # ===== 生产力工具 =====
    {
        "slug": "notion-api",
        "category": "superpowers",
        "zh_name": "Notion API 集成",
        "description": "Notion 完整 API 集成，支持数据库查询、页面创建、内容同步和自动化工作流，构建 Notion 驱动的知识系统。",
        "content": """# Notion API

Full Notion API integration skill. Use to **read from and write to Notion** — databases, pages, and blocks — programmatically.

## When to Use

- Sync data from other tools into Notion
- Build automated reporting in Notion
- Read Notion as a data source for other apps
- Bulk create or update database entries

## Key Operations

### Query a Database
```python
from notion_client import Client

notion = Client(auth=os.environ["NOTION_TOKEN"])

results = notion.databases.query(
    database_id="your-database-id",
    filter={
        "property": "Status",
        "select": {"equals": "In Progress"}
    },
    sorts=[{"property": "Priority", "direction": "descending"}]
)
```

### Create a Page
```python
notion.pages.create(
    parent={"database_id": "your-db-id"},
    properties={
        "Name": {"title": [{"text": {"content": "New Task"}}]},
        "Status": {"select": {"name": "Todo"}},
        "Due": {"date": {"start": "2025-04-20"}}
    },
    children=[
        {
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"text": {"content": "Task description here"}}]
            }
        }
    ]
)
```

### Update Properties
```python
notion.pages.update(
    page_id="page-id",
    properties={
        "Status": {"select": {"name": "Done"}},
        "Completed": {"date": {"start": datetime.now().isoformat()}}
    }
)
```

## Setup

1. Create integration at https://www.notion.so/my-integrations
2. Share database with your integration
3. Get database ID from page URL

## Common Use Cases

- CRM: auto-log meetings from calendar
- Content: track articles with auto-status updates
- Sprint: sync Jira tickets to Notion board
"""
    },
    {
        "slug": "jira-skill",
        "category": "dev-workflow",
        "zh_name": "Jira 项目管理集成",
        "description": "Jira REST API 完整集成，支持 Issue 创建/更新/查询、Sprint 管理、工作流转换和自动化报告生成。",
        "content": """# Jira Skill

Complete Jira integration skill. Use to **manage Jira projects, issues, and sprints** programmatically from any workflow.

## When to Use

- Create issues from external triggers (emails, Slack, webhooks)
- Bulk update issue status or fields
- Generate sprint reports and burndown data
- Sync Jira with other project management tools

## Core Operations

### Create Issue
```python
from jira import JIRA

jira = JIRA(
    server="https://yourcompany.atlassian.net",
    basic_auth=("email@company.com", "api_token")
)

issue = jira.create_issue(
    project="PROJ",
    summary="[BUG] Login fails on mobile Safari",
    description="Detailed steps to reproduce...",
    issuetype={"name": "Bug"},
    priority={"name": "High"},
    labels=["mobile", "auth"],
    assignee={"name": "john.doe"}
)
print(f"Created: {issue.key}")  # PROJ-123
```

### JQL Search
```python
# All open high-priority bugs in current sprint
issues = jira.search_issues(
    'project = PROJ AND issuetype = Bug AND priority = High '
    'AND sprint in openSprints() AND status != Done',
    maxResults=50
)

# Recently updated (for standup)
issues = jira.search_issues(
    'project = PROJ AND updated >= -1d ORDER BY updated DESC'
)
```

### Sprint Management
```python
# Get active sprint
from jira import JIRA
boards = jira.boards(projectKeyOrID="PROJ")
sprints = jira.sprints(boards[0].id, state='active')
active_sprint = sprints[0]

# Get sprint velocity
completed = jira.search_issues(
    f'sprint = {active_sprint.id} AND status = Done'
)
velocity = sum(i.fields.story_points or 0 for i in completed)
```

## Automation Examples

- Slack command → create Jira issue
- GitHub PR merged → transition issue to "In Review"
- Daily report → post sprint burndown to Slack
"""
    },
    {
        "slug": "todoist-api",
        "category": "superpowers",
        "zh_name": "Todoist 任务管理",
        "description": "Todoist API 集成，支持任务创建、项目管理、优先级设置、自然语言时间解析和跨工具同步。",
        "content": """# Todoist API

Todoist task management integration. Use to **create and manage tasks, projects, and reminders** in Todoist from any workflow.

## When to Use

- Capture tasks from emails, messages, or meetings automatically
- Daily task planning and prioritization
- Sync tasks from GitHub, Jira, or other tools
- Build personal productivity automation

## Key Operations

### Create Task
```python
import requests

headers = {"Authorization": f"Bearer {TODOIST_TOKEN}"}

# Simple task
task = requests.post(
    "https://api.todoist.com/rest/v2/tasks",
    headers=headers,
    json={
        "content": "Review PR #234",
        "due_string": "today 5pm",
        "priority": 4,  # 1=normal, 4=urgent
        "project_id": "2203306141",
        "labels": ["work", "code-review"]
    }
)
```

### Natural Language Due Dates
```python
# Todoist understands natural language:
"due_string": "every monday 9am"
"due_string": "next friday"
"due_string": "in 3 days at 2pm"
"due_string": "tomorrow morning"
```

### Query Tasks
```python
# Get today's tasks
tasks = requests.get(
    "https://api.todoist.com/rest/v2/tasks",
    headers=headers,
    params={"filter": "today | overdue"}
).json()

# High priority incomplete tasks
tasks = requests.get(
    "https://api.todoist.com/rest/v2/tasks",
    headers=headers,
    params={"filter": "p1 & !completed"}
).json()
```

## Productivity Workflows

```
Morning Routine:
1. Get today + overdue tasks
2. Sort by priority + energy required
3. Time-block in calendar
4. Send summary to Slack

Weekly Review:
1. Complete overdue items or reschedule
2. Review completed tasks for reflection
3. Plan next week's priorities
```
"""
    },
    {
        "slug": "slack-api",
        "category": "superpowers",
        "zh_name": "Slack 消息自动化",
        "description": "Slack API 完整集成，支持消息发送、频道管理、Bot 创建、Slash 命令和工作流自动化通知。",
        "content": """# Slack API

Slack API integration skill. Use to **send messages, manage channels, build bots**, and create automated notifications in Slack.

## When to Use

- Send automated reports and alerts to team channels
- Build slash commands for team productivity
- Create interactive approval workflows
- Sync external tool notifications to Slack

## Core Operations

### Send Message
```python
from slack_sdk import WebClient

client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])

# Simple message
client.chat_postMessage(
    channel="#general",
    text="Deployment to production completed! 🚀"
)

# Rich message with blocks
client.chat_postMessage(
    channel="#deployments",
    blocks=[
        {
            "type": "header",
            "text": {"type": "plain_text", "text": "🚀 Deploy Complete"}
        },
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": "*Environment:*\nProduction"},
                {"type": "mrkdwn", "text": "*Version:*\nv2.4.1"},
                {"type": "mrkdwn", "text": "*Duration:*\n4m 23s"},
            ]
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "View Logs"},
                    "url": "https://logs.example.com"
                }
            ]
        }
    ]
)
```

### Slash Commands
```python
# Flask webhook handler for /standup command
@app.route("/slack/standup", methods=["POST"])
def standup():
    user = request.form["user_name"]
    # Fetch their Jira/Linear tasks
    tasks = get_user_tasks(user)
    return jsonify({
        "response_type": "in_channel",
        "text": f"*{user}'s standup:*\n" + "\n".join(f"• {t}" for t in tasks)
    })
```

## Common Automation Patterns

- GitHub PR → Slack notification with review button
- Daily standup reminder with task summary
- Alert on error rates from monitoring
- Weekly metrics digest
"""
    },

    # ===== 媒体 & 内容 =====
    {
        "slug": "youtube-analytics",
        "category": "superpowers",
        "zh_name": "YouTube 数据分析",
        "description": "YouTube Analytics API 集成，分析频道/视频表现、受众画像、留存率和增长趋势，支持竞品对标。",
        "content": """# YouTube Analytics

YouTube Analytics API skill. Use to **analyze channel and video performance**, audience demographics, and growth trends.

## When to Use

- Content creator performance review
- Competitive analysis of YouTube channels
- Identifying best-performing content formats
- Audience research for marketing campaigns

## Key Metrics

| Metric | Formula / API Field |
|--------|-------------------|
| AVD (Avg View Duration) | `averageViewDuration` |
| CTR | `annotationClickThroughRate` |
| Retention Rate | `relativeRetentionPerformance` |
| Revenue per View | `estimatedRevenue / views` |
| Subscriber Value | `subscribersGained / views` |

## Analytics Queries

```python
from googleapiclient.discovery import build

youtube_analytics = build('youtubeAnalytics', 'v2', credentials=creds)

# Top videos last 30 days
response = youtube_analytics.reports().query(
    ids='channel==MINE',
    startDate='2025-03-12',
    endDate='2025-04-12',
    metrics='views,estimatedMinutesWatched,averageViewDuration,subscribersGained',
    dimensions='video',
    sort='-views',
    maxResults=20
).execute()
```

## Competitive Analysis (Public Data)

```python
# Scrape public channel stats (no auth required)
url = f"https://www.youtube.com/channel/{channel_id}/about"
# Parse: subscriber count, total views, video count

# Video metadata via oembed
url = f"https://www.youtube.com/oembed?url=https://youtu.be/{video_id}&format=json"
```

## Report Template

```markdown
## YouTube Performance Report — April 2025

### Channel Overview
- Total Views: 1.2M (+18% MoM)
- Watch Time: 89K hours (+12% MoM)
- Subscribers: +2,340 this month

### Top Performers
| Video | Views | CTR | AVD |
|-------|-------|-----|-----|
| ...   | ...   | ... | ... |
```
"""
    },
    {
        "slug": "wechat-publisher",
        "category": "superpowers",
        "zh_name": "微信公众号发布助手",
        "description": "一键发布 Markdown 到微信公众号草稿箱，支持自动排版、代码高亮、图片上传和多主题渲染。",
        "content": """# WeChat Publisher

Publish Markdown content to WeChat Official Account (公众号). Use to **automate content publishing** to 微信公众号 with beautiful formatting.

## When to Use

- Publish technical articles to 公众号
- Batch publish scheduled content
- Convert internal docs/notes to 公众号 format
- A/B test different article formats

## Features

- **Markdown → 公众号 HTML**: Full syntax support
- **代码高亮**: Syntax highlighting for 20+ languages
- **图片自动上传**: Local images auto-uploaded to 微信 CDN
- **主题**: Multiple article themes (default, night, minimalist)
- **草稿箱**: Push to draft for manual review before publish

## Usage

```python
from wechat_publisher import WeChatPublisher

publisher = WeChatPublisher(
    app_id=os.environ["WECHAT_APP_ID"],
    app_secret=os.environ["WECHAT_APP_SECRET"]
)

# Read Markdown file
with open("article.md") as f:
    content = f.read()

# Publish to draft
draft_id = publisher.create_draft(
    title="Python 异步编程深度指南",
    content=content,
    thumb_media_id="...",  # cover image ID
    author="Your Name",
    digest="文章摘要..."
)
print(f"Draft created: {draft_id}")
```

## Markdown Support

```markdown
# 一级标题

**粗体** _斜体_ ~~删除线~~

```python
def hello():
    print("代码高亮")
```

> 引用块

| 表格 | 支持 |
|------|------|
| 数据 | 渲染 |
```

## CLI Usage

```bash
# Install
pip install wenyan-cli

# Publish
wenyan publish article.md --title "标题" --theme default
```
"""
    },

    # ===== 搜索专项 =====
    {
        "slug": "feishu-bitable-api",
        "category": "superpowers",
        "zh_name": "飞书多维表格 API",
        "description": "飞书多维表格(Bitable)API 技能，支持记录的增删改查、视图筛选、字段管理和数据同步自动化。",
        "content": """# Feishu Bitable API

飞书多维表格 (Bitable) API skill. Use to **read and write Feishu spreadsheet-databases** — the Chinese enterprise equivalent of Notion/Airtable.

## When to Use

- Sync data into 飞书 databases from other systems
- Build reporting dashboards in 飞书
- Automate data entry from forms/webhooks
- Read 飞书 as a backend data store

## Authentication

```python
import requests

# Get access token
def get_token(app_id, app_secret):
    resp = requests.post(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        json={"app_id": app_id, "app_secret": app_secret}
    )
    return resp.json()["tenant_access_token"]
```

## Core Operations

### List Records
```python
headers = {"Authorization": f"Bearer {token}"}
app_token = "bascn..."  # from Bitable URL
table_id = "tbl..."

records = requests.get(
    f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records",
    headers=headers,
    params={
        "page_size": 100,
        "filter": 'AND(CurrentValue.[状态]="进行中")',
        "sort": '[{"field_name":"优先级","desc":true}]'
    }
).json()
```

### Create Record
```python
requests.post(
    f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records",
    headers=headers,
    json={
        "fields": {
            "任务名称": "修复登录Bug",
            "状态": "待处理",
            "优先级": "P0",
            "负责人": [{"id": "user_id_xxx"}],
            "截止日期": "2025-04-20"
        }
    }
)
```

## Common Automations

- GitHub Issue → 飞书 任务
- 定时同步销售数据到汇报表
- 飞书表单 → 自动分配任务
"""
    },
    {
        "slug": "baidu-search",
        "category": "superpowers",
        "zh_name": "百度智能搜索",
        "description": "利用百度 AI 搜索引擎进行网页搜索，适合中文内容检索，支持新闻、学术、百科多源聚合。",
        "content": """# Baidu Search

百度 AI 搜索技能。Use for **Chinese-language web search** — news, encyclopedia, academic papers, and general web content in Chinese.

## When to Use

- Research Chinese market, companies, or trends
- Find Chinese language technical documentation
- Search for information primarily in Chinese
- News monitoring for China-related topics

## Why Baidu for Chinese Content

- Better coverage of `.cn` domains and 中文内容
- Baidu Baike (encyclopedia) integration
- News results from 新浪, 网易, 腾讯 etc.
- Academic integration with CNKI abstracts

## API Usage

```python
import requests

# Baidu Custom Search API
def baidu_search(query: str, count: int = 10):
    url = "https://aip.baidubce.com/rpc/2.0/nlp/v1/search"
    params = {
        "access_token": get_access_token(),
        "q": query,
        "pn": 0,  # page offset
        "rn": count,  # result count
    }
    return requests.post(url, json=params).json()

# Alternative: SerpApi with Baidu engine
params = {
    "engine": "baidu",
    "q": query,
    "api_key": SERPAPI_KEY
}
```

## Search Operators

```
# Exact phrase
"人工智能大模型"

# Site-specific
site:zhihu.com Python教程

# File type
filetype:pdf 产品需求文档模板

# Exclude
机器学习 -深度学习

# Time range
2025年 AI应用案例
```

## Output Processing

```python
# Extract key info from results
for result in results:
    print(f"Title: {result['title']}")
    print(f"URL: {result['url']}")
    print(f"Snippet: {result['abstract']}")
```
"""
    },

    # ===== 开发流程 =====
    {
        "slug": "changelog-generator",
        "category": "dev-workflow",
        "zh_name": "自动 Changelog 生成器",
        "description": "分析 git 提交历史，按 Conventional Commits 规范自动生成格式化的更新日志，支持中英文输出。",
        "content": """# Changelog Generator

Automatic changelog generation from git history. Use to **generate professional release notes** from conventional commits.

## When to Use

- Creating CHANGELOG.md for releases
- Generating release notes for GitHub releases
- Sprint review summaries
- Documentation updates

## Supported Formats

- **Keep a Changelog** (keepachangelog.com) — Standard format
- **GitHub Release Notes** — Markdown with categories
- **npm CHANGELOG** — Conventional format
- **中文更新日志** — Chinese localized output

## Process

```bash
# 1. Analyze commits since last tag
git log v1.2.0..HEAD --format="%H %s" | python changelog_gen.py

# 2. Categorize by type
feat    → Added
fix     → Fixed
perf    → Changed (Performance)
refactor → Changed
docs    → Documentation
security → Security
BREAKING CHANGE → ⚠️ Breaking Changes
```

## Generated Output

```markdown
# Changelog

## [2.0.0] - 2025-04-12

### ⚠️ Breaking Changes
- **auth**: JWT tokens now expire in 1 hour (was 24 hours) (#234)

### Added
- feat(search): Add semantic search with vector embeddings (#230)
- feat(api): Rate limiting per user tier (#228)
- feat(ui): Dark mode support (#225)

### Fixed
- fix(auth): Refresh tokens not invalidated on logout (#232)
- fix(db): Connection pool exhaustion under high load (#231)

### Performance
- perf(query): 40% faster search with index optimization (#229)

### Dependencies
- chore: Upgrade to FastAPI 0.110, SQLAlchemy 2.0
```

## Configuration

```yaml
# changelog.yml
output: CHANGELOG.md
from_tag: auto  # or specific: v1.2.0
types:
  feat: Added
  fix: Fixed
  perf: Performance
  docs: Documentation
  security: Security
include_breaking: true
locale: zh-CN  # Chinese output
```
"""
    },
    {
        "slug": "pentest-skill",
        "category": "dev-workflow",
        "zh_name": "渗透测试辅助工具",
        "description": "渗透测试辅助技能，提供 OWASP Top 10 测试方法、常用工具命令、漏洞验证和报告模板。",
        "content": """# Pentest Skill

Penetration testing assistance skill. Use to **guide security testing** with OWASP methodologies, tool commands, and report templates.

> **⚠️ Legal Notice**: Only use on systems you own or have explicit written permission to test.

## When to Use

- Pre-launch security assessment
- Bug bounty research (in scope)
- Internal red team exercises
- Security training and CTF

## Testing Phases

```
1. Reconnaissance  → Gather public info, enumerate attack surface
2. Scanning        → Port scan, service fingerprinting, vuln scan
3. Exploitation    → Test discovered vulnerabilities
4. Post-Exploit    → Privilege escalation, lateral movement
5. Reporting       → Document findings with severity ratings
```

## Common Tools Quick Reference

### Reconnaissance
```bash
# DNS enumeration
amass enum -d target.com

# Subdomain bruteforce
subfinder -d target.com -o subdomains.txt

# Port scanning
nmap -sV -sC -p- target.com -oN scan.txt
```

### Web Application Testing
```bash
# Directory brute force
gobuster dir -u https://target.com -w /usr/share/wordlists/dirb/common.txt

# Parameter fuzzing
ffuf -w params.txt -u "https://target.com/api?FUZZ=test"

# SQL injection
sqlmap -u "https://target.com/api/user?id=1" --dbs

# XSS scanning
dalfox url https://target.com/search?q=test
```

### SSRF Testing
```bash
# Test with Burp Collaborator or interactsh
curl -I "https://target.com/fetch?url=https://your-interactsh-server.com"
```

## Report Template

```markdown
## Vulnerability Report

### Critical: Remote Code Execution
**CVSS Score**: 9.8
**Affected**: POST /api/upload endpoint
**Description**: File upload without extension validation allows PHP webshell upload
**PoC**: [reproduction steps]
**Impact**: Full server compromise
**Remediation**: Whitelist allowed file types, sandbox uploads, disable PHP execution in upload dir
**References**: CWE-434, OWASP A03:2021
```
"""
    },
    {
        "slug": "imap-email",
        "category": "superpowers",
        "zh_name": "IMAP 邮件处理",
        "description": "IMAP 邮件读取和处理技能，支持多账户邮件监控、规则过滤、内容提取和自动回复工作流。",
        "content": """# IMAP Email

IMAP email processing skill. Use to **read, filter, and process emails** from any IMAP-compatible mailbox (Gmail, Outlook, custom servers).

## When to Use

- Monitor inbox for specific emails and trigger actions
- Extract data from incoming emails (invoices, orders, reports)
- Build email-to-task automation
- Auto-categorize or respond to emails

## Connection Setup

```python
import imaplib
import email
from email.header import decode_header

# Connect to Gmail
mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
mail.login("user@gmail.com", "app_password")  # Use app-specific password

# Connect to Outlook
mail = imaplib.IMAP4_SSL("outlook.office365.com", 993)
mail.login("user@outlook.com", "password")
```

## Core Operations

### Fetch Unread Emails
```python
mail.select("inbox")
_, message_ids = mail.search(None, "UNSEEN")

for mid in message_ids[0].split():
    _, msg_data = mail.fetch(mid, "(RFC822)")
    msg = email.message_from_bytes(msg_data[0][1])

    subject = decode_header(msg["Subject"])[0][0]
    sender = msg["From"]

    # Get text body
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True).decode()
    else:
        body = msg.get_payload(decode=True).decode()
```

### Filter by Sender/Subject
```python
# Search by sender
_, ids = mail.search(None, 'FROM "invoices@supplier.com"')

# Search by subject
_, ids = mail.search(None, 'SUBJECT "Order Confirmation"')

# Since date
_, ids = mail.search(None, 'SINCE "01-Apr-2025"')

# Combined
_, ids = mail.search(None, '(FROM "alerts@github.com" UNSEEN)')
```

## Automation Patterns

```python
# Email → Todoist task
def process_flagged_emails():
    for email in get_starred_emails():
        subject = extract_subject(email)
        create_todoist_task(subject, due="tomorrow")
        mark_processed(email)
```
"""
    },
    {
        "slug": "stock-analysis",
        "category": "superpowers",
        "zh_name": "股票数据分析",
        "description": "股票和金融数据分析技能，支持 A股/美股实时行情、技术指标计算、基本面数据获取和可视化报告。",
        "content": """# Stock Analysis

Stock and financial data analysis skill. Use to **analyze stocks, calculate technical indicators**, and generate investment research reports.

## When to Use

- Daily market monitoring and alerts
- Technical analysis (MA, RSI, MACD, Bollinger Bands)
- Fundamental analysis (P/E, revenue growth, margins)
- Portfolio performance tracking
- Sector rotation analysis

> ⚠️ **Disclaimer**: For informational purposes only. Not financial advice.

## Data Sources

| Source | Coverage | Free? |
|--------|---------|-------|
| yfinance | US/Global stocks | ✅ Free |
| akshare | A股 (Chinese market) | ✅ Free |
| tushare | A股 (detailed) | Partial free |
| Alpha Vantage | US stocks | Free tier |
| 东方财富 API | A股实时 | ✅ Free |

## Technical Analysis

```python
import yfinance as yf
import pandas as pd
import talib

ticker = yf.Ticker("AAPL")
df = ticker.history(period="1y")

# Moving Averages
df['MA20'] = talib.SMA(df['Close'], timeperiod=20)
df['MA60'] = talib.SMA(df['Close'], timeperiod=60)

# RSI
df['RSI'] = talib.RSI(df['Close'], timeperiod=14)

# MACD
df['MACD'], df['Signal'], df['Hist'] = talib.MACD(df['Close'])

# Bollinger Bands
df['BB_upper'], df['BB_mid'], df['BB_lower'] = talib.BBANDS(df['Close'])
```

## A股 Data (akshare)

```python
import akshare as ak

# 实时行情
df = ak.stock_zh_a_spot_em()  # 全部A股实时数据

# 历史数据
df = ak.stock_zh_a_hist(
    symbol="000001",  # 平安银行
    period="daily",
    start_date="20250101",
    end_date="20250412",
    adjust="qfq"  # 前复权
)

# 财务数据
df = ak.stock_financial_analysis_indicator(symbol="000001", start_year="2024")
```

## Report Template

```markdown
## 股票分析报告：贵州茅台 (600519)

### 技术面
- 当前价格：1,650.00 ¥
- 20日均线：1,620.00 ¥（金叉信号）
- RSI(14)：62.3（中性偏多）
- MACD：0.45（零轴上方，多头）

### 基本面
- PE(TTM)：28.5x（历史中位数 30x）
- ROE：35.2%（行业最高）
- 营收增长(YoY)：+18.3%
```
"""
    },
    {
        "slug": "linkedin-lead-gen",
        "category": "superpowers",
        "zh_name": "LinkedIn 线索挖掘",
        "description": "LinkedIn 潜在客户挖掘和分析技能，支持目标用户搜索、公司信息提取、联系人触达和销售线索管理。",
        "content": """# LinkedIn Lead Generation

LinkedIn prospecting and lead research skill. Use to **find and qualify potential customers** for B2B sales and business development.

## When to Use

- Building prospect lists for B2B sales
- Finding decision makers at target companies
- Researching potential partners or hires
- Account-based marketing (ABM) campaigns

## Search Strategies

### Boolean Search Operators
```
# Find VP/Director of Engineering in SaaS companies
"VP Engineering" OR "Director of Engineering" AND "SaaS" AND "Series B"

# Target by company size + role
"Head of Product" AND ("50-200 employees" OR "startup") NOT "intern"

# Industry + location
"Product Manager" AND "fintech" AND "San Francisco"
```

### Sales Navigator Filters
```
Role: [Target title]
Seniority: Director, VP, C-Suite
Company size: 50-500 employees
Industry: Software, SaaS, Fintech
Posted on LinkedIn: Last 30 days (signals activity)
```

## Profile Data Extraction

```python
# Using LinkedIn API (requires permission)
import linkedin_api

api = linkedin_api.Linkedin(email, password)

profile = api.get_profile("john-doe-123")
# Returns: name, headline, experience, education, skills

company = api.get_company("company-slug")
# Returns: size, industry, website, recent updates
```

## Outreach Templates

### Connection Request (< 300 chars)
```
Hi [Name], I saw your post about [topic] — really resonated. 
I'm working on [relevant thing]. Would love to connect.
```

### First Message
```
Hi [Name],

Noticed you're leading engineering at [Company]. 
We help [similar companies] [specific outcome].

Worth a 15-min call to see if there's a fit?

[Your name]
```

## Lead Scoring

| Signal | Score |
|--------|-------|
| Viewed your profile | +5 |
| Posted content recently | +3 |
| Job change in last 6 months | +4 |
| Company raised funding | +5 |
| Connected with your competitor | +3 |
"""
    },
    {
        "slug": "ga4-analytics",
        "category": "superpowers",
        "zh_name": "GA4 网站分析",
        "description": "Google Analytics 4 API 集成，支持流量分析、用户行为追踪、转化漏斗、事件分析和自动化报告。",
        "content": """# GA4 Analytics

Google Analytics 4 (GA4) API skill. Use to **analyze website traffic, user behavior, and conversions** programmatically.

## When to Use

- Weekly/monthly website performance reports
- Conversion funnel analysis
- Landing page performance comparison
- A/B test result analysis
- Marketing channel attribution

## Key Metrics

| Metric | API Name | Description |
|--------|----------|-------------|
| Users | `totalUsers` | Unique visitors |
| Sessions | `sessions` | Visit sessions |
| Bounce Rate | `bounceRate` | Single-page sessions |
| Avg Session Duration | `averageSessionDuration` | Time on site |
| Conversion Rate | `sessionConversionRate` | Goal completions |
| Revenue | `totalRevenue` | Ecommerce revenue |

## API Setup

```python
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Metric, Dimension

client = BetaAnalyticsDataClient()

request = RunReportRequest(
    property=f"properties/{PROPERTY_ID}",
    dimensions=[
        Dimension(name="pagePath"),
        Dimension(name="deviceCategory"),
    ],
    metrics=[
        Metric(name="sessions"),
        Metric(name="bounceRate"),
        Metric(name="averageSessionDuration"),
    ],
    date_ranges=[DateRange(start_date="30daysAgo", end_date="today")],
    order_bys=[{"metric": {"metric_name": "sessions"}, "desc": True}],
    limit=20,
)

response = client.run_report(request)
```

## Conversion Funnel Analysis

```python
# Funnel: Landing → Product → Cart → Checkout → Purchase
funnel_steps = ["page_view", "view_item", "add_to_cart", "begin_checkout", "purchase"]

request = RunFunnelReportRequest(
    property=f"properties/{PROPERTY_ID}",
    funnel={
        "steps": [
            {"name": step, "filterExpression": {"eventFilter": {"eventName": step}}}
            for step in funnel_steps
        ]
    },
    date_ranges=[DateRange(start_date="30daysAgo", end_date="today")]
)
```

## Report Template

```markdown
## Website Analytics — April 2025

### Traffic Overview
- Total Users: 124,523 (+12% MoM)
- Sessions: 187,234 (+8% MoM)
- Avg Session Duration: 3m 42s (+15s)
- Bounce Rate: 42.3% (-3.2% improvement)

### Top Pages
| Page | Sessions | Bounce Rate |
|------|---------|------------|
| /    | 45,230  | 38%        |
```
"""
    },
    {
        "slug": "apify-scraper",
        "category": "superpowers",
        "zh_name": "Apify 网页抓取",
        "description": "Apify 平台集成的网页抓取工具，支持 JavaScript 渲染、反爬绕过、数据提取和结构化存储，覆盖主流平台。",
        "content": """# Apify Scraper

Apify web scraping skill. Use to **extract data from any website** — handles JavaScript rendering, anti-bot measures, and returns structured data.

## When to Use

- Competitor pricing monitoring
- Job listing aggregation
- Product review collection
- Social media data extraction
- Real estate or e-commerce scraping

## Pre-built Actors (No Code)

```python
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])

# Amazon product scraper
run = client.actor("junglee/amazon-crawler").call(run_input={
    "searchKeywords": "mechanical keyboard",
    "maxItems": 100,
    "country": "US"
})
results = list(client.dataset(run["defaultDatasetId"]).iterate_items())

# LinkedIn company scraper
run = client.actor("curious_coder/linkedin-company-scraper").call(run_input={
    "urls": ["https://www.linkedin.com/company/openai"],
})

# Instagram profile scraper
run = client.actor("apify/instagram-scraper").call(run_input={
    "directUrls": ["https://www.instagram.com/openai"],
    "resultsType": "posts",
    "resultsLimit": 50,
})
```

## Custom Scraper

```python
# Playwright-based custom scraper
run_input = {
    "startUrls": [{"url": "https://target.com/products"}],
    "pseudoUrls": ["https://target.com/product/[.*]"],
    "pageFunction": (
        "async function pageFunction(context) {\n"
        "    const { $, request } = context;\n"
        "    return {\n"
        "        title: $('h1').text(),\n"
        "        price: $('.price').text(),\n"
        "        rating: $('[data-rating]').attr('data-rating'),\n"
        "        url: request.url\n"
        "    };\n"
        "}"
    ),
    "maxPagesPerCrawl": 1000,
    "proxy": {"useApifyProxy": True, "apifyProxyGroups": ["RESIDENTIAL"]}
}
```

## Rate Limiting & Ethics

1. Respect `robots.txt`
2. Add delays between requests: `requestHandlerTimeoutSecs: 2`
3. Use residential proxies for sites with IP blocks
4. Check ToS before scraping commercially
5. Store only necessary data (GDPR compliance)
"""
    },
]

# =========================================================
# 写入仓库
# =========================================================
created = []
skipped = []

for skill in SELECTED_SKILLS:
    slug = skill["slug"]
    skill_dir = ALL_SKILLS_DIR / slug
    skill_dir.mkdir(parents=True, exist_ok=True)

    skill_file = skill_dir / "SKILL.md"
    if skill_file.exists():
        skipped.append(slug)
        continue

    # 写 SKILL.md
    display_name = slug.replace('-', ' ').title()
    header = f"""---
name: {display_name}
slug: {slug}
description: {skill['description']}
category: {skill['category']}
source: clawhub
---

"""
    with open(skill_file, "w", encoding="utf-8") as f:
        f.write(header + skill["content"])

    created.append(slug)
    print(f"  [OK] Created: {slug}")

print(f"\n=== 完成 ===")
print(f"创建: {len(created)} 个 skills")
print(f"跳过(已存在): {len(skipped)} 个")
