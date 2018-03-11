#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt


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
        rx = r_circle + int(r*cos_a) + dx
        ry = r_circle + int(r*sin_a) + dy
        matrix.append((rx,ry))		
	
    return matrix


def draw_line(img, size, alpha, delta, value):
    matrix = line_coord(alpha, delta, size)
    for (x,y) in matrix:
        img[x,y] = value		


def draw_rays(img_size: int, n_angles: int, n_detectors: int, width: float) -> np.ndarray:
    img = np.zeros((img_size, img_size), dtype=float)

    width_det_line = img_size * width
    for ang in range(n_angles):
        for detector in range(n_detectors):
            angle = ang/n_angles * np.pi
            delta = width_det_line * (-0.5 + detector/n_detectors)
            value = (ang+1)/n_angles
            draw_line(img, img_size, angle, delta, value)
    return img


def test():
    img_size = 400
    n_angles = 20
    n_detectors = 20
    width = 0.4
    img = draw_rays(img_size, n_angles, n_detectors, width)

    plt.imshow(img)
    # plt.imsave(fname="output.png", arr=img, cmap=plt.cm.gray)
    plt.show()


if __name__ == "__main__":
	test()