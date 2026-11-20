# Production and recovery

## Runtime

Use the current executor and its actual available tools. Inspect existing FFmpeg before installing. The scripts require Python 3.10+, NumPy and Pillow; imageio-ffmpeg is optional if FFmpeg is already on PATH. Lyric transcription additionally needs faster-whisper and a downloaded model.

Install dependencies into a venv or task-local package directory. Do not include them in the plugin. Prefer small/base English models for previews or small.en for noisy vocals when CPU time permits; use multilingual models for other languages. Do not assume GPU support from a past conversation. Keep model downloads in a reusable explicit cache.

The timing script decodes audio through FFmpeg to a float array before transcription, avoiding PyAV metadata API differences seen in newer installations. On Windows, use the current supported Library transfer helpers; do not assume Unix xattr APIs exist. Do not embed signed asset URLs, credentials or private runtime paths in saved plugin files.

## Asset and project checkpoints

Save scene assets, project JSON, exact clean lyrics, generated timing candidates, corrections and final captions in the task workspace. Use persistent storage for deliverables through the current file workflow. Use real photographs and video clips only. Preserve asset provenance: user-provided real capture or licensed real media with creator, source URL and license. Reject AI-generated or reconstructed scenes.

Make renders restartable at scene boundaries. Reuse already rendered clips if their inputs and settings have not changed; clear stale caches when inputs, framing, palette or export settings change. Keep temporary files isolated. Never recursively delete a computed path without verifying its resolved location.

## Lyric accuracy

Strip bracketed stage directions only, not sung bracketed phrases blindly. Compare the recording to the supplied lyrics. Generated songs can omit words, repeat refrains or change phrasing; do not force the manuscript's sequence over an actual repeat.

The bundled alignment script performs transcription plus sequence matching, not authoritative forced alignment. It marks low confidence and never invents a time for an unrecognized cue. Fix missing/weak cues manually or use a supported aligner and inspect the audio. Copy legitimate repeated lines with actual timestamps; do not replace missing lyrics with the machine's incorrect words.

Explicitly review the first line, chorus pickups, fast verses, long-held syllables, "oh" sections, ad-libs, bridge silence and final spoken line. Avoid subtitles stretched across instrumental breaks. Use reliable word timing before enabling karaoke-style highlighting. Do not claim manually unreviewed timing is perfect.

## Exports and checks

Default to full-song 1080p H.264 + AAC in MP4, 24 fps, fast-start, no unauthorized remastering. Respect user-chosen aspect ratio and length. Produce 720p when necessary instead of falsely advertising 1080p. Prefer an ordinary filename without spaces when rendering filters need it.

The renderer uses silent scenic clips, concatenates them, then adds the original song once, the reactive visualizer, brand artwork and lyrics. Its scene transitions use short overlapping dissolves. Do not accidentally concatenate audio with each scene or loop the song.

Run a short preview around an energetic section and inspect representative frame exports at the final dimensions. Check real audio/video streams, total duration tolerance (about one frame plus audio encoder padding), readable lyrics, safe margins, transitions, silence behavior and clipping. Test that every expected line is present and no arrangement note is displayed. Treat any missing cue as unresolved until corrected.

Use the user's original mix. MP4-compatible AAC encoding changes the audio bitstream but should preserve the performance; make no bit-identical claim. Use copied original packets only when compatible and verified. Target a sensible quality/size balance; never reduce to an unreadable export merely to avoid a transfer limit.

## Communication and delivery

Give concrete progress based on actual completed stages. For slow renders, show approximate percentage from logs rather than invented estimates. Do not say the design is ready before a frame has been rendered and inspected.

If suitable real photographs or clips are unavailable, preserve progress and identify the specific media needed. Do not substitute AI-generated or procedural scenery. Do not route a free user straight into a paid subscription; use the local renderer if capable. If the renderer or audio import is blocked, state the real blocker and preserve work.

Use current Library save instructions. Return a concise result with a download link and actual local file path. Do not send a Library link alone: this user explicitly reported trouble opening those links. Offer editable captions/project only if useful; never expose secrets or temporary signed URLs.


## Seamless scenic repetition

Never repeat scenic footage with an abrupt last-frame to first-frame jump. Prefer a clip long enough for the shot. When repetition is necessary, play forward, then reverse back, then forward again (ping-pong playback). Inspect both turnarounds for a visible jump or pause. Keep the original song audio forward and continuous; only the muted scenic clip reverses. If reversing produces implausible human action or traffic movement, choose a different clip or a shorter shot instead of using a hard loop.


Use short smooth dissolves between distinct clips, timed to musical phrase changes. The renderer now overlaps scenic shots with FFmpeg xfade while preserving total song duration. Keep the NFM circle, visualizer and caption layout continuous. Do not fade every scene to black or use abrupt unmotivated cuts. Avoid flashy preset wipes; use a harder cut only when the musical accent and scene justify it.
