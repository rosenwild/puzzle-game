from puzzle import *


class GamePlay:
    def __init__(self, puzzle_code):
        self.close_game = False
        self.puzzle_code = puzzle_code
        self.change = True
        self.zero_block = None
        self.row_size = int((self.puzzle_code + 1) ** 0.5)
        self.game = Game(self.puzzle_code)
        self.last_move = None
        self.hint = -1

    def main_loop(self):
        while not self.close_game:
            self.print_blocks()
            if self.game.win:
                key_pressed = input("YOU WIN!!!\nRESTART[R]\nQUIT[Q]\n")
            else:
                key_pressed = input("CONTINUE[C]\nHINT[H]\nQUIT[Q]\nRESET[R]\n")
            if key_pressed == "Q":
                self.close_game = True
            elif key_pressed == "R":
                self.hint = -1
                self.game.reset_game()
            elif key_pressed == "H":
                self.hint, score = self.game.next_hint(self.last_move)
                if self.hint == -1:
                    print("No moves available!!!")
                else:
                    print(self.hint, self.find_block(self.hint).pos)
            if key_pressed == "C" or key_pressed == "H":
                self.move(int(input("INPUT INDEX OF THE ROW: ")) - 1, int(input("INPUT INDEX OF THE COLUMN: ")) - 1)

    def move(self, x, y):
        self.zero_block = self.find_block(0)
        block, number = self.get_block(x, y)
        if block is not None or number != -1:
            if block in (self.zero_block.up, self.zero_block.down, self.zero_block.left, self.zero_block.right):
                self.game.swap_blocks(self.zero_block, block)
                self.last_move = self.zero_block

    def get_block(self, x, y):
        return self.game.blocks[(x, y)], self.game.blocks[(x, y)].number

    def find_block(self, num):
        for i in range(self.row_size):
            for j in range(self.row_size):
                if self.game.blocks[(i, j)].number == num:
                    return self.game.blocks[(i, j)]

    def print_blocks(self):
        for i in range(self.row_size):
            for j in range(self.row_size):
                print(self.game.blocks[(i, j)].number, end=" ")
            print()


difficulty = 0
if difficulty == 0:
    game8 = GamePlay(8)
    game8.main_loop()
elif difficulty == 1:
    game8 = GamePlay(15)
    game8.main_loop()
