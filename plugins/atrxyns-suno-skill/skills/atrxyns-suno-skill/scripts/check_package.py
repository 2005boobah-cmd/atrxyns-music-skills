"""Validate a temporary Suno handoff JSON; this is not a Suno API schema."""
import argparse
import json
import math
from pathlib import Path
import re
from check_lyrics import measure


def validate_package(payload, limit=5000):
    if not isinstance(limit, int) or isinstance(limit, bool) or limit < 1:
        raise ValueError('limit must be a positive integer')
    errors, warnings = [], []
    counts = None
    if not isinstance(payload, dict):
        return {'pass': False, 'errors': ['Package must be a JSON object.'], 'warnings': [], 'lyrics_count': None}
    text_fields = ('title', 'lyrics', 'styles', 'exclude_styles')
    for name in text_fields:
        if not isinstance(payload.get(name), str):
            errors.append(f'{name} must be present as a string.')
    settings = payload.get('settings')
    if not isinstance(settings, dict):
        errors.append('settings must be present as an object.')
        settings = {}
    instrumental = settings.get('instrumental')
    if not isinstance(instrumental, bool):
        errors.append('settings.instrumental must be a JSON boolean.')
    required_settings = ['mode', 'model', 'duration']
    if instrumental is not True:
        required_settings.extend(['vocal_gender', 'lyrics_mode'])
    for name in required_settings:
        value = settings.get(name)
        valid = isinstance(value, str) and bool(value.strip())
        if name == 'duration':
            valid = valid or (isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) and value > 0)
        if not valid:
            errors.append(f'settings.{name} needs an actual selection/value or a clear Not applicable string.')
    for name in ('weirdness', 'style_influence', 'audio_influence'):
        if name == 'audio_influence' and name not in settings:
            continue
        value = settings.get(name)
        numeric = isinstance(value, (int, float)) and not isinstance(value, bool)
        unavailable = isinstance(value, str) and re.match(r'^(?:not applicable|unavailable|not exposed|not supported|n/a)(?:\b|\s|$)', value.strip(), re.I)
        if numeric and math.isfinite(value) and 0 <= value <= 100:
            pass
        elif unavailable:
            pass
        else:
            errors.append(f'settings.{name} must be a finite number from 0 to 100, or an explicit unavailable/Not applicable note.')
    if 'max_mode' in settings and not isinstance(settings['max_mode'], bool):
        errors.append('settings.max_mode must be a JSON boolean when supplied.')
    if 'variety' in settings:
        value = settings['variety']
        if not (isinstance(value, str) and value.strip()) and not (isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) and value >= 0):
            errors.append('settings.variety needs a nonnegative finite value or an applicability note; its UI scale must be verified separately.')
    for name in ('title', 'styles'):
        if isinstance(payload.get(name), str) and not payload[name].strip():
            errors.append(f'{name} must not be blank.')
    lyrics = payload.get('lyrics')
    if isinstance(lyrics, str):
        counts = measure(lyrics, limit)
        if not counts['pass']:
            errors.append(f'Lyrics must remain strictly below {limit} characters under every reported count.')
        if instrumental is True and lyrics.strip():
            errors.append('Instrumental is on but the lyrics field is not blank.')
        elif instrumental is False and not lyrics.strip():
            errors.append('Vocal songs need nonblank lyrics.')
        if re.search(r'(?m)^\s*(```|~~~)', lyrics):
            warnings.append('Remove Markdown fences from the pasted lyrics field.')
        if re.search(r'(?im)^\s*\[(?:(?:repeat\s+(?:the\s+)?chorus)|(?:chorus\s*(?:x|times)\s*\d+))\]\s*$', lyrics):
            warnings.append('Expand repeat-chorus shorthand into the actual sung lyrics.')
        elif re.search(r'(?im)^\s*(?:\(?repeat\s+(?:the\s+)?chorus\)?|\(?chorus\s*(?:x|times)\s*\d+\)?)\s*$', lyrics):
            warnings.append('Expand repeat-chorus shorthand into the actual sung lyrics.')
        if re.search(r'(?im)^\s*(?:\[(?:write|insert|add)\s+(?:the\s+)?(?:verse|chorus|lyrics)[^\]]*\]|(?:verse|chorus|lyrics)\s+go(?:es)?\s+here)\s*$', lyrics):
            warnings.append('Replace unfinished lyric placeholders before delivery.')
    for name in ('title', 'styles', 'exclude_styles'):
        value = payload.get(name)
        if isinstance(value, str) and re.search(r'(?m)^\s*(```|~~~)', value):
            warnings.append(f'Remove Markdown fences from the pasted {name} field.')
    exclusions = payload.get('exclude_styles')
    styles = payload.get('styles')
    if isinstance(exclusions, str):
        if not exclusions.strip():
            warnings.append('Exclude Styles is intentionally blank; confirm no exclusions are needed.')
        if isinstance(styles, str):
            excluded_items = {part.strip().lower() for part in re.split(r'[,;\n]', exclusions) if part.strip()}
            for term in ('piano', 'guitar', 'bass', 'drums', 'strings', 'synths', 'vocals'):
                if term in excluded_items and re.search(r'\b' + re.escape(term) + r'\b', styles, re.I):
                    warnings.append(f'Review {term}: present in both Styles and an exact Exclude entry.')
    return {'pass': not errors, 'errors': errors, 'warnings': warnings, 'lyrics_count': counts}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path', type=Path)
    parser.add_argument('--limit', type=int, default=5000)
    args = parser.parse_args()
    if args.limit < 1:
        parser.error('--limit must be positive')
    try:
        payload = json.loads(args.path.read_bytes().decode('utf-8-sig'))
        result = validate_package(payload, args.limit)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        parser.exit(2, f'Cannot validate package: {exc}\n')
    print(json.dumps(result, ensure_ascii=True))
    raise SystemExit(0 if result['pass'] else 1)


if __name__ == '__main__':
    main()
