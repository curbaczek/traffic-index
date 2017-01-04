from PIL import Image, ImageFont, ImageDraw

DRAW_TEXT_FONT = "res/fonts/arial_bold.ttf"
DRAW_TEXT_FONT_SIZE = 30
DRAW_TEXT_FONT_COLOR = (255, 255, 255)
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
    tile_information = tiles_matrix[0][0]
    tile_image = Image.open(tile_information[2])
    return tile_image.size


def init_grid_image(tiles_matrix, tiles_margin):
    (tiles_hcount, tiles_vcount) = get_grid_size(tiles_matrix)
    (tile_width, tile_height) = get_grid_tile_size(tiles_matrix)
    grid_width = tile_width + (tiles_hcount-1) * (tile_width + tiles_margin)
    grid_height = tile_height + (tiles_vcount-1) * (tile_height + tiles_margin)
    tile_scale = 1.0
    if grid_width > MAX_GRID_SIZE or grid_height > MAX_GRID_SIZE:
        hscale = MAX_GRID_SIZE/(tiles_hcount * tile_width)
        vscale = MAX_GRID_SIZE/(tiles_vcount * tile_height)
        tile_scale = min(hscale, vscale)
        grid_width = min(grid_width, MAX_GRID_SIZE)
        grid_height = min(grid_height, MAX_GRID_SIZE)
    grid = Image.new("RGB", (grid_width, grid_height))
    return (grid, tile_scale)


def draw_grid_tile_coordinates(image, tile_pos_x, tile_pos_y, grid_x, grid_y):
    draw = ImageDraw.Draw(image)
    draw.text(
        (tile_pos_x + DRAW_TEXT_MARGIN, tile_pos_y + DRAW_TEXT_MARGIN),
        "({}|{})".format(grid_x, grid_y),
        DRAW_TEXT_FONT_COLOR,
        font=ImageFont.truetype(DRAW_TEXT_FONT, DRAW_TEXT_FONT_SIZE))


def get_scaled_tile(filename, scale):
    im = Image.open(filename)
    (w, h) = im.size
    im = im.resize((round(w * scale), round(h * scale)), Image.ANTIALIAS)
    return im


def generate_grid_image(image_filename, tiles_matrix, tiles_margin=3, show_coords=True):
    (grid, tile_scale) = init_grid_image(tiles_matrix, tiles_margin)
    for x in range(len(tiles_matrix)):
        for y in range(len(tiles_matrix[x])):
            tile_information = tiles_matrix[x][y]
            tile_image = get_scaled_tile(tile_information[2], tile_scale)
            (tile_width, tile_height) = tile_image.size
            tile_pos_x = round(x * (tile_width + tiles_margin))
            tile_pos_y = round(y * (tile_height + tiles_margin))
            grid.paste(tile_image, (tile_pos_x, tile_pos_y))
            draw_grid_tile_coordinates(grid, tile_pos_x, tile_pos_y, tile_information[0], tile_information[1])
    grid.save(image_filename)
