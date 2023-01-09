"""
@file hough_lines.py
@brief This program demonstrates line finding with the Hough transform
"""
import statistics
import itertools
import cv2 as cv
import numpy as np

__DEBUG__ = False


def build_grid_coordinates_v_array(cdst_p, dimensions, h_mode, v_coords, v_line):
    """Build array of vertical coordinates from grid"""
    for i in range(1, len(v_line)):
        prev = v_line[i - 1][0] + h_mode
        cur = v_line[i][0]
        while prev + 5 < cur:
            v_coords.append(prev)
            if __DEBUG__:
                cv.line(cdst_p, (prev, 0),
                        (prev, dimensions[0]), (0, 255, 0), 2, cv.LINE_AA)
            prev += h_mode
        v_coords.append(cur)

        if __DEBUG__:
            cv.line(cdst_p, (cur, 0),
                    (cur, dimensions[0]), (0, 255, 0), 2, cv.LINE_AA)


def build_grid_coordinates_h_arrays(cdst_p, dimensions, h_coords, h_lines, h_mode):
    """Build array of horizontal coordinates from grid"""
    for i in range(1, len(h_lines)):
        prev = h_lines[i - 1][1] + h_mode
        cur = h_lines[i][1]
        while prev + 5 < cur:
            h_coords.append(prev)
            if __DEBUG__:
                cv.line(cdst_p, (0, prev),
                        (dimensions[1], prev), (0, 0, 255), 2, cv.LINE_AA)
            prev += h_mode
        h_coords.append(cur)
        if __DEBUG__:
            cv.line(cdst_p, (0, cur),
                    (dimensions[1], cur), (0, 0, 255), 2, cv.LINE_AA)


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


def grid_coordinates(argv):
    """
    Finds coordinates of a grid
    """
    default_file = 'sunflower/img.png'
    filename = argv if len(argv) > 0 else default_file
    # Loads an image
    src = cv.imread(cv.samples.findFile(filename))
    # Check if image is loaded fine
    if src is None:
        print('Error opening image!')
        print(
            'Usage: hough_lines.py [image_name -- default ' + default_file + '] \n')
        return -1

    dst = cv.Canny(src, 50, 200, None, 3)

    # Copy edges to the images that will display the results in BGR
    cdst = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)
    cdst_p = np.copy(cdst)

    linesP = cv.HoughLinesP(dst, rho=2, theta=np.pi / 180,
                            threshold=50, lines=None, minLineLength=100, maxLineGap=2)

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
    ini_h = h_lines[0][1]
    cv.line(cdst_p, (0, ini_h),
            (dimensions[1], ini_h), (0, 0, 255), 2, cv.LINE_AA)

    h_coords = [ini_h]
    build_grid_coordinates_h_arrays(cdst_p, dimensions, h_coords, h_lines, h_mode)

    ini_v = h_lines[0][0]
    cv.line(cdst_p, (ini_v, 0),
            (ini_v, dimensions[0]), (0, 255, 0), 2, cv.LINE_AA)

    v_coords = [ini_v]
    build_grid_coordinates_v_array(cdst_p, dimensions, h_mode, v_coords, v_line)

    if __DEBUG__:
        cv.imshow("Detected Lines (in red) - Probabilistic Line Transform", cdst_p)
        cv.waitKey()

    return h_coords, v_coords, h_mode

# if __name__ == "__main__":
#     grid_coordinates(sys.argv[1:])
