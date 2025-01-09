import pygame
from src.grid import Grid
from src.tetrimino import Tetrimino

class SandtrisGame:
    def __init__(self, screen):
        """
        初始化游戏对象
        """
        self.screen = screen  # 游戏窗口
        self.grid = Grid(15, 30, 24)  # 网格
        self.current_tetrimino = Tetrimino(self.grid)  # 当前操作的方块


        # 加载字体
        self.font = pygame.font.Font("assets/font.ttf", 40)

        # 控制方块下落的计时器
        self.drop_timer = 0
        self.drop_interval = 350  # 每 500ms 下落一次


    def handle_input(self, key):
        """
        处理用户输入
        """
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.current_tetrimino.move(-3, 0)

        elif keys[pygame.K_RIGHT]:
            self.current_tetrimino.move(1, 0)

        elif keys[pygame.K_DOWN]:
            self.current_tetrimino.move(0, 1)

        elif keys[pygame.K_UP]:
            self.current_tetrimino.rotate()

    def update(self):
        """
        更新游戏逻辑
        """
        current_time = pygame.time.get_ticks()

        if current_time - self.drop_timer >= self.drop_interval:
            if not self.current_tetrimino.move(0, 1):  # 如果不能下落
                self.grid.add_tetrimino_to_sand(self.current_tetrimino)  # 将方块分解为沙粒
                self.grid.collapse_sand(current_time)  # 沙粒自由下落
                self.grid.clear_connected_sand()  # 检查并清除符合规则的沙粒
                self.current_tetrimino = Tetrimino(self.grid)  # 生成新的方块

                if self.grid.is_game_over():
                    self.show_game_over()
                    return False

            self.drop_timer = current_time

        self.grid.collapse_sand(current_time)

        return True

    def show_game_over(self):
        """
        显示游戏结束画面
        """
        self.screen.fill((0, 0, 0))
        game_over_text = self.font.render("GAME OVER", True, (255, 0, 0))
        self.screen.blit(game_over_text, (70, 360))
        pygame.display.flip()
        pygame.time.wait(3000)  # 显示 3 秒

    def draw(self):
        """
        绘制游戏画面
        """
        self.screen.fill((0, 0, 0))  # 背景黑色
        self.grid.draw(self.screen)  # 绘制网格和已经落下来的沙粒
        self.current_tetrimino.draw(self.screen)  # 绘制当前方块

        score_text = self.font.render(f"Score: {self.grid.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))