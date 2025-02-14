> ⚠ **WARNING:**  
> PLEASE USE:
> ```python
> self.mask = pygame.mask.from_surface(self.image)  # for every sprite you make that should collide with the player
> ```
>
> And implement an efficient collision check:
> ```python
> def check_collisions(self, lvl_token_g: 'sprite group') -> None:
>     rect_collide_list = pygame.sprite.spritecollide(player.sprite, lvl_token_g, False)
>     if rect_collide_list:
>         for sprite in rect_collide_list:
>             if pygame.sprite.collide_mask(player.sprite, sprite):
>                 # action
> ```
