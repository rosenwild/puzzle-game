from puzzle import *


class GamePlay:
    def __init__(self, puzzle_code):
        self.closeGame = False
        self.puzzle_Code = puzzle_code
        self.change = True
        self.blockInfo = []
        self.zeroBlock = None
        self.row_size = int((self.puzzle_Code + 1) ** 0.5)
        self.game = Game(self.puzzle_Code)
        self.lastMove = None
        self.hint = -1

    def mainLoop(self):
        while not self.closeGame:
            self.print_blocks()
            if self.game.win:
                key_pressed = input("YOU WIN!!!\nRESTART[R]\nQUIT[Q]\n")
            else:
                key_pressed = input("CONTINUE[C]\nHINT[H]\nQUIT[Q]\nRESET[R]\n")
            if key_pressed == "Q":
                self.closeGame = True
            elif key_pressed == "R":
                self.hint = -1
                self.game.reset_game()
            elif key_pressed == "H":
                self.hint, score = self.game.nextHint(self.lastMove)
                if self.hint == -1:
                    print("No moves available!!!")
                else:
                    print(self.hint, self.find_block(self.hint).pos)
            if key_pressed == "C" or key_pressed == "H":
                self.move(int(input("INPUT INDEX OF THE ROW: ")) - 1, int(input("INPUT INDEX OF THE COLUMN: ")) - 1)

    def move(self, x, y):
        self.zeroBlock = self.find_block(0)
        block, number = self.get_block(x, y)
        if block is not None or number != -1:
            if block in (self.zeroBlock.up, self.zeroBlock.down, self.zeroBlock.left, self.zeroBlock.right):
                self.game.swapBlocks(self.zeroBlock, block)
                self.lastMove = self.zeroBlock

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
    game8.mainLoop()
elif difficulty == 1:
    game8 = GamePlay(15)
    game8.mainLoop()
