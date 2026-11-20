# Private music skills: maintained source

Prepared from the owned Suno 1.2.0 and Video Studio 1.2.1 releases on 2026-11-19. This directory is not yet a hosted repository. No recipient access has been granted.

## Distribution choice

Use one PRIVATE Git repository with two plugins in the included marketplace. Keep the marketplace name `atrxyns-music-skills`, both plugin names, and their source paths stable. Combining the skills would add migration work without fixing personal-account sharing.

The existing personal cloud plugins remain private and unchanged. Their backend IDs are `plugins_6afb6d70e9608191807799732408d401` and `plugins_6afb7d12f6c081918e88d01ff9b1ee5f`. This marketplace does not convert or take over those cloud identities. Its installations use the stable marketplace/plugin names. Do not put the personal backend IDs into a workspace-import `pluginId`: OpenAI requires that target plugin to already belong to the importing workspace.

## Initial owner setup

1. Create or select a PRIVATE Git repository owned by you or your organization. Publish only this directory, never the parent song workspace.
2. Use `main` as the release branch. Keep drafts on a different branch. Push this prepared source to main for the initial release.
3. Give your friend authenticated READ access only. Do not grant plugin editor access. GitHub personal-repository collaborators may have write access; use an organization repository with its Read role, or another Git service that can enforce read-only access. Check the actual role before sending access. No invitation has been sent.
4. Both machines need Git authentication that can read this private repository. Use credential manager or SSH setup, never tokens embedded in a URL or this package.

No working installation URL exists until the repository is hosted. Replace 2005boobah-cmd/atrxyns-music-skills below with its actual path; these are placeholders, not install links.

## Friend: install once

Use Codex in the ChatGPT desktop app (or the supported local Codex client), with current plugin marketplace support. In a terminal:

```text
codex plugin marketplace add 2005boobah-cmd/atrxyns-music-skills --ref main
codex plugin marketplace list
```

Restart the desktop app. Open Plugins Directory, select Atrxyns Music Skills, and install Atrxyns Suno Skill and UnkownSongs Video Studio. Start a new chat and select the appropriate plugin/skill. Test one short songwriting request and a short local video preview before attempting a full render.

This is a local desktop/Codex route. It does not install these personal plugins into ordinary ChatGPT web/mobile or attach them to a custom GPT. Uploading these files to a custom GPT is a separate static-copy workflow and does not synchronize future releases.

## Future save → publish → update

1. Edit the files in THIS repository on a draft branch. Saving local files or a draft branch does not release them to the friend tracking main. Editing the old personal cloud plugin separately also does not update this repository.
2. Preserve skill resources and plugin names. Bump each changed plugin's version in BOTH `plugin.json` and `.codex-plugin/plugin.json`.
3. Review the diff for private data, validate manifests/scripts, run the Suno validators and a short video preview when affected. Keep songs, lyrics, render projects, model caches, credentials and installed packages outside this repository.
4. Merge the approved source into main and push main. This is the release event for this route. A GitHub Release page or tag alone does not update a client tracking main. Optionally tag the commit for rollback, but keep the tracked ref unchanged.
5. Friend runs `codex plugin marketplace upgrade atrxyns-music-skills`, checks that the marketplace resolves correctly, restarts the desktop app, and starts a NEW chat. Verify the installed version and changed behavior. If the client's Plugins UI offers an Update action, complete it if the installed version remains behind.

Official documentation establishes an explicit marketplace refresh and local app restart. The local CLI help also confirms `upgrade` refreshes Git marketplace snapshots. Automatic background delivery and the exact installed-package refresh behavior have NOT been tested on your friend's machine. Do not promise push updates, zero-click updates or changes to existing chats. He should not need another ZIP or manual instruction replacement after this initial marketplace installation.

## Runtime setup on friend's PC

Suno writing is instruction-driven; its character/handoff validators use Python's standard library. It does not connect to Suno, submit songs or generate audio. Your friend's Suno account and features are separate.

Video production requires actual shell/process execution, filesystem read/write access, Python 3.10+, NumPy, Pillow, FFmpeg with H.264/AAC support, adequate disk space and render time. Example Windows setup from this directory:

```powershell
py -3 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements-video.txt
```

FFmpeg may be on PATH or supplied by the imageio-ffmpeg fallback. Optional transcription:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements-transcription.txt
```

Transcription downloads a model and needs network/storage; it is candidate alignment requiring review. Dependency ranges are portable declarations, not a tested lockfile for every OS. No dependencies, models or FFmpeg binaries are bundled. A plugin installation alone supplies none of these execution permissions/capabilities. Plain ChatGPT chat is not a guarantee of a suitable rendering environment.

Follow the preserved production and project-format references for real-photo/clip sourcing, licensing, project preparation, accurate lyrics and preview review. Keep recipient songs in a separate working directory. Use only authorized real media for scenery. The reusable emblem is included.

## What was preserved and checked

All 22 original files are present. All 18 skill files (instructions, references, scripts, agent YAML, style and PNG) are byte-identical to the current owned archives. Only author contact email was removed from the four manifests. Names and versions were preserved. No personal song, private lyric, chat, credentials, cache or installed dependency was copied. Generic OS font fallbacks remain portable; they are not personal paths.

JSON parsing, Python parsing, selected lyric boundary/invalid-handoff checks, PNG decoding and a targeted private-data scan passed. No end-to-end friend install, authenticated private Git fetch, actual recipient update, or recipient render has been run. The package is prepared, not published/live.

## Official sources checked

- https://developers.openai.com/plugins/build/plugins — private local marketplaces, stable plugin names, marketplace add/upgrade, restart and workspace publishing boundary.
- https://learn.chatgpt.com/docs/build-plugins — sharing versus installation; workspace permissions; separate app/tool access.
- https://learn.chatgpt.com/docs/enterprise/plugin-management — workspace-only GitHub import, daily sync/Sync now, and same-workspace requirement for keeping an existing backend ID.

The workspace route is an alternative if both of you later join one eligible workspace: its admin can configure a private GitHub marketplace with daily sync or Sync now. That is different from the personal-account local route prepared here.
