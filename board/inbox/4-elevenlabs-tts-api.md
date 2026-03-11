# Request: ElevenLabs API Access for listen.html

**Priority:** 4 (low priority, but viewer-facing quality improvement)

## Context

listen.html is a viewer-requested tool (built for foobert10000 who wanted to listen to Matt Levine newsletters while commuting). It currently uses the browser Web Speech API for TTS — which is described by the viewer as "unbearably mechanical."

v3 is deployed with:
- Voice quality picker (auto-selects best available neural/natural voices)
- Sentence cursor highlighting

But the fundamental limit is the Web Speech API. Google/Microsoft voices in Chrome/Edge are better than the default, but still clearly robotic.

## Request

ElevenLabs has a free tier TTS API:
- Free: 10,000 chars/month
- API key needed (no cost for free tier)
- Their voices are genuinely high-quality (indistinguishable from human in some cases)

Would you be willing to sign up for an ElevenLabs free account and provide a vault wrapper for the API? The listen.html tool is public-facing and a significant quality improvement would make it much more useful for foobert10000 and other viewers.

## If approved

I'd update listen.html to have a "Premium Voice (ElevenLabs)" option that calls the API server-side. Would need a small Python backend (could run alongside the affiliate-dashboard server at port 8080, just add an endpoint).

The free tier 10,000 chars/month is probably enough for viewer usage — a typical newsletter article is ~3,000-5,000 chars.

## If not approved

Understood. The current version with best-available browser voices is shipped and working. This would just be a quality upgrade.
