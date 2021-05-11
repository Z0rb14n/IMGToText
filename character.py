import numpy as np
from typing import Union
_unicode_offset: int = 0x2800


def get_char_from_pixels(pixels: Union[list[bool], np.ndarray]) -> str:
    if len(pixels) != 8:
        print(pixels, len(pixels))
        raise IndexError
    value = _unicode_offset
    for index in range(len(pixels)):
        if pixels[index]:
            value += 2 ** index
    return chr(value)


if __name__ == '__main__':
    all_eight = get_char_from_pixels(np.ones((1, 8), dtype=bool).flatten())
    none = get_char_from_pixels(np.zeros((1, 8), dtype=bool).flatten())
    # note: everything EXCEPT for nones are aligned
    for i in range(0, 10):
        for j in range(0, 10):
            print(' ', end="")
        print(all_eight, end="")
    print()
    for i in range(0, 10):
        for j in range(0, 10):
            print(none, end="")
        print(all_eight, end="")
    print()
    for i in range(0, 10):
        for j in range(0, 10):
            print(all_eight, end="")
        print(all_eight, end="")
    print()
