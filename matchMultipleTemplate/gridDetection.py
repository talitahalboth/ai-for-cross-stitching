"""
@file gridDetection.py
@brief This program finds grid coordinates and cell sizes for a cross stitch pattern image
"""
import statistics
import itertools
import cv2 
import numpy as np
from matplotlib import pyplot as plt
from logger import log

__DEBUG__ = True


def build_grid_coordinates_v_array(cdst_p, dimensions, h_mode, v_coords, v_line, rgb,lineWidth):
    """Build array of vertical coordinates from grid"""
    for i in range(1, len(v_line)):
        prev = v_line[i - 1][0] + h_mode
        cur = v_line[i][0]
        while prev + 5 < cur:
            v_coords.append(prev)
            if __DEBUG__:
                cv2.line(cdst_p, (prev, 0),
                        (prev, dimensions[0]), rgb, lineWidth, cv2.LINE_AA)
            prev += h_mode
        v_coords.append(cur)

        if __DEBUG__:
            cv2.line(cdst_p, (cur, 0),
                    (cur, dimensions[0]), rgb, lineWidth, cv2.LINE_AA)


def build_grid_coordinates_h_arrays(cdst_p, dimensions, h_coords, h_lines, h_mode, rgb,lineWidth):
    """Build array of horizontal coordinates from grid"""
    for i in range(1, len(h_lines)):
        prev = h_lines[i - 1][1] + h_mode
        cur = h_lines[i][1]

        while prev + 5 < cur:
            h_coords.append(prev)
            if __DEBUG__:
                cv2.line(cdst_p, (0, prev),
                        (dimensions[1], prev), rgb, lineWidth, cv2.LINE_AA)
            prev += h_mode
        h_coords.append(cur)
        if __DEBUG__:
            cv2.line(cdst_p, (0, cur),
                    (dimensions[1], cur), rgb, lineWidth, cv2.LINE_AA)


def build_grid_lines_array(dimensions, h_lines, linesP, v_line):
    for line in linesP:
        l = line[0]
        if l[0] == l[2] or l[1] == l[3]:
            if l[0] == l[2]:
                line[0][1] = 0
                line[0][3] = dimensions[1]
                v_line.append(list(line[0]))
            if l[1] == l[3]:
                line[0][0] = 0
                line[0][2] = dimensions[0]
                h_lines.append(list(line[0]))


def remove_coordinates_close(input_list, threshold=(5, 5)):
    """
    Remove coordinates that are too close to each other based on a given treshold from the input_list
    """
    combos = itertools.combinations(input_list, 2)
    points_to_remove = [point2
                        for point1, point2 in combos
                        if
                        abs(point1[0] - point2[0]) <= threshold[0] and abs(point1[1] - point2[1]) <= threshold[1]]
    points_to_keep = [
        point for point in input_list if point not in points_to_remove]
    return points_to_keep


def grid_coordinates(dir_name, verbose=False):
    """
    Finds coordinates of a grid
    """
    log("Finding grid coordinates", "VERBOSE")

    default_file = 'sunflower/img.png'
    filename = dir_name if len(dir_name) > 0 else default_file
    # Loads an image
    src = cv2.imread(cv2.samples.findFile(filename))
    # Check if image is loaded fine
    if src is None:
        log('Error opening image!', "ERROR")
        log(
            'Usage: hough_lines.py [image_name -- default ' + default_file + '] \n', "ERROR")
        return -1

    dst = cv2.Canny(src, 50, 200, None, 3)

    # Copy edges to the images that will display the results in BGR
    cdst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
    cdst_p = np.copy(cdst)
    shape = src.shape
    linesP = cv2.HoughLinesP(dst, rho=2, theta=np.pi / 180,
                            threshold=50, lines=None, minLineLength=shape[0]/10, maxLineGap=shape[0]/100)

    h_lines = []
    v_line = []

    dimensions = src.shape
    build_grid_lines_array(dimensions, h_lines, linesP, v_line)

    def sort_by_y(e):
        return e[1]

    def sort_by_x(e):
        return e[0]

    v_line.sort(key=sort_by_x)
    v_line = remove_coordinates_close(v_line)
    h_lines.sort(key=sort_by_y)
    h_lines = remove_coordinates_close(h_lines)
    h_diff = []
    for i in range(1, len(h_lines)):
        diff = h_lines[i][1] - h_lines[i - 1][1]
        if diff > 0:
            h_diff.append(diff)

    h_diff.sort()
    h_mode = statistics.mode(h_diff)
    log(h_mode, "DEBUG")
    ini_h = h_lines[0][1]
    rgb = (0,255,0)
    line_width = 8
    if __DEBUG__:
        cv2.line(cdst_p, (0, ini_h),
            (dimensions[1], ini_h), rgb, 4, cv2.LINE_AA)

    h_coords = [ini_h]
    build_grid_coordinates_h_arrays(cdst_p, dimensions, h_coords, h_lines, h_mode, rgb, line_width)

    ini_v = h_lines[0][0]
    if __DEBUG__:
        cv2.line(cdst_p, (ini_v, 0),
            (ini_v, dimensions[0]), rgb, 4, cv2.LINE_AA)

    v_coords = [ini_v]
    rgb = (0,0,255)
    build_grid_coordinates_v_array(cdst_p, dimensions, h_mode, v_coords, v_line, rgb, line_width)

    log("DONE --- Found grid coordinates", "VERBOSE")
    if __DEBUG__:
        fig = plt.figure(figsize=(10, 10))
        plt.imshow(cdst_p, alpha=0.6)
        plt.show()
        # cv2.imshow("Detected Lines (in red) - Probabilistic Line Transform", cdst_p)
        # cv2.waitKey()

    return h_coords, v_coords, h_mode

