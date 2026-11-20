"""Join adopted A and B without trimming or re-encoding; verify source frames."""
import json
import subprocess
from pathlib import Path

import cv2
import imageio_ffmpeg

root = Path(__file__).resolve().parents[1]
videos = root / 'videos'
sources = ['SEG-A-Wan3-480P-v07-adopted.mp4', 'SEG-B-Wan3-480P-v08-adopted.mp4']
output = videos / 'SEG-AB-Wan3-480P-v01-direct-24s.mp4'
preview = root / 'previews' / 'SEG-AB-v01-junction-10-14s.mp4'
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

def run(args):
    overwrite = [] if '-y' in args else ['-n']
    subprocess.run([ffmpeg, '-hide_banner', '-loglevel', 'error', *overwrite, *args], check=True)

def frame(path, index):
    cap = cv2.VideoCapture(str(path))
    cap.set(cv2.CAP_PROP_POS_FRAMES, index)
    ok, value = cap.read()
    cap.release()
    assert ok, (path, index)
    return value

def info(path):
    cap = cv2.VideoCapture(str(path))
    result = dict(file=path.name, frames=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
                  fps=cap.get(cv2.CAP_PROP_FPS),
                  size=[int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))])
    cap.release()
    result['seconds'] = result['frames'] / result['fps']
    return result

source_info = [info(videos / name) for name in sources]
assert all(i['frames'] == 360 and i['fps'] == 30 and i['size'] == [854, 480] for i in source_info)
concat = videos / 'SEG-AB-v01-concat.txt'
concat.write_text(''.join(f"file '{name}'\n" for name in sources), encoding='utf-8')
if not output.exists():
    run(['-f', 'concat', '-safe', '0', '-i', str(concat), '-map', '0:v:0',
         '-an', '-c:v', 'copy', '-movflags', '+faststart', str(output)])
output_info = info(output)
assert output_info['frames'] == 720 and output_info['seconds'] == 24
checks = []
for out_index, source_index, src_frame in [(0, 0, 0), (359, 0, 359), (360, 1, 0), (719, 1, 359)]:
    a, b = frame(output, out_index), frame(videos / sources[source_index], src_frame)
    exact = bool((a == b).all())
    assert exact
    checks.append(dict(output_frame=out_index, source=sources[source_index], source_frame=src_frame, exact_pixels=exact))
run(['-y', '-i', str(output), '-vf', 'trim=start_frame=300:end_frame=420,setpts=N/(30*TB)',
     '-an', '-c:v', 'libx264', '-crf', '16', '-preset', 'slow', '-pix_fmt', 'yuv420p',
     '-r', '30', '-fps_mode', 'cfr', '-movflags', '+faststart', str(preview)])
preview_info = info(preview)
assert preview_info['frames'] == 120 and preview_info['seconds'] == 4
manifest = dict(output=output_info, sources=source_info,
                edit='A [0,12) + B [0,12); hard cut at 12.000s; video stream copy; silent',
                rationale='Boundary poses and stage composition closely match. Keep the final A pose before B begins its floor move. Reassess beat timing after music placement.',
                preview=preview_info, source_match_checks=checks)
(videos / 'SEG-AB-v01-edit-manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
print(json.dumps(manifest, indent=2))
