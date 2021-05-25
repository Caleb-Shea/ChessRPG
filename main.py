import pygame as pyg
import random
import math
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'

FPS = 30


class Tile(pyg.sprite.Sprite):
    """
         XXXXXXXXXXXXXXXX
               XXXX
               XXXX
               XXXX
               XXXX
               XXXX
               XXXX

    Minimap label
    """
    def __init__(self, window, color, palette, pos, size):
        super().__init__()
        self.window = window

        if color == 'black':
            self.color = (0, 0, 0)
        else:
            self.color = (250, 250, 250)

        self.palette = palette

        self.size = size
        self.true_pos = pos
        self.scaled_pos = self.true_pos

        #self.image = pyg.image.load(get_path('assets', 'imgs', 'tiles', palette, f'{color}.png'))
        self.image = pyg.Surface((self.size, self.size)).convert()
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.scaled_pos
        self.draw_rect = self.rect

    def update(self):
        self.scaled_pos = (self.true_pos[0]*self.size,
                           self.true_pos[1]*self.size)
        self.rect.topleft = self.scaled_pos
        self.image = pyg.Surface((self.size, self.size)).convert()
        self.image.fill(self.color)

    def render(self):
        if self.draw_rect.colliderect(window_rect):
            self.window.blit(self.image, self.draw_rect)

class Board():
    """
         XXXXXXXXXXXX
         XXXX       XXXX
         XXXX       XXXX
         XXXXXXXXXXXX
         XXXX       XXXX
         XXXX       XXXX
         XXXXXXXXXXXX

    Minimap label
    """
    def __init__(self, window):
        self.window = window

        self.tiles = pyg.sprite.Group()

    def generate(self, size=(100, 100), palette='default'):
        for y in range(size[1]):
            for x in range(size[0]):
                if x % 2 == y % 2:
                    color = 'white'
                else:
                    color = 'black'

                tile = Tile(self.window, color, palette, (x, y), 60)
                self.tiles.add(tile)

    def zoom(self, amount):
        for tile in self.tiles:
            if amount < 0:
                if tile.size > 10:
                    tile.size -= 7
                else:
                    tile.size = 10
            else:
                if tile.size < 100:
                    tile.size += 7
                else:
                    tile.size = 100
    def set_tile_size(self, size):
        for tile in self.tiles:
            tile.size = size

    def render(self):
        for tile in self.tiles:
            tile.render()


class Camera():
    """
            XXXXXXXXX
         XXXX       XXXX
         XXXX
         XXXX
         XXXX
         XXXX       XXXX
            XXXXXXXXX

    Minimap label
    """
    def __init__(self):
        self.rect = pyg.rect.Rect(0, 0, WIDTH, HEIGHT)

    def get_world_pos(self, pos):
        return (pos[0] - self.rect.left, pos[1] - self.rect.top)

    def apply_lens(self, player, world, world_decor):
        player.draw_rect = player.rect.move(self.rect.topleft)
        world_decor.bg_draw_rect = world_decor.bg_rect.move(self.rect.topleft)

        everything = (world.walls.sprites() +
                      world.statics.sprites() +
                      world.pickups.sprites() +
                      world.enemies.sprites() +
                      world.bullets.sprites())

        for sprite in everything:
            sprite.draw_rect = sprite.rect.move(self.rect.topleft)

    def follow(self, sprite):
        pos = sprite.rect.center

         # Subtract half of the screen to center the sprite
        top = pos[0] - WIDTH//2
        left = pos[1] - HEIGHT//2
        width = self.rect.width
        height = self.rect.height

        self.rect = pyg.rect.Rect(-top, -left, width, height)


def terminate():
    pyg.quit()
    raise SystemExit()

def get_path(*path):
    """Returns the full file path of a file."""
    dirname = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(dirname, path)

def play_sound(sound):
    se_channel = pyg.mixer.find_channel()

    se_channel.play(sound)

def main():
    """
        XXX         XXX
        XXXXX     XXXXX
        XXX XXX XXX XXX
        XXX  XXXXX  XXX
        XXX   XXX   XXX
        XXX         XXX
        XXX         XXX

    Minimap label
    """

     # Custom Events
    #custom_event = pyg.USEREVENT + 1
    #pyg.time.set_timer(custom_event, 0)

    board = Board(window)
    board.generate()

    clock = pyg.time.Clock()

    paused = False

    while True:
        if not paused:
            for event in pyg.event.get():
                if event.type == pyg.QUIT:
                    terminate()
                elif event.type == pyg.KEYDOWN:
                    if event.key == pyg.K_ESCAPE:
                        paused = True
                    elif event.key == pyg.K_BACKQUOTE:
                        terminate()
                    elif event.key == pyg.K_SPACE:
                        ...
                elif event.type == pyg.MOUSEWHEEL:
                    board.zoom(event.y)

            #camera.follow(player)
            #camera.apply_lens(player, world, world_decor)

            window.fill((50, 50, 200))

            for tile in board.tiles:
                tile.update()
            board.render()

            pyg.display.flip()
            clock.tick(FPS)

        else: # If paused
            for event in pyg.event.get():
                if event.type == pyg.QUIT:
                    terminate()
                elif event.type == pyg.KEYDOWN:
                    if event.key == pyg.K_ESCAPE:
                        paused = False
                    elif event.key == pyg.K_BACKQUOTE:
                        terminate()

            window.fill((100, 100, 200))

            pyg.display.flip()

            clock.tick(FPS)


if __name__ == '__main__':
    pyg.mixer.pre_init(44100, -16, 2, 512)
    pyg.mixer.init()
    pyg.init()
    pyg.display.set_caption("ChessRPG")
    window = pyg.display.set_mode(flags=pyg.HWSURFACE | pyg.FULLSCREEN | pyg.DOUBLEBUF)
    window_rect = window.get_rect()
    WIDTH, HEIGHT = pyg.display.get_window_size()

    # Init camera outside of main() so we can access it anywhere
    camera = Camera()

    main()
