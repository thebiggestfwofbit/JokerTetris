import pygame
from src.game import SandtrisGame

def main():
    pygame.init()

    screen = pygame.display.set_mode((360, 720))
    pygame.display.set_caption("JokerTetris")

    clock = pygame.time.Clock()

    game = SandtrisGame(screen)

    # 主循环
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 退出
                running = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                game.handle_input(event.key)

        running = game.update()

        game.draw()
        pygame.display.flip()

        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()