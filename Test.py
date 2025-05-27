from pygame import mixer
import pygame
from os import path

display_surface = pygame.display.set_mode((500,500))
s = pygame.Surface((500,500))
r = s.get_rect()

mixer.init()
mixer.music.load(path.join('music', 'tetrisTechno.mp3'))
mixer.music.play(-1)

display_surface.blit(s,r)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        pygame.display.update()