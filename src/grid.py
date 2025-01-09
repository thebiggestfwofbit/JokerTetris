import pygame

class Grid:
    def __init__(self, cols, rows, cell_size):
        """
        初始化游戏网格
        """
        self.score = 0  # 游戏得分
        self.cols = cols  # 网格列数
        self.rows = rows  # 网格行数
        self.cell_size = cell_size  # 格大小
        self.grid = [[(0, None) for _ in range(cols)] for _ in range(rows)]

        self.sand_timer = 0
        self.sand_interval = 50

    def add_tetrimino_to_sand(self, tetrimino):
        """
        将方块分解为沙粒并添加到网格
        """
        for x, y in tetrimino.blocks:
            if 0 <= y < self.rows:
                self.grid[y][x] = (1, tetrimino.color)

    def collapse_sand(self, current_time):
        """
        让沙粒自由下落
        """
        if current_time - self.sand_timer < self.sand_interval:
            return

        self.sand_timer = current_time

        for y in range(self.rows - 2, -1, -1):
            for x in range(self.cols):
                if self.grid[y][x][0] == 1 and self.grid[y + 1][x][0] == 0:
                    self.grid[y + 1][x] = self.grid[y][x]
                    self.grid[y][x] = (0, None)

    def clear_connected_sand(self):
        """
        清除同时接触左右两壁的相连同色沙粒
        """
        visited = [[False for _ in range(self.cols)] for _ in range(self.rows)]

        def dfs(x, y, color):
            """
            深度优先搜索，查找连通的沙粒块
            """
            if x < 0 or x >= self.cols or y < 0 or y >= self.rows:
                return set(), False, False
            if visited[y][x] or self.grid[y][x][1] != color:
                return set(), False, False

            visited[y][x] = True
            connected = {(x, y)}
            touches_left = (x == 0)
            touches_right = (x == self.cols - 1)

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                sub_connected, sub_touches_left, sub_touches_right = dfs(x + dx, y + dy, color)
                connected |= sub_connected
                touches_left |= sub_touches_left
                touches_right |= sub_touches_right

            return connected, touches_left, touches_right

        # 遍历网格，查找所有连通的沙粒块
        for y in range(self.rows):
            for x in range(self.cols):
                if self.grid[y][x][0] == 1 and not visited[y][x]:
                    color = self.grid[y][x][1]
                    connected, touches_left, touches_right = dfs(x, y, color)
                    if touches_left and touches_right:
                        for cx, cy in connected:
                            self.grid[cy][cx] = (0, None)  # 清除沙粒
                            self.score += 1

    def is_game_over(self):
        """
        检查是否游戏结束（沙粒堆积到顶部）
        """
        return any(self.grid[0][x][0] == 1 for x in range(self.cols))

    def draw(self, screen):
        """
        绘制网格和沙粒
        """
        for y, row in enumerate(self.grid):
            for x, (state, color) in enumerate(row):
                if state == 1:
                    pygame.draw.rect(
                        screen,
                        color,
                        pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size),
                    )