from __future__ import division
from PIL import Image, ImageChops, ImageDraw
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
    """ takes a list of color classes tuples (name, color) and assign the image colors
        with the given threshold to these classes """
    result = {}
    color_counts = get_color_count(image, True)

    if (len(color_classes) > 0):
        for color_class_definition in color_classes:
            filtered_color_count = []
            matched_colors = []
            class_name = color_class_definition[0]
            class_color = color_class_definition[1]
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
            result.update({
                class_name: {
                    "seed": class_color,
                    "count": sum_color_count(matched_colors),
                    "colors": matched_colors
                }
            })

    result.update({
        "z-no-class": {
            "count": sum_color_count(color_counts),
            "colors": color_counts
        }
    })

    return result


"""
def get_difference_image(src_1, src_2, dest, opacity=0.0):

    img1 = Image.open(src_1)
    img1_rgb = Image.open(src_1).convert('RGB')
    img2 = Image.open(src_2)
    img2_rgb = Image.open(src_2).convert('RGB')

    diff = ImageChops.difference(img1, img2)
    diff.save("temp/diff_test_diff_img1_img2.png")

    diff = ImageChops.difference(img1_rgb, img2_rgb)
    diff.save("temp/diff_test_diff_img1_img2_rgb.png")

    diff = ImageChops.difference(img1_rgb, img2_rgb)
    diff = ImageChops.invert(diff).convert('RGB')
    diff.save("temp/diff_test_diff_img1_img2_rgb_invert.png")

    # hist = diff.histogram()
    # print sum(hist)

    img = Image.open("temp/diff_test_diff_img1_img2_rgb_invert.png").convert('RGB')
    # print img.getpixel((100,100))
    colors = img.getcolors()
    # print colors

    diff = ImageChops.subtract(img1, img2)
    diff.save("temp/diff_test_sub_img1_img2.png")

    diff = ImageChops.subtract(img1_rgb, img2_rgb)
    diff.save("temp/diff_test_sub_img1_img2_rgb.png")

    diff = ImageChops.subtract(img2, img1)
    diff.save("temp/diff_test_sub_img2_img1.png")

    diff = ImageChops.subtract(img2_rgb, img1_rgb)
    diff.save("temp/diff_test_sub_img2_img1_rgb.png")

    # ---
    diff = ImageChops.difference(b,a)
    diff = diff.convert('L')

    thresholded_diff = diff
    for repeat in range(3):
        thresholded_diff  = ImageChops.add(thresholded_diff, thresholded_diff)

    h,w = size = diff.size
    mask = new_gray(size, int(255 * (opacity)))
    shade = new_gray(size, 0)
    new = a.copy()
    new.paste(shade, mask=mask)
    new.paste(b, mask=thresholded_diff)
    new.save(dest)
    # ---
"""
