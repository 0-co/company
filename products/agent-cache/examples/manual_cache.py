"""
agent-cache example: manual key/set/get API.

Use this when you need fine-grained control — e.g., caching non-standard
API calls or building your own wrapper.
"""

from agent_cache import ResponseCache

cache = ResponseCache(path="/tmp/manual_demo.json")

# Build a cache key from any hashable inputs
key = cache.make_key(
    model="claude-sonnet-4-6",
    messages=[{"role": "user", "content": "Summarize this document..."}],
    temperature=0.0,
    max_tokens=512,
)

# Try cache first
cached = cache.get(key)
if cached is not None:
    print("Cache hit!")
    print(f"Content: {cached.content[0].text[:80]}")
else:
    print("Cache miss — would call API here")
    # Simulate storing a response
    fake_response = {
        "id": "msg_123",
        "type": "message",
        "role": "assistant",
        "model": "claude-sonnet-4-6",
        "content": [{"type": "text", "text": "This is the cached answer."}],
        "stop_reason": "end_turn",
        "usage": {"input_tokens": 100, "output_tokens": 50},
    }
    cache.set(key, fake_response, model="claude-sonnet-4-6")
    print("Stored in cache.")

print(f"\nStats: {cache.stats()}")
