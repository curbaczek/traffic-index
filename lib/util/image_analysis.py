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

    if (len(color_counts) > 0):
        result.update({
            "z-no-class": {
                "count": sum_color_count(color_counts),
                "colors": color_counts
            }
        })

    return result


""" -------------------------------------- """


THRESHOLD = 140  # 100 -> 112%, 170 -> 95%


def get_white_color_percent(image_filename):
    image_file = Image.open(image_filename)
    image = image_file.convert('L')
    image = numpy.array(image)
    image = binarize_array(image, THRESHOLD)

    white_pixels = 0
    other_pixels = 0

    for i in range(len(image)):
        for j in range(len(image[0])):
            if image[i][j] == 255:
                white_pixels += 1
            else:
                other_pixels += 1

    """colors = image.getcolors()
    white_pixels = 0
    other_pixels = 0
    print image
    for count,color in colors:
        #if (color[0] == color[1] and color[1] == color[2] and color[0] >= 254):
        if (color == 255):
            white_pixels += count
        else:
            other_pixels += count"""

    print "white: {}, other: {}".format(white_pixels, other_pixels)
    return 100*white_pixels/(white_pixels + other_pixels)


def binarize_image(img_path, target_path, threshold):
    """Binarize an image."""
    """http://stackoverflow.com/a/37497975"""
    image_file = Image.open(img_path)
    image = image_file.convert('L')  # convert image to monochrome
    image = numpy.array(image)
    image = binarize_array(image, threshold)
    imsave(target_path, image)


def binarize_array(numpy_array, threshold=THRESHOLD):
    """Binarize a numpy array."""
    for i in range(len(numpy_array)):
        for j in range(len(numpy_array[0])):
            if numpy_array[i][j] > threshold:
                numpy_array[i][j] = 255
            else:
                numpy_array[i][j] = 0
    return numpy_array


def bottom_crop_image(image_filename, bottom_margin):
    im = Image.open(image_filename)
    img_width, img_height = im.size
    im.crop((0, 0, img_width, img_height-bottom_margin)).save(image_filename)


def generate_color_to_black_image(image_filename, new_image_filename, search_color):
    im = Image.open(image_filename).convert('RGB')
    img_width, img_height = im.size
    for x in range(img_width):
        for y in range(img_height):
            current_color = im.getpixel((x, y))
            if (current_color == search_color):
                im.putpixel((x, y), (0, 0, 0))
    im.save(new_image_filename)


def new_gray(size, color):
    img = Image.new('L', size)
    dr = ImageDraw.Draw(img)
    dr.rectangle((0, 0) + size, color)
    return img


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
    print colors

    diff = ImageChops.subtract(img1, img2)
    diff.save("temp/diff_test_sub_img1_img2.png")

    diff = ImageChops.subtract(img1_rgb, img2_rgb)
    diff.save("temp/diff_test_sub_img1_img2_rgb.png")

    diff = ImageChops.subtract(img2, img1)
    diff.save("temp/diff_test_sub_img2_img1.png")

    diff = ImageChops.subtract(img2_rgb, img1_rgb)
    diff.save("temp/diff_test_sub_img2_img1_rgb.png")

    """diff = ImageChops.difference(b,a)
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
    new.save(dest)"""
