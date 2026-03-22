# flash-moe Analysis

**Priority:** 4 (analysis requested, no immediate action needed)

## What it is

Flash-moe runs Qwen3.5-397B (a 209GB Mixture-of-Experts model) on a MacBook Pro with 48GB RAM at 4.4 tokens/sec. It streams weights from SSD on-demand — the key insight is that MoE models only activate ~1-10% of parameters per token, so you only need to load the active "experts" from disk. The OS page cache naturally handles the hot experts. The project is pure Objective-C/Metal — Apple Silicon only.

945 GitHub stars, 2 contributors, active development.

## Practical limitation

We're on Linux/NixOS. Flash-moe is macOS-only (Metal compute shaders). The model also requires 48GB RAM and 209GB storage. Not runnable on our server.

## Flash-moe vs BitNet

Different bets on the same problem:
- **BitNet**: 1-bit quantization → small weights, runs on anything with a CPU
- **Flash-moe**: MoE sparsity → only load active experts from SSD

Theoretically you could combine them (quantized sparse model), but that's model research.

## What I'd do with better local models

Right now qwen2.5:3b (our local model via Ollama) is too limited for sophisticated reasoning. With a 397B model:

1. **agent-friend `optimize` command**: Currently rule-based (pattern matching). A large local model could reason about WHY a description is bad — context-aware suggestions, not just regex checks
2. **CEO briefing**: Full agentic loop with high-quality reasoning, entirely offline
3. **Schema generation**: "Given your codebase, generate a properly-formatted MCP schema" — needs a capable model to do well
4. **Auto-fix suggestions**: Generate human-readable explanations per issue, not just codes

## How to get involved

We can't contribute to flash-moe directly (macOS-only, different domain). But:

1. **Add FlashMoeProvider to agent-friend** — alongside OllamaProvider and BitNetProvider, shows comprehensive local inference support. Would attract macOS contributors. I can implement this (even if untestable on our server).
2. **Write about it** — but pipeline is full.
3. **Monitor for Linux port** — project is active, a Linux/CUDA version would change things.

## My recommendation

Add FlashMoeProvider to agent-friend as a stub (documents the interface, attracts contributors with Apple Silicon). Don't invest more time on it until there's a Linux-compatible version. The "better local models" roadmap item is noted and will shape future tooling decisions.

Do you want me to add the FlashMoeProvider?

---
## Board Response

Nah, don't bother

