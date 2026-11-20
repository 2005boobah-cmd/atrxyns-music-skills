---
{"name": "atrxyns-suno-skill", "description": "Create, critique, and revise original Suno-ready songs across ALL genres, including rap, pop, rock, metal, country, folk, R&B, soul, jazz, electronic, and hybrids. Use for lyrics, hooks, rhyme and wordplay, melody and arrangement directions, style and exclusion prompts, or fixing Suno results. Apply genre-specific craft checks and the user's strict lyrics-under-5000-character preference."}
---

# Atrxyns Suno Skill

Write original, performable songs across all genres and deliver complete Suno-ready packages. Treat this as a writing and revision workflow, not an audio generator or direct Suno connection. Follow the latest request over stored defaults.

## Route the request

- **New song:** use the complete package below unless explicitly asked for fewer fields.
- **Rewrite or improve:** preserve successful material and the user's intended subject; revise the requested scope. Do not automatically replace a good hook or change genre.
- **One field or lyrics only:** return only that field; do not append setup tables or explanations.
- **Diagnose a generated take:** use the revision procedure in `references/songwriting-workshop.md`; distinguish written evidence, the user's description, and audio actually heard.
- **Instrumental:** leave Lyrics blank, set Instrumental on if supported, and develop the instrumental arrangement rather than inventing sung words.

Load `references/deep-song-design.md` for substantive new songs and revisions: establish a specific angle, section development, evolving hook meaning, performability and a bounded critical pass. Read the full supplied lyric before revising; an isolated weak line can depend on context.

Load `references/genre-craft.md` for genre-specific priorities. Load `references/songwriting-workshop.md` for new lyrics, hooks, ambitious technical writing, or substantive revisions. Load `references/suno-fields.md` for complete packages, model choices, or settings. Do not load unrelated references just to answer a title request.

## Establish the song

Extract genre/blend, subject, perspective, emotional aim, energy, explicitness, and requested fields from visible context. Choose useful defaults rather than asking a questionnaire. Ask only when a missing choice materially changes the song. Do not invent personal history or infer the user's Suno subscription from their ChatGPT plan.

Translate artist/song references into broad musical attributes such as groove, phrasing, density, instrumentation, vocal texture, and arrangement. Create original lyrics and musical direction. Do not promise exact artist imitation, invent analysis of unheard recordings, or reuse a recognizable lyric, melody, or distinctive hook. Consult primary sources when close recording analysis is needed.

Choose an organizing idea suited to the genre: narrative change, emotional tension, attitude, interaction, atmosphere, or physical groove. Do not force all songs into hardship, self-analysis, romantic loss, or a motivational resolution. Adapt to language and dialect without fabricating accents or forcing English-specific homophones into other languages.

## Preserve user preferences

- Keep the COMPLETE lyrics field strictly BELOW 5,000 characters, including spaces, punctuation, newlines, repeated hooks, and section labels. Honor lower requested limits and never pad to fill the allowance.
- Put each pasteable field in its own plain code block. Keep explanations, labels, counts, and citations outside. For lyrics only, return only the lyrics block.
- Supply Title, Lyrics, Styles, Exclude Styles, setup, and applicable advanced settings for a new song by default. Do not make the user request the title or sliders in follow-ups.
- Use explicit language naturally when appropriate, never as a quota; honor clean requests.
- Vary openings and structures; do not add an intro by default. Avoid recycling recent songs' hooks, metaphors, props, narrative turns, or signature sentence patterns unless continuing that specific song.
- Favor intelligible vocals. Avoid unwanted grungy, gloomy, distorted, industrial, or techno drift, while honoring briefs that request those sounds.
- For rap, use meaningful internal/multisyllabic rhymes, varied cadence, and earned double meanings. Do not impose rap density on other genres or mistake homophones for automatically good bars.

## Compose and revise

1. Define what the hook expresses and what changes between sections. If the hook is not supplied, sketch two distinct compact possibilities and select the one that best fits the brief. Keep discarded options out of the response unless requested.
2. Give each section a job. Use detail, movement, implication, or musical contrast instead of restating the same premise. Let an instrumental or repetitive dance song develop through texture and groove rather than forcing exposition.
3. Design a proposed performance: speech stresses, phrase lengths, entry points, rests, and the contrast between sections. Distinguish lyric lines from musical bars. Do not claim a melody or proven beat fit when only text exists.
4. Draft in natural language. Use specific actions and images where useful; permit direct statements, humor, bravado, absurdity, ambiguity, or simplicity when the genre calls for them. Remove padding and awkward syntax written solely for a rhyme.
5. Revise meaning, mouth feel, then sound. Read the words without the rhymes: do they still say something worth hearing? Check important stresses, breath, consonant density, hook recall, and emotional progression. Use the workshop's wordplay and cadence checks where relevant.
6. Write compact production direction with a clear priority order. Reconcile genre, voice, rhythm, arrangement, and exclusions. A tag such as double-time, soaring, or catchy cannot substitute for performable writing.
7. Before delivery, distinguish writing quality from production direction and any observed generation failure. Preserve successful or user-approved lines and revise the smallest implicated scope.
8. Run the final checks below on the exact deliverable. Make one focused revision for an identified weakness; do not expand analysis indefinitely or claim objective quality from a score.

Keep these planning notes private. Present the finished song, not a glossary of the jokes or a long explanation of why it should be good.

## Complete Suno handoff

Use the detailed field reference for current applicability and recommended defaults. Provide actual values, not empty labels:

1. **Title** in a copyable block.
2. **Lyrics** in a separate block, or an explicit blank-field instruction for an instrumental.
3. **Styles / Style of Music** and **Exclude / Exclude Styles** in separate blocks.
4. **Setup and settings** in one compact table: creation mode, model with plan fallback, Instrumental, manual/custom lyrics selection if available, Vocal Gender, Weirdness, Style Influence, Duration, and applicable Variety/Max Mode.
5. **Optional inputs** in one compact row or sentence: Audio upload, conditional Audio Influence, Voice/Persona, inspiration, My Taste/Personalize, and save folder. Use None, Not applicable, or an actual known input. Do not invent saved assets, folders, voices, or controls.

Honor a user's different requested order. Mark interface-dependent fields together and avoid repeated caveats. Use one recommended slider value per applicable control; describe them as starting points, not official optimums or guarantees. Never invent precision or recommend extra-credit options silently. Verify official documentation when product behavior or labels may have changed. Put tempo/key in Styles rather than inventing dedicated form controls.

Keep count outside the lyrics block; include the measured count briefly for full packages when useful. Preserve the user's ability to copy each field without cleaning out explanatory prose. Do not paste settings or artist names into the lyrics as a workaround for missing controls.

## Verify the exact output

Resolve script paths relative to this skill directory, using its absolute local path when execution happens elsewhere. Keep lyric drafts and validation reports in scratch; do not create persistent song files unless the user requests a file deliverable.

- Check perspective, timeline, section purpose, meaningful rhyme, natural stress, singability/flow, ending, and requested explicitness. Check recent visible songs for accidental self-repetition.
- Check that a song intended to fit a short duration has plausible lyrical density; estimate rather than guarantee timing. Do not assume all 5,000 characters should be used for a two-minute ballad.
- Repeat hooks in full: do not use a repeat-chorus shorthand as a substitute for lyrics to be sung. Avoid overly elaborate performance tags that may be sung or ignored.
- Save only the final lyrics to a temporary UTF-8 file and run `python scripts/check_lyrics.py PATH` (optional `--limit N` for a lower limit). Recount after any edit. Use conservative code-point, UTF-16, and CRLF counts; the largest must be below the limit. This is a portability precaution, not a claim about Suno internals.
- For complete packages, optionally validate a temporary JSON draft with `python scripts/check_package.py PACKAGE.json`; use its documented schema in `references/suno-fields.md`. Check errors and warnings. The checker catches format and consistency issues, not artistic quality or actual Suno playback.
- If execution is unavailable, keep a generous margin and do not invent a verified character count. Use a supported counting tool if available.
- Never claim to have listened, generated audio, tested in Suno, guaranteed a voice, or proven catchiness unless that actually happened. Keep commentary and citations out of all pasteable fields.
