import pygame
from settings import *

screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))


class SpriteSheet:

    def __init__(self, filename):
        """Load the sheet."""
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error as e:
            print(f"Unable to load spritesheet image: {filename}")
            raise SystemExit(e)

    def image_at(self, rectangle, colorkey=None):
        """Load a specific image from a specific rectangle."""
        """rectangle is a tuple with (x, y, x+offset, y+offset)"""
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((5, 5))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def images_at(self, rects, colorkey=None):
        """Load a whole bunch of images and return them as a list."""
        return [self.image_at(rect, colorkey) for rect in rects]

    def load_strip(self, rect, image_count, colorkey=None):
        """Load a whole strip of images, and return them as a list."""
        tups = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)

    def load_grid_images(self, num_rows, num_cols, x_margin=0, x_padding=0,
                         y_margin=0, y_padding=0, width=None, height=None, colorkey=None):
        """Load a grid of images.
        x_margin is the space between the top of the sheet and top of the first
        row. x_padding is space between rows. Assumes symmetrical padding on
        left and right.  Same reasoning for y. Calls self.images_at() to get a
        list of images.
        """

        sheet_rect = self.sheet.get_rect()

        sheet_width, sheet_height = sheet_rect.size

        # To calculate the size of each sprite, subtract the two margins,
        #   and the padding between each row, then divide by num_cols.
        # Same reasoning for y.
        if width and height:
            x_sprite_size = width
            y_sprite_size = height
        else:
            x_sprite_size = (sheet_width - 2 * x_margin
                             - (num_cols - 1) * x_padding) / num_cols
            y_sprite_size = (sheet_height - 2 * y_margin
                             - (num_rows - 1) * y_padding) / num_rows

        sprite_rects = []
        for row_num in range(num_rows):
            for col_num in range(num_cols):
                # Position of sprite rect is margin + one sprite size
                #   and one padding size for each row. Same for y.
                x = x_margin + col_num * (x_sprite_size + x_padding)
                y = y_margin + row_num * (y_sprite_size + y_padding)
                sprite_rect = (x, y, x_sprite_size, y_sprite_size)
                sprite_rects.append(sprite_rect)

        return self.images_at(sprite_rects, colorkey)


class Layout:
    def __init__(self, display):
        self.display = display
        tile_sheet = SpriteSheet('sheet.png')
        rusty_box = SpriteSheet('Rusty Crate.png')

        # blocks and tiles for the game
        plain_block = tile_sheet.image_at((128, 1, 54, 16))
        rustybox_block = rusty_box.image_at((0, 0, 32, 32))
        rockplatform_block = tile_sheet.image_at((159, 1, 48, 16))
        caverock_block = tile_sheet.image_at((160, 31, 49, 16))
        rock_item = tile_sheet.image_at((257, 101, 12, 16))

        self.tile_list = []
        for i, row in enumerate(layout1):
            for j, col in enumerate(row):
                x_val = j * TILE_SIZE
                y_val = i * TILE_SIZE

                # layout for the game
                if col == "1":
                    image_rect = plain_block.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val
                    tile = (plain_block, image_rect)
                    self.tile_list.append(tile)
                if col == '2':
                    image_rect = rustybox_block.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val
                    tile = (rustybox_block, image_rect)
                    self.tile_list.append(tile)
                if col == '3':
                    image_rect = rockplatform_block.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val
                    tile = (rockplatform_block, image_rect)
                    self.tile_list.append(tile)
                if col == '4':
                    image_rect = caverock_block.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val
                    tile = (caverock_block, image_rect)
                    self.tile_list.append(tile)
                if col == '5':
                    image_rect = rock_item.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val
                    tile = (rock_item, image_rect)
                    self.tile_list.append(tile)

    def update(self, display):
        for tile in self.tile_list:
            display.blit(tile[0], tile[1])

    def get_tiles(self):
        return self.tile_list


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_size, tile):
        pygame.sprite.Sprite.__init__(self)
        character_sheet = SpriteSheet('characters.png')

        # image set for the player
        self.run_right = []
        self.run_rt = character_sheet.image_at((6, 73, 20, 25))
        self.run_right.append(self.run_rt)
        self.run_rt1 = character_sheet.image_at((38, 72, 21, 26))
        self.run_right.append(self.run_rt1)
        self.run_rt2 = character_sheet.image_at((70, 70, 21, 31))
        self.run_right.append(self.run_rt2)
        self.run_rt3 = character_sheet.image_at((101, 68, 22, 32))
        self.run_right.append(self.run_rt3)
        self.run_rt4 = character_sheet.image_at((486, 72, 20, 27))
        self.run_right.append(self.run_rt4)
        self.run_rt5 = character_sheet.image_at((518, 70, 20, 30))
        self.run_right.append(self.run_rt5)
        self.run_rt6 = character_sheet.image_at((550, 71, 20, 30))
        self.run_right.append(self.run_rt6)
        self.run_left = [pygame.transform.flip(image, True, False) for image in self.run_right]
        self.index = 0
        self.tile_size = tile_size
        self.tile = tile
        self.image = self.run_right[self.index]
        self.rect = self.image.get_rect()
        self.last = pygame.time.get_ticks()
        self.image_delay = 100
        self.rect.x = x
        self.rect.y = y
        self.right = False
        self.left = False

    def update(self, display):
        dy = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.dx = 5
            self.right = True
            self.left = False
            now = pygame.time.get_ticks()
            if now - self.image_delay >= self.last:
                self.last = now
                if self.index >= len(self.run_right) - 1:
                    self.index = 0
                else:
                    self.index += 1
                self.image = self.run_right[self.index]