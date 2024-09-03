import numpy as np
import logging

def compute_edges(img, crop_percent=15):
    rows, cols = img.shape
    img = img[
        int(rows * crop_percent/100): int(rows * (1 - crop_percent/100)),
        int(cols * crop_percent/100): int(cols * (1 - crop_percent/100))
    ]
    distances = np.zeros(img.shape)

    above = np.roll(img, 1, axis=0)
    below = np.roll(img, -1, axis=0)
    left = np.roll(img, 1, axis=1)
    right = np.roll(img, -1, axis=1)
    
    distances = np.sqrt(
        (img - above)**2 +
        (img - below)**2 +
        (img - left)**2 +
        (img - right)** 2
    )
    distances = distances / np.max(distances)

    distances = distances[2:-2, 2:-2]
    return distances

def resize(img, factor):
    if factor == 1: return img
    rows, cols = img.shape
    new_rows = int(rows / factor)
    new_cols = int(cols / factor)
    resized = np.zeros((new_rows, new_cols))
    for i in range(new_rows):
        for j in range(new_cols):
            resized[i, j] = img[i*factor, j*factor]
    return resized

def compute_alignment(base, to_align, search_len, offset_x, offset_y, depth):
    base_resized = resize(base, 2**depth)
    to_align_resized = resize(to_align, 2**depth)
    logging.info(f'Computing alignment: Depth {depth}')
    
    min_diff = np.inf
    best_x, best_y = None, None
    for x in range(offset_x - search_len, offset_x + search_len + 1):
        for y in range(offset_y - search_len, offset_y + search_len + 1):
            attempt = np.roll(to_align_resized, (x, y), axis=(0, 1))
            diff = np.sqrt(np.sum((base_resized - attempt)**2))
            # logging.info(f'Attempt: {x}, {y} - {diff}')
            if diff < min_diff:
                min_diff = diff
                best_x, best_y = x, y
    print("Best:", best_x, best_y)
    if depth == 0: return best_x, best_y
    return compute_alignment(base, to_align, search_len, best_x*2, best_y*2, depth-1)
