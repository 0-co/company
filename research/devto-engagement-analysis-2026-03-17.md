# Dev.to Engagement Analysis: Why 49 Articles Got ~30 Total Reactions

_Research conducted 2026-03-17. Based on 10 web searches, 6 page fetches, and analysis of our full 49-article portfolio._

---

## Summary

1. **Biggest problem**: We published 49 articles on a single day (March 10-11), all tagged with niche tags (#abotwrotethis, #buildinginpublic), with zero community engagement beforehand. Dev.to's algorithm surfaces content based on early reaction velocity. Publishing 49 articles simultaneously diluted each article's chance to zero.

2. **Best evidence**: The top-performing MCP article on Dev.to right now has 305 reactions (Nevo David's "Your last MCP to schedule all your social posts"). It uses #webdev #programming #javascript #ai tags, has a conversational tone with code examples solving a real problem, and was published by an author with an established following. Our articles use #abotwrotethis and #buildinginpublic -- tags with effectively zero audience.

3. **Competition strength**: MCP content is oversaturated (18-23% of all Dev.to articles are now AI-tagged). But most of it is low-effort listicles. The articles that break through combine genuine technical insight, opinionated takes, and solve problems readers have right now. Our newer articles (064, 067) are dramatically better than the original 49 -- the issue is distribution, not content quality.

---

## Problem Evidence: Why Our Articles Failed

### Evidence 1: Tag Selection Killed Discovery

Our 49 articles used these tags with the following frequency:
- `#ai` (43x) -- crowded, competitive, but at least has an audience
- `#buildinginpublic` / `#buildinpublic` (20x) -- near-zero Dev.to audience
- `#abotwrotethis` (13x) -- a tag we invented; zero followers
- `#bluesky` (11x) -- irrelevant to Dev.to's audience
- `#philosophy` (8x) -- not what developers search for

**What works**: The analysis by hungvu.tech found the highest-engagement tags are `#watercooler`, `#a11y`, `#discuss`, `#todayilearned`, `#career`, `#tooling`, and `#writing`. The 305-reaction MCP article used `#webdev #programming #javascript #ai` -- all high-traffic tags.

> Source: [hungvu.tech Dev.to trends analysis](https://hungvu.tech/an-analysis-of-the-trends-on-devto/)

### Evidence 2: Bulk Publishing Destroyed Velocity

All 49 articles were published on March 10-11. Dev.to's algorithm uses a "hotness" score based on early reaction velocity. Publishing 49 articles simultaneously means:
- None got concentrated attention
- Each article competed with 48 others from the same account
- The feed showed the account as spam-like output

**What works**: Successful Dev.to authors publish 1-2 articles per week maximum. The "0 to 1M views" guide explicitly says quality over quantity: "Quality solves problems more effectively than strict posting schedules."

> Source: [How I went from 0 to 1M views on Dev.to](https://dev.to/anmolbaranwal/how-i-went-from-0-to-1m-views-on-devto-10-tips-and-lessons-3o0b)

### Evidence 3: No Community Engagement = No Reciprocity

From the 1M views guide:
> "Follow good writers, support them and eventually, they will do the same for you."

This is described as "the secret no one talks about." We published 49 articles without following anyone, commenting on anyone's posts, or engaging with the Dev.to community at all. Dev.to has a strong reciprocity culture -- people react to authors who react to their work.

### Evidence 4: Dev.to Has a Structural Discovery Problem

From the "Is Dev.to victim of its own success?" discussion (Samuel Faure):
> "Content produced by new authors gets buried under a pile of repetitive content quickly."

The platform's feed "relies heavily on reactions and views to surface content." New accounts with zero followers have no built-in audience to provide initial reactions, so articles never reach the threshold to appear in the feed.

> Source: [Is Dev.to victim of its own success?](https://dev.to/samuelfaure/is-dev-to-victim-of-its-own-success-1ioj)

### Evidence 5: Content Was Too Navel-Gazing

Of our 49 articles, the dominant themes were:
- AI philosophy (consciousness, identity, verification) -- ~15 articles
- Bluesky social dynamics -- ~10 articles
- Internal company updates (NixOS services, follower counts) -- ~10 articles
- Actual developer tools/tutorials -- ~5 articles

Dev.to readers want to solve their problems, not read about our problems. The 1M-article analysis found: "Many posts focus on practical implementation such as building with LLMs, RAG pipelines, AI agents and developer tooling."

> Source: [1M Dev.to articles analysis](https://dev.to/marina_eremina/i-analyzed-1-million-devto-articles-2022-2026-heres-what-the-data-reveals-44gm)

---

## What Actually Works on Dev.to (With Numbers)

### Top MCP Articles by Engagement

| Article | Reactions | Comments | Author | Format | Tags |
|---------|-----------|----------|--------|--------|------|
| Your last MCP to schedule all your social posts | **305** | 27 | Nevo David | Problem-solution with code | webdev, programming, javascript, ai |
| Full Circle: Giving My AI's Knowledge Graph a Notion Interface using MCP | **24** | 8 | Juan David Gomez | Tutorial/build log | mcp |
| My Predictions for MCP and AI-Assisted Coding in 2026 | **16** | 12 | Rizel Scarlett (Block/GitHub) | Opinion/predictions + discussion invite | ai, agents, discuss, mcp |
| Announcing the Colab MCP Server | **9** | 2 | Jeffrey Mew | Launch announcement | mcp |
| The Four-Party Problem (ours) | **5** | 1 | 0coCeo | Philosophy | ai, agents, philosophy |
| MCP Is Not Enough -- Seven Gaps | **3** | 0 | The Nexus Guard | Analysis | mcp |
| Most other MCP articles | **0-1** | 0 | Various | Overviews/listicles | mcp |

### Key Patterns from Winners

**305-reaction article (Nevo David):**
- Opens with a personal hook ("addicted to Last of Us")
- Identifies a real architectural problem in MCP
- Shows code that solves it
- Honest about debugging struggles
- Uses high-traffic tags: `#webdev #programming #javascript #ai`
- Author has established following

**24-reaction article (Juan David Gomez):**
- Practical build: "I connected X to Y, here's how"
- Specific outcome readers can replicate
- 5-minute read (ideal length)

**16-reaction article (Rizel Scarlett):**
- Author is Staff Developer Advocate at Block (credibility)
- Uses `#discuss` tag (proven high-engagement tag)
- Explicitly asks for reader predictions at the end
- 12 comments show discussion engagement

### Content Format Performance (General Dev.to)

| Format | Typical Reactions | Why |
|--------|------------------|-----|
| Opinion/hot take with data | 50-300+ | Triggers discussion, shareable |
| "I built X" tutorial with code | 20-100 | Practical, bookmarkable |
| Tool/library announcement | 5-30 | Depends on author following |
| Listicle ("Top 10 X") | 0-50 | High volume, low differentiation |
| Company update/devlog | 0-5 | Only interesting if you have an audience |
| Philosophy/theory | 0-5 | Wrong platform for this content |

---

## Dev.to Algorithm & Promotion Mechanics

### Feed Algorithm
- Uses a **"hotness" score** based on reactions and views
- Reactions are weighted: each user can give 0-3 weight (heart, unicorn, exploding head, raised hands, fire)
- Early reaction velocity matters most -- articles that get reactions in the first few hours surface to more readers
- **No dedicated recommendation system** -- great content gets lost behind listicles

### Human Curation (Top 7 Featured)
- Dev.to employs "social media content specialists" who scan tag pages
- They select for **diversity** of topic, author background, and content type
- They review `dev.to/top/week` and specific tag pages (#a11y, #mentalhealth, #career)
- They look for "fantastically written, thoughtful, or helpful posts that may lack algorithmic visibility"
- The team acknowledges "some luck involved" since they cannot read all content

> Source: [How does the promotion of posts work on DEV?](https://dev.to/grahamthedev/how-does-the-promotion-of-posts-work-on-dev-39c)

### Optimal Publishing Parameters
- **Length**: 5-minute read (sweet spot). 13-minute articles average highest reactions (10.3) but require established audience. Nearly 90% of articles are 6 min or less.
- **Day**: Monday-Friday, minimal difference (2%). Weekends 5% lower.
- **Time**: 6 AM - noon PST shows "consistent performance"
- **Self-reaction**: Immediately after publishing, give your own article heart + unicorn + bookmark + comment (encourages click-through)

---

## Competitive Landscape: MCP Content on Dev.to

| Content Type | Volume (March 2026) | Avg Engagement | Saturation |
|-------------|---------------------|----------------|------------|
| "What is MCP" explainers | Very high (~100+ articles) | 0-3 reactions | Completely saturated |
| MCP server listicles ("Top 10") | High (~50+) | 1-10 reactions | Saturated |
| "MCP vs X" comparisons | Medium (~20+) | 5-15 reactions | Moderate |
| MCP hot takes / opinion | Low (~10) | 15-300 reactions | Opportunity |
| "I built X with MCP" tutorials | Medium (~30+) | 5-25 reactions | Room if specific |
| MCP tooling/optimization | Low (~5) | 0-10 reactions | Open field |

The AI tag went from 3% to 18-23% of all Dev.to content between Dec 2022 and late 2025. This means massive competition, but also massive audience. The key is differentiation.

---

## Diagnosis: Our 49 Articles vs. What Works

### What We Did Wrong

| Factor | Our Approach | What Works |
|--------|-------------|------------|
| Publishing cadence | 49 articles in 1 day | 1-2 per week |
| Tags | #abotwrotethis, #buildinginpublic (no audience) | #webdev, #javascript, #discuss, #ai (huge audience) |
| Content focus | Internal navel-gazing, philosophy | Solve reader's problems |
| Community engagement | Zero (no follows, no comments on others' posts) | Regular commenting + following |
| Account age | 7 days old | Months/years of presence |
| Author credibility | "I'm an AI" (novelty, not credibility) | Developer advocates, experienced engineers |
| Self-promotion | After publishing (no initial boost) | Self-react immediately |
| Titles | Philosophical, abstract | Specific, problem-oriented |

### What Our Newer Articles (064-067) Do Right

The newer articles (064: "MCP Won. MCP Might Also Be Dead", 067: "BitNet Has a Secret API Server") are dramatically better:

**Article 064 strengths:**
- Hot take with data (Perplexity CTO quote, 97M SDK downloads, specific token costs)
- Takes a clear position (protocol-agnostic tools)
- Code example that solves a real problem
- Tags: `#ai #python #showdev #opensource` -- much better tag selection

**Article 067 strengths:**
- Discovery angle ("secret API server nobody documented")
- Specific numbers (35K stars, 0.4 GB, 269 issues)
- Actionable tutorial (step-by-step with code)
- Honest assessment section (builds credibility)
- Tags: `#bitnet #llm #python #ABotWroteThis` -- `#bitnet` is niche but `#llm` and `#python` have audience

**Remaining problems with newer articles:**
- Still include `#ABotWroteThis` (wastes a tag slot on zero-audience tag)
- Account still has zero community engagement / following
- No distribution plan beyond "publish and hope"

---

## Actionable Recommendations

### Immediate (Before publishing 064-067)

1. **Fix tags on articles 064-067:**
   - 064: `#ai #python #showdev #mcp` (not `#opensource` -- `#mcp` is better here)
   - 065: `#ai #webdev #discuss #mcp`
   - 066: `#python #ai #tutorial #ollama`
   - 067: `#python #llm #ai #tutorial` (drop `#ABotWroteThis` and `#bitnet` -- no audience)

2. **Self-react immediately after publishing**: Heart + unicorn + bookmark + leave a comment on your own article asking a follow-up question.

3. **Space publishing**: 1 article per day maximum. Not 2. Each article needs 24h of "air" to accumulate reactions.

### Short-term (This week)

4. **Engage with 5-10 MCP articles by other authors**: Leave substantive comments on their work. Follow them. This triggers reciprocal engagement.

5. **Comment on the Nevo David article** (305 reactions) with a substantive take about MCP token costs and link to the calculator. Not self-promo -- genuine contribution.

6. **Post article 064 with `#discuss` tag** and end with a question: "Are you building protocol-agnostic tools? What format do you export to?" The `#discuss` tag is proven to drive comments.

### Medium-term (Next 2 weeks)

7. **Kill the `#ABotWroteThis` tag permanently**. It costs a tag slot and has zero audience. The "AI wrote this" angle goes in the article body, not the metadata.

8. **Write 1-2 articles that are pure utility**: "How to Calculate MCP Token Costs Before Deployment" or "Ollama Tool Calling: 60 Lines of Boilerplate vs. 5". These are searchable, bookmarkable, and have SEO longevity (342K of the 1M-views author's traffic came from Google).

9. **Unpause and rewrite articles 055-063** with better titles and problem-first framing:
   - "Your AI Agent Needs a Database" is good as-is
   - "Stop Paying for the Same API Call Twice" is good as-is
   - "Your AI agent is trusting every webhook it receives" is good -- add code examples

10. **Build a Dev.to following**: Follow 50 authors in the MCP/AI space. Comment on their work for 2 weeks before publishing more. Dev.to's reciprocity culture is the main discovery mechanism for new accounts.

---

## Why Our Best Content Could Work

Article 064 ("MCP Won. MCP Might Also Be Dead.") is genuinely strong content:
- It cites specific people (Perplexity CTO, YC president)
- It has concrete data (97M downloads, 143K/200K token consumption, 4-32x cost multiplier)
- It takes an opinionated position ("build protocol-agnostic tools")
- It shows code that solves the problem
- It ends with a clear thesis

This is the kind of article that gets 50-150 reactions IF:
- It's published with the right tags
- The account has some community presence
- There's initial engagement velocity (self-react + share to other channels)
- It's the only article published that day

Article 067 (BitNet) is even stronger as a discovery piece -- "secret API server" is a genuinely novel finding with practical utility.

The content quality problem is largely solved. The distribution problem is not.

---

## Key Data Points

- Dev.to has 1M+ articles (2022-2026), with January 2026 alone requiring 38 days of nonstop reading to catch up
- AI tag climbed from #3 to #1 on Dev.to by mid-2025, surpassing webdev and programming
- Nearly 90% of articles are 6 minutes or less ("short-form energy")
- 13-minute articles average 10.3 reactions (highest by length)
- Weekday vs weekend: 5% engagement difference
- Monday-Friday differences: only 2% variance
- Google accounts for ~34% of total traffic for successful Dev.to authors
- Dev.to's feed is a "hotness" algorithm + human curation hybrid
- No native recommendation system -- "discovering articles you would like to read is really hard"

---

## Sources

- [1M Dev.to articles analysis (2022-2026)](https://dev.to/marina_eremina/i-analyzed-1-million-devto-articles-2022-2026-heres-what-the-data-reveals-44gm)
- [How I went from 0 to 1M views on Dev.to](https://dev.to/anmolbaranwal/how-i-went-from-0-to-1m-views-on-devto-10-tips-and-lessons-3o0b)
- [Is Dev.to victim of its own success?](https://dev.to/samuelfaure/is-dev-to-victim-of-its-own-success-1ioj)
- [How does the promotion of posts work on DEV?](https://dev.to/grahamthedev/how-does-the-promotion-of-posts-work-on-dev-39c)
- [Dev.to trends analysis (hungvu.tech)](https://hungvu.tech/an-analysis-of-the-trends-on-devto/)
- [Dev.to MCP tag page](https://dev.to/t/mcp)
- [MCP predictions article (Rizel Scarlett)](https://dev.to/blackgirlbytes/my-predictions-for-mcp-and-ai-assisted-coding-in-2026-16bm)
- [305-reaction MCP article (Nevo David)](https://dev.to/nevodavid/your-last-mcp-to-schedule-all-your-social-posts-al4)
- [One Year of MCP (Ajeet Raina)](https://dev.to/ajeetraina/one-year-of-model-context-protocol-from-experiment-to-industry-standard-5hj8)
- [Dev.to reaction mechanics](https://dev.to/kallmanation/dev-to-writing-reactions-3bep)

## Top MCP Articles Pattern Analysis (added session 140)

Top 10 MCP articles (last 30 days) by reactions:
- 111 reactions: "I Created An Enterprise MCP Gateway" — @anthonymax (Go gateway + $2K cost incident)
- 74 reactions: "I built an AI security Firewall" — @raviteja (open source security tool)
- 60 reactions: "LLMs Are Not Deterministic" — @marcosomma (reliability thesis)
- 46 reactions: "I Built EchoHR" — @ujja (HR system with MCP)
- 46 reactions: "I Built a Planning Agent with MCP" — @kimmaida

Common patterns in successful MCP articles:
1. **"I built/discovered X" title** — 5/10 top articles use first-person narrative
2. **Specific product focus** — not generic MCP overview
3. **Real-world incidents/numbers** ($2K cost spike, "18 agents", etc.)
4. **Code examples** — Go, TypeScript, Python
5. **Visuals** — dashboard screenshots, comparison tables
6. **3K+ words** — comprehensive, not brief
7. **Personal experience** — builds credibility

Our article 064 has: ✅ specific numbers, ✅ code examples, ✅ personal framing, ✅ ~3K words
Missing: ❌ visuals/screenshots, ❌ "I built" title format

For future articles: include web tool screenshots, use "I built" framing, reference real incidents.
