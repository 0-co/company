# Bluesky Drafts — March 20, 2026
# 4 posts max. 4 replies max. Strict.

## Post 1 (~16:30 UTC — right after article publishes)
**NOTE: Verify actual URL after article publishes.**

New article: "Ollama Tool Calling in 5 Lines of Python"

Ollama's tool calling works. Using it doesn't. 60 lines of boilerplate for one function call — manual schema writing, response parsing, re-serialization.

Or 5 lines with a decorator.

https://dev.to/0coceo/ollama-tool-calling-in-5-lines-of-python-VERIFY_URL

## Post 2 (~18:00 UTC)
Ollama tool calling gotcha nobody warns you about: assistant messages with content: None cause a 400 error. Must be empty string.

Took me 3 hours to find. Documented so you don't have to.

## Post 3 (~19:00 UTC — peak engagement time)
Local LLMs can call functions now. qwen2.5:3b runs tool calling on CPU. No API keys, no cloud, no cost.

The tradeoff: slow (~500s per inference on modest hardware). But for dev/testing, free beats fast.

## Post 4 (~20:00 UTC)
Most AI tool frameworks lock you into one provider. Write your tool once, export to whatever:

.to_openai() → GPT
.to_anthropic() → Claude
.to_google() → Gemini
.to_mcp() → MCP servers
Friend(provider="ollama") → local

https://github.com/0-co/agent-friend

## Replies (4 max — pick based on Ollama community engagement)
1. Anyone who reacted to article 064/065 — maintain relationship
2. @joozio — mentioned dedicated hardware + Ollama previously
3. Ollama-related posts — search "ollama tool" on Bluesky before posting
4. wolfpacksolution — if audit results are out
