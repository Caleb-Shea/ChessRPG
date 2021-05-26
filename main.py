import pygame as pyg
import random
import math
import os


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

    A class to represent one square on the game board.
    """
    def __init__(self, window, color, palette, pos):
        super().__init__()
        self.window = window

        if color == 'black':
            self.color = (0, 0, 0)
        else:
            self.color = (250, 250, 250)

        self.palette = palette

        self.size = 20
        self.true_pos = pos
        self.scaled_pos = self.true_pos

        #self.image = pyg.image.load(get_path('assets', 'imgs', 'tiles', palette, f'{color}.png'))
        self.image = pyg.Surface((self.size, self.size)).convert()
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.scaled_pos

    def update(self, camera_pos):
        """
        Update any data related to this tile.  Called every tick.

        1) set position according to size and camera_pos
        2) update image accordingly
        """
        self.scaled_pos = (self.true_pos[0]*self.size,
                           self.true_pos[1]*self.size)
        self.rect.topleft = self.scaled_pos

        self.rect.x += camera_pos[0]
        self.rect.y += camera_pos[1]

        self.image = pyg.Surface((self.size, self.size)).convert()
        self.image.fill(self.color)

    def render(self):
        """Render the tile, but only if it is onscreen."""
        if self.rect.colliderect(window_rect):
            self.window.blit(self.image, self.rect)

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

    A management class to keep track of the board state, the tiles, and
    the pieces.  Camera management (zooming) is done here as well.
    """
    def __init__(self, window):
        self.window = window

        self.tiles = pyg.sprite.Group()
        self.pieces = pyg.sprite.Group()

    def generate(self, size=(50, 50), topleft=(0, 0), palette='standard'):
        """Create a square region of tiles in alternating colors."""
        for y in range(size[1]):
            for x in range(size[0]):
                if x % 2 == y % 2:
                    color = 'white'
                else:
                    color = 'black'

                tile = Tile(self.window, color, palette, (x+topleft[0], y+topleft[1]))
                self.tiles.add(tile)

    def zoom(self, amount):
        """
        Make all tiles and pieces bigger, but within the boundries of
        10px and 100px.
        """
        zoomables = self.tiles.sprites() + self.pieces.sprites()
        for things in zoomables:
            if amount < 0:
                if things.size > 10:
                    things.size -= 7
                else:
                    things.size = 10
            else:
                if things.size < 100:
                    things.size += 7
                else:
                    things.size = 100

    def render(self):
        """
        Render all tiles and all pieces.  The check to see if the sprites
        are onscreen is done by the sprites themselves.
        """
        for tile in self.tiles:
            tile.render()
        for piece in self.pieces:
            piece.render()


class Piece(pyg.sprite.Sprite):
    def __init__(self, window, pos, type, color, palette):
        """
             XXXXXXXXXXXX
             XXXX       XXXX
             XXXX       XXXX
             XXXXXXXXXXXX
             XXXX
             XXXX
             XXXX

        Minimap label

        A class to represent a playing piece.
        """
        super().__init__()
        self.window = window

        if color == 'black':
            self.color = (0, 0, 0)
        else:
            self.color = (250, 250, 250)

        self.type = type

        self.size = 20 # Must be the same size as the initial size of the tiles
        self.true_pos = pos
        self.scaled_pos = self.true_pos

        self.spritesheet = pyg.image.load(get_path('assets', 'imgs', 'pieces', f'{palette}.png'))
        self.sheet_pos = [None, None]

        # Get spritesheet coords based on the type of piece
        if type == 'king':
            self.sheet_pos[0] = (0, 330)
        elif type == 'queen':
            self.sheet_pos[0] = (331, 695)
        elif type == 'bishop':
            self.sheet_pos[0] = (696, 1024)
        elif type == 'knight':
            self.sheet_pos[0] = (1025, 1343)
        elif type == 'rook':
            self.sheet_pos[0] = (1344, 1615)
        elif type == 'pawn':
            self.sheet_pos[0] = (1616, 1848)
        if color == 'white':
            self.sheet_pos[1] = (0, 334)
        elif color == 'black':
            self.sheet_pos[1] = (335, 675)
        self.sheet_rect = pyg.rect.Rect(self.sheet_pos[0][0],
                                        self.sheet_pos[1][0],
                                        self.sheet_pos[0][1] - self.sheet_pos[0][0],
                                        self.sheet_pos[1][1] - self.sheet_pos[1][0])

        # Get the correct size image based on the piece
        self.base_image = pyg.Surface(self.sheet_rect.size).convert_alpha()
        self.base_image.fill((0, 0, 0, 0))
        self.base_image.blit(self.spritesheet, (0, 0), self.sheet_rect)

        self.image = pyg.transform.smoothscale(self.base_image, (self.size, self.size)).convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.topleft = self.scaled_pos

    def open_menu(self):
        """
        Called when the piece is clicked.  Used to open any menus that
        are related to the piece and also to display the available moves.
        """

    def update(self, camera_pos):
        """
        Update any data related to this piece.  Called every tick.

        1) set position according to size and camera_pos
        2) update image accordingly
        """
        self.scaled_pos = (self.true_pos[0]*self.size,
                           self.true_pos[1]*self.size)
        self.rect.topleft = self.scaled_pos

        self.rect.x += camera_pos[0]
        self.rect.y += camera_pos[1]

        self.image = pyg.transform.smoothscale(self.base_image, (self.size, self.size)).convert_alpha()

    def render(self):
        """Render the tile, but only if it is onscreen."""
        if self.rect.colliderect(window_rect):
            self.window.blit(self.image, self.rect)


def terminate():
    """Cleanly exit the program."""
    pyg.quit()
    raise SystemExit()

def get_path(*path):
    """Returns the full file path of a file."""
    dirname = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(dirname, *path)

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

    board = Board(window)
    board.generate()

    camera_pos = [0, 0]

    p1 = Piece(window, (10, 10), 'queen', 'white', 'standard')
    p2 = Piece(window, (20, 12), 'knight', 'black', 'standard')
    board.pieces.add(p1, p2)

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
                elif event.type == pyg.MOUSEBUTTONUP:
                    for piece in board.pieces:
                        if pieces.rect.collidepoint(event.pos):
                            piece.open_menu()
                            break
                # Zoom in and out using the scroll wheel
                elif event.type == pyg.MOUSEWHEEL:
                    board.zoom(event.y)
                # Drag the board around using the mouse pointer
                elif event.type == pyg.MOUSEMOTION:
                    if event.buttons[0]:
                        # Using event.rel is easy but is a bit laggy
                        camera_pos[0] += event.rel[0]
                        camera_pos[1] += event.rel[1]

            window.fill((50, 50, 200))

            for tile in board.tiles:
                tile.update(camera_pos)
            for piece in board.pieces:
                piece.update(camera_pos)

            board.render()

            pyg.display.flip()
            clock.tick(30)

        else: # If paused
            for event in pyg.event.get():
                if event.type == pyg.QUIT:
                    terminate()
                elif event.type == pyg.KEYDOWN:
                    if event.key == pyg.K_ESCAPE:
                        paused = False
                    elif event.key == pyg.K_BACKQUOTE:
                        terminate()

            window.fill((0, 0, 0))

            pyg.display.flip()
            clock.tick(30)


if __name__ == '__main__':
    pyg.mixer.pre_init(44100, -16, 2, 512)
    pyg.mixer.init()
    pyg.init()
    pyg.display.set_caption("ChessRPG")
    window = pyg.display.set_mode(flags=pyg.HWSURFACE | pyg.FULLSCREEN | pyg.DOUBLEBUF)
    window_rect = window.get_rect().inflate(180, 180) # 180 padding so rendering is nice
    WIDTH, HEIGHT = pyg.display.get_window_size()

    main()
