# Suno field handoff

Verified against official Suno help and release notes on 2026-11-16. Recheck current documentation or the actual visible form when controls or model names differ. These notes describe a Custom-mode songwriting handoff, not permission to operate the user's account or spend credits.

## Field mapping

| Field or selection | What to provide | Applicability |
| --- | --- | --- |
| Title / Song Title | Finished original title | Complete song package |
| Creation mode | Custom or the user's equivalent advanced/manual form | Own lyrics and separate styles |
| Model | Specific available model recommendation and plan fallback | Use the visible current model selector |
| Lyrics | Original complete text and a verified character count outside the block | Vocal songs; strictly fewer than 5,000 characters by user preference |
| Instrumental | Off for vocals; On for instrumental requests | If the toggle exists |
| Lyrics mode | Manual/custom or equivalent; paste supplied lyrics | Only if the interface has that selector; exact labels unverified |
| Styles / Style of Music | Genre, groove, tempo direction, instruments, voice texture, arrangement | Separate from lyrics |
| Exclude / Exclude Styles | Unwanted genres, delivery, instruments, or textures relevant to this song | Advanced controls when available |
| Vocal Gender | Appropriate visible selection or leave unselected | Male/Female documented; do not invent additional dropdown choices |
| Weirdness | One reasoned starting value, not a range without a choice | Documented scale runs Safe to Chaos, with 50% described as normal |
| Style Influence | One reasoned starting value | Loose to Strong; stronger values favor style adherence |
| Audio upload / Audio Influence | None and Not applicable without an input; otherwise actual input and a recommendation | Audio Influence appears with uploaded audio; other reference-related availability can vary |
| Variety | 0 for preserved style tags, higher only for requested exploration | v6 control when available; do not invent an undocumented maximum or percentage scale |
| Max Mode | Off for tests; consider On for requested higher-credit refinement | v6 when available; costs extra credits |
| Duration | Auto, or a requested target supported by the UI | Duration control documented on web; do not promise exact timing |
| Voice / Persona / Inspiration | None unless a real user-provided or accessible selection exists | Optional inputs; do not invent assets or IDs |
| My Taste / Personalize | Leave unchanged, or recommend disabling style augmentation for exact prompt control if the UI permits | Product-dependent; My Taste can influence magic-wand style suggestions |
| Save to / folder | Current/default folder, or a folder the user actually names | Only if shown; user account choice rather than creative content |

## Models and recommendations

The official v6 documentation at this verification date lists v6 as the focused flagship, v6-wild for exploration, and v6-mini as the option available on all plans. v6 and v6-wild require Pro/Premier. Use v6 for a focused brief when available, with v6-mini as the fallback. Do not assume the user's ChatGPT plan establishes their Suno plan. Reverify rather than assuming these names and eligibility will remain current.

Treat suggested slider settings as creative judgment. Official documentation explains what controls do, not a single best combination for every genre. For focused conventional songs, approximately 35% Weirdness / 75% Style Influence is a fallback recommendation; adapt to the brief and visible scale. Do not call those numbers scientifically tested or official defaults.

Keep optional controls compact: for example, Audio upload: None; Audio Influence: Not applicable; Voice/Persona: None; Inspiration: None; Save to: Current/default folder. If a field is absent in the user's interface, omit or mark it unavailable rather than instructing the user to find a fictional control.

## Official sources

- Custom mode, lyrics, Instrumental, Styles, title: https://help.suno.com/en/articles/3726721
- Exclude: https://help.suno.com/en/articles/3161921
- Vocal Gender: https://help.suno.com/en/articles/10153473
- Weirdness, Style Influence, and conditional Audio Influence: https://help.suno.com/en/articles/6141377
- v6 model eligibility, Variety, and Max Mode: https://help.suno.com/en/articles/13924481
- Model selection: https://help.suno.com/en/articles/13924801
- Duration on web: https://suno.com/release-notes/duration-slider-on-web
- My Taste: https://help.suno.com/en/articles/11362561
- Style augmentation context: https://suno.com/release-notes/introducing-v5-5-voices-custom-models-and-my-taste

Treat the manual lyrics selector and account-specific folder/reference controls conditionally: the official sources above do not establish that every listed control or exact label appears in every interface.

## Optional package-checker schema

Write a temporary UTF-8 JSON object with `title`, `lyrics`, `styles`, `exclude_styles` as strings and `settings` as an object. Include `settings.instrumental` as a JSON boolean. For vocal songs, include `mode`, `model`, `lyrics_mode`, `vocal_gender`, `weirdness`, `style_influence`, and `duration` in settings using actual chosen values; a clear string such as Not applicable is valid when a control is unavailable. List conditional controls as additional keys when relevant. Do not mistake this internal draft schema for a Suno API or paste it into Suno.

Run `python scripts/check_package.py PATH` or add `--limit N` for a lower exclusive lyric limit. The script checks required fields, nonblank vocal lyrics/styles/title, the lyric limit, basic settings completeness, and an instrumental/lyrics conflict. It warns about pasted code fences, repeat-chorus shorthand, empty exclusions, and suspicious control/brief conflicts; review rather than treating every warning as an artistic error. Do not force a needless exclusion just to remove a warning. The script cannot judge rhyme quality, know the user's interface, or measure actual performance.

## Rechecked controls and validator, 2026-11-19

Rechecked the official v6 FAQ, Creative Sliders guide and Custom Mode guide:
- https://help.suno.com/en/articles/13924481
- https://help.suno.com/en/articles/6141377
- https://help.suno.com/en/articles/3726721

v6-mini is the free fallback; v6 and v6-wild require an eligible subscription. Variety at 0 preserves style-tag control. Max Mode costs extra credits. Audio Influence is conditional on an audio upload. These sources do not establish every account-specific field or exact UI label. Recommended slider starting values are creative choices, not official optimums.

The package checker requires finite numeric Weirdness/Style Influence values from 0 to 100, or explicit unavailable/Not applicable notes. Optional Audio Influence follows the same rule. Use numbers, not percentage strings. Optional max_mode must be a JSON boolean. Numeric variety must be finite and nonnegative; its actual UI scale remains conditional. A numeric duration must be positive and is only a target. The checker flags common unfinished lyric placeholders and unbracketed repeat-chorus shorthand. These checks do not measure musical quality or actual Suno behavior.
