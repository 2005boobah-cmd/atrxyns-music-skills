# Fixed identity, flexible art direction

Use the published “Questions” composition as the default. Frame a believable, near-symmetrical environment with cool blue-gray edges, deep shadows and a soft warm light behind the badge. Change the setting and accent colors with the song. Use shallow depth of field and slow movement to keep the scene visible behind the foreground graphics.

## Background families

| Family | Scenes and lighting | Best fit |
| --- | --- | --- |
| afterhours | Empty small-town roads, blue-hour storefronts, headlights, distant water towers; indigo shadows and practical amber light | Indie nostalgia, reflective rap, alternative |
| summer-memory | Late-summer fields, passenger-window reflections, old roadside architecture, warm dusk, subtle film grain | Euphoric indie, pop, bittersweet memories |
| rain-on-glass | Foreground raindrops, soft city reflections, intimate window light; charcoal and muted violet | R&B, intimate pop, slower tracks |
| moonlit-coast | Dark shoreline, silver surf, distant motel lights, wide negative space | Spacious, wistful, cinematic songs |
| liminal-neon | Realistic night interiors, sparse signage, wet pavement, controlled magenta/cyan | Electronic, energetic rap, nocturnal tracks |

Default to afterhours/summer-memory for nostalgic songs; select from the song rather than blindly reusing this preference. For acoustic, jazz, rock and other genres, preserve the identity while adapting the locations, texture and visual energy.

## Scene progression

Map intro → verses → choruses → bridge → final chorus → outro. Track emotional change: establish a place, reveal personal detail, widen the world in the chorus, withdraw for the bridge, return with changed light or perspective. Use recurring motifs with a different composition, not identical duplicates.

Use multiple distinct real clips across a full song. Do not stretch one clip over the entire track, or alternate the same two clips for the whole video. Build a coherent sequence with new shots at meaningful lyrical and musical changes: verses, hooks, builds, drops, breakdowns and outro. Match every shot to both genre and song meaning. Forward/reverse repetition is only a short extension within an individual shot, never a substitute for sourcing enough footage. Review the whole scene list for excessive reuse before rendering; vary framing and action while keeping a consistent visual world. A single-backdrop visualizer is allowed only when the user explicitly requests it. Keep the badge anchored through transitions.

Source real photographs and real video footage only. Inspect each selected asset for authentic camera capture and appropriate composition; reject AI-generated, reconstructed or synthetic scenes. Preserve source and license records. A still photograph with a pan remains a photograph, not live-action footage.

Search brief structure: real location/action, time and lighting, emotional function tied to a specific lyric section, quiet center for the badge, dark lower lyric area, intended aspect ratio. Select naturally suitable shots before cropping. Use the lyric interpretation workflow to connect shots across the song.

## Centered badge and visualizer

Reuse the permanent chrome/crimson NFM PNG at ../assets/NFM_Brand_Emblem.png with its exact NFM wordmark, gunmetal texture and crimson highlights. Keep a clean fixed silver circular border around the emblem.

The current treatment is a loose smoky aura emitted directly from the circle circumference. Its root hugs the border while bass pushes feathered wisps outward. Use uneven density, fine turbulent curls and soft open gaps within the smoke. The effect must not become a solid rubber ring, an opaque connected blob, detached solid pieces, an orbiting band separated from the circle, or a discrete bar equalizer.

Use the recording to drive layered response: low-frequency energy and kicks control the main crimson/charcoal smoke and emblem pulse; vocal-range energy controls finer silver wisps; high frequencies accent sparse red embers. This is a band-energy estimate rather than isolated vocal stems. Match the song-specific logo accent and visualizer palette, keeping neutral gunmetal/silver detail and avoiding random rainbow cycling. Keep full-frame contrast steady.

Anchor the identity slightly above center in widescreen to reserve room for peak smoke motion above two-line lyrics. Preserve quiet dynamics, avoid full-frame flashing, and inspect the actual preview during both a bass peak and a quieter vocal passage. Scenery remains real photographs and camera footage only; the aura is a graphic overlay.

## Text and finishing

Use large regular-weight white sans-serif lyrics with a soft dark shadow. Keep chorus typography consistent with verses. Keep text horizontal and centered within the format's safe region; use one line where possible and two when needed. Avoid unnecessary italic fallback fonts. Maintain case from the supplied lyrics. Use an unobtrusive dark lower gradient and soft outline instead of a large opaque caption card.

Keep the wordmark readable at mobile size. Keep social-platform controls in mind: larger right and bottom exclusions on 9:16. Use 100–180 ms lyric fades and gentle transitions without blank flicker between continuous lines. Treat credits/CTA as optional; do not add fake engagement claims or unrequested outros.

Preserve a restrained cinematic finish: stable exposure, believable color, subtle movement. Do not add hard strobes or deep bloom that turns text/spectrum into glare.

Approved visualizer: Preview 03, implemented in scripts/badge_effects.py. Edge-rooted layered smoke, long uneven bass tendrils, finer silver filaments, visible outlined sparks and a fixed crisp circle. Keep smoke outside the opaque NFM logo. Prefer real clips selected for genre and lyric meaning, not generic driving/balcony montages.


Use short smooth dissolves between distinct clips, timed to musical phrase changes. The renderer now overlaps scenic shots with FFmpeg xfade while preserving total song duration. Keep the NFM circle, visualizer and caption layout continuous. Do not fade every scene to black or use abrupt unmotivated cuts. Avoid flashy preset wipes; use a harder cut only when the musical accent and scene justify it.


## Song-specific palette and fresh footage

Before production, choose and record a song-specific palette with a reason grounded in the lyrics, genre and mood. Do not force every song to use red. For example, reflective music may suit muted blue/teal or warm amber; aggressive material may suit crimson or acid accents; these are examples, not rigid genre stereotypes. Keep the exact NFM geometry and equal-sized letters; shift only its colored accents, preserving chrome, shadow detail and the silver circle. The bundled source PNG is the master and must not be overwritten. The renderer's `accent_color` field recolors the logo overlay, smoke, rim accents and particles together at render time. Match scenery grading to that palette while keeping real footage believable. Use a short preview to check palette and contrast before a full export. Do not automatically change color on every beat; any palette evolution should follow meaningful song sections.

Source fresh real clips for each new song. Do not default to footage downloaded for earlier videos. Check the source URLs/assets against prior projects and record intentional reuse. Reuse a recognizable shot only when the user approves the connection. Genre fit and lyric meaning must justify every selected clip.
