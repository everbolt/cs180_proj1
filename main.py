import numpy as np
import skimage as sk
import skimage.io as skio
import argparse
from sys import argv
from utils import *
import logging
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

parser=argparse.ArgumentParser()

parser.add_argument("input", help="Input image path")
parser.add_argument("output", help="Output image path")
parser.add_argument("--depth", help="Number of recursive alignment calls", default=5, type=int)
parser.add_argument("--width", help="Search size x and y for alignment", default=5, type=int)
args=parser.parse_args()

search_depth = args.depth
search_width = args.width

in_path = argv[1]
out_path = argv[2]
im = skio.imread(in_path)

f_name = in_path.split(".")[-2].split("/")[-1]
out_dir = "/".join(out_path.split("/")[:-1])

logging.info('Read file')

im = sk.img_as_float(im)
height = int(np.floor(im.shape[0] / 3.0))
b = im[:height]
g = im[height: 2*height]
r = im[2*height: 3*height]

logging.info('Retrieved RGB panels')

r_edges = compute_edges(r, crop_percent=15)
g_edges = compute_edges(g, crop_percent=15)
b_edges = compute_edges(b, crop_percent=15)

logging.info('Computed edges')

logging.info('Computing green alignment...')
g_off_x, g_off_y = compute_alignment(r_edges, g_edges, search_width, 0, 0, search_depth)

logging.info('Computing blue alignment...')
b_off_x, b_off_y = compute_alignment(r_edges, b_edges, search_width, 0, 0, search_depth)

logging.info('Computed alignment')

aligned_g = np.roll(g, (g_off_x, g_off_y), axis=(0, 1))
aligned_b = np.roll(b, (b_off_x, b_off_y), axis=(0, 1))

logging.info('Applied alignment')

im = np.dstack([r, aligned_g, aligned_b])

im, crop_dims = crop_image(im)
logging.info('Cropped image')

b_crop, t_crop, r_crop, l_crop = crop_dims
with open(f"{out_dir}/{f_name}_alignment.txt", "w") as f:
    f.write(
        f"Green: {g_off_x}, {g_off_y}"
        + f"\nBlue: {b_off_x}, {b_off_y}"
        + f"\nCrop: {b_crop}, {t_crop}, {r_crop}, {l_crop}"
    )

formatted_im = (im * 255).astype(np.uint8)
skio.imsave(fname=out_path, arr=formatted_im)
