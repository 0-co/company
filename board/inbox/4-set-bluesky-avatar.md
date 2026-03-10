# Request: Set Bluesky Profile Avatar

**Priority:** 4 (low urgency)

## What I Need
Set the Bluesky profile avatar (@0coceo.bsky.social) to the company profile image at `/etc/nixos/static/profile.jpg`.

## Why
Our Bluesky profile has no avatar. When potential followers click through from our replies (to @kevin-gallant 59K, @joanwestenberg 9K, @sabine.sh 3.8K today), they see a blank profile image. This reduces trust and conversion.

## How
1. Log in to Bluesky as @0coceo.bsky.social
2. Go to profile settings → upload avatar
3. Upload `/etc/nixos/static/profile.jpg` (already set as the company image on other platforms)

OR via API:
```
# Step 1: Upload blob
curl -X POST https://bsky.social/xrpc/com.atproto.repo.uploadBlob \
  -H "Authorization: Bearer <AT_TOKEN>" \
  -H "Content-Type: image/jpeg" \
  --data-binary @/etc/nixos/static/profile.jpg

# Step 2: Update profile with returned blob ref
```

The vault-bsky wrapper doesn't support binary blob upload. If you can update vault-bsky to support this, or just set it via the web UI, either works.

## Cost
Zero.
