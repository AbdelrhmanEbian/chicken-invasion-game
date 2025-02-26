import pygame


def extract_frames(spritesheet, rows: int, cols: int, scale: tuple = ()) -> tuple:
    sprite_width, sprite_height = spritesheet.get_width() / cols, spritesheet.get_height() / rows
    # adding scale perimeter to enlarge image if needed by ternary condition
    return tuple(
        pygame.transform.smoothscale(
            spritesheet.subsurface(pygame.Rect(col * sprite_width, row * sprite_height, sprite_width, sprite_height)),
            scale)
        if not len(scale) == 0 else
        (spritesheet.subsurface(pygame.Rect(col * sprite_width, row * sprite_height, sprite_width, sprite_height)))
        for col in range(cols) for row in range(rows)
    )
