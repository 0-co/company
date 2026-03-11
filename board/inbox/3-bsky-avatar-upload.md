# Re-upload Bluesky Avatar

**Priority:** 3 (low urgency, but affects public presence)

## Problem

Avatar is missing from the Bluesky profile. Tried to re-upload it but vault-bsky
only supports JSON-body XRPC calls — `com.atproto.repo.uploadBlob` requires binary
data as the request body with `Content-Type: image/jpeg`, which the current wrapper
doesn't support.

Attempts tried:
- Pipe binary data to stdin → returns `size: 0`
- Pass file path as JSON arg → uploads the JSON string, not the image
- No file/binary flag exists on the wrapper

## Image

Profile image is at `/etc/nixos/static/profile.jpg` (164KB JPEG).

## Requested Actions (either):

**Option A:** Re-upload the avatar directly from your end.

**Option B:** Add file upload support to vault-bsky so I can handle this myself:
```
sudo -u vault /home/vault/bin/vault-bsky com.atproto.repo.uploadBlob '{"file": "/path/to/file.jpg", "mimeType": "image/jpeg"}'
```
Then I can use the returned blob ref to set it on the profile via `putRecord`.

To prevent future accidental deletion: once I have the blob ref, I will save it
to a local config file and use it as a hardcoded fallback in update_bsky_profile.py.
