import math
import gridDetection
import os

import cv2
import numpy as np
from matplotlib import pyplot as plt


__DEBUG__ = False


def check_templates_match(image_list, template):
    """
    check if a template matches any image in a list
    """
    for tmp in image_list:
        template_img_gray = cv2.cvtColor(tmp, cv2.COLOR_BGR2GRAY)
        check = cv2.matchTemplate(template_img_gray,
                                  template,
                                  cv2.TM_CCOEFF_NORMED)
        threshold = 0.9
        loc = np.where(check >= threshold)
        if len(list(zip(*loc[::-1]))) > 0:
            return True
    return False


def crop_borders_from_margin_value(template):
    """
    crop margins out of an image
    """
    margin = 5
    shape = template.shape
    cropped_image = template[margin:shape[0] -
                                    margin, margin:shape[1] - margin]

    return cropped_image


def find_grid_lines(lines, x_lines, y_lines, cdst):
    """Find horizontal and vertical lines from HoughLines transformation"""
    if lines is not None:
        for line in lines:
            rho, theta = line[0]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * (a)))
            pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * (a)))
            theta_degrees = math.degrees(theta)

            if abs(180 - theta_degrees) < 5 or abs(theta_degrees) < 5:
                new_x = math.floor((pt1[0] + pt2[0]) / 2)
                y_lines.append(new_x)
                cv2.line(cdst, pt1, pt2, (0, 0, 255), 3, cv2.LINE_AA)
            elif abs(90 - theta_degrees) < 5:
                new_y = math.floor((pt1[1] + pt2[1]) / 2)
                x_lines.append(new_y)
                cv2.line(cdst, pt1, pt2, (0, 0, 255), 3, cv2.LINE_AA)


def crop_grid_borders_from_template(template):
    """
    crop margins out of an image based on grid lines
    """
    dst = cv2.Canny(template, 50, 200, None, 3)
    if dst is None:
        return template
    shape = dst.shape
    grid_size = shape[0]
    lines = cv2.HoughLines(dst, 1, np.pi / 180, 25, grid_size * 2, 0, 0)
    x_lines = [0, grid_size]
    y_lines = [0, grid_size]

    halfway_point = grid_size / 2
    cdst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
    cdstP = np.copy(cdst)

    find_grid_lines(lines, x_lines, y_lines, cdstP)

    if __DEBUG__:
        fig = plt.figure(figsize=(10, 10))
        plt.imshow(template)
        plt.imshow(cdstP)
        plt.show()

    x_lines.sort()
    y_lines.sort()
    x = np.array(x_lines)
    x_smaller, x_greater = x[x < halfway_point -
                             grid_size / 10], x[x > halfway_point + grid_size / 10]
    y = np.array(y_lines)
    y_smaller, y_greater = y[y < halfway_point -
                             grid_size / 10], y[y > halfway_point + grid_size / 10]

    template_copy = template.copy()
    margin = 4
    cropped_image = template_copy[
                    x_smaller[-1] + margin:x_greater[0] - margin,
                    y_smaller[-1] + margin:y_greater[0] - margin]

    return cropped_image


def find_template_images():
    """
    Find template images on cross stich pattern
    """
    dir_name = "rocket"

    if not os.path.isdir(dir_name + "/filled/"):
        # if the demo_folder2 directory is
        # not present then create it.
        os.makedirs(dir_name + "/filled/")
    filedFilled = os.listdir(dir_name + "/filled/")
    for f in filedFilled:
        os.remove(dir_name + "/filled/" + f)

    if not os.path.isdir(dir_name + "/templates/"):
        # if the demo_folder2 directory is
        # not present then create it.
        os.makedirs(dir_name + "/templates/")
    files = os.listdir(dir_name + "/templates/")
    for f in files:
        os.remove(dir_name + "/templates/" + f)
    filename = dir_name + "/img.png"
    src = cv2.imread(filename)
    img_RGB = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)

    cv2.imwrite(dir_name + "/filled/template0-filled.png",  cv2.cvtColor(img_RGB, cv2.COLOR_BGR2RGB))
    # and convert it from BGR to GRAY
    img_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

    # get coordinates of grid from file
    coords = gridDetection.grid_coordinates(filename)
    grid_size = coords[2]
    template_counter = 1
    saved_templates = []
    for h_coord in coords[0]:
        for v_coord in coords[1]:
            y = v_coord
            x = h_coord
            margin = 4

            image_copy = src.copy()

            try:
                # crop template
                cropped_image = image_copy[x - margin:x + grid_size + margin, y - margin:y + grid_size + margin]

                cropped_image_no_grid = crop_grid_borders_from_template(
                    cropped_image.copy())


                # if __DEBUG__:
                #     plt.clf()
                #
                #     fig = plt.figure(figsize=(10, 10))
                #     plt.imshow(cropped_image_no_grid)
                #     plt.show()
                # cropped_image_no_grid = crop_borders_from_margin_value(cropped_image.copy())

                if np.mean(cropped_image_no_grid) >= 250:
                    continue
                if cropped_image_no_grid.shape[0] < grid_size / 2 or cropped_image_no_grid.shape[1] < grid_size / 2:
                    continue
                cv2.imwrite("cropped.png", cropped_image_no_grid)

                template = cv2.imread('cropped.png', 0)

                # get template shape
                w, h = template.shape
                # So, we take our image, our template and the template matching method
                res = cv2.matchTemplate(img_gray,
                                        template,
                                        cv2.TM_CCOEFF_NORMED)
                threshold = 0.9
                # then we get the locations, that have values bigger, than our threshold
                loc = np.where(res >= threshold)

                if len(list(zip(*loc[::-1]))) > 0:
                    # check if template matches previous saved templates
                    isCopy = check_templates_match(saved_templates, template)

                    for pt in zip(*loc[::-1]):
                        cv2.rectangle(img_RGB,
                                      pt,
                                      (pt[0] + w, pt[1] + h),
                                      (0, 255, 255),
                                      -1)
                        cv2.rectangle(img_gray,
                                      pt,
                                      (pt[0] + w, pt[1] + h),
                                      (0, 255, 255),
                                      -1)
                    if isCopy:
                        continue
                    saved_templates.append(cropped_image)

                    cv2.imwrite(dir_name + "/templates/template" + str(template_counter) + ".png",
                                cropped_image_no_grid)
                    cv2.imwrite(dir_name + "/filled/template" +
                                str(template_counter) + "-filled.png",  cv2.cvtColor(img_RGB, cv2.COLOR_BGR2RGB))

                    template_counter += 1

            except cv2.error:
                continue


find_template_images()
