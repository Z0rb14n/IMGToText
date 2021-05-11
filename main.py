import pygame
import evthandler

cat = None


def draw_rect(a, b, c, d, color=(0, 0, 0)):
    temp = pygame.Rect((a, b), (a + c, b + d))
    pygame.draw.rect(screen, color, temp, 0)


def get_cat() -> pygame.Surface:
    global cat, screen
    if cat is None or cat.get_rect() != screen.get_rect() :
        cat = pygame.image.load("C:\\Users\\babyb\\Pictures\\cat.png")
        cat = pygame.transform.scale(cat, screen.get_rect().size)
    return cat


if __name__ == '__main__':
    pygame.init()
    size = width, height = 120, 120
    black = (0, 0, 0)
    screen = pygame.display.set_mode((width, height))

    assert pygame.image.get_extended()
    cat = get_cat()
    cat_rect = cat.get_rect()
    evthandler.init((width, height))
    while 1:
        evthandler.update()
        if evthandler.get_surface().get_rect() != screen.get_rect():
            screen = pygame.display.set_mode(evthandler.get_surface().get_rect().size)
            cat = get_cat()
            cat_rect = cat.get_rect()
        screen.fill(black)
        screen.blit(cat, cat_rect)
        screen.blit(evthandler.get_surface(), evthandler.get_surface().get_rect())
        pygame.display.update()
