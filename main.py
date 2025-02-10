import pygame
pygame.font.init()
pygame.mixer.init()

fps = 60
playing = True

def draw():
    # draw the objects which will be displayed on the screen
    pygame.display.update()
    pass

def main():
    clock = pygame.time.Clock()
    while playing :
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
        
main()