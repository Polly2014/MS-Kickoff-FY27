"""Create local review assets from the downloaded B clip; no model calls."""
from pathlib import Path
import hashlib
import json
import subprocess

import cv2
import imageio_ffmpeg
from PIL import Image, ImageDraw


def main():
    root = Path(__file__).resolve().parent
    b_path = root / 'raw-video/TEST-B_Feng-Scott_v01.mp4'
    cap = cv2.VideoCapture(str(b_path))
    if not cap.isOpened():
        raise SystemExit('Download B first: ' + str(b_path))
    fps = cap.get(cv2.CAP_PROP_FPS)
    count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    times = [0, 1, 2.5, 4, 5.5, 7, 8.5, 9.5, 10.5, 12, 13.5, 14.8]
    sheet = Image.new('RGB', (427 * 3, 265 * 4), '#151515')
    draw = ImageDraw.Draw(sheet)
    for i, t in enumerate(times):
        cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
        ok, frame = cap.read()
        if not ok:
            continue
        im = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        im.thumbnail((427, 240))
        x, y = i % 3 * 427, i // 3 * 265
        sheet.paste(im, (x, y))
        draw.text((x + 8, y + 244), f'{t:.1f}s', fill='white')
    sheet.save(root / 'previews/TEST-B-Feng-Scott-v01-contact.jpg')
    cap.release()

    # A ends at the approved candidate's neighborhood; this edit is review-only.
    # No interpolation or dissolve is used to conceal the actual boundary.
    combined = root / 'previews/TEST-AB-12s-plus-15s-v01.mp4'
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    subprocess.run([
        ffmpeg, '-hide_banner', '-loglevel', 'error', '-n',
        '-i', str(root / 'raw-video/TEST-A_blue-local_v02.mp4'),
        '-i', str(b_path), '-filter_complex',
        '[0:v]trim=start=0:end=12,setpts=PTS-STARTPTS,fps=30,setsar=1[a];'
        '[1:v]setpts=PTS-STARTPTS,fps=30,setsar=1[b];'
        '[a][b]concat=n=2:v=1:a=0[v]',
        '-map', '[v]', '-an', '-c:v', 'libx264', '-crf', '18',
        '-preset', 'fast', '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
        str(combined),
    ], check=True)
    probe = subprocess.run([ffmpeg, '-hide_banner', '-i', str(b_path)],
                           capture_output=True, text=True)
    details = dict(width=width, height=height, fps=fps, frames=count,
                   duration_seconds=count / fps,
                   bytes=b_path.stat().st_size,
                   sha256=hashlib.sha256(b_path.read_bytes()).hexdigest(),
                   audio_stream_detected='Audio:' in probe.stderr,
                   sample_times_seconds=times,
                   contact_sheet='previews/TEST-B-Feng-Scott-v01-contact.jpg',
                   combined_preview='previews/TEST-AB-12s-plus-15s-v01.mp4',
                   boundary_edit='A 0-12s + full B; hard cut; review only; originals unchanged')
    (root / 'TEST-B-Feng-Scott-v01-media.json').write_text(
        json.dumps(details, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(details, ensure_ascii=False))


if __name__ == '__main__':
    main()
