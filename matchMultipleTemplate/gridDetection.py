"""
@file hough_lines.py
@brief This program demonstrates line finding with the Hough transform
"""
import sys
import math
import cv2 as cv
import numpy as np
import itertools
import statistics


def remove_coordinates_close(input_list, threshold=(5, 5)):
    # [x1,y1,x2,y2]
    combos = itertools.combinations(input_list, 2)
    points_to_remove = [point2
                        for point1, point2 in combos
                        if
                        abs(point1[0] - point2[0]) <= threshold[0] and abs(point1[1] - point2[1]) <= threshold[1]]
    points_to_keep = [point for point in input_list if point not in points_to_remove]
    return points_to_keep


def gridCoordinates(argv):
    default_file = 'sunflower/img.png'
    filename = argv if len(argv) > 0 else default_file
    # Loads an image
    src = cv.imread(cv.samples.findFile(filename))
    # Check if image is loaded fine
    if src is None:
        print('Error opening image!')
        print('Usage: hough_lines.py [image_name -- default ' + default_file + '] \n')
        return -1

    dst = cv.Canny(src, 50, 200, None, 3)

    # Copy edges to the images that will display the results in BGR
    cdst = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)
    cdstP = np.copy(cdst)

    linesP = cv.HoughLinesP(dst, rho=2, theta=np.pi / 180, threshold=50, lines=None, minLineLength=100, maxLineGap=2)

    hLines = []
    vLines = []

    dimensions = src.shape
    for line in linesP:
        l = line[0]
        if l[0] == l[2] or l[1] == l[3]:
            if l[0] == l[2]:
                line[0][1] = 0
                line[0][3] = dimensions[1]
                vLines.append(list(line[0]))
            if l[1] == l[3]:
                line[0][0] = 0
                line[0][2] = dimensions[0]
                hLines.append(list(line[0]))

    def sortByY(e):
        return e[1]

    def sortByX(e):
        return e[0]

    vLines.sort(key=sortByX)
    vLines = remove_coordinates_close(vLines)
    hLines.sort(key=sortByY)
    hLines = remove_coordinates_close(hLines)
    hDiff = []
    for i in range(1, len(hLines)):
        diff = hLines[i][1] - hLines[i - 1][1]
        if diff > 0:
            hDiff.append(diff)

    vDiff = []
    for i in range(1, len(vLines)):
        diff = vLines[i][0] - vLines[i - 1][0]
        if diff > 0:
            vDiff.append(diff)
    hDiff.sort()
    vDiff.sort()
    hMode = statistics.mode(hDiff)
    iniH = hLines[0][1]
    cv.line(cdstP, (0, iniH), (dimensions[1], iniH), (0, 0, 255), 2, cv.LINE_AA)

    hCoords = []
    hCoords.append(iniH)
    for i in range(1, len(hLines)):
        prev = hLines[i - 1][1] + hMode
        cur = hLines[i][1]
        while prev + 5 < cur:
            hCoords.append(prev)
            cv.line(cdstP, (0, prev), (dimensions[1], prev), (0, 0, 255), 2, cv.LINE_AA)
            prev += hMode
        hCoords.append(cur)
        cv.line(cdstP, (0, cur), (dimensions[1], cur), (0, 0, 255), 2, cv.LINE_AA)

    iniV = hLines[0][0]
    cv.line(cdstP, (iniV, 0), (iniV, dimensions[0]), (0, 255, 0), 2, cv.LINE_AA)

    vCoords = []
    vCoords.append(iniV)
    for i in range(1, len(vLines)):
        prev = vLines[i - 1][0] + hMode
        cur = vLines[i][0]
        while prev + 5 < cur:
            vCoords.append(prev)
            cv.line(cdstP, (prev, 0), (prev, dimensions[0]), (0, 255, 0), 2, cv.LINE_AA)
            prev += hMode
        vCoords.append(cur)

        cv.line(cdstP, (cur, 0), (cur, dimensions[0]), (0, 255, 0), 2, cv.LINE_AA)


    # cv.imshow("Detected Lines (in red) - Probabilistic Line Transform", cdstP)
    # for i in range(1):
    #     crop_img = src[hCoords[i]+2:hCoords[i] + hMode-2, vCoords[i]+2:vCoords[i] + hMode -2]
    #     cv.imshow("cropped"+str(i), crop_img)
    #
    # cv.waitKey()

    return (hCoords, vCoords, hMode)

    return 0

#
# if __name__ == "__main__":
#     gridCoordinates(sys.argv[1:])
