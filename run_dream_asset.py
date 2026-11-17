"""Use dream-painter's configured edit functions, retaining requested PNG resolution."""
from pathlib import Path
import argparse
import importlib.util
import io
import sys
from contextlib import redirect_stdout

class Tee(io.TextIOBase):
    def __init__(self, stream, log):
        self.stream, self.log = stream, log
    def write(self, text):
        self.stream.write(text)
        self.stream.flush()
        self.log.write(text)
        return len(text)
    def flush(self):
        self.stream.flush()
        self.log.flush()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('reference', type=Path)
    parser.add_argument('prompt', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--size', default='1024x1536')
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit('Refusing to overwrite an existing image: ' + str(args.output))
    repo = Path(__file__).resolve().parents[2]
    script = repo / '.claude/skills/dream-painter/scripts/paint_dream.py'
    spec = importlib.util.spec_from_file_location('dream_painter', script)
    painter = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(painter)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.with_suffix('.log').open('w', encoding='utf-8') as log:
        with redirect_stdout(Tee(sys.stdout, log)):
            print('Reference:', args.reference)
            print('Prompt file:', args.prompt)
            config = painter.get_config()
            data = painter.generate_image_edit(args.prompt.read_text(encoding='utf-8'), args.reference, config, size=args.size, quality='high')
            painter.save_image(data, args.output, max_width=1536)
            print('Saved requested resolution without the CLI 1200px downscale.')

if __name__ == '__main__':
    main()
