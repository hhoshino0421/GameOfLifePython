from collections import namedtuple
from GridMain import Grid
from GridMain import ColumnPrinter

'''
状態定数定義
'''
ALIVE = 1
EMPTY = 0

# セルの状態取得
Query = namedtuple('Query', ('y', 'x'))

# セルの状態を変更
Transition = namedtuple('Transition', ('y', 'x', 'state'))

# 世代管理
TICK = object()


# 隣接する生存セルの個数を計算
def count_neighbors(y, x):
    # 隣接するセルの状態を取得
    n_ = yield Query(y + 1, x + 0)
    ne = yield Query(y + 1, x + 1)
    e_ = yield Query(y + 0, x + 1)
    se = yield Query(y - 1, x + 1)
    s_ = yield Query(y - 1, x + 0)
    sw = yield Query(y - 1, x - 1)
    w_ = yield Query(y + 0, x - 1)
    nw = yield Query(y + 1, x - 1)

    neighbor_status = [n_, ne,e_, se, s_, sw, w_, nw]

    count = 0
    for status in neighbor_status:
        if status == ALIVE:
            count += 1

    return count


# 次のステップでのセル状態遷移
def step_cell(y, x):

    state = yield Query(y, x)
    neighbors = yield from count_neighbors(y, x)
    next_state = game_logic(state, neighbors)
    yield Transition(y, x, next_state)


# ビジネスロジックを実装
def game_logic(state, neighbors):
    if state == ALIVE:
        if neighbors < 2:
            # 過疎
            return EMPTY
        elif neighbors > 3:
            # 過密
            return EMPTY
    else:
        if neighbors == 3:
            # 再生
            return ALIVE

    # 現状の状態を返却
    return state


# シミュレーション関数
def simulate(height, width):
    while True:
        for y in range(height):
            for x in range(width):
                yield from step_cell(y,x)

        yield TICK


def live_a_generation(grid, sim):
    progeny = Grid(grid.height, grid.width)
    item = next(sim)
    while item is not TICK:
        if isinstance(item, Query):
            state = grid.query(item.y, item.x)
            item = sim.send(state)
        else:
            progeny.assign(item.y, item.x, item.state)
            item = next(sim)
    return progeny


# テスト用ロジック
grid = Grid(5, 5)
grid.assign(1, 1, ALIVE)
grid.assign(2, 2, ALIVE)
grid.assign(2, 3, ALIVE)
grid.assign(3, 3, ALIVE)
columns = ColumnPrinter()
sim = simulate(grid.height, grid.width)

for i in range(100):
    columns.append(str(grid))
    grid = live_a_generation(grid, sim)

print(columns)
