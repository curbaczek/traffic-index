from PIL import Image


def bottom_crop_image(image_filename, bottom_margin):
    im = Image.open(image_filename)
    img_width, img_height = im.size
    im.crop((0, 0, img_width, img_height-bottom_margin)).save(image_filename)
