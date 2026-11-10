#!/usr/bin/env python3
"""Render a checked-in HyperFrames project with its authored audio and chapters."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parent


def main():
    catalog = json.loads((ROOT / 'manifest.json').read_text())['videos']
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', choices=[row['id'] for row in catalog])
    parser.add_argument('--output', type=Path, help='Override the output MP4 path')
    args = parser.parse_args()
    for command in ['npx', 'ffmpeg', 'ffprobe']:
        if not shutil.which(command):
            parser.error(f'Install {command} before rendering.')
    project = ROOT / args.project
    recipe = json.loads((project / 'video.json').read_text())
    output = args.output.resolve() if args.output else project / 'renders' / f'{args.project}.mp4'
    if output == project / f'{args.project}.mp4':
        parser.error('Choose an output other than the checked-in delivery video.')
    output.parent.mkdir(parents=True, exist_ok=True)
    capture = output.with_name(output.stem + '.capture.mp4')
    cli = ['npx', '--yes', 'hyperframes@' + recipe['hyperframes_version']]
    subprocess.run(cli + ['check'], cwd=project, check=True)
    subprocess.run(cli + ['render', '--quality', 'delivery', '--workers', '1',
                         '-o', str(capture)], cwd=project, check=True)
    # The included narration preserves the authored mix rather than renderer gain changes.
    subprocess.run([
        'ffmpeg', '-v', 'error', '-y', '-i', str(capture),
        '-i', str(project / recipe['narration']),
        '-i', str(project / recipe['chapters']),
        '-map', '0:v:0', '-map', '1:a:0', '-map_metadata', '2', '-map_chapters', '2',
        '-c', 'copy', '-movflags', '+faststart', str(output),
    ], check=True)
    probe = json.loads(subprocess.check_output([
        'ffprobe', '-v', 'error', '-show_format', '-show_streams', '-of', 'json', str(output),
    ]))
    picture = next(stream for stream in probe['streams'] if stream['codec_type'] == 'video')
    if (picture['width'], picture['height']) != (recipe['width'], recipe['height']):
        raise RuntimeError('Rendered dimensions differ from video.json.')
    if abs(float(probe['format']['duration']) - recipe['duration_seconds']) > 0.1:
        raise RuntimeError('Rendered duration differs from video.json.')
    capture.unlink()
    print(output)


if __name__ == '__main__':
    main()
