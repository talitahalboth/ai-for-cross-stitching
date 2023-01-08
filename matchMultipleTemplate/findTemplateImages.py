import math
import gridDetection

import cv2
import numpy as np


def check_templates_match(templates_list, image):
    """
    check if a image matches any template in a list
    """
    for tmp in templates_list:
        template_img_gray = cv2.cvtColor(tmp, cv2.COLOR_BGR2GRAY)
        check = cv2.matchTemplate(template_img_gray,
                                  image,
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
            elif abs(90 - theta_degrees) < 5:
                new_y = math.floor((pt1[1] + pt2[1]) / 2)
                x_lines.append(new_y)

    x_lines.sort()

    y_lines.sort()
    halfway_point = grid_size / 2
    x = np.array(x_lines)
    x_smaller, x_greater = x[x < halfway_point -
                             grid_size / 4], x[x > halfway_point + grid_size / 4]
    y = np.array(y_lines)
    y_smaller, y_greater = y[y < halfway_point -
                             grid_size / 4], y[y > halfway_point + grid_size / 4]

    template_copy = template.copy()
    margin = 4
    cropped_image = template_copy[x_smaller[-1] + margin:x_greater[0] - margin,
                    y_smaller[-1] + margin:y_greater[0] - margin]

    return cropped_image


def find_template_images():
    """
    Find template images on cross stich pattern
    """
    dir_name = "starryNight"
    filename = dir_name + "/img.png"
    src = cv2.imread(filename)
    img_RGB = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
    # and convert it from BGR to GRAY
    img_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

    # get coordinates of grid from file
    coords = gridDetection.grid_coordinates(filename)
    grid_size = coords[2]
    template_counter = 0
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
                                str(template_counter) + "-filled.png", img_RGB)

                    template_counter += 1

            except cv2.error:
                continue


find_template_images()
