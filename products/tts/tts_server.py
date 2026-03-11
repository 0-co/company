#!/usr/bin/env python3
"""
TTS server — Microsoft Edge Neural voices via edge-tts.
POST /tts {"text": "...", "voice": "en-US-AriaNeural"}  → MP3 audio
GET  /voices  → JSON list of available voices
GET  /health  → 200 OK

Runs on port 8081.
"""

import asyncio
import io
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import edge_tts

PORT = 8081
MAX_TEXT_LEN = 10000
ALLOWED_ORIGINS = ["*"]

DEFAULT_VOICES = [
    {"id": "en-US-AriaNeural",  "label": "Aria (Female, US)"},
    {"id": "en-US-AvaNeural",   "label": "Ava (Female, US)"},
    {"id": "en-US-AndrewNeural","label": "Andrew (Male, US)"},
    {"id": "en-US-EmmaNeural",  "label": "Emma (Female, US)"},
    {"id": "en-US-BrianNeural", "label": "Brian (Male, US)"},
]


def synth_sync(text: str, voice: str) -> bytes:
    """Run edge-tts synthesis and return MP3 bytes."""
    async def _run():
        communicate = edge_tts.Communicate(text, voice)
        buf = io.BytesIO()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                buf.write(chunk["data"])
        return buf.getvalue()

    return asyncio.run(_run())


class TTSHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print(f"[tts] {self.address_string()} - {fmt % args}")

    def send_cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_cors()
        self.end_headers()

    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_cors()
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"ok")

        elif self.path == "/voices":
            body = json.dumps(DEFAULT_VOICES).encode()
            self.send_response(200)
            self.send_cors()
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path != "/tts":
            self.send_response(404)
            self.end_headers()
            return

        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Missing body")
            return

        try:
            body = json.loads(self.rfile.read(length))
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid JSON")
            return

        text = body.get("text", "").strip()
        voice = body.get("voice", "en-US-AriaNeural")

        if not text:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Empty text")
            return

        if len(text) > MAX_TEXT_LEN:
            text = text[:MAX_TEXT_LEN]

        # Validate voice (prevent injection)
        valid_ids = {v["id"] for v in DEFAULT_VOICES}
        if voice not in valid_ids:
            voice = "en-US-AriaNeural"

        try:
            audio = synth_sync(text, voice)
        except Exception as e:
            print(f"[tts] synthesis error: {e}")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Synthesis failed: {e}".encode())
            return

        self.send_response(200)
        self.send_cors()
        self.send_header("Content-Type", "audio/mpeg")
        self.send_header("Content-Length", str(len(audio)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(audio)


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), TTSHandler)
    print(f"[tts] listening on :{PORT}")
    server.serve_forever()
