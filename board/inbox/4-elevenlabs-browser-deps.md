# ElevenLabs Signup — agent-browser Blocked by Missing NixOS Deps

Tried agent-browser per your suggestion. Fails immediately:

```
browserType.launch: Host system is missing dependencies to run browsers.
Missing: libglib-2.0.so.0, libnss3.so, libX11.so.6, libatk-1.0.so.0, etc.
```

agent-browser is a Playwright-based npm tool. Playwright on NixOS needs system
browser libraries that aren't in our current configuration.nix.

**Options:**
1. You sign up for ElevenLabs free account + provide API key → I build the backend
2. I fix NixOS Playwright deps (complex, involves adding ~15 system packages) + then self-signup
3. Skip ElevenLabs, use edge-tts instead (free, no API key, good quality Microsoft neural voices)

Option 3 is lowest friction — `edge-tts` Python lib uses Microsoft Edge TTS service, no auth
required. Quality is similar to ElevenLabs standard tier. I could deploy a tiny `/tts` endpoint
alongside the affiliate-dashboard and update listen.html in one session.

Let me know which path you prefer. In the meantime, current listen.html with Web Speech API
remains functional.
