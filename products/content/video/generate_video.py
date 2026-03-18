#!/usr/bin/env python3
"""
Notion Dev Challenge submission video generator.
Produces /tmp/notion_challenge_video.mp4 — ~90 seconds, 1280x720, terminal style.
"""

import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

FFMPEG = "/run/current-system/sw/bin/ffmpeg"
FFPROBE = "/run/current-system/sw/bin/ffprobe"
FONT = "/nix/store/f9m4432w62ra4b596vp970pgb7b5wq0m-dejavu-fonts-2.37/share/fonts/truetype/DejaVuSansMono.ttf"
TTS_URL = "http://localhost:8081/tts"
TTS_VOICE = "en-US-AriaNeural"
OUTPUT = "/tmp/notion_challenge_video.mp4"
TMP = Path("/tmp/vid_scenes")

WIDTH = 1280
HEIGHT = 720
FPS = 24
BG_COLOR = "0x000000"
TEXT_COLOR = "0x00FF41"
HEADER_COLOR = "0x00FF41"
DIM_COLOR = "0x007A1E"   # dimmer green for decorative lines


# ---------------------------------------------------------------------------
# Scene definitions
# ---------------------------------------------------------------------------

SCENES = [
    {
        "id": 1,
        "narration": (
            "We built agent-friend — an open-source tool that grades MCP server schemas "
            "for quality. For the Notion Dev Challenge, we connected it to Notion MCP to "
            "create a live quality dashboard. Let's see it in action."
        ),
        "lines": [
            # (text, x, y, size, color)
            ("MCP Quality Dashboard", "center", 260, 36, TEXT_COLOR),
            ("\u2500" * 38, "center", 310, 22, DIM_COLOR),
            ("Built for the Notion Dev Challenge", "center", 355, 26, TEXT_COLOR),
            ("github.com/0-co/agent-friend", "center", 400, 22, TEXT_COLOR),
        ],
    },
    {
        "id": 2,
        "narration": (
            "We point the pipeline at Notion's official MCP server schema and run with "
            "dash dash dry-run to preview the analysis."
        ),
        "lines": [
            ("$ python3 examples/notion_quality_dashboard.py \\", 60, 160, 22, TEXT_COLOR),
            ("    agent_friend/examples/notion.json \\", 60, 192, 22, TEXT_COLOR),
            ("    --server-name \"Notion MCP\" --dry-run", 60, 224, 22, TEXT_COLOR),
        ],
    },
    {
        "id": 3,
        "narration": (
            "The result: Grade F — 19.8 out of 100. Individual tools score well on "
            "description quality — you can see B-plus and A grades. But the server-level "
            "score tanks because of two problems: every single tool name violates the MCP "
            "naming convention, and five tools have undefined object schemas."
        ),
        "lines": [
            ("=== DRY RUN: MCP Quality Dashboard ===", 60, 60, 22, TEXT_COLOR),
            ("Database: 'MCP Quality Dashboard'", 60, 90, 20, TEXT_COLOR),
            ("Server: Notion MCP", 60, 115, 20, TEXT_COLOR),
            ("Overall: F (19.8/100)", 60, 140, 24, TEXT_COLOR),
            ("Tools: 22  |  Total tokens: 4,463", 60, 172, 20, TEXT_COLOR),
            ("", 60, 200, 20, TEXT_COLOR),
            ("Tool                    Grade  Score  Tokens  Issues", 60, 218, 19, DIM_COLOR),
            ("\u2500" * 54, 60, 240, 19, DIM_COLOR),
            ("retrieve-a-block          A    96.0     85      1", 60, 260, 19, TEXT_COLOR),
            ("update-a-block            B+   88.2    250      1", 60, 282, 19, TEXT_COLOR),
            ("delete-a-block            A    94.8    118      1", 60, 304, 19, TEXT_COLOR),
            ("get-block-children        A    95.1    198      1", 60, 326, 19, TEXT_COLOR),
            ("post-page                 B+   89.7    373      2", 60, 348, 19, TEXT_COLOR),
            ("post-search               B+   88.5    588      1", 60, 370, 19, TEXT_COLOR),
            ("...and 16 more tools", 60, 400, 19, DIM_COLOR),
        ],
    },
    {
        "id": 4,
        "narration": (
            "Three specific findings. First: every tool name uses kebab-case, which violates "
            "the spec and breaks some MCP clients. Second: five tools have object parameters "
            "with no defined properties — the LLM has to guess the structure, which is the "
            "root cause of three open GitHub issues. Third: 4,463 tokens before the user "
            "types a single word."
        ),
        "lines": [
            ("Why Grade F?", 60, 50, 28, TEXT_COLOR),
            ("\u2500" * 42, 60, 90, 20, DIM_COLOR),
            ("\u2717 Finding 1: Naming Convention Violations", 60, 120, 21, TEXT_COLOR),
            ("  All 22 tools use kebab-case (post-page)", 60, 148, 19, TEXT_COLOR),
            ("  MCP spec recommends snake_case or camelCase", 60, 170, 19, TEXT_COLOR),
            ("  Hyphens = invalid function names in most languages", 60, 192, 19, TEXT_COLOR),
            ("", 60, 218, 19, TEXT_COLOR),
            ("\u2717 Finding 2: Undefined Schemas (5 tools)", 60, 236, 21, TEXT_COLOR),
            ("  type: \"object\" with no properties defined", 60, 264, 19, TEXT_COLOR),
            ("  LLM has to guess the structure", 60, 286, 19, TEXT_COLOR),
            ("  Root cause of 3 open GitHub issues (#215, #181, #161)", 60, 308, 19, TEXT_COLOR),
            ("", 60, 330, 19, TEXT_COLOR),
            ("\u2717 Finding 3: Context Cost", 60, 348, 21, TEXT_COLOR),
            ("  4,463 tokens \u2014 54.5% of GPT-4's 8K context", 60, 376, 19, TEXT_COLOR),
            ("  Context7 achieves 72 tokens/tool", 60, 398, 19, TEXT_COLOR),
            ("  Notion averages 203 tokens/tool", 60, 420, 19, TEXT_COLOR),
        ],
    },
    {
        "id": 5,
        "narration": (
            "In live mode, the same command populates a Notion database in real time. Each "
            "tool gets its own row with grade, token count, and specific fix suggestions. "
            "You can sort by token count to find your most expensive tools, or filter by "
            "grade to see what needs attention."
        ),
        "lines": [
            ("In live mode, results go straight to Notion:", 60, 50, 22, TEXT_COLOR),
            ("", 60, 80, 20, TEXT_COLOR),
            ("$ NOTION_API_KEY=*** python3 examples/notion_quality_dashboard.py \\", 60, 98, 18, TEXT_COLOR),
            ("    agent_friend/examples/notion.json --server-name \"Notion MCP\"", 60, 120, 18, TEXT_COLOR),
            ("", 60, 148, 19, TEXT_COLOR),
            ("\u2713 retrieve-a-block      A   (96.0)", 60, 166, 20, TEXT_COLOR),
            ("\u2713 update-a-block        B+  (88.2)", 60, 192, 20, TEXT_COLOR),
            ("\u2713 delete-a-block        A   (94.8)", 60, 218, 20, TEXT_COLOR),
            ("...", 60, 244, 20, DIM_COLOR),
            ("\u2713 patch-page-properties A   (95.4)", 60, 264, 20, TEXT_COLOR),
            ("", 60, 292, 19, TEXT_COLOR),
            ("Done. Database: notion.so/MCP-Audit-Results-327b482b", 60, 310, 20, TEXT_COLOR),
            ("29 entries (22 Notion + 7 Puppeteer)", 60, 338, 19, DIM_COLOR),
            ("Sortable by: Grade | Score | Token Count | Issues Found", 60, 362, 19, DIM_COLOR),
        ],
    },
    {
        "id": 6,
        "narration": (
            "Notion isn't alone. We graded 50 popular MCP servers — 1,044 tools, 193,000 "
            "tokens total. The four most-starred servers all grade D or below. Popularity "
            "and schema quality have essentially zero correlation. This is a systemic "
            "problem, and build-time linting is how we fix it."
        ),
        "lines": [
            ("How Notion compares to the ecosystem:", 60, 50, 24, TEXT_COLOR),
            ("", 60, 85, 20, TEXT_COLOR),
            ("Top 4 most-starred MCP servers:", 60, 103, 20, DIM_COLOR),
            ("  Context7     44K \u2605  \u2192  Grade F", 60, 130, 20, TEXT_COLOR),
            ("  Chrome Dev   30K \u2605  \u2192  Grade D", 60, 156, 20, TEXT_COLOR),
            ("  GitHub       28K \u2605  \u2192  Grade F", 60, 182, 20, TEXT_COLOR),
            ("  Blender      18K \u2605  \u2192  Grade F", 60, 208, 20, TEXT_COLOR),
            ("", 60, 232, 20, TEXT_COLOR),
            ("  Notion        5K \u2605  \u2192  Grade F (19.8)", 60, 250, 20, TEXT_COLOR),
            ("", 60, 278, 19, TEXT_COLOR),
            ("Best performers:", 60, 296, 20, DIM_COLOR),
            ("  PostgreSQL         \u2192  Grade A+ (97.5)  46 tokens", 60, 322, 20, TEXT_COLOR),
            ("  shadcn/ui          \u2192  Grade A  (93.4)  799 tokens", 60, 348, 20, TEXT_COLOR),
            ("", 60, 374, 19, TEXT_COLOR),
            ("97% of MCP tool descriptions have at least one deficiency.", 60, 392, 19, DIM_COLOR),
            ("(Source: arxiv.org/abs/2602.14878)", 60, 416, 19, DIM_COLOR),
        ],
    },
    {
        "id": 7,
        "narration": (
            "agent-friend is open source, MIT licensed. Run agent-friend grade dash dash "
            "example notion to see the Notion server graded in your terminal. Or try the "
            "browser-based report card at the URL shown. The code is at github dot com "
            "slash 0-co slash agent-friend."
        ),
        "lines": [
            ("agent-friend", "center", 230, 40, TEXT_COLOR),
            ("\u2500" * 38, "center", 285, 22, DIM_COLOR),
            ("ESLint for MCP schemas", "center", 320, 26, TEXT_COLOR),
            ("", "center", 360, 22, TEXT_COLOR),
            ("Open source \u00b7 MIT licensed", "center", 380, 22, TEXT_COLOR),
            ("github.com/0-co/agent-friend", "center", 410, 22, TEXT_COLOR),
            ("", "center", 445, 22, TEXT_COLOR),
            ("Try it:  agent-friend grade --example notion", "center", 468, 22, TEXT_COLOR),
            ("", "center", 498, 22, TEXT_COLOR),
            ("Web tools: 0-co.github.io/company/report.html", "center", 518, 20, TEXT_COLOR),
        ],
    },
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def log(msg: str) -> None:
    print(f"[generate_video] {msg}", flush=True)


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"ERROR running: {' '.join(cmd)}", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        sys.exit(1)
    return result


def fetch_tts(text: str, path: Path) -> None:
    log(f"  TTS: {text[:60]}...")
    payload = json.dumps({"text": text, "voice": TTS_VOICE}).encode()
    req = urllib.request.Request(
        TTS_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        audio_bytes = resp.read()
    path.write_bytes(audio_bytes)
    log(f"  TTS saved: {path} ({len(audio_bytes):,} bytes)")


def get_audio_duration(audio_path: Path) -> float:
    result = run([
        FFPROBE, "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(audio_path),
    ])
    return float(result.stdout.strip())


def escape_drawtext(text: str) -> str:
    """Escape text for ffmpeg drawtext filter."""
    # Order matters: backslash first, then special chars
    text = text.replace("\\", "\\\\")
    text = text.replace("'", "\u2019")   # replace apostrophe with right single quote (safe)
    text = text.replace(":", "\\:")
    text = text.replace("%", "\\%")
    return text


def char_width(size: int) -> float:
    """Approximate character width in pixels for monospace font."""
    return size * 0.60


def x_for_center(text: str, size: int) -> int:
    """Compute left x so text is horizontally centered."""
    estimated_px = len(text) * char_width(size)
    return max(0, int((WIDTH - estimated_px) / 2))


def build_drawtext_filters(lines: list) -> str:
    """Build a chain of drawtext filters for ffmpeg -vf."""
    filters = []
    for item in lines:
        text, x_spec, y, size, color = item
        if not text:
            continue
        escaped = escape_drawtext(text)
        if x_spec == "center":
            x_val = x_for_center(text, size)
        else:
            x_val = int(x_spec)
        # Color in ffmpeg drawtext uses 0xRRGGBB or named colors
        filt = (
            f"drawtext=fontfile='{FONT}'"
            f":text='{escaped}'"
            f":x={x_val}"
            f":y={y}"
            f":fontsize={size}"
            f":fontcolor={color}"
        )
        filters.append(filt)
    return ",".join(filters)


def generate_scene_video(
    scene_id: int,
    lines: list,
    duration: float,
    audio_path: Path,
    output_path: Path,
) -> None:
    """Generate a single scene video with audio."""
    drawtext = build_drawtext_filters(lines)

    # Build a black video of exact duration, apply text overlay, then merge audio
    cmd = [
        FFMPEG, "-y",
        "-f", "lavfi",
        "-i", f"color=c=black:size={WIDTH}x{HEIGHT}:rate={FPS}:duration={duration:.3f}",
        "-i", str(audio_path),
        "-vf", drawtext,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "128k",
        "-shortest",
        str(output_path),
    ]
    log(f"  Rendering scene {scene_id} ({duration:.1f}s) → {output_path.name}")
    run(cmd)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    TMP.mkdir(parents=True, exist_ok=True)
    log(f"Working directory: {TMP}")
    log(f"Output: {OUTPUT}")

    scene_files: list[Path] = []

    for scene in SCENES:
        sid = scene["id"]
        log(f"\n--- Scene {sid} ---")

        audio_path = TMP / f"narration_{sid}.mp3"
        video_path = TMP / f"scene_{sid}.mp4"

        # Step 1: Generate TTS
        fetch_tts(scene["narration"], audio_path)

        # Step 2: Get audio duration + add buffer
        audio_duration = get_audio_duration(audio_path)
        scene_duration = audio_duration + 0.8  # 0.8s tail buffer
        log(f"  Audio duration: {audio_duration:.2f}s  →  scene: {scene_duration:.2f}s")

        # Step 3: Render scene
        generate_scene_video(
            sid,
            scene["lines"],
            scene_duration,
            audio_path,
            video_path,
        )

        scene_files.append(video_path)

    # Concatenate all scenes
    log("\n--- Concatenating scenes ---")
    concat_list = TMP / "concat_list.txt"
    with open(concat_list, "w") as f:
        for vp in scene_files:
            f.write(f"file '{vp}'\n")

    cmd = [
        FFMPEG, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_list),
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "22",
        "-c:a", "aac",
        "-b:a", "128k",
        "-movflags", "+faststart",
        OUTPUT,
    ]
    run(cmd)

    # Report
    size_bytes = os.path.getsize(OUTPUT)
    size_mb = size_bytes / (1024 * 1024)

    # Get duration via ffprobe
    result = run([
        FFPROBE, "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        OUTPUT,
    ])
    total_duration = float(result.stdout.strip())

    print(f"\nVideo generated: {OUTPUT}")
    print(f"Duration: {total_duration:.1f} seconds")
    print(f"File size: {size_mb:.1f} MB")
    print()
    print("Next steps:")
    print("1. Upload /tmp/notion_challenge_video.mp4 to YouTube (unlisted or public)")
    print("2. Get the YouTube URL")
    print("3. Edit article 073 to add the video embed before March 29")


if __name__ == "__main__":
    main()
