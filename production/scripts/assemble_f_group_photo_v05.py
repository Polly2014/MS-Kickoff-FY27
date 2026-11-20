"""Shorten only the picture fade to nine frames; preserve v04 audio and duration."""
import json

import cv2
import numpy as np

from assemble_f_ending_v01 import ROOT, run, video_frame

TAG = 'v05-group-photo-fade03'
FINAL = ROOT/f'exports/FY27-A-F-51p43s-480P-{TAG}-music.mp4'
PREVIEW = ROOT/f'previews/SEG-E-F-8p50s-{TAG}-music.mp4'


def main():
    # v04 is already a still cast photo from F frame 92 through frame 149.
    # Extend that bright hold six frames, then fade over the final nine frames.
    for label in ('1080P-layout', '480P'):
        source = ROOT/f'videos/SEG-F-LibTV-cameos-{label}-v04-group-photo-silent.mp4'
        dest = ROOT/f'videos/SEG-F-LibTV-cameos-{label}-{TAG}-silent.mp4'
        if not dest.exists():
            run(['-i', source, '-vf',
                 'trim=end_frame=150,loop=loop=15:size=1:start=149,setpts=N/(30*TB),fps=30,'
                 'fade=t=out:start_frame=156:nb_frames=8',
                 '-frames:v', 165, '-an', '-c:v', 'libx264', '-crf', 16,
                 '-preset', 'veryfast' if label == '1080P-layout' else 'slow',
                 '-pix_fmt', 'yuv420p', '-video_track_timescale', 15360,
                 '-movflags', '+faststart', dest])
    ae = ROOT/'exports/FY27-A-E-45p93s-480P-roughcut-v03-beam-relay-silent.mp4'
    ending = ROOT/f'videos/SEG-F-LibTV-cameos-480P-{TAG}-silent.mp4'
    concat = ROOT/f'exports/FY27-A-F-{TAG}-concat.txt'
    concat.write_text(f"file '{ae.as_posix()}'\nfile '{ending.as_posix()}'\n", encoding='utf-8')
    old = ROOT/'exports/FY27-A-F-51p43s-480P-v04-group-photo-LibTV-cameos-music.mp4'
    if not FINAL.exists():
        run(['-f', 'concat', '-safe', 0, '-i', concat, '-i', old,
             '-map', '0:v:0', '-map', '1:a:0', '-c', 'copy',
             '-movflags', '+faststart', FINAL])
    if not PREVIEW.exists():
        run(['-i', FINAL, '-ss', 1378/30-3, '-t', 8.5, '-c:v', 'libx264',
             '-crf', 17, '-preset', 'fast', '-c:a', 'aac', '-b:a', '192k',
             '-movflags', '+faststart', PREVIEW])
    cap = cv2.VideoCapture(str(FINAL))
    assert int(cap.get(7)) == 1543 and cap.get(5) == 30
    cap.release()
    for i in (0, 297, 298, 657, 897, 1137, 1377):
        assert np.array_equal(video_frame(ae, i), video_frame(FINAL, i))
    last = video_frame(FINAL, 1542)
    assert last.max() <= 3
    for i in (149, 155, 156, 160, 164):
        cv2.imwrite(str(ROOT/f'previews/F-{TAG}-frame-{i:03}.jpg'), video_frame(FINAL, 1378+i))
    # Compare compressed audio packets as an extracted elementary stream.
    def audio(path):
        return run(['-i', path, '-map', '0:a:0', '-c:a', 'copy', '-f', 'adts', '-']).stdout
    assert audio(old) == audio(FINAL)
    run(['-xerror', '-i', FINAL, '-f', 'null', '-'])
    manifest = {
        'status': 'pending_user_review', 'output': str(FINAL), 'preview': str(PREVIEW),
        'frames': 1543, 'fps': 30, 'duration_seconds': 1543/30,
        'f_duration_seconds': 5.5, 'fade_out_frames': 9, 'fade_out_seconds': .3,
        'fade_start_f_seconds': 5.2, 'cast_photo_hold_before_fade_seconds': 5.2-92/30,
        'credits_spent': 0, 'audio': 'identical compressed audio packets to v04',
        'verification': {'full_decode': 'passed', 'AE_sampled_frames': 'exact pixels',
                         'last_frame': 'black', 'audio_packet_comparison': 'passed'},
        'method': 'retain v04 F frames 0-149, clone bright cast photo, final nine-frame fade',
    }
    (ROOT/f'exports/FY27-A-F-51p43s-{TAG}-manifest.json').write_text(
        json.dumps(manifest, indent=2), encoding='utf-8')
    print(json.dumps(manifest, indent=2))


if __name__ == '__main__':
    main()
