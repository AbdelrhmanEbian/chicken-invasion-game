import pygame
pygame.init()
text_font = pygame.font.SysFont('comicsans', 30, bold=True)


class Button(pygame.sprite.Sprite):
    def __init__(self, x: float, y: float, width: float, height: float, bg_color, color, text: str) -> None:
        super().__init__()
        self.color = color
        self.bg_color = bg_color
        self.font = text_font
        self.text = text
        self.width = width
        self.height = height
        self.hover = False
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        self.render_text()  # Render initially

    def render_text(self):
        """Renders the button with text and hover effects."""
        self.image.fill((0, 0, 0, 0))  # Clear previous surface

        # Background color changes on hover
        bg_color = (20, 20, 20, 200) if self.hover else (0, 0, 0, 200)
        pygame.draw.rect(self.image, bg_color, (0, 0, self.width, self.height), border_radius=20)

        # Render text
        text_surface = self.font.render(self.text, True, self.color)
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
        self.image.blit(text_surface, text_rect)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        prev_hover = self.hover
        self.hover = self.rect.collidepoint(mouse_pos)

        # Only re-render if hover state changes
        if self.hover != prev_hover:
            self.render_text()
