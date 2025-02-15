import pygame
text_font = pygame.font.SysFont('comicsans' , 30 , bold=True)
class Button(pygame.sprite.Sprite):
    def __init__(self , x , y , width , height , bg_color , color , text):
        super().__init__()
        self.color = color
        self.bg_color = bg_color
        self.current_bg_color = self.bg_color
        self.font = text_font
        self.text = text
        self.width = width
        self.height = height
        self.image = pygame.Surface((width , height),pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x,y))
        self.hover = False
        self.render_text()
    def render_text(self):
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        if self.hover : 
            text_surface = self.font.render(self.text, True, self.color)
            pygame.draw.rect(self.image, (20, 20, 20, 200) , (0, 0, self.width + 50, self.height + 30 ), border_radius=20)
        else:
            text_surface = self.font.render(self.text, True, self.color)
            pygame.draw.rect(self.image, (0,0,0,200), (0, 0, self.width, self.height), border_radius=20)
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
        self.image.blit(text_surface, text_rect)
    def animate(self):
        coordinates = pygame.mouse.get_pos()
        if self.rect.collidepoint(coordinates):
            self.hover = True
        else:
            self.hover = False
            self.current_bg_color = self.bg_color
    def update(self):
        self.animate()
        self.render_text()