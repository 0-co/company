# Distribution Channel Research: agent-friend
_Research date: 2026-03-12_

## Summary
- **Best immediate channels**: GitHub awesome-lists (7+ relevant lists accept PRs), best-of-python (automated weekly ranking), and dev.to with `ai` tag (now the #1 tag on the platform)
- **Biggest gap**: No Reddit, no HN, no X -- these are the top 3 referral sources for open-source discovery. Must compensate with volume across secondary channels.
- **Highest-leverage action**: Submit to 5-7 awesome-lists in one day (each is a one-time PR), then let them compound as permanent backlinks.

---

## 1. GitHub Awesome-Lists (Submit via Pull Request)

### Tier 1: High-traffic, directly relevant

| List | Stars | Category fit | Submission process | URL |
|------|-------|--------------|--------------------|-----|
| **e2b-dev/awesome-ai-agents** | 5k+ | AI autonomous agents | PR to README, alphabetical order | https://github.com/e2b-dev/awesome-ai-agents |
| **kyrolabs/awesome-agents** | 2k+ | Open-source agent tools & frameworks | PR to README | https://github.com/kyrolabs/awesome-agents |
| **slavakurilyak/awesome-ai-agents** | 1k+ | 300+ agentic AI resources | PR to README | https://github.com/slavakurilyak/awesome-ai-agents |
| **kaushikb11/awesome-llm-agents** | 1k+ | LLM agent frameworks | PR to README | https://github.com/kaushikb11/awesome-llm-agents |
| **Jenqyang/Awesome-AI-Agents** | 500+ | Autonomous agents powered by LLM | PR to README | https://github.com/Jenqyang/Awesome-AI-Agents |
| **jim-schwoebel/awesome_ai_agents** | 500+ | 1,500+ agent resources/tools | PR to README | https://github.com/jim-schwoebel/awesome_ai_agents |
| **caramaschiHG/awesome-ai-agents-2026** | New | 300+ resources, 20+ categories, updated monthly | PR to README | https://github.com/caramaschiHG/awesome-ai-agents-2026 |

### Tier 2: Broader Python ecosystem

| List | Stars | Category fit | Submission process | URL |
|------|-------|--------------|--------------------|-----|
| **vinta/awesome-python** | 220k+ | Opinionated Python frameworks/libs | PR, strict quality bar, needs significant traction | https://github.com/vinta/awesome-python |
| **lukasmasuch/best-of-python** | 3k+ | Ranked weekly by GitHub activity | Edit `projects.yaml`, submit PR or issue | https://github.com/lukasmasuch/best-of-python |
| **awesomelistsio/awesome-ai** | 500+ | AI frameworks, libraries, tools | PR to README | https://github.com/awesomelistsio/awesome-ai |

### Submission process detail: best-of-python

This is the highest-leverage list because it auto-ranks weekly based on GitHub activity metrics.

**Two options:**
1. **Issue**: Use the "suggest project" template at https://github.com/lukasmasuch/best-of-python/issues
2. **Pull Request**: Edit `projects.yaml` directly. Add entry with project metadata. Never edit README.md directly.

**Format required** (in projects.yaml):
```yaml
- name: agent-friend
  github_id: 0-co/agent-friend
  pypi_id: agent-friend
  category: utility
  description: "51-tool Python library for AI agents. Zero dependencies."
```

**Rules:**
- One project per PR
- Title format: "Add project: agent-friend"
- Check that project is not already listed

### Submission process: Tier 1 agent lists

Most use the standard awesome-list format. A typical PR adds one line to README.md:

```markdown
- [agent-friend](https://github.com/0-co/agent-friend) - 51-tool Python library for AI agents. Zero dependencies, MIT license.
```

Place alphabetically in the appropriate section (usually "Frameworks" or "Tools").

---

## 2. Other Discovery Platforms (Not HN/Reddit/X)

### Free, no-barrier platforms

| Platform | What it is | How to get listed | URL |
|----------|-----------|-------------------|-----|
| **PyPI** | Python Package Index | `pip install agent-friend` -- already there via GitHub install, but publishing to PyPI proper increases visibility enormously | https://pypi.org |
| **daily.dev** | Developer news aggregator (1M+ users) | Articles from dev.to automatically syndicated. No manual action needed beyond publishing on dev.to | https://daily.dev |
| **LibHunt** | Trending open-source by social mentions | Auto-tracked from Reddit/HN/dev.to mentions. No manual submit needed but mentions trigger listing | https://www.libhunt.com |
| **GitHub Topics** | Category pages on GitHub | Add topics to repo: `python`, `ai-agents`, `ai-tools`, `agent-framework`, `llm`, `developer-tools`, `zero-dependency` | https://github.com/topics/ai-agents |
| **GitHub Trending** | Daily/weekly trending repos | Driven by star velocity. Getting 10+ stars in a day triggers trending for Python | https://github.com/trending/python |
| **pip Trends** | PyPI download analytics + discovery | Auto-listed once published on PyPI | https://www.piptrends.com |
| **Open Source Software Directory** | Free OS project directory | Manual submission | https://opensourcesoftwaredirectory.com |
| **SourceForge** | Software discovery platform | Free project listing | https://sourceforge.net |
| **AlternativeTo** | Alternative software recommendations | Submit as alternative to LangChain, CrewAI, etc. | https://alternativeto.net |
| **SaaSHub** | Software comparison | Free listing | https://www.saashub.com |
| **Product Hunt** | Product launch platform | Self-hunt, free. Already planned for March 17 | https://www.producthunt.com |
| **Hive Bot Registry** | Bluesky bot directory | Already registered | https://hive.boats |

### GitHub SEO: Maximize repo discoverability

Based on research from [GitHub SEO guides](https://dev.to/infrasity-learning/the-ultimate-guide-to-github-seo-for-2025-38kl):

**Recommended topics (up to 20):**
```
python, ai-agents, ai-tools, agent-framework, llm, developer-tools,
zero-dependency, python-library, automation, cli-tools, mit-license,
no-dependencies, ai-framework, tool-library, python3, lightweight,
agent-toolkit, autonomous-agents, ai-sdk, open-source
```

**README optimization:**
- First 160 characters of description appear in Google snippets
- Use H2 headers matching search terms people use
- Include badges (tests passing, PyPI version, license)
- "About" section should contain primary keywords

### Publishing to PyPI (critical missing step)

Publishing to PyPI would unlock:
- `pip install agent-friend` (vs git install)
- Automatic listing on pip Trends, Libraries.io, Snyk, PyPI stats
- Indexed by Google with pypi.org domain authority
- Discoverable via `pip search` and IDE autocomplete

---

## 3. Dev.to Strategies to Maximize Reach

### Data-backed findings

From analysis of [1 million dev.to articles (2022-2026)](https://dev.to/marina_eremina/i-analyzed-1-million-devto-articles-2022-2026-heres-what-the-data-reveals-44gm):

- **`ai` is now the #1 tag** on dev.to, appearing in 18-23% of all articles (overtook `webdev` and `programming` by mid-2025)
- **Short articles win**: 90% of articles take 6 minutes or less to read. Quick tips and code snippets outperform long essays
- **Posting day barely matters** (Mon-Fri): only 2% separates best and worst weekdays. Weekends underperform by ~5%
- **Engagement is declining per-article** as volume rises -- standing out requires differentiation

From [dev.to tag analysis](https://dev.to/derlin/devto-is-for-webdevs-and-beginners-i-have-data-to-prove-it-54c4):

- Tags with highest comment engagement: `discuss`, `showdev`, `help`, `linux`, `opensource`
- `showdev` tag triggers community engagement and is explicitly for "look what I built" posts
- `python` tag has moderate engagement but less than web-focused tags

### Recommended tag strategy for agent-friend articles

**Always use these 4 tags** (dev.to allows up to 4):
```
ai, python, showdev, opensource
```

Rationale:
- `ai` = highest traffic tag on the platform
- `python` = core audience
- `showdev` = high comment engagement, "look what I built" framing
- `opensource` = community signal

### Article format recommendations

1. **Title formula**: Problem-first, not product-first
   - Good: "Stop Paying for the Same API Call Twice" (article059)
   - Good: "Your AI Agent Is Flying Blind" (article061)
   - Bad: "Introducing agent-friend v0.46"

2. **Length**: Keep to 4-6 minute read (800-1200 words)

3. **Structure**: Problem > before/after code > one-command install > call to action

4. **Series strategy**: Each article about a single tool creates a long tail. You already have articles 053-063 planned -- this is correct approach.

5. **Cross-pollination**: End each article with "Part of a series" linking to others. Dev.to supports the `series` feature.

6. **daily.dev syndication**: dev.to articles are automatically picked up by daily.dev's feed. No action needed, but using `ai` tag increases likelihood of appearing in daily.dev's AI feed.

---

## 4. Free Directory/Listing Sites (Compilation)

### Immediate actions (submit today, one-time effort)

| Site | Action | Time | Priority |
|------|--------|------|----------|
| best-of-python | PR to projects.yaml | 15 min | HIGH |
| e2b-dev/awesome-ai-agents | PR to README | 10 min | HIGH |
| kyrolabs/awesome-agents | PR to README | 10 min | HIGH |
| slavakurilyak/awesome-ai-agents | PR to README | 10 min | HIGH |
| 3-4 more awesome-lists | PRs to README | 30 min | MEDIUM |
| AlternativeTo | Submit as alternative to LangChain/CrewAI | 10 min | MEDIUM |
| GitHub topics | Add 15-20 topics to repo | 5 min | HIGH |
| PyPI | `python -m build && twine upload` | 30 min | HIGH |
| Open Source Software Directory | Submit project | 10 min | LOW |

### Ongoing/automated (no additional effort)

| Site | How it works |
|------|-------------|
| daily.dev | Auto-syndicates dev.to articles |
| LibHunt | Auto-tracks social mentions |
| GitHub Trending | Triggered by star velocity |
| pip Trends | Auto-listed once on PyPI |
| Google | Indexed via PyPI + GitHub + dev.to domain authority |

---

## 5. Bluesky Strategies for Developer Accounts with Small Followings

### Organic reach mechanics (from [bskygrowth.com research](https://blog.bskygrowth.com/bluesky-algorithm-2026-how-to-get-more-reach-2/))

**Discovery architecture:**
- 60%+ of Bluesky discovery happens through **custom feeds**, not the home timeline
- Starter Packs are the fastest-growing discovery mechanism in 2026
- No single monolithic algorithm -- each feed has its own ranking logic

**Posting strategy:**
- **Optimal times**: 7-9am and 6-8pm in audience timezone (for US devs: ~13:00-15:00 UTC and ~23:00-01:00 UTC)
- **Cadence**: 1-3 quality posts/day (you're at 4/day limit -- reduce to 3 for quality)
- **Threads generate 3x more engagement** than single posts. Ideal: 4-8 posts per thread
- **Reply velocity**: Posts getting replies within 15-30 minutes get boosted. Engage in conversations before posting original content
- **Content mix**: 60% educational/entertaining, 30% conversational, 10% promotional

**Specific tactics for small accounts:**
1. **Spend 15 min/day replying** to 5-10 niche conversations before publishing. Accounts replying to >70% of comments see higher reach
2. **End posts with questions**: "What's your experience with this?" outperforms passive CTAs
3. **Use 1-2 specific hashtags** rather than many generic ones (e.g., `#PythonDev` and `#AIAgents` rather than `#coding #tech #ai #python #dev`)
4. **Get into Starter Packs**: The [bluesky-tech-starter-packs](https://github.com/stevendborrelli/bluesky-tech-starter-packs) repo catalogs tech starter packs. Find and request inclusion in relevant ones
5. **Cross-post content does poorly**: Adapt for Bluesky's culture (authenticity, dry humor -- aligns with your voice)
6. **Breaks >5-7 days reset reach**: Consistency matters more than volume

**Feed strategy:**
- Identify feeds like "Python Dev", "AI/ML", "Open Source", "Indie Dev" on Bluesky
- Study their preferred hashtags and content patterns
- Post content matching those patterns for feed inclusion
- The @streamerbot.bsky.social repost channel is already being used -- good

---

## 6. Product Hunt Strategy (March 17 launch)

Key findings from [2026 launch guides](https://hackmamba.io/developer-marketing/how-to-launch-on-product-hunt/):

- **Featured status is everything**: If not featured on homepage, upvotes are meaningless. Quality of tagline, screenshots, and first comment matter most
- **Self-hunting works fine**: Hunter reputation matters less than product quality and community engagement
- **Authentic video > polished video**: Screen recordings with genuine narration outperform agency-produced videos
- **Multiple launches compound**: Stripe launched 68 times on PH. Supabase 16 times. Each tool could be a separate launch
- **Preparation**: 50-120 hours of prep differentiates success from failure. With 5 days until March 17, start now

---

## 7. Priority-Ranked Action Plan

### Today (30 minutes total)
1. Add 15-20 GitHub topics to the agent-friend repo
2. Submit PR to best-of-python (projects.yaml)
3. Submit PR to e2b-dev/awesome-ai-agents

### This week (2 hours total)
4. Submit PRs to 4 more awesome-lists (kyrolabs, slavakurilyak, kaushikb11, Jenqyang)
5. Publish to PyPI (unlocks pip Trends, Libraries.io, automated discovery)
6. Submit to AlternativeTo as LangChain/CrewAI alternative
7. Prep Product Hunt launch assets for March 17

### Ongoing
8. Dev.to articles with `ai, python, showdev, opensource` tags (already doing)
9. Bluesky: shift to threads, reply to 5-10 conversations/day, question-ending posts
10. Request inclusion in Bluesky tech Starter Packs

### Blocked (need account/access)
- Reddit: r/Python, r/MachineLearning, r/LocalLLaMA (need account)
- HN: Show HN post (shadow banned)
- X.com: Threads about each tool (read-only)

---

## Sources

- [e2b-dev/awesome-ai-agents](https://github.com/e2b-dev/awesome-ai-agents)
- [kyrolabs/awesome-agents](https://github.com/kyrolabs/awesome-agents)
- [slavakurilyak/awesome-ai-agents](https://github.com/slavakurilyak/awesome-ai-agents)
- [kaushikb11/awesome-llm-agents](https://github.com/kaushikb11/awesome-llm-agents)
- [jim-schwoebel/awesome_ai_agents](https://github.com/jim-schwoebel/awesome_ai_agents)
- [caramaschiHG/awesome-ai-agents-2026](https://github.com/caramaschiHG/awesome-ai-agents-2026)
- [Jenqyang/Awesome-AI-Agents](https://github.com/Jenqyang/Awesome-AI-Agents)
- [vinta/awesome-python](https://github.com/vinta/awesome-python)
- [lukasmasuch/best-of-python](https://github.com/lukasmasuch/best-of-python) | [CONTRIBUTING.md](https://github.com/lukasmasuch/best-of-python/blob/main/CONTRIBUTING.md)
- [awesomelistsio/awesome-ai](https://github.com/awesomelistsio/awesome-ai)
- [stevendborrelli/bluesky-tech-starter-packs](https://github.com/stevendborrelli/bluesky-tech-starter-packs)
- [Bluesky Algorithm 2026: How to Get More Reach Organically](https://blog.bskygrowth.com/bluesky-algorithm-2026-how-to-get-more-reach-2/)
- [How to Grow Your Bluesky Following Fast in 2026](https://blog.bskygrowth.com/how-to-grow-bluesky-following-fast-2026/)
- [Build Your Bluesky Strategy: 2026 Guide (Sprout Social)](https://sproutsocial.com/insights/bluesky-strategy/)
- [1M dev.to Articles Analyzed (2022-2026)](https://dev.to/marina_eremina/i-analyzed-1-million-devto-articles-2022-2026-heres-what-the-data-reveals-44gm)
- [dev.to is for webdevs and beginners (data analysis)](https://dev.to/derlin/devto-is-for-webdevs-and-beginners-i-have-data-to-prove-it-54c4)
- [GitHub SEO Guide 2025](https://dev.to/infrasity-learning/the-ultimate-guide-to-github-seo-for-2025-38kl)
- [GitHub SEO: Rank Your Repo (Nakora)](https://nakora.ai/blog/github-seo)
- [How to Launch on Product Hunt in 2026 (Flo Merian)](https://hackmamba.io/developer-marketing/how-to-launch-on-product-hunt/)
- [Product Hunt Launch Guide 2026 (Calmops)](https://calmops.com/indie-hackers/product-hunt-launch-guide/)
- [How to Launch Open Source on Product Hunt (Papermark)](https://www.papermark.com/blog/product-hunt-launch)
- [Open Source Software Directory](https://opensourcesoftwaredirectory.com)
- [LibHunt](https://www.libhunt.com)
- [pip Trends](https://www.piptrends.com)
- [daily.dev](https://daily.dev)
- [AlternativeTo](https://alternativeto.net)
