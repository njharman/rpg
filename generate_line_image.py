#!/usr/bin/env python

import sys
from random import randint
import math

import ssim
import numpy as np
from PIL import Image
from PIL import ImageDraw


def generate_line(max_width, max_height, max_length=50):
    start = (randint(0, max_width), randint(0, max_width))
    length = float(randint(0, max_length))
    angle = math.radians(float(randint(0, 360)))
    x = length * math.cos(angle) + start[0]
    y = length * math.sin(angle) + start[1]
    line = [start, (x, y)]
    return line


def mean_squared_error(img1, img2):
    if img1.size != img2.size:
        raise Exception("size of images must be the same")
    if img1.mode != 'L':
        img1 = img1.convert('L')
    if img2.mode != 'L':
        img2 = img2.convert('L')
    img1 = np.array(img1.getdata())
    img2 = np.array(img2.getdata())
    return np.mean(np.absolute(img1 - img2)) / 255.0


def psnr(img1, img2):
    mse = mean_squared_error(img1, img2)
    return 10.0 * math.log10(1.0 / mse)


def main(name):
    img = Image.open(name)
    result_img = Image.new("RGB", img.size)
    draw = ImageDraw.Draw(result_img)
    draw.rectangle([(0, 0), result_img.size], fill=(255, 255, 255))
    max_width, max_height = result_img.size
    for i in range(6000):
        best_img = result_img.copy()
        best_score = ssim.compute_ssim(img, result_img)
        for l in range(40):
            temp_img = result_img.copy()
            draw = ImageDraw.Draw(temp_img)
            line = generate_line(max_width, max_height)
            draw.line(line, width=1, fill=(0, 0, 0))
            score = ssim.compute_ssim(img, temp_img)
            if score > best_score:
                print i, score
                score = best_score
                best_img = temp_img.copy()
        result_img = best_img
        if (i % 100) == 0:
            output_name = str(i).zfill(6) + '.png'
            result_img.save(output_name)


if __name__ == "__main__":
    main(sys.argv[1])
