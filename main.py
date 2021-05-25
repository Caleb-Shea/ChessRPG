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
    def __init__(self, window, color, palette):
        super().__init__()
        self.window = window
        self.color = color
        self.palette = palette

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

    def generate(self, size=(8, 8), palette='default'):
        for y in range(size[1]):
            for x in range(size[0]):
                if x % 2 == y % 2:
                    color = 'white'
                else:
                    color = 'black'

                tile = Tile(self.window, color, palette)
                self.tiles.add(tile)


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
    custom_event = pyg.USEREVENT + 1
    #pyg.time.set_timer(custom_event, 0)

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

            camera.follow(player)
            camera.apply_lens(player, world, world_decor)

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

            window.fill((255, 255, 255))

            pyg.display.flip()

            clock.tick(FPS)


if __name__ == '__main__':
    pyg.mixer.pre_init(44100, -16, 2, 512)
    pyg.mixer.init()
    pyg.init()
    pyg.display.set_caption("ChessRPG")
    window = pyg.display.set_mode(flags=pyg.HWSURFACE | pyg.FULLSCREEN | pyg.DOUBLEBUF)
    WIDTH, HEIGHT = pyg.display.get_window_size()

    # Init camera outside of main() so we can access it anywhere
    camera = Camera()

    main()
