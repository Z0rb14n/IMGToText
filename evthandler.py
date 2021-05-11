import numpy as np
import sys
import pygame
import pandas as pd
import character

_pixels: np.ndarray = np.zeros((0, 0), bool)
_pressed: list[bool] = [False, False, False]
_size: tuple[int, int] = (0, 0)
_surface: pygame.surface = pygame.Surface((0, 0))
brush_width: int = 2
_pixel_scaling: int = 1
is_brush_square: bool = False
_pixel_on_color: tuple[int, int, int] = (255, 255, 255)
_pixel_off_color: tuple[int, int, int] = (0, 0, 0)


def get_surface() -> pygame.Surface:
    return _surface


def set_pixel_scaling(pixel_scaling: int):
    global _surface, _pixel_scaling, _pixels
    _surface = pygame.Surface((_size[0] * pixel_scaling, _size[1] * pixel_scaling))
    _surface.set_colorkey(_pixel_off_color)
    for x in range(_pixels.shape[0]):
        for y in range(_pixels.shape[1]):
            if _pixels[x][y]:
                _surface.fill(_pixel_on_color, ((x * pixel_scaling, y * pixel_scaling), (pixel_scaling, pixel_scaling)))
            else:
                _surface.fill(_pixel_off_color,
                              ((x * pixel_scaling, y * pixel_scaling), (pixel_scaling, pixel_scaling)))
    _pixel_scaling = pixel_scaling


def _get_left_bound(x: int) -> int:
    global brush_width
    return max(0, x - brush_width)


def _get_right_bound(x: int) -> int:
    global brush_width, _size
    return min(_size[0], x + brush_width)


def _get_top_bound(y: int) -> int:
    global brush_width
    return max(0, y - brush_width)


def _get_bottom_bound(y: int) -> int:
    global brush_width, _size
    return min(_size[1], y + brush_width)


def _ensure_pixels_init():
    global _pixels
    if _pixels is None:
        init()


def _pixel(pos: tuple, color: tuple):
    global _surface, _pixel_scaling
    pos = tuple(ti * _pixel_scaling for ti in pos)
    _surface.fill(color, (pos, (_pixel_scaling, _pixel_scaling)))


def init(size=(854, 480)):
    global _pixels, _size, _surface
    _size = size
    _pixels = np.zeros(size, bool)
    _surface = pygame.Surface(_size)
    _surface.set_colorkey(_pixel_off_color)


def get_pixels() -> np.ndarray:
    global _pixels
    _ensure_pixels_init()
    return _pixels


def add_pixels(pos: tuple):
    global _pixels
    _ensure_pixels_init()
    if not is_brush_square:
        for x in range(_get_left_bound(pos[0]), _get_right_bound(pos[0])):
            for y in range(_get_top_bound(pos[1]), _get_bottom_bound(pos[1])):
                if (x - pos[0]) ** 2 + (y - pos[1]) ** 2 <= brush_width ** 2:
                    _pixel((x, y), _pixel_on_color)
                    _pixels[x][y] = True
    else:
        for x in range(_get_left_bound(pos[0]), _get_right_bound(pos[0])):
            for y in range(_get_top_bound(pos[1]), _get_bottom_bound(pos[1])):
                _pixel((x, y), _pixel_on_color)
                _pixels[x][y] = True


def clear_pixels(pos: tuple):
    _ensure_pixels_init()
    if not is_brush_square:
        for x in range(_get_left_bound(pos[0]), _get_right_bound(pos[0])):
            for y in range(_get_top_bound(pos[1]), _get_bottom_bound(pos[1])):
                if (x - pos[0]) ** 2 + (y - pos[1]) ** 2 <= brush_width ** 2:
                    _pixel((x, y), _pixel_off_color)
                    _pixels[x][y] = False
    else:
        for x in range(_get_left_bound(pos[0]), _get_right_bound(pos[0])):
            for y in range(_get_top_bound(pos[1]), _get_bottom_bound(pos[1])):
                _pixel((x, y), _pixel_off_color)
                _pixels[x][y] = False


def get_string_from_surface() -> str:
    result = ''
    for y in range(0, _pixels.shape[1], 4):
        for x in range(0, _pixels.shape[0], 2):
            bool_array = [_pixels[x][y], _pixels[x + 1][y],
                          _pixels[x][y + 1], _pixels[x + 1][y + 1],
                          _pixels[x][y + 2], _pixels[x + 1][y + 2],
                          _pixels[x][y + 3], _pixels[x + 1][y + 3]]
            result += character.get_char_from_pixels(bool_array)
        result += '\n'
    return result


def _clear_or_add_pixels(pos: tuple):
    pos = tuple(int(ti / _pixel_scaling) for ti in pos)
    if _pressed[1]:
        clear_pixels(pos)
    elif _pressed[0]:
        add_pixels(pos)


def update():
    global _pixels, _pressed, is_brush_square, brush_width, _surface
    _ensure_pixels_init()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            _pressed[event.button - 1] = True
            _clear_or_add_pixels(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            _pressed[event.button - 1] = False
            _clear_or_add_pixels(event.pos)
        elif event.type == pygame.MOUSEMOTION:
            _clear_or_add_pixels(event.pos)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_e:
                df = pd.DataFrame([get_string_from_surface()])
                df.to_clipboard(index=False, header=False)
                print("Exported to clipboard.")
            elif event.key == pygame.K_r:
                _pixels = np.zeros(_size, dtype=bool)
                _surface.fill(_pixel_off_color)
                print("Cleared screen.")
            elif event.key == pygame.K_a:
                brush_width = min(1, brush_width)
                print("Decreased brush width to: ", brush_width)
            elif event.key == pygame.K_d:
                brush_width += 1
                print("Increased brush width to: ", brush_width)
            elif event.key == pygame.K_s:
                is_brush_square = not is_brush_square
                print("Is using square brush: ", is_brush_square)
            elif event.key == pygame.K_m:
                set_pixel_scaling(_pixel_scaling + 1)
                print("Pixel scaling increased to ", _pixel_scaling)
            elif event.key == pygame.K_n:
                set_pixel_scaling(max(1, _pixel_scaling - 1))
                print("Pixel scaling decreased to ", _pixel_scaling)
