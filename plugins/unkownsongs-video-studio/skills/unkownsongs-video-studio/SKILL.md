---
name: unkownsongs-video-studio
description: Create or improve UnkownSongs music videos, lyric videos, audio visualizers, and equalizers from uploaded songs. Use when the user asks to turn a song into a video, add timed lyrics, improve music-video backgrounds, restyle an equalizer, or make horizontal or vertical branded music content. Keep UnkownSongs styling consistent while tailoring cinematic backgrounds to the music.
---

# Nox FM Video Studio

Produce the actual video file, not merely a storyboard or prompts. Use **Nox FM** as the channel name and the exact equal-sized **NFM** lettering in the bundled logo. Keep the technical skill name unchanged for installation compatibility. Default to a free local workflow and include timed lyrics when they are supplied. Do not impose song-lyric character limits from songwriting tools on a video.

## Start and preserve progress

1. Resolve the attached audio using available attachment/Library tools. Read the current Library skill before transferring or saving files. Reuse existing materialized audio, renders, project files and checkpoints.
2. Inspect duration, sample rate, channels, tools, CPU/GPU availability and writable paths. Prefer existing FFmpeg, Python, NumPy and Pillow. Install missing dependencies into a task environment only when necessary; do not hard-code a prior user's runtime, home or cache paths. Pass subprocess arguments as arrays.
3. Read [art direction](references/art-direction.md) and [production](references/production.md). Use [project format](references/project-format.md) for the bundled renderer. Keep the project and timing records so revisions do not restart expensive work.
4. Infer format from intent: TikTok/Reels/Shorts → 9:16; ordinary music video/YouTube → 16:9. Default to 1080p, 24 fps, full song. Use 720p when the available machine makes 1080p impractical and state the actual export dimensions. Do not silently shorten the song.
5. Ask only for material missing information. Use exact lyrics from the user/Suno when available; otherwise attempt free transcription, then request uncertain words if necessary. Do not demand permission for routine reversible preparation or rendering.

## Keep the identity; improve the scene

Default to the composition from the published “Questions” video. Place the circular NFM badge in the center over a cinematic, almost symmetrical scene, with a soft backlight, drifting particles and large white lyrics below. Adapt the scene to each song. Use the clean original badge when available and keep player interface elements out of the artwork.

Choose cinematic environments that support the lyric's imagery and emotional arc. Use distinct connected scenes, credible lighting, film texture and subtle camera movement. Read [lyric interpretation](references/lyric-interpretation.md) and complete its section-by-section meaning and scene plan before sourcing assets. Prefer a small set of excellent frames with meaningful progression over a large random slideshow. Avoid identical framing, unrelated fantasy scenery and invented real evidence.

Use only real photographs and real video clips for all scene imagery and backgrounds. Do not use AI-generated or AI-reconstructed pictures, AI-generated video, synthetic environments, or procedural scenery. Source user-provided media or licensed footage/photographs, verify the source, and record creator, source URL and license. Editing, cropping, grading, gentle photo movement, typography, branding and audio-reactive graphics are allowed; they must not replace the real scene imagery. Do not spend paid credits, buy assets, or initiate subscription upgrades without authorization. If suitable real media cannot be sourced, explain the specific missing asset instead of substituting generated scenery.

## Make the visualizer feel designed

Use the permanent chrome/crimson NFM profile PNG at assets/NFM_Brand_Emblem.png. This is branding only, never background scenery. Do not bundle a stock scene pack or reuse the logo/PFP as a scene. Select licensed real photographs and clips for each song after interpreting its lyrics. The renderer loads this exact logo automatically; preserve its exact NFM lettering and colors rather than regenerating the logo. Keep a crisp fixed silver circular border around it.

The default reactive treatment is a loose, layered smoky aura rooted directly at the circle edge. Wisps billow and stretch outward from that circumference. Do not leave an empty gap or make an orbiting outer ring. Use uneven density, soft feathering, fine curls and natural gaps within the smoke, rather than a solid rubber band, opaque sheet, gear teeth, separate solid chunks, thin spectrum bars, or a uniformly blurred ring.

Match the PNG palette: deep crimson/oxblood, charcoal, gunmetal and brushed-silver highlights. Use tonal variation within these colors; no unrelated rainbow. Keep the logo sharp, the circle clearly visible, and the real footage visible through the aura.

Drive independent layers from the recording: 30-160 Hz bass and transients push the main edge-rooted smoke outward and pulse the emblem; 250-3500 Hz vocal-range energy shapes finer silver wisps; energy above 4000 Hz accents sparse crimson ember particles. Mid-frequency energy can include instruments: do not claim isolated vocals without source separation. Preserve bass-driven particle kicks and a spring-like settling response.

Use global song calibration, fast attack and slower decay, retaining silence and quiet dynamics. No random beat triggers, per-frame loudness normalization, full-frame flashes or dense white snow. Keep captions stable and leave adequate clearance for peak motion. Render the emblem and fixed border sharply; cache static material/geometry where possible.

Use the earlier ribbon or discrete spectrum only when specifically requested. Inspect a short actual rendered preview at both quiet and bass-heavy moments before exporting the full song.

## Lyrics and timing

Remove bracketed arrangement/performance notes from the lyric display; retain sung words, punctuation, explicit language and intentional capitalization. Do not censor or rewrite supplied lyrics. Align to the actual recording, including repeats and omissions. Prefer existing timed captions when reliable.

Use `scripts/lyric_timing.py` with user lyrics and optional free local transcription. Inspect its confidence and gap reports. Review all low-confidence cues, chorus entrances, vocalizations and long pauses against the audio. Never silently stretch an unmatched line through an instrumental break or treat interpolated timings as verified. Fix cues before a final export. Use line-by-line lyrics by default; offer word highlighting only when word timestamps are reliable.

Use one or two readable lines, strong contrast, generous margins, and no collisions with the spectrum or platform controls. Clear lyrics during instrumental passages. Do not put production directions on screen.

## Render, review, deliver

- Create a short preview around a chorus and inspect actual frames before a full render. A preview is a design checkpoint, not a new approval gate.
- Use `scripts/render_video.py PROJECT.json --check` to validate paths, dimensions, scenes and cues.
- Use `--preview 12 --start <seconds>` for a short export; omit preview flags for the full song.
- Verify duration, dimensions, audio presence, chapter transitions, lyric completeness and representative frames from intro, chorus, bridge and outro. Check for clipped text and mismatched aspect ratios.
- Preserve the original performance and mix. Avoid remastering, stretching or loudness changes unless asked. AAC conversion for MP4 compatibility is allowed; never call it bit-identical unless verified.
- Save the final video through the current Library workflow where available. Return a working download link **and the exact actual local file location**, since this user had trouble with Library links. Do not claim a file exists at a guessed path. Use the file's real name.
- Include actual duration/resolution and any material timing uncertainties briefly. Do not call an unfinished render complete. Never force a ZIP for the video.
- Keep project JSON, source-asset map and editable timed captions alongside the render for revisions; offer those only when useful or requested. Do not package the user's song, private lyrics, credentials, caches or installed dependencies inside this plugin.


Make the edge-rooted smoky aura prominent: rich crimson, visible gunmetal/silver variation, denser feathered wisps and broader bass excursions. Keep the fixed circle distinct and the center clear; do not reduce the smoke to a barely visible haze.
