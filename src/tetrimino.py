import random
import pygame

class Tetrimino:
    SHAPES = {
        "I": [(0, 0), (1, 0), (2, 0), (3, 0)],
        "O": [(0, 0), (1, 0), (0, 1), (1, 1)],
        "T": [(1, 0), (0, 1), (1, 1), (2, 1)],
        "S": [(1, 0), (2, 0), (0, 1), (1, 1)],
        "Z": [(0, 0), (1, 0), (1, 1), (2, 1)],
        "L": [(0, 0), (0, 1), (0, 2), (1, 2)],
        "J": [(1, 0), (1, 1), (1, 2), (0, 2)],
    }

    COLORS = [
        (0, 255, 255),  # 天蓝色
        (255, 255, 0),  # 黄色
        (12, 145, 53),  # 绿色
        (255, 0, 255),  # 紫色
    ]

    def __init__(self, grid):
        """
        初始化方块
        """
        self.grid = grid
        self.shape = random.choice(list(self.SHAPES.keys()))
        self.blocks = [(x + 6, y) for x, y in self.SHAPES[self.shape]]
        self.color = random.choice(self.COLORS)

    def move(self, dx, dy):
        """
        移动方块
        """
        if self.can_move(dx, dy):
            self.blocks = [(x + dx, y + dy) for x, y in self.blocks]
            return True
        return False

    def rotate(self):
        """
        旋转方块
        """
        pivot = self.blocks[0]  # 选择第一个方块作为旋转枢轴
        rotated = []
        for x, y in self.blocks:
            rotated.append((pivot[0] - y + pivot[1], pivot[1] + x - pivot[0]))  # 计算旋转后的坐标

        # 检查旋转后的位置是否超出边界
        if all(0 <= nx < self.grid.cols and 0 <= ny < self.grid.rows and self.grid.grid[ny][nx][0] == 0 for nx, ny in
               rotated):
            self.blocks = rotated

    def can_move(self, dx, dy):
        """
        检查是否可以移动
        """
        for x, y in self.blocks:
            nx, ny = x + dx, y + dy
            if nx < 0 or nx >= self.grid.cols or ny >= self.grid.rows or self.grid.grid[ny][nx][0] == 1:
                return False
        return True

    def draw(self, screen):
        """
        绘制当前方块
        """
        for x, y in self.blocks:
            pygame.draw.rect(
                screen,
                self.color,
                pygame.Rect(x * self.grid.cell_size, y * self.grid.cell_size, self.grid.cell_size, self.grid.cell_size),
            )