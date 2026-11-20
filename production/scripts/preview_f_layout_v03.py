"""Preview the approved credits hierarchy; cameos remain static placeholders."""
from pathlib import Path
import json

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
W, H = 1920, 1080
FONT_DIR = Path('C:/Windows/Fonts')


def main():
    credits = json.loads((ROOT/'credits-info.json').read_text(encoding='utf-8'))
    source = Image.open(ROOT/'frames/F-E-tail-background-v01.png').convert('RGB')
    source = source.resize((W,H), Image.Resampling.LANCZOS).convert('RGBA')
    # Keep the whole width and its lighting continuous. Reframe upward only;
    # blend the original dark bottom into a matching extended surround.
    alpha = np.full((H,W), 255, np.uint8)
    alpha[-100:,:] = np.linspace(255,0,100)[:,None].astype(np.uint8)
    source.putalpha(Image.fromarray(alpha))
    image = Image.new('RGBA',(W,H),(4,12,29,255))
    image.alpha_composite(source,(0,-90))
    draw = ImageDraw.Draw(image)

    def center(text, y, filename, size, color, max_width=1660):
        while True:
            font=ImageFont.truetype(str(FONT_DIR/filename),size)
            box=draw.textbbox((0,0),text,font=font)
            width=box[2]-box[0]
            if width <= max_width:
                break
            size-=1
        draw.text(((W-width)//2,y),text,font=font,fill=color)
        return {'size':size,'width':width,'y':y}

    typography={}
    typography['idea']=center(credits['ending_idea_draft'],835,'seguisb.ttf',44,(232,245,255,255))
    typography['creators']=center('创作团队  Baoli Wang · Yun Gu',910,'msyh.ttc',32,(225,233,245,255))
    typography['models']=center('AI Models: '+credits['ending_models_display'],994,'segoeui.ttf',24,(185,202,223,255))
    typography['tools']=center('Tools: '+credits['ending_tools_display'],1031,'segoeui.ttf',24,(185,202,223,255))
    for index,name in enumerate(('Baoli-Wang','Yun-Gu')):
        cameo=Image.open(ROOT/f'frames/creators/F-cameo-{name}-v02-transparent.png').convert('RGBA')
        cameo.thumbnail((150,138),Image.Resampling.LANCZOS)
        x=42 if index==0 else W-42-cameo.width
        image.alpha_composite(cameo,(x,H-cameo.height+8))
    output=ROOT/'previews/F-credits-layout-v03-bold-idea-static-placeholder.jpg'
    image.convert('RGB').save(output,quality=95)
    (ROOT/'previews/F-credits-layout-v03-typography.json').write_text(
        json.dumps({'status':'static_layout_only','typography':typography},indent=2),encoding='utf-8')
    print(output)
    print(json.dumps(typography,indent=2))


if __name__=='__main__':
    main()
