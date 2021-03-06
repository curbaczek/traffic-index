from PIL import Image, ImageFont, ImageDraw

DRAW_TEXT_FONT = "res/fonts/arial_bold.ttf"
DRAW_TEXT_FONT_SIZE = 30
DRAW_DATE_FONT_SIZE = 100
DRAW_TEXT_FONT_COLOR = (0, 0, 0)
DRAW_TEXT_MARGIN = 5

MAX_GRID_SIZE = 5000


def bottom_crop_image(image_filename, bottom_margin):
    im = Image.open(image_filename)
    img_width, img_height = im.size
    im.crop((0, 0, img_width, img_height-bottom_margin)).save(image_filename)


def get_grid_size(tiles_matrix):
    hcount = len(tiles_matrix)
    vcount = 0 if hcount == 0 else len(tiles_matrix[0])
    return (hcount, vcount)


def get_grid_tile_size(tiles_matrix):
    assert len(tiles_matrix) > 0 and len(tiles_matrix[0]) > 0
    tile_image = None
    for x in range(len(tiles_matrix)):
        if tile_image is not None:
            break
        for y in range(len(tiles_matrix[x])):
            tile_information = tiles_matrix[x][y]
            tile_filename = tile_information[2]
            if tile_filename is not None:
                tile_image = Image.open(tile_filename)
                break
    return tile_image.size


def init_grid_image(tiles_matrix, tiles_margin, max_grid_size):
    (tiles_hcount, tiles_vcount) = get_grid_size(tiles_matrix)
    (tile_width, tile_height) = get_grid_tile_size(tiles_matrix)
    grid_width = tile_width + (tiles_hcount-1) * (tile_width + tiles_margin)
    grid_height = tile_height + (tiles_vcount-1) * (tile_height + tiles_margin)
    tile_scale = 1.0
    if grid_width > max_grid_size or grid_height > max_grid_size:
        hscale = max_grid_size/(tiles_hcount * tile_width)
        vscale = max_grid_size/(tiles_vcount * tile_height)
        tile_scale = min(hscale, vscale)
        grid_width = min(grid_width, max_grid_size)
        grid_height = min(grid_height, max_grid_size)
    grid = Image.new("RGB", (grid_width, grid_height))
    return (grid, tile_scale)


def get_draw_text_width(image, text, font, font_size):
    draw = ImageDraw.Draw(image)
    text_width, text_height = draw.textsize(
        text,
        font=ImageFont.truetype(font, font_size))
    return text_width


def draw_grid_text(image, x, y, txt, fontsize=DRAW_TEXT_FONT_SIZE):
    draw = ImageDraw.Draw(image)
    draw.text(
        (x, y), txt, DRAW_TEXT_FONT_COLOR,
        font=ImageFont.truetype(DRAW_TEXT_FONT, fontsize))


def draw_grid_tile_coordinates(image, tile_pos_x, tile_pos_y, grid_x, grid_y):
    draw_grid_text(
        image, tile_pos_x + DRAW_TEXT_MARGIN, tile_pos_y + DRAW_TEXT_MARGIN,
        "({}|{})".format(grid_x, grid_y))


def draw_grid_date(image, grid_date_str):
    if grid_date_str is not None:
        (image_width, image_height) = image.size
        text_width = get_draw_text_width(image, grid_date_str, DRAW_TEXT_FONT, DRAW_DATE_FONT_SIZE)
        draw_grid_text(
            image, image_width - text_width,
            image_height - DRAW_TEXT_MARGIN - DRAW_DATE_FONT_SIZE,
            grid_date_str,
            fontsize=DRAW_DATE_FONT_SIZE)


def get_scaled_image(filename, scale):
    im = Image.open(filename)
    (w, h) = im.size
    im = im.resize((round(w * scale), round(h * scale)), Image.ANTIALIAS)
    return im


def get_skipped_tile(width, height):
    return Image.new("RGB", (width, height), "#EFEFEF")


def generate_grid_image(image_filename, tiles_matrix, max_grid_size=MAX_GRID_SIZE,
                        tiles_margin=3, show_coords=True, grid_date_str=None, final_size=None):
    (grid, tile_scale) = init_grid_image(tiles_matrix, tiles_margin, max_grid_size)
    (tile_width, tile_height) = get_grid_tile_size(tiles_matrix)
    for x in range(len(tiles_matrix)):
        for y in range(len(tiles_matrix[x])):
            tile_information = tiles_matrix[x][y]
            tile_filename = tile_information[2]
            if (tile_filename is None):
                tile_image = get_skipped_tile(tile_width, tile_height)
            else:
                tile_image = get_scaled_image(tile_filename, tile_scale)
            tile_pos_x = round(x * (tile_width*tile_scale + tiles_margin))
            tile_pos_y = round(y * (tile_height*tile_scale + tiles_margin))
            grid.paste(tile_image, (tile_pos_x, tile_pos_y))
            draw_grid_tile_coordinates(grid, tile_pos_x, tile_pos_y, tile_information[0], tile_information[1])
    if grid_date_str is not None:
        draw_grid_date(grid, grid_date_str)
    if final_size is not None:
        grid.thumbnail(final_size, Image.ANTIALIAS)
    grid.save(image_filename)
