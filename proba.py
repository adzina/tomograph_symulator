#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt



img = np.zeros((300, 300), dtype=np.int64)

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
	sin_a = np.sin(alpha)
	cos_a = np.cos(alpha)
	dx = -int(disp * sin_a)
	dy = int(disp * cos_a)

	x0 = r_circle + int(-r_max * cos_a) + dx
	y0 = r_circle + int(-r_max * sin_a) + dy

	x1 = r_circle + int(r_max * cos_a) + dx
	y1 = r_circle + int(r_max * sin_a) + dy

	return bresenham((x0, y0), (x1, y1))


# do usuniecia
def line_coord(alpha: float, disp: float, size: int):
	r_circle = size // 2
	max_r = int(np.sqrt((r_circle ** 2) - (disp ** 2))) - 1
	span_r = range(-max_r, max_r)
	sin_a = np.sin(alpha)
	cos_a = np.cos(alpha)
	dx = -int(disp * sin_a)
	dy = int(disp * cos_a)

	matrix = []

	for r in span_r:
		rx = r_circle + int(r * cos_a) + dx
		ry = r_circle + int(r * sin_a) + dy
		matrix.append((rx, ry))

	return matrix


def draw_line(img, size, alpha, delta, value):
	matrix = line_coord_bresen(alpha, delta, size)

	for x, y in matrix:
		img[x, y] = 1


# do usuniecia
def draw_rays(img_size: int, n_angles: int, n_detectors: int, width: float) -> np.ndarray:
	width_det_line = img_size * width
	for ang in range(n_angles):
		for detector in range(n_detectors):
			angle = ang / n_angles * np.pi
			delta = width_det_line * (-0.5 + detector / n_detectors)
			value = (ang + 1) / n_angles
			draw_line(img, img_size, angle, delta, value)

	return img


def radon(img: np.ndarray, sinogram: np.ndarray, n_angles: int, n_detectors: int, \
          width: float):
	assert len(img.shape) == 2  # image in greyscale
	img_size = min(img.shape)
	width_px = img_size * width
	for ang in range(n_angles):
		for detector in range(n_detectors):
			angle = ang / n_angles * np.pi
			delta = width_px * (-0.5 + detector / n_detectors)
			points = line_coord(angle, delta, img_size)
			for x, y in points:
				sinogram[ang, detector] += img[x, y]
		yield ang


def reverse_radon(img, sinogram, width, img_size):
	n_angles = sinogram.shape[0]
	n_detectors = sinogram.shape[1]
	width_px = img_size * width
	for i_angle in range(n_angles):
		if i_angle != 0:
			img[i_angle] = img[i_angle - 1].copy()
		for i_detector in range(n_detectors):
			angle = i_angle / n_angles * np.pi
			delta = width_px * (-0.5 + i_detector / n_detectors)
			points = line_coord(angle, delta, img_size)
			npoints = len(points[0])**2
			for x, y in points:
				img[i_angle][x, y] += sinogram[i_angle, i_detector] / npoints
		yield i_angle


def test():
	img_size = 300
	n_angles = 10
	n_detectors = 10
	width = 0.2
	draw_rays(img_size, n_angles, n_detectors, width)
	sinogram = np.zeros(shape=(n_angles, n_detectors), dtype=np.int64)
	for step in radon(img, sinogram, n_angles, n_detectors, width):
		plt.imshow(sinogram)
	plt.imshow(img)
	# plt.imsave(fname="output.png", arr=img, cmap=plt.cm.gray)
	plt.show()


if __name__ == "__main__":
	test()