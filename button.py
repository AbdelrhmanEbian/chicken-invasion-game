from init import *
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
        bg_color = (20, 20, 20, 200) if self.hover else self.bg_color
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


class ControlButton(Button):
    control_buttons = [None, None]  # index (0) for save settings , index (1) for continue game
    """Button to save settings to file"""

    def __init__(self, x, y, width, height, bg_color, color, text):
        self.is_changed = False
        super().__init__(x=x, y=y, width=width, height=height, bg_color=bg_color, color=color, text=text)

    def render_text(self):
        condition = self.hover and self.is_changed
        if hasattr(self, 'active'):
            self.is_changed = settings.continue_game
        self.image.fill((0, 0, 0, 0))  # Clear the surface
        if condition:
            text_surface = self.font.render(self.text, True, self.color)
            pygame.draw.rect(self.image, (20, 20, 20, 200), (0, 0, self.width + 50, self.height + 30), border_radius=20)
        else:
            text_surface = self.font.render(self.text, True, self.color if self.is_changed else (50, 50, 50, 200))
            pygame.draw.rect(self.image, (0, 0, 0, 150), (0, 0, self.width, self.height), border_radius=20)
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
        self.image.blit(text_surface, text_rect)

    def control(self):
        pass

    def check_collision(self):
        if pygame.mouse.get_pressed()[0]:  # Left mouse button
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos) and settings.is_game_pause:
                self.control()

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.hover = self.rect.collidepoint(mouse_pos)
        if self.hover or self.is_changed:
            self.render_text()
        self.check_collision()
