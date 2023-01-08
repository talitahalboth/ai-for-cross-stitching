import math
import gridDetection

import cv2
import numpy as np
import os
from matplotlib import pyplot as plt


def checkTemplatesMatch(savedTemplates, template):
    for tmp in savedTemplates:
        # tmpImg = cv2.imread(dirName + "/templates/" + tmp)
        tmpImgGray = cv2.cvtColor(tmp, cv2.COLOR_BGR2GRAY)
        check = cv2.matchTemplate(tmpImgGray,
                                  template,
                                  cv2.TM_CCOEFF_NORMED)
        threshold = 0.9
        locTemplates = np.where(check >= threshold)
        if len(list(zip(*locTemplates[::-1]))) > 0:
            return True
    return False


def cropBordersFromMarginValue(template):
    margin = 5
    shape = template.shape
    croppedImage = template[margin:shape[0] - margin, margin:shape[1] - margin]

    return croppedImage


def cropGridBordersFromTemplate(template):
    dst = cv2.Canny(template, 50, 200, None, 3)

    shape = dst.shape
    gridSize = shape[0]
    lines = cv2.HoughLines(dst, 1, np.pi / 180, 25, gridSize * 2, 0, 0)
    xLines = []
    yLines = []
    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * (a)))
            pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * (a)))
            thetaDegrees = math.degrees(theta)
            if math.fabs(180 - thetaDegrees) < 5 or math.fabs(thetaDegrees) < 5:
                newX = math.floor((pt1[0] + pt2[0]) / 2)
                yLines.append(newX)
            elif math.fabs(90 - thetaDegrees) < 5:
                newY = math.floor((pt1[1] + pt2[1]) / 2)
                xLines.append(newY)

    xLines.append(0)
    xLines.append(gridSize)
    xLines.sort()

    yLines.append(0)
    yLines.append(gridSize)
    yLines.sort()
    cutPoint = gridSize / 2
    y = np.array(xLines)
    xSmaller, xGreater = y[y < cutPoint - gridSize / 4], y[y > cutPoint + gridSize / 4]
    y = np.array(yLines)
    ySmaller, yGreater = y[y < cutPoint], y[y > cutPoint]

    templateCopy = template.copy()
    margin = 4
    croppedImage = templateCopy[xSmaller[-1] + margin:xGreater[0] - margin,
                              ySmaller[-1] + margin:yGreater[0] - margin]

    return croppedImage


def findTemplateImages():
    dirName = "heart"
    filename = dirName + "/img.png"
    src = cv2.imread(filename)
    imgRGB = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
    # and convert it from BGR to GRAY
    imgGray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

    # get coordinates of grid from file
    coords = gridDetection.gridCoordinates(filename)
    gridSize = coords[2]
    templateCounter = 0
    savedTemplates = []
    for hcoord in coords[0]:
        for vcoord in coords[1]:
            y = vcoord
            x = hcoord
            margin = 4

            image_copy = src.copy()

            try:

                # crop template
                croppedImage = image_copy[x - margin:x + gridSize + margin, y - margin:y + gridSize + margin]
                croppedImageNoGrid = cropGridBordersFromTemplate(croppedImage.copy())
                # croppedImageNoGrid = cropBordersFromMarginValue(croppedImage.copy())

                if np.mean(croppedImageNoGrid) >= 250:
                    continue
                if croppedImageNoGrid.shape[0] < gridSize / 2 or croppedImageNoGrid.shape[1] < gridSize / 2:
                    continue
                cv2.imwrite("cropped.png", croppedImageNoGrid)

                template = cv2.imread('cropped.png', 0)

                # get template shape
                w, h = template.shape
                # So, we take our image, our template and the template matching method
                res = cv2.matchTemplate(imgGray,
                                        template,
                                        cv2.TM_CCOEFF_NORMED)
                threshold = 0.9
                # then we get the locations, that have values bigger, than our threshold
                loc = np.where(res >= threshold)

                if len(list(zip(*loc[::-1]))) > 0:
                    # check if template matches previous saved templates
                    isCopy = checkTemplatesMatch(savedTemplates, template)

                    for pt in zip(*loc[::-1]):
                        cv2.rectangle(imgRGB,
                                      pt,
                                      (pt[0] + w, pt[1] + h),
                                      (0, 255, 255),
                                      -1)
                        cv2.rectangle(imgGray,
                                      pt,
                                      (pt[0] + w, pt[1] + h),
                                      (0, 255, 255),
                                      -1)
                    if isCopy:
                        continue
                    savedTemplates.append(croppedImage)
                    cv2.imwrite(dirName + "/templates/template" + str(templateCounter) + ".png",
                                croppedImageNoGrid)
                    cv2.imwrite(dirName + "/filled/template" + str(templateCounter) + "-filled.png", imgRGB)

                    templateCounter += 1

            except cv2.error as e:
                continue


findTemplateImages()
