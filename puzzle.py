from random import shuffle


class Block:
    def __init__(self, number, i, j, max_blocks):
        self.dx = self.dy = -1
        if 0 <= number < max_blocks:
            self.number = number
            self.pos = (i, j)
            self.up = None
            self.down = None
            self.left = None
            self.right = None
            self.num_blocks = max_blocks
            self.old_moves = []
            self.calculate_offset()
        else:
            print("Puzzle Crashed!!")
            quit()

    def calculate_offset(self):
        if self.number != 0:
            self.dy = abs(((self.number - 1) % int(self.num_blocks ** 0.5)) - self.pos[1])
            self.dx = abs(int((self.number - 1) // int(self.num_blocks ** 0.5)) - self.pos[0])


class Game:
    def __init__(self, puzzle_code):
        self.blocks = {}
        self.num_blocks = puzzle_code + 1
        self.old_moves = [[self.blocks[(i, j)].number for i in range(int(self.num_blocks ** 0.5)) for j in
                           range(int(self.num_blocks ** 0.5))]]
        self.final_set = [i + 1 for i in range(self.num_blocks - 1)].append(0)
        self.get_solvable()
        self.win = False
        self.score = 0
        self.reset_game()
        self.start_set = [i for i in range(self.num_blocks)]
        self.start_set = [1, 2, 3, 4, 5, 6, 7, 0, 8]

    def reset_game(self):
        if self.win:
            self.get_solvable()

        self.win = False
        for i in range(int(self.num_blocks ** 0.5)):
            for j in range(int(self.num_blocks ** 0.5)):
                self.blocks[(i, j)] = Block(self.start_set[int((self.num_blocks ** 0.5) * i) + j], i, j,
                                            self.num_blocks)

        for i in range(int(self.num_blocks ** 0.5)):
            for j in range(int(self.num_blocks ** 0.5)):
                self.assign_adjacent(i, j)
        self.score = self.calculate_score()

    def swap_blocks(self, block1, block2):
        if not self.win:
            block1.number, block2.number = block2.number, block1.number
            block1.calculate_offset()
            block2.calculate_offset()
        if len(self.old_moves) <= 32:
            self.old_moves.append([self.blocks[(i, j)].number for i in range(int(self.num_blocks ** 0.5)) for j in
                                   range(int(self.num_blocks ** 0.5))])
        else:
            del self.old_moves[0]
            self.old_moves.append([self.blocks[(i, j)].number for i in range(int(self.num_blocks ** 0.5)) for j in
                                   range(int(self.num_blocks ** 0.5))])
        self.declare_win()

    def assign_adjacent(self, i, j):
        if i == 0:
            self.blocks[(i, j)].up, self.blocks[(i, j)].down = None, self.blocks[(i + 1, j)]
        elif i == int((self.num_blocks ** 0.5) - 1):
            self.blocks[(i, j)].up, self.blocks[(i, j)].down = self.blocks[(i - 1, j)], None
        else:
            self.blocks[(i, j)].up, self.blocks[(i, j)].down = self.blocks[(i - 1, j)], self.blocks[(i + 1, j)]

        if j == 0:
            self.blocks[(i, j)].left, self.blocks[(i, j)].right = None, self.blocks[(i, j + 1)]
        elif j == int((self.num_blocks ** 0.5) - 1):
            self.blocks[(i, j)].left, self.blocks[(i, j)].right = self.blocks[(i, j - 1)], None
        else:
            self.blocks[(i, j)].left, self.blocks[(i, j)].right = self.blocks[(i, j - 1)], self.blocks[(i, j + 1)]

    def declare_win(self):
        self.score = self.calculate_score()
        if not self.score:
            self.win = True

    def calculate_score(self):
        overall = 0
        for i in range(int(self.num_blocks ** 0.5)):
            for j in range(int(self.num_blocks ** 0.5)):
                if self.blocks[(i, j)].number != 0:
                    overall += self.blocks[(i, j)].dx + self.blocks[(i, j)].dy
        return overall

    def get_solvable(self):
        while True:
            inversion = 0
            shuffle(self.start_set)
            for i in range(0, self.num_blocks - 1):
                for j in range(i + 1, self.num_blocks):
                    if self.start_set[j] and self.start_set[i] and self.start_set[i] > self.start_set[j]:
                        inversion += 1
            if self.num_blocks % 2 != 0 or self.find0() % 2 != 0:
                if inversion % 2 == 0: break

    def find0(self):
        for i in range(int(self.num_blocks ** 0.5) - 1, -1, -1):
            for j in range(int(self.num_blocks ** 0.5) - 1, -1, -1):
                if self.start_set[i * (int(self.num_blocks ** 0.5)) + j] == 0:
                    return int(self.num_blocks ** 0.5) - i

    def next_hint(self, last_move):
        rank = {}
        old_score = self.calculate_score()
        best_score = 999
        number = -1
        if not self.win:
            zero_block = None
            for i in range(int(self.num_blocks ** 0.5)):
                for j in range(int(self.num_blocks ** 0.5)):
                    if self.blocks[(i, j)].number == 0:
                        zero_block = self.blocks[(i, j)]
            if zero_block is not None:
                up, down, left, right = zero_block.up, zero_block.down, zero_block.left, zero_block.right
                for i in up, down, left, right:
                    if i is not None and (last_move is None or last_move.number != i.number):
                        self.swap_blocks(i, zero_block)
                        next_move = self.old_moves[len(self.old_moves) - 1]
                        del self.old_moves[len(self.old_moves) - 1]
                        score = self.calculate_score()
                        if next_move not in self.old_moves:
                            rank[i] = score
                        self.swap_blocks(i, zero_block)
                        del self.old_moves[len(self.old_moves) - 1]

                if len(rank) > 0:
                    best_score = min(rank.values())
                    rank = {i: value for i, value in list(rank.items()) if value == best_score}
                    if len(rank) > 1 and best_score < old_score:
                        for i in rank:
                            self.swap_blocks(i, zero_block)
                            next_move = self.old_moves[len(self.old_moves) - 1]
                            del self.old_moves[len(self.old_moves) - 1]
                            if next_move not in self.old_moves:
                                _, rank[i] = self.next_hint(zero_block)
                            else:
                                del self.old_moves[len(self.old_moves) - 1]
                            self.swap_blocks(i, zero_block)
                            del self.old_moves[len(self.old_moves) - 1]

                        best_score = min(rank.values())
                        for i in rank: number, best_score = i.number, rank[i]
                    else:
                        for i in rank: number, best_score = i.number, rank[i]
                else:
                    try:
                        number, best_score = i.number, best_score
                    except:
                        return -1, -1
        return number, best_score
