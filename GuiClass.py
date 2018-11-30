"""
select function (computer bor human)
"""

import pygame

class GuiClass():
    def gui():

        pygame.init()
        screen = pygame.display.set_mode((800,600))

        pygame.mouse.set_visible(1)
        pygame.key.set_repeat(1, 30)

        pygame.display.set_caption("Vier-Gewinnt")
        done = False

        clock = pygame.time.Clock()

        running = True
        while running:

            clock.tick(30)
            screen.fill ((32,178,170))
            pygame.display.flip()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

