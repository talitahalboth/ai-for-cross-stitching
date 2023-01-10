"""
@file griddetection.py
@brief This program finds grid coordinates and cell sizes for a cross stitch pattern image
"""
import statistics
import itertools
import cv2 
import numpy as np
from matplotlib import pyplot as plt
from .logger import SingletonLogger

__DEBUG__ = False


def build_grid_coordinates_v_array(cdst_p, dimensions, v_mode, v_coords, v_lines, rgb,lineWidth):
    """Build array of vertical coordinates from grid"""
    for i in range(1, len(v_lines)):
        prev = v_lines[i - 1][0] + v_mode
        cur = v_lines[i][0]
        while prev + 5 < cur:
            v_coords.append(prev)
            if __DEBUG__:
                cv2.line(cdst_p, (prev, 0),
                        (prev, dimensions[0]), rgb, lineWidth, cv2.LINE_AA)
            prev += v_mode
        v_coords.append(cur)

        if __DEBUG__:
            cv2.line(cdst_p, (cur, 0),
                    (cur, dimensions[0]), rgb, lineWidth, cv2.LINE_AA)

    logger = SingletonLogger()
    logger.log("Vertical coordinates: " + str(v_coords), "DEBUG")


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

def build_grid_lines_array(dimensions, h_lines, linesP, v_lines):
    for line in linesP:
        l = line[0]
        if l[0] == l[2] or l[1] == l[3]:
            if l[0] == l[2]:
                line[0][1] = 0
                line[0][3] = dimensions[1]
                v_lines.append(list(line[0]))
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


def grid_coordinates(file_name, verbose=False):
    """
    Finds coordinates of a grid
    """
    logger = SingletonLogger()
    logger.log("Finding grid coordinates", "VERBOSE")

    default_file = 'sunflower/img.png'
    filename = file_name if len(file_name) > 0 else default_file
    # Loads an image
    src = cv2.imread(cv2.samples.findFile(filename))
    # Check if image is loaded fine
    if src is None:
        logger.log('Error opening image!', "ERROR")
        logger.log(
            'Usage: hough_lines.py [image_name -- default ' + default_file + '] \n', "ERROR")
        return -1

    dst = cv2.Canny(src, 50, 200, None, 3)

    # Copy edges to the images that will display the results in BGR
    cdst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
    cdst_p = np.copy(cdst)
    shape = src.shape
    # the minimum lenght allowed for the line
    # should be at least 1/5th of the figure size
    minLineLength = min(shape[0],shape[1])/5
    # the maximum gap allowed between two points in a line
    maxLineGap = min(shape[0],shape[1])/100
    # Probabilistic Hough Line Transform
    linesP = cv2.HoughLinesP(dst, rho=2, theta=np.pi / 180,
                            threshold=50, lines=None, minLineLength=minLineLength, maxLineGap=maxLineGap)

    h_lines = []
    v_lines = []

    dimensions = src.shape
    build_grid_lines_array(dimensions, h_lines, linesP, v_lines)

    def sort_by_y(e):
        return e[1]

    def sort_by_x(e):
        return e[0]

    v_lines.sort(key=sort_by_x)
    v_lines = remove_coordinates_close(v_lines)
    h_lines.sort(key=sort_by_y)
    h_lines = remove_coordinates_close(h_lines)
    h_diff = []
    for i in range(1, len(h_lines)):
        diff = h_lines[i][1] - h_lines[i - 1][1]
        if diff > 0:
            h_diff.append(diff)
    h_diff.sort()
    h_mode = statistics.mode(h_diff)

    logger.log(f"h diff:{h_diff}", "DEBUG")
    logger.log(f"h mode:{h_mode}", "DEBUG")

    v_diff = []
    for i in range(1, len(v_lines)):
        diff = v_lines[i][0] - v_lines[i - 1][0]
        if diff > 0:
            v_diff.append(diff)
    v_diff.sort()
    v_mode = statistics.mode(v_diff)

    logger.log(f"v diff:{v_diff}", "DEBUG")
    logger.log(f"v mode:{v_mode}", "DEBUG")

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
    build_grid_coordinates_v_array(cdst_p, dimensions, h_mode, v_coords, v_lines, rgb, line_width)

    logger.log("DONE --- Found grid coordinates", "VERBOSE")
    if __DEBUG__:
        fig = plt.figure(figsize=(10, 10))
        plt.imshow(cdst_p, alpha=0.6)
        plt.show()
        # cv2.imshow("Detected Lines (in red) - Probabilistic Line Transform", cdst_p)
        # cv2.waitKey()

    return h_coords, v_coords, h_mode

