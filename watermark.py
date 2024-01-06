#!/usr/bin/env python3
from pathlib import Path
import argparse
import math
import dataclasses
from typing import *
from PIL import ImageFont, ImageOps, ImageDraw, Image
SUPPORTED_SUFFIX = ('.jpg', '.jpeg', '.png')
RGB_SUFFIX = ('.jpg', '.jpeg')


@dataclasses.dataclass
class InputImage:
    name: str
    image: Image.Image


def gen_watermark(text: str, font: ImageFont.ImageFont, size: Tuple[int, int], rot_degree, color) -> Image.Image:
    print('Generating watermark...')
    
    width, height = size
    rot_rad = rot_degree / 180 * math.pi
    real_width = int(math.ceil(
        abs(width * math.cos(rot_rad)) + abs(height * math.sin(rot_rad))
    ))
    real_height = int(math.ceil(
        abs(height * math.cos(rot_rad)) + abs(width * math.sin(rot_rad))
    ))

    watermark = Image.new('RGBA', (real_width, real_height), (255, 0, 0, 0))
    draw = ImageDraw.Draw(watermark)
    bbox = font.getbbox(f'    {text}    ')
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
    box_width = text_width
    box_height = text_height * 2
    for i in range(0, real_width, box_width):
        for j in range(0, real_height, box_height):
            draw.text((i, j), text, font=font, fill=color)
    watermark = watermark.rotate(rot_degree)
    watermark = watermark.crop(
        ((real_width - width) // 2, (real_height - height) // 2, (real_width - width) // 2 + width, (real_height - height) // 2 + height))
    return watermark


def watermarkize(bg: Image.Image, wm: Image.Image) -> Image.Image:
    if wm.size != bg.size:
        wm = wm.crop((0, 0, bg.width, bg.height))
    # 转换为rgba模式
    if bg.mode != "RGBA":
        bg = bg.convert("RGBA")
    if wm.mode != "RGBA":
        wm = wm.convert("RGBA")
    # 合并水印文件
    out = Image.alpha_composite(bg, wm)
    return out


def parse_args(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('text', type=str, help='watermark text')
    parser.add_argument('-f', '--file', default='.',
                        type=Path, help='input folder')
    parser.add_argument('-o', '--output', default='output',
                        type=Path, help='output folder')
    parser.add_argument('--rot', default=15,
                        type=int, help='watermark rotation degree')
    parser.add_argument('--font-file', default='fs.ttf',
                        type=Path, help='ttf watermark font')
    parser.add_argument('--font-size', default=45,
                        type=int, help='size of watermark font')
    parser.add_argument('--alpha', default=0.5,
                        type=float, help='alpha of watermark color')
    return parser.parse_args(args)


def main(args: argparse.Namespace):
    text: str = args.text
    file: Path = args.file
    output: Path = args.output
    rot: int = args.rot
    font_file: Path = args.font_file
    font_size: int = args.font_size
    alpha: float = args.alpha

    font = ImageFont.truetype(str(font_file), font_size)

    images: List[InputImage] = []
    for filename in file.iterdir():
        if filename.name.endswith(SUPPORTED_SUFFIX) and filename.is_file():
            img = Image.open(filename)
            ImageOps.exif_transpose(img, in_place=True)
            images.append(InputImage(name=filename.name, image=img))
    
    max_width = max(img.image.width for img in images)
    max_height = max(img.image.height for img in images)
    watermark = gen_watermark(text, font, (max_width, max_height), rot, (0x7f, 0x7f, 0x7f, int(0xff * alpha)))
    
    output.mkdir(parents=True, exist_ok=True)
    for img in images:
        print(f'Dealing with {img.name}')
        with watermarkize(img.image, watermark) as output_image:
            if img.name.endswith(RGB_SUFFIX):
                output_image = output_image.convert('RGB')
            output_image.save(output / img.name)


if __name__ == "__main__":
    main(parse_args())
