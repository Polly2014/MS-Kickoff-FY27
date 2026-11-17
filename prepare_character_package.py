"""Prepare immutable-reference inputs and prompts; no image API calls here."""
from pathlib import Path
import argparse
import json
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent
CHARS = ROOT / 'assets/characters'
PACK = CHARS / 'production-pack'
REFS = ROOT / 'references/lt/production-pack'
PROMPTS = ROOT / 'prompts/production-pack'
PEOPLE = {
    'jessica': ('style-calibration-trio-fresh-feng-v02.png', (175, 30, 637, 990), (300, 75, 550, 300), 'chin-length dark bob with bangs, reddish rectangular eyeglasses, bright upper-teeth smile, friendly oval face'),
    'feng': ('style-calibration-trio-fresh-feng-v02.png', (620, 15, 960, 995), (675, 35, 875, 275), 'distinctive tall exposed forehead with receding temples, short side-parted hair, thin metal rectangular eyeglasses, long tapered face, noticeable ears, warm upper-teeth smile'),
    'song': ('style-calibration-trio-fresh-feng-v02.png', (950, 30, 1400, 990), (1045, 55, 1285, 295), 'short dark pixie haircut, no eyeglasses, small stud earrings, bright upper-teeth smile and softly rounded face'),
    'amy': ('style-calibration-amy-scott-wei-v04.png', (185, 35, 590, 990), (285, 65, 490, 300), 'long dark side-parted hair below the shoulders, no eyeglasses, softly oval face and gentle closed-mouth smile'),
    'scott': ('style-calibration-amy-scott-wei-v04.png', (590, 25, 970, 990), (670, 45, 865, 285), 'short neatly side-parted hair, full hairline, dark rectangular eyeglasses, broad softly squared face, fuller cheeks and gentle closed-mouth smile; do not borrow Feng\'s high receding forehead or long tapered face'),
    'wei': ('style-calibration-amy-scott-wei-v04.png', (980, 30, 1380, 990), (1050, 50, 1265, 290), 'short straight hair with forward fringe, broad face, opaque dark aviator sunglasses with thin metal frame, subtle relaxed smile; keep sunglasses opaque with no invented visible eyes'),
}
UNIFORM = '''Preserve the exact approved uniform: midnight-navy short bomber jacket with ribbed stand collar and open silver zipper over a plain white crew-neck shirt; narrow continuous cyan-blue-violet gradient fabric trim at BOTH jacket sleeve cuff edges and both front waistband edges, same trim width and placement as the reference. Each cuff has ONE narrow band, not two stacked lines and not wide bright blocks. Plain solid navy straight ankle trousers with turned-up hems, absolutely NO colored trim at trouser hems or ankles; white low-top lace-up sneakers. Preserve garment construction, fabric texture and navy shade. No logos, lettering, badges, props, added accessories, bracelets, jewelry additions, ties or lanyards.'''


def write_new(path, text):
    if path.exists():
        raise FileExistsError(path)
    path.write_text(text, encoding='utf-8')


def prepare_fronts():
    for folder in (PACK, REFS, PROMPTS):
        folder.mkdir(parents=True, exist_ok=True)
    for name, (source_name, body_box, face_box, identity) in PEOPLE.items():
        reference = REFS / f'{name}-front-input-v01.png'
        if reference.exists():
            raise FileExistsError(reference)
        source = Image.open(CHARS / source_name).convert('RGB')
        board = Image.new('RGB', (1200, 1600), '#dadde5')
        draw = ImageDraw.Draw(board)
        draw.text((20, 15), f'{name.upper()} / APPROVED CHARACTER ONLY / DO NOT REDESIGN', fill='black')
        body = ImageOps.contain(source.crop(body_box), (690, 1500), Image.Resampling.LANCZOS)
        board.paste(body, ((720-body.width)//2, 60+(1500-body.height)//2))
        face = ImageOps.contain(source.crop(face_box), (450, 530), Image.Resampling.LANCZOS)
        board.paste(face, (730+(450-face.width)//2, 90))
        detail_box = (body_box[0]+30, 290, body_box[2]-20, 650)
        detail = ImageOps.contain(source.crop(detail_box), (450, 760), Image.Resampling.LANCZOS)
        board.paste(detail, (730+(450-detail.width)//2, 710))
        draw.text((750, 55), 'SAME PERSON: FACE DETAIL', fill='black')
        draw.text((750, 670), 'SAME PERSON: UNIFORM DETAIL', fill='black')
        board.save(reference)
        prompt = f'''Use case: identity-preserve. Asset: single-character production master for an animated dance video.
The reference board shows ONE APPROVED CARTOON CHARACTER, {name.upper()}, in full body at left with enlarged face and uniform details at right. These are all the SAME PERSON. Extract and reproduce this EXACT character as ONE clean high-resolution full-body FRONT master. Do not output the board, labels, detail inserts, duplicate figures or any neighboring hand fragments from the original group crop.

IDENTITY IS ALREADY FINAL. Preserve the reference character's exact face shape, head outline, hairline, hairstyle, eye size and spacing, glasses shape, nose, cheeks, smile and apparent adult cartoon age. Identity reminder: {identity}. Do not reinterpret from real photography, beautify into a different person, change the face, increase realism, make a child or replace with a generic doll. Preserve the approved moderately oversized head, compact stylized adult body, limb lengths, hands and smooth animated-film material design. Identity fidelity takes priority over novelty or a new interpretation. Match the reference head-to-body proportions; do not lengthen the body or neck.

{UNIFORM}

One person only, true front view with shoulders and hips toward camera, eye-level neutral camera, face looking straight ahead, keep their approved friendly smile. Relaxed symmetric standing pose, feet naturally apart, arms lowered slightly away from torso and complete natural relaxed hands, no overlapping limbs. Full head and BOTH entire shoes visible with generous margins. Centered vertical 2:3 frame, subject occupies approximately 88 percent of image height. No hand-held items, action, dynamic perspective or camera tilt.

Replace only the surrounding blue-purple studio with a clean seamless very light cool-gray studio background and floor, softly lit neutral key light, restrained soft contact shadow under feet. Retain the approved blue/navy clothing colors and skin tones; no neon colored spill across the face. Polished coherent 3D animation-film rendering with clean sculpted hair, smooth non-photoreal skin and cloth detail. No pore texture, realistic wrinkles, toy stand, scenery, text, watermarks or borders. Output only the single approved character as the production front master.
'''
        write_new(PROMPTS / f'{name}-front-v01.txt', prompt)
    print('Prepared six front reference boards and six exact prompts.')


def prepare_turnaround(name):
    if name not in PEOPLE:
        raise ValueError(name)
    front = PACK / name / f'{name}-front-v01.png'
    if not front.exists():
        raise FileNotFoundError(front)
    identity = PEOPLE[name][3]
    prompt = f'''Use case: identity-preserve. Asset: professional THREE-VIEW character turnaround sheet for animated video continuity.
The image input is the authoritative approved single-character FRONT MASTER of {name.upper()}. Show this exact SAME character exactly THREE times in a single landscape 3:2 sheet: LEFT true FRONT view looking at camera; CENTER strict 90-degree SIDE PROFILE with the nose pointing toward the RIGHT edge of the image; RIGHT straight BACK view facing directly away from camera. The FRONT character must closely reproduce the provided master with no face or outfit redesign. All three are rotations of ONE identical 3D character with the same anatomy, hair volume, silhouette, proportions and clothes. This is not three different people or three fashion variations.

Identity locks: {identity}. Preserve the master's precise face, hairline, glasses, head-to-body ratio, eye stylization, apparent adult cartoon age, rounded sculpting and cloth/skin materials. Extend the approved hair volume and jacket construction consistently into the unseen side and back. Do not introduce any new hairstyle, ponytail, hood, backpack, rear lettering, decorations or extra accessories. Keep eyewear on the side profile where present. Back view shows the back of the head, not a head turned toward camera. Do not add a visible eye on the far side of the strict profile.

{UNIFORM}
The back of the jacket stays plain navy with the same narrow continuous gradient band along its lower waistband, connecting naturally around to the front; no logos or large rear graphics. White shirt may be visible only where consistent with the jacket length. Trousers remain plain solid navy down to their turned-up hems, without colored ankle stripes.

Three complete full-body views in ONE horizontal row, equal display scale and camera distance, same top-of-head height and shoe baseline. Orthographic-like neutral eye-level camera, no perspective foreshortening. Keep full hair and both shoes of every view inside the frame with margins. Relaxed neutral stance, arms lowered very slightly away from the torso; no running or dance pose. The profile rotates the entire body and both feet, not only the head. Front and back views have shoulders and hips square to camera. Complete hands and consistent limb lengths. Clear gaps, no overlap, no panels or separators. Position view centers around 20%, 50%, 80% of width. Figures occupy about 86% of canvas height.

Clean continuous very light cool-gray studio background and floor matching the front master, soft neutral shared lighting and restrained contact shadows under each view. Same polished 3D animated-film rendering. No text, labels, names, arrows, dimension marks, extra portraits, fourth view, props, borders or watermarks. Output only FRONT / RIGHT-FACING SIDE / BACK views of the same reference character in that order.
'''
    write_new(PROMPTS / f'{name}-three-view-v01.txt', prompt)
    print(f'Prepared {name} turnaround prompt against its verified front master.')


def review(kind):
    paths = [(name, PACK/name/f'{name}-{kind}-v01.png') for name in PEOPLE]
    thumb_size = (340, 510) if kind == 'front' else (600, 400)
    cols = 3 if kind == 'front' else 2
    rows = (len(paths)+cols-1)//cols
    board = Image.new('RGB', (cols*thumb_size[0], rows*(thumb_size[1]+42)), '#e6e9f0')
    draw = ImageDraw.Draw(board)
    font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 24)
    for i, (name, path) in enumerate(paths):
        if not path.exists():
            continue
        x, y = (i%cols)*thumb_size[0], (i//cols)*(thumb_size[1]+42)
        draw.text((x+15, y+7), name.title(), fill='#17213a', font=font)
        with Image.open(path) as im:
            tile = ImageOps.contain(im.convert('RGB'), thumb_size, Image.Resampling.LANCZOS)
        board.paste(tile, (x+(thumb_size[0]-tile.width)//2, y+42))
    target=PACK/f'all-{kind}-preview.jpg'
    board.save(target, quality=93)
    print(target)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['fronts', 'turnaround', 'review-front', 'review-three-view'])
    parser.add_argument('name', nargs='?')
    args = parser.parse_args()
    if args.action == 'fronts':
        prepare_fronts()
    elif args.action == 'turnaround':
        prepare_turnaround(args.name)
    else:
        review(args.action.removeprefix('review-'))
