# Atrxyns Music Skills

Install the Suno songwriting and music-video plugins in Codex on desktop.

## Install

You need Git and a current Codex installation with plugin marketplace support. Run this in a terminal:

```text
codex plugin marketplace add 2005boobah-cmd/atrxyns-music-skills --ref main
```

1. Restart the desktop app.
2. Open the Plugins Directory and select **Atrxyns Music Skills**.
3. Install **Atrxyns Suno Skill** and **UnkownSongs Video Studio**.
4. Start a new chat and select the plugin you want to use.

This installation is for local Codex/desktop use. It does not install the plugins into ChatGPT web, mobile, or a custom GPT.

## Use

- **Suno:** Ask for a song, revised lyrics, or a Suno style prompt. Python is needed to run the bundled character and handoff validators. Submit the finished song instructions in your own Suno account.
- **Music videos:** Attach your song and lyrics, then ask for a music video or visualizer. Video rendering needs local execution tools and the dependencies below. Use real photographs or clips for scenery.

## Video setup

You need Python 3.10 or newer and an environment that allows shell commands and file access. Clone this repository, then run:

```powershell
git clone https://github.com/2005boobah-cmd/atrxyns-music-skills.git
cd atrxyns-music-skills
py -3 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements-video.txt
```

This installs NumPy, Pillow, and the FFmpeg fallback. An existing FFmpeg installation on PATH also works. Tell Codex to use this virtual environment for rendering.

For optional lyric transcription:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements-transcription.txt
```

Transcription downloads a model and needs network access and storage. Review generated lyric timings before the final render. Installing the plugin alone does not install these dependencies or provide rendering tools.

## Update

Run:

```text
codex plugin marketplace upgrade atrxyns-music-skills
```

Restart the desktop app and start a new chat. If the Plugins Directory shows an **Update** action, apply it. You do not need to import another ZIP or replace the instructions manually.

## If the marketplace does not appear

Run `codex plugin marketplace list` to check that it was registered, then restart the app. If the marketplace commands are unavailable, update Codex to a version that supports plugin marketplaces.
