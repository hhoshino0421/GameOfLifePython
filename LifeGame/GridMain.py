
#
# 状態定数定義
#
ALIVE = 1
EMPTY = 0


class Grid(object):

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.rows = []
        for _ in range(self.height):
            self.rows.append([EMPTY] * self.width)

    def __str__(self):
        # TODO ここの実装内容が不明
        # printした時にこの関数が呼ばれる？
        pass

    def query(self, y, x):
        return self.rows[y % self.height][x % self.width]

    def assign(self, y, x, state):
        self.rows[y % self.height][x % self.width] = state
