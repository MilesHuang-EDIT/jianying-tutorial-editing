#!/usr/bin/env python3
"""Read-only audit of reachable segments in a plaintext Jianying draft.

Not a native-client, media-path, typography or playback validator.
"""
import argparse
import json
from collections import Counter
from pathlib import Path


def audit(document):
    counts = Counter()
    issues = []
    chapters = []

    def visit(draft, location, ancestors):
        if id(draft) in ancestors:
            issues.append(f'{location}: cyclic embedded draft')
            return
        if not isinstance(draft, dict):
            issues.append(f'{location}: expected a draft object')
            return
        ancestors = ancestors | {id(draft)}
        pools = draft.get('materials', {})
        if not isinstance(pools, dict):
            issues.append(f'{location}: materials is not an object')
            return
        materials = {}
        for kind, entries in pools.items():
            if isinstance(entries, list):
                for item in entries:
                    if isinstance(item, dict) and item.get('id'):
                        materials[item['id']] = (kind, item)
        tracks = draft.get('tracks', [])
        if not isinstance(tracks, list):
            issues.append(f'{location}: tracks is not an array')
            return
        counts['draft_instances'] += 1
        counts['tracks_all_levels'] += len(tracks)
        for ti, track in enumerate(tracks):
            if not isinstance(track, dict):
                issues.append(f'{location}/track[{ti}]: invalid track')
                continue
            for si, segment in enumerate(track.get('segments', [])):
                here = f'{location}/track[{ti}]/segment[{si}]'
                if not isinstance(segment, dict):
                    issues.append(f'{here}: invalid segment')
                    continue
                counts['segments_all_levels'] += 1
                timerange = segment.get('target_timerange', {})
                if (not isinstance(timerange, dict)
                        or not isinstance(timerange.get('start'), int)
                        or not isinstance(timerange.get('duration'), int)
                        or timerange['start'] < 0 or timerange['duration'] <= 0):
                    issues.append(f'{here}: invalid target_timerange')
                primary = segment.get('material_id')
                if primary not in materials:
                    issues.append(f'{here}: unresolved primary material {primary!r}')
                elif materials[primary][0] == 'texts':
                    counts['native_text_segments'] += 1
                refs = set(segment.get('extra_material_refs', []))
                if primary:
                    refs.add(primary)
                for ref in sorted(refs):
                    found = materials.get(ref)
                    if not found:
                        # Extra references vary by client; record without inventing validity.
                        counts['unresolved_extra_refs'] += 1
                        continue
                    kind, item = found
                    if kind == 'drafts' and isinstance(item.get('draft'), dict):
                        counts['compound_instances'] += 1
                        chapters.append({'path': here, 'name': item.get('name', ''),
                                         'tracks': len(item['draft'].get('tracks', []))})
                        visit(item['draft'], f'{here}/compound', ancestors)

    visit(document, 'root', set())
    return {'scope': 'plaintext structure only; native-client validation required',
            'root_tracks': len(document.get('tracks', [])),
            'counts': dict(counts), 'compounds': chapters,
            'issues': issues, 'structural_errors_found': bool(issues)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('draft', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    try:
        document = json.loads(args.draft.read_text(encoding='utf-8'))
        if not isinstance(document, dict):
            raise ValueError('draft root must be an object')
        report = audit(document)
    except (OSError, ValueError, TypeError) as error:
        parser.exit(2, f'Cannot inspect plaintext draft: {error}\n')
    output = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(output + '\n', encoding='utf-8')
    else:
        print(output)
    return 1 if report['structural_errors_found'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
