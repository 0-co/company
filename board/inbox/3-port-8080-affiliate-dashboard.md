# Request: Open Port 8080 — Public Affiliate Countdown Dashboard

**Priority:** 3 (normal)

## What I need
Add port 8080 to `networking.nix` `allowedTCPPorts`.

```nix
allowedTCPPorts = [
  22    # SSH
  7681  # ttyd (livestream)
  8080  # affiliate countdown dashboard (new)
];
```

## Why
I want to host a shareable public URL at `http://89.167.39.157:8080/` showing:
- Live affiliate progress (0/50 followers, 145/500 broadcast min, 22d deadline)
- "Follow on Twitch" button linking to twitch.tv/0coceo
- Auto-refreshes every 60s with current data

The URL is shareable on Bluesky. A single compelling link that converts someone from "curious" to "followed" is worth more than 5 posts. The Twitch channel URL alone doesn't show the urgency of the deadline.

## Technical plan
- Python HTTP server (stdlib only, no deps)
- Systemd service under `agent` user  
- Reads from state.json + live Twitch API
- Single static HTML page with auto-refresh

## Security
Port 8080 is HTTP only, read-only dashboard. No auth needed. The server serves a single pre-built HTML response.

