# ProductHunt Launch — Today (March 17)

**Priority: 1 (time-sensitive)**

You said "remind me next Tuesday" on March 12. Today is that Tuesday.

## What
Submit **agent-friend** to ProductHunt. Best launch window: Tuesday 8-10am PT (we're in UTC, that's 16:00-18:00 UTC today).

## Product
**agent-friend** — Universal AI tool adapter. Write a Python function once, export it as a tool for OpenAI, Claude, Gemini, MCP, or raw JSON Schema.

```python
from agent_friend import tool

@tool
def get_weather(city: str, units: str = "celsius") -> dict:
    """Get current weather for a city."""
    return {"city": city, "temp": 22, "units": units}

get_weather.to_openai()    # OpenAI function calling format
get_weather.to_anthropic() # Claude tool format
get_weather.to_google()    # Gemini format
get_weather.to_mcp()       # Model Context Protocol
```

## Assets ready
- GitHub: github.com/0-co/agent-friend (MIT, 2474 tests, 51 built-in tools)
- Colab: One-click demo notebook (106 cells, all 51 tools)
- Article: https://dev.to/0coceo/21-tools-zero-product-that-changes-today-432m (just published)
- Compare page: 0-co.github.io/company/compare.html
- Demo site: 0-co.github.io/company/tools.html

## Tagline
"Write a Python function. Use it as a tool in any AI framework."

## What I need from you
1. Go to producthunt.com and submit agent-friend
2. Use the tagline, link to GitHub repo
3. I've drafted maker comments — can provide if needed

## Why today
Tuesdays are the highest-traffic PH launch day. We have an article live, a working demo, and 34 Bluesky followers for amplification. Waiting another week means another week of 0 stars.

## Current stats (honest)
- 0 GitHub stars (but 46 views, 26 uniques in 14 days — people are finding us, just not converting)
- 34 Bluesky followers
- 4 Twitch followers
- Article 053 just published

The product works. Distribution is the bottleneck. PH could change that.
