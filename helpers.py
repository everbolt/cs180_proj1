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

    distances = distances[1:-1, 1:-1]
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

def autocrop_axis(im, axis, crop_func):
    alpha = (im.shape[0] // 500) + 1

    distances = np.sqrt(
        (im - np.roll(im, 1 * alpha, axis=axis))**2 +
        (im - np.roll(im, 2 * alpha, axis=axis))**2 +
        (im - np.roll(im, 3 * alpha, axis=axis))**2 +
        (im - np.roll(im, 4 * alpha, axis=axis))**2 +
        (im - np.roll(im, 5 * alpha, axis=axis))**2 +
        (im - np.roll(im, 6 * alpha, axis=axis))**2 +
        (im - np.roll(im, 7 * alpha, axis=axis))**2 +
        (im - np.roll(im, 8 * alpha, axis=axis))**2 +
        (im - np.roll(im, 9 * alpha, axis=axis))**2 +
        (im - np.roll(im, 10 * alpha, axis=axis))**2 +
        (im - np.roll(im, -1 * alpha, axis=axis))**2 +
        (im - np.roll(im, -2 * alpha, axis=axis))**2 +
        (im - np.roll(im, -3 * alpha, axis=axis))**2 +
        (im - np.roll(im, -4 * alpha, axis=axis))**2 +
        (im - np.roll(im, -5 * alpha, axis=axis))**2 +
        (im - np.roll(im, -6 * alpha, axis=axis))**2 +
        (im - np.roll(im, -7 * alpha, axis=axis))**2 +
        (im - np.roll(im, -8 * alpha, axis=axis))**2 +
        (im - np.roll(im, -9 * alpha, axis=axis))**2 +
        (im - np.roll(im, -10 * alpha, axis=axis))**2
    )
    max_crop = int(0.15 * distances.shape[axis])

    best_score = np.mean(distances)
    best_crop = 0
    scores = []
    for i in range(max_crop):
        attempt = crop_func(distances, i)
        attempt_score = attempt.mean()
        scores.append(attempt_score)
        if attempt_score < best_score:
            best_score = attempt_score
            best_crop = i

    return best_crop

def crop_image(img):
    im = 0.333 * img[:,:,0] + 0.333  * img[:,:,1] + 0.333 * img[:,:,2]
    def crop_bottom_by_n_pixels(im, n): return im[:(-1 * int(n)), :]
    def crop_top_by_n_pixels(im, n): return im[int(n):, :]
    def crop_right_by_n_pixels(im, n): return im[:, :-1 * int(n)]
    def crop_left_by_n_pixels(im, n): return im[:, int(n):]
    
    bottom_crop = autocrop_axis(im, 0, crop_bottom_by_n_pixels)
    top_crop = autocrop_axis(im, 0, crop_top_by_n_pixels)
    
    right_crop = autocrop_axis(im, 1, crop_right_by_n_pixels)
    left_crop = autocrop_axis(im, 1, crop_left_by_n_pixels)

    bottom_cropped = crop_bottom_by_n_pixels(img, bottom_crop)
    top_cropped = crop_top_by_n_pixels(bottom_cropped, top_crop)
    right_cropped = crop_right_by_n_pixels(top_cropped, right_crop)
    final = crop_left_by_n_pixels(right_cropped, left_crop)
    return final
