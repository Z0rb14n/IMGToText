import pygame
import evthandler
import numpy as np

cat = None


def get_cat(size: tuple[int, int]=None) -> pygame.Surface:
    global cat, screen
    if cat is None or (size is not None and cat.get_rect().size != size):
        cat = pygame.image.load("C:\\Users\\babyb\\Pictures\\cat.png")
        if size is not None:
            cat = pygame.transform.scale(cat, size)
    return cat


if __name__ == '__main__':
    pygame.init()
    drawer_size = 100, 120
    drawer_offset = (30, 30)
    drawer_additional_padding = (30, 30)
    black = (0, 0, 0)

    assert pygame.image.get_extended()
    cat = get_cat()
    cat_rect = cat.get_rect()
    evthandler.init(drawer_size)
    window_size = tuple(np.add(evthandler.get_surface_size(),
                               np.add(drawer_offset, drawer_additional_padding)))
    screen = pygame.display.set_mode(window_size)
    draw_rect_area = evthandler.get_surface().get_rect().move(drawer_offset[0], drawer_offset[1])
    while 1:
        evthandler.update(offset=drawer_offset)
        new_size = tuple(np.add(evthandler.get_surface_size(),
                                np.add(drawer_additional_padding,
                                       drawer_offset)))
        if new_size != screen.get_rect().size:
            screen = pygame.display.set_mode(new_size)
            cat = get_cat()
            cat_rect = cat.get_rect()
        screen.fill(black)
        screen.blit(cat, cat_rect)
        screen.blit(evthandler.get_surface(), draw_rect_area)
        pygame.display.update()
