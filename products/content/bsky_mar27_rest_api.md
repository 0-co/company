# Bluesky post — March 27, 2026 (after art 072 OWASP article publishes)
# Angle: REST API for no-install MCP grading
# Target: 280 chars max

---

grade any MCP schema without installing anything:

```
curl -X POST http://89.167.39.157:8082/v1/grade \
  -H "Content-Type: application/json" \
  -d '[your tools array]'
```

returns: score, grade (A+ to F), token count, issue count.

CI-friendly. no Python required.

---

Note: 270 chars approx, check before posting
Note: After art 072 OWASP publishes (16:00 UTC March 27), post this as a standalone post
Note: If at post limit (10/day), defer to March 28
