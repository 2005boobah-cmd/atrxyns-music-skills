# Project format and commands

Resolve these scripts relative to this skill directory. The file paths below are examples, not existing assets.

```json
{
  "brand": "Nox FM",
  "title": "Song title",
  "audio": "song.mp3",
  "lyrics": "reviewed_cues.json",
  "width": 1920,
  "height": 1080,
  "fps": 24,
  "font": "/actual/path/to/regular-or-semibold-font.ttf",
  "font_bold": "/actual/path/to/bold-font.ttf",
  "scenes": [
    {"file": "scene_01.png", "duration": 20, "provenance": "generated"},
    {"file": "scene_02.mp4", "duration": 24, "provenance": "user"}
  ],
  "output": "NoxFM_Song_Title.mp4"
}
```

Omit `layout` for the centered badge style. The renderer automatically uses the bundled `assets/NFM_Brand_Emblem.png`. Add `"logo": "custom_emblem.png"` only to override it with user-requested artwork. The source PFP has a dark square background; the renderer clips it inside the fixed circular border. The default fallback is a simple Nox FM badge. Use `"layout": "ribbon"` for the earlier horizontal spectrum. Choose the layout explicitly when recreating an older project.

All paths resolve relative to the project file. Dimensions must be even. Use 1080×1920 for 9:16 and 1920×1080 for 16:9. Other ratios are supported but require manual composition review. Provide an actual installed regular and bold font path to avoid platform-dependent italic fallbacks.

Omit scene durations to distribute the full duration evenly. When durations are provided, provide all of them and ensure they sum to the audio length (within 0.15 seconds). Use actual local scene assets; no URL strings, guessed paths or placeholders. Images pan/zoom gently; videos are muted and can loop only within their assigned scene. Prefer a dedicated video long enough for the shot.

`lyrics` accepts a JSON array of reviewed cues:
```json
[
  {"start": 0.7, "end": 3.4, "text": "An exact sung line"},
  {"start": 4.1, "end": 7.3, "text": "The following sung line", "chorus": true}
]
```
Times are seconds. Include every actual sung line once per occurrence. Use literal newlines for intentional two-line captions. Do not leave null times or unresolved confidence flags. The renderer refuses those rather than silently guessing. Omit lyrics only when making a visualizer without captions.

```text
python scripts/lyric_timing.py --audio song.mp3 --lyrics lyrics.txt --out timing_candidates.json --cache model_cache
python scripts/render_video.py project.json --check
python scripts/render_video.py project.json --preview 12 --start 75 --output preview.mp4
python scripts/render_video.py project.json
```

The timing command saves candidate cues and a sibling report. Inspect and correct candidates, remove `needs_review` after actually resolving the relevant cue, then point the renderer at the reviewed JSON. All timestamps remain relative to the original full recording, including for a preview.

Use `--ffmpeg /actual/path/to/ffmpeg` if needed. The rendering command creates a task-local work directory beside the output, a final project snapshot, editable SRT and a preview JPG. Scene caches use content/config fingerprints to avoid re-rendering unchanged scenes. Revisions to captions only should reuse scenic clips. Do not include work directories or audio in a plugin archive.
