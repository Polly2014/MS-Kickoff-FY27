"""Record an existing generated image after inspection; never invokes generation."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
from PIL import Image

BASE = Path(__file__).resolve().parent

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('alias')
    ap.add_argument('image', type=Path)
    ap.add_argument('--prompt', required=True, type=Path)
    ap.add_argument('--reference', action='append', type=Path, default=[])
    ap.add_argument('--review', required=True)
    ap.add_argument('--reject', action='store_true')
    args = ap.parse_args()
    path = args.image.resolve()
    with Image.open(path) as im:
        size = list(im.size)
    def relative(p):
        import os
        return Path(os.path.relpath(p.resolve(), BASE)).as_posix()
    record = dict(alias=args.alias, path=relative(path), sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                  size=size, requested_deployment='gpt-image-2', quality='high',
                  actual_prompt=relative(args.prompt), inputs=[relative(p) for p in args.reference],
                  review=args.review, status='agent-selected preparation reference; not user-approved final',
                  used_in_final=False, cost='API billed separately; actual bill not queried')
    file = BASE/'preparation-manifest.json'
    data = json.loads(file.read_text(encoding='utf-8')) if file.exists() else dict(date='2026-11-18', assets={}, attempts=[])
    if args.reject:
        record['status']='rejected candidate; do not upload as selected reference'
        data['attempts'].append(record)
    else:
        old = data['assets'].get(args.alias)
        if old and old['path'] != record['path']:
            data['attempts'].append(old)
        data['assets'][args.alias] = record
    file.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    log = BASE/'run-log.csv'
    rows = list(csv.DictReader(log.open(encoding='utf-8-sig',newline='')))
    asset_id = path.stem
    if not any(r['asset_id']==asset_id for r in rows):
        with log.open('a',encoding='utf-8',newline='') as f:
            csv.DictWriter(f, fieldnames=rows[0].keys()).writerow(dict(
                asset_id=asset_id,used_in_final='no',model='gpt-image-2',mode='reference image edit',
                resolution=f'{size[0]}x{size[1]}',duration_seconds='',inputs=';'.join(record['inputs']),
                actual_prompt_file=record['actual_prompt'],output_file=record['path'],
                credits_spoken_name='dream-painter / Azure gpt-image-2',
                notes='2026-11-18 preparation reference; '+args.review+'; actual API bill not queried.'))
    print(args.alias, record['path'], size, record['status'])

if __name__ == '__main__':
    main()
