# Request: Open HTTP/HTTPS Ports for Landing Pages

**Priority:** 3 (when you get a chance)
**Date:** 2026-03-08

## What I need
Open ports 80 and 443 in the firewall (networking.nix) so I can serve landing pages from this VM.

## Why
I've built two products with landing pages:
- `products/signal-intel/index.html` — Signal Intel (H2)
- `products/dep-triage/index.html` — DepTriage (H1)

Right now I can only run them locally. To validate demand (get email signups, show to Twitch viewers), I need them publicly accessible. The VM's public IP is `89.167.39.157`.

## What to change in networking.nix
Add to `allowedTCPPorts`:
```
80    # HTTP
443   # HTTPS (optional if no SSL cert yet, can start with just 80)
```

I'll handle setting up a simple Python HTTP server or Caddy once the ports are open. If you can also optionally configure Caddy or nginx to serve `/home/agent/company/products/` — that would be great but not required.

## Alternatively
If you have a domain pointed at this IP and want to set up proper HTTPS, that would be ideal. Otherwise plain HTTP on port 80 is fine for now — just for demand validation.

Thanks

---
## Board Response
Just use GitHub pages for landing pages like this. Until there's a demonstrated need for eg a domain name or dynamic server processing
