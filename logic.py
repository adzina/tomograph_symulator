#!/usr/bin/python3
import numpy as np
# import math
from typing import Iterable, Tuple
import matplotlib.pyplot as plt


def bresenham(p0, p1):
	x0, y0 = p0
	x1, y1 = p1
	matrix = []
	if (x0 == x1 and y0 == y1):
		draw(x0, y0)
		return
	dx = x1 - x0
	if (dx < 0):
		sx = -1
	else:
		sx = 1
	dy = y1 - y0
	if (dy < 0):
		sy = -1
	else:
		sy = 1

	if (abs(dy) < abs(dx)):
		slope = dy / dx
		pitch = y0 - slope * x0
		while (x0 != x1):
			matrix.append((x0, int(slope * x0 + pitch)))
			x0 += sx
	else:
		slope = dx / dy
		pitch = x0 - slope * y0
		while (y0 != y1):
			matrix.append((int(slope * y0 + pitch), y0))
			y0 += sy
	matrix.append((x1, y1))
	return matrix


def line_coord_bresen(alpha: float, disp: float, size: int):
	r_circle = size // 2
	r_max = int(np.sqrt((r_circle ** 2) - (disp ** 2))) - 1
	ray_length = range(-r_max, r_max)
	
	sin_a = np.sin(alpha)
	cos_a = np.cos(alpha)
	dx = -int(disp * sin_a)
	dy = int(disp * cos_a)

	x0 = r_circle + int(-r_max * cos_a) + dx
	y0 = r_circle + int(-r_max * sin_a) + dy

	x1 = r_circle + int(r_max * cos_a) + dx
	y1 = r_circle + int(r_max * sin_a) + dy

	return bresenham((x0, y0), (x1, y1)), len(ray_length)

def radon(img: np.ndarray, sinogram: np.ndarray, n_angles: int, n_detectors: int, \
                     width: float):
    assert len(img.shape) == 2  #image in greyscale
    
    img_size = min(img.shape)
    width_px = img_size * width
    for ang in range(n_angles):
        for detector in range(n_detectors):
            angle = ang/n_angles * np.pi
            delta = width_px * (-0.5 + detector/n_detectors)
            points, _ = line_coord_bresen(angle,delta,img_size)
            for x, y in points:
                sinogram[ang, detector] += img[x, y]


def reverse_radon(img, sinogram, width, img_size):
    n_angles = sinogram.shape[0]
    n_detectors = sinogram.shape[1]
    width_px = img_size * width
    for i_angle in range(n_angles):
        if i_angle != 0:
            img[i_angle] = img[i_angle-1].copy()
        for i_detector in range(n_detectors):
            angle = i_angle/n_angles * np.pi
            delta = width_px * (-0.5 + i_detector/n_detectors)
            points, npoints = line_coord_bresen(angle, delta, img_size)
            for x, y in points:
                img[i_angle][x, y] += sinogram[i_angle, i_detector] / npoints


def get_mask(mask_size):
    assert isinstance(mask_size, int)
    assert mask_size > 1

    mask = np.zeros(shape=(mask_size, ), dtype=np.float64)

    mask[0] = 1.0
    for i in range(1, mask_size):
        if i % 2 == 0:
            mask[i] == 0.0
        else:
            mask[i] = (-4 / (np.pi ** 2)) / (i ** 2)
    return mask


def filter(sinogram, mask):
    n_angles, n_detectors = sinogram.shape
    assert n_detectors > 2
    mask_size = mask.shape[0]
    filtered = np.empty_like(sinogram)
    for ang in range(n_angles):
        for detector in range(n_detectors):
            value = sinogram[ang, detector] * mask[0]
            for dx in range(1, mask_size):
                if detector + dx < n_detectors:
                    value += sinogram[ang, detector + dx] * mask[dx]
                if detector - dx >= 0:
                    value += sinogram[ang, detector - dx] * mask[dx]
            filtered[ang, detector] = value
    return filtered


