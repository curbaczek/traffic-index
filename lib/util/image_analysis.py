from __future__ import division
from PIL import Image, ImageChops, ImageDraw, ImageMath
from scipy.misc import imsave
import numpy


def get_color_count(image, sort=False):
    """ return a list of tuples (color, count) """
    im = Image.open(image).convert('RGB')
    colors = im.getcolors()
    if (colors is None):
        colors = im.getcolors(256*256)
    if (colors is None):
        raise Exception('can not get all colors of the image, raise maximum value or reduce image colors')
    if (sort is True):
        colors.sort(key=lambda tup: tup[0])
    return [(t[1], t[0]) for t in colors]


def sum_color_count(color_count):
    return sum([t[1] for t in color_count])


def get_color_classes(image, color_classes=[], threshold=10):
    """ takes a list of color classes tuples (name, color list) and assign the image colors
        with the given threshold to these classes """
    result = {}
    color_counts = get_color_count(image, True)

    if (len(color_classes) > 0):
        for color_class_definition in color_classes:
            class_name = color_class_definition[0]
            assert isinstance(color_class_definition[1], list)
            for class_color in color_class_definition[1]:
                filtered_color_count = []
                matched_colors = []
                for color, count in color_counts:
                    if (
                        color[0] in range(class_color[0]-threshold, class_color[0]+threshold) and
                        color[1] in range(class_color[1]-threshold, class_color[1]+threshold) and
                        color[2] in range(class_color[2]-threshold, class_color[2]+threshold)
                    ):
                        matched_colors.append((color, count))
                    else:
                        filtered_color_count.append((color, count))

                color_counts = filtered_color_count

                if class_name in result:
                    result[class_name]["colors"] += matched_colors
                    result[class_name]["count"] += sum_color_count(matched_colors)
                else:
                    result.update({
                        class_name: {
                            "count": sum_color_count(matched_colors),
                            "colors": matched_colors
                        }
                    })

    result.update({
        "unknown": {
            "count": sum_color_count(color_counts),
            "colors": color_counts
        }
    })

    return result


def get_filled_up_image(src, dest, color_classes=[], threshold=10, unassigned_color=(255, 255, 255)):
    """ takes a list of color classes tuples (class_color, single_color) and colors the pixel colors
        of the image with the given threshold """

    img = Image.open(src).convert('RGB')
    pxdata = numpy.array(img)
    color_counts = get_color_count(src, True)

    color_no = 0
    for color, count in color_counts:
        color_no += 1
        color_class_found = False
        for color_class_definition in color_classes:
            class_color = color_class_definition[0]
            seed_color = color_class_definition[1]
            if (
                color[0] in range(seed_color[0]-threshold, seed_color[0]+threshold) and
                color[1] in range(seed_color[1]-threshold, seed_color[1]+threshold) and
                color[2] in range(seed_color[2]-threshold, seed_color[2]+threshold)
            ):
                pxdata[(pxdata == color).all(axis=-1)] = class_color
                color_class_found = True
                break
        if not(color_class_found):
            pxdata[(pxdata == color).all(axis=-1)] = unassigned_color

    imgdest = Image.fromarray(pxdata, mode='RGB')
    imgdest.save(dest)


def get_difference_image(src_1, src_2, dest, opacity=0.0):
    img1_rgb = Image.open(src_1).convert('RGB')
    img2_rgb = Image.open(src_2).convert('RGB')
    diff = ImageChops.difference(img1_rgb, img2_rgb)
    ImageChops.invert(diff).convert('RGB').save(dest)
