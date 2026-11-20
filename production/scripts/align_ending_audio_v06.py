"""Tighten the music's very quiet tail and align its fade with the v05 picture."""
import json

import numpy as np

from assemble_f_ending_v01 import ROOT, run

TAG = 'v06-group-photo-avfade03'
SOURCE = ROOT/'exports/FY27-A-F-51p43s-480P-v05-group-photo-fade03-music.mp4'
FINAL = ROOT/f'exports/FY27-A-F-51p43s-480P-{TAG}-music.mp4'
PREVIEW = ROOT/f'previews/SEG-E-F-8p50s-{TAG}-music.mp4'
DURATION = 1543/30


def main():
    music = ROOT/'music/MUSIC-FY27-street-dance-60s-ElevenMusicV3-v01.mp3'
    # Retain the timing and gain of the original head, including all of A-E.
    # Use the same four-second closing section length, ending before the near-silent decay.
    head_end = DURATION-4+.15
    audio_filter = (f'[1:a]asplit=2[head][tail];'
        f'[head]atrim=0:{head_end},asetpts=PTS-STARTPTS[h];'
        '[tail]atrim=start=54:end=58,asetpts=PTS-STARTPTS[t];'
        '[h][t]acrossfade=d=0.15:c1=tri:c2=tri,volume=-4dB,'
        f'afade=t=out:st={DURATION-.3}:d=0.3[a]')
    if not FINAL.exists():
        run(['-i', SOURCE, '-i', music, '-filter_complex', audio_filter,
             '-map', '0:v:0', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac',
             '-b:a', '256k', '-ar', 44100, '-t', DURATION, '-movflags', '+faststart', FINAL])
    if not PREVIEW.exists():
        run(['-i', FINAL, '-ss', 1378/30-3, '-t', 8.5, '-c:v', 'libx264',
             '-crf', 17, '-preset', 'fast', '-c:a', 'aac', '-b:a', '192k',
             '-movflags', '+faststart', PREVIEW])
    def picture(path):
        return run(['-i', path, '-map', '0:v:0', '-c:v', 'copy', '-f', 'h264', '-']).stdout
    assert picture(SOURCE) == picture(FINAL)
    run(['-xerror', '-i', FINAL, '-f', 'null', '-'])
    samples = np.frombuffer(run(['-i', FINAL, '-vn', '-ar', 48000, '-ac', 1,
                                '-f', 'f32le', '-']).stdout, dtype='<f4')
    assert abs(len(samples)/48000-DURATION) < .04
    assert np.max(np.abs(samples)) < 1
    levels = {}
    for label, start, end in [('before_fade', DURATION-.55, DURATION-.3),
                               ('fade_end', DURATION-.025, DURATION)]:
        window = samples[round(start*48000):round(end*48000)]
        levels[label] = float(20*np.log10(max(1e-10, float(np.sqrt(np.mean(window**2))))))
    assert levels['fade_end'] < levels['before_fade']-12
    manifest = {
        'status': 'pending_user_review', 'output': str(FINAL), 'preview': str(PREVIEW),
        'duration_seconds': DURATION, 'audio_visual_fade_seconds': .3,
        'audio_fade_start': DURATION-.3, 'music_head_end': head_end,
        'music_tail_source_seconds': [54, 58], 'gain_db': -4, 'crossfade_seconds': .15,
        'credits_spent': 0, 'video': 'identical compressed picture stream to v05',
        'verification': {'full_decode': 'passed', 'picture_packet_comparison': 'passed',
                         'audio_duration': 'passed', 'tail_rms_dbfs': levels},
        'note': 'Original music has a natural gradual decay; last .3s applies a shared closing envelope. No listening verification claimed.'
    }
    (ROOT/f'exports/FY27-A-F-51p43s-{TAG}-manifest.json').write_text(
        json.dumps(manifest, indent=2), encoding='utf-8')
    print(json.dumps(manifest, indent=2))


if __name__ == '__main__':
    main()
