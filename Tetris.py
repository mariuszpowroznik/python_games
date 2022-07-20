import math
import sys
import random
from enum import Enum
from tkinter import *
from tkinter import messagebox

ROW_NUM = 20
COL_NUM = 15
#DEFAULT_COLOR = "lightgrey"


class BlockType(Enum):
    BLOCK_I = 1
    BLOCK_T = 2
    BLOCK_Z = 3
    BLOCK_S = 4
    BLOCK_O = 5
    BLOCK_L = 6
    BLOCK_LL = 7


class Block:

    def __init__(self, board):
        self.blocks = [BlockType.BLOCK_I, BlockType.BLOCK_T, BlockType.BLOCK_Z, BlockType.BLOCK_S, BlockType.BLOCK_O,
                       BlockType.BLOCK_L, BlockType.BLOCK_LL]
        # self.blocks = [BlockType.BLOCK_L]
        self.colors = ["black", "red", "green", "blue", "cyan", "yellow", "magenta"]

        self.rot = [[], [], [], [], [], [], [], []]
        self.rot[BlockType.BLOCK_I.value].append(
            [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0}, {"x": 3, "y": 0}])
        self.rot[BlockType.BLOCK_I.value].append(
            [{"x": 0, "y": 0}, {"x": 0, "y": -1}, {"x": 0, "y": -2}, {"x": 0, "y": -3}])
        self.rot[BlockType.BLOCK_T.value].append(
            [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0}, {"x": 1, "y": -1}])
        self.rot[BlockType.BLOCK_T.value].append(
            [{"x": 1, "y": 0}, {"x": 1, "y": -1}, {"x": 1, "y": -2}, {"x": 0, "y": -1}])
        self.rot[BlockType.BLOCK_T.value].append(
            [{"x": 0, "y": -1}, {"x": 1, "y": -1}, {"x": 2, "y": -1}, {"x": 1, "y": 0}])
        self.rot[BlockType.BLOCK_T.value].append(
            [{"x": 0, "y": 0}, {"x": 0, "y": -1}, {"x": 0, "y": -2}, {"x": 1, "y": -1}])
        self.rot[BlockType.BLOCK_Z.value].append(
            [{"x": 0, "y": -1}, {"x": 1, "y": -1}, {"x": 1, "y": 0}, {"x": 2, "y": 0}])
        self.rot[BlockType.BLOCK_Z.value].append(
            [{"x": 0, "y": 0}, {"x": 0, "y": -1}, {"x": 1, "y": -1}, {"x": 1, "y": -2}])
        self.rot[BlockType.BLOCK_S.value].append(
            [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 1, "y": -1}, {"x": 2, "y": -1}])
        self.rot[BlockType.BLOCK_S.value].append(
            [{"x": 0, "y": -2}, {"x": 0, "y": -1}, {"x": 1, "y": -1}, {"x": 1, "y": 0}])
        self.rot[BlockType.BLOCK_O.value].append(
            [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 0, "y": -1}, {"x": 1, "y": -1}])
        self.rot[BlockType.BLOCK_L.value].append(
            [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0}, {"x": 2, "y": -1}])
        self.rot[BlockType.BLOCK_L.value].append(
            [{"x": 0, "y": -2}, {"x": 1, "y": -2}, {"x": 1, "y": -1}, {"x": 1, "y": 0}])
        self.rot[BlockType.BLOCK_L.value].append(
            [{"x": 0, "y": 0}, {"x": 0, "y": -1}, {"x": 1, "y": -1}, {"x": 2, "y": -1}])
        self.rot[BlockType.BLOCK_L.value].append(
            [{"x": 0, "y": -2}, {"x": 0, "y": -1}, {"x": 0, "y": 0}, {"x": 1, "y": 0}])
        self.rot[BlockType.BLOCK_LL.value].append(
            [{"x": 0, "y": -1}, {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0}])
        self.rot[BlockType.BLOCK_LL.value].append(
            [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 1, "y": -1}, {"x": 1, "y": -2}])
        self.rot[BlockType.BLOCK_LL.value].append(
            [{"x": 0, "y": -1}, {"x": 1, "y": -1}, {"x": 2, "y": -1}, {"x": 2, "y": 0}])
        self.rot[BlockType.BLOCK_LL.value].append(
            [{"x": 0, "y": 0}, {"x": 0, "y": -1}, {"x": 0, "y": -2}, {"x": 1, "y": -2}])

        self.type = random.choice(self.blocks)
        self.color = random.choice(self.colors)
        self.rotation = 0
        self.blockXY = self.rot[self.type.value][0]
        self.currXY = {"x": 0, "y": 0}
        if self.type != BlockType.BLOCK_I:
            self.currXY['y'] = 1
        self.board = board

    def fit_x_to_wnd(self, newBlockXY):
        seq = [x["x"] for x in newBlockXY]
        maxX = max(seq)
        if self.currXY["x"] + maxX >= COL_NUM:
            return COL_NUM - 1 - maxX
        return self.currXY["x"]

    def fit_y_to_wnd(self, newBlockXY):
        seq = [y["y"] for y in newBlockXY]
        minY = min(seq)
        if self.currXY["y"] + minY < 0:
            return abs(minY)
        return self.currXY["y"]

    def rotate(self):
        newRotation = self.rotation
        if self.rotation == len(self.rot[self.type.value]) - 1:
            newRotation = 0
        else:
            newRotation += 1
        newBlockXY = self.rot[self.type.value][newRotation]

        x = self.fit_x_to_wnd(newBlockXY)
        y = self.fit_y_to_wnd(newBlockXY)

        if self.can_move(x, y, newBlockXY):
            self.clear_block()
            self.currXY["x"] = x
            self.currXY["y"] = y
            self.blockXY = self.rot[self.type.value][newRotation]
            self.rotation = newRotation
            self.draw_block()

    def move_left(self):
        x = self.currXY["x"] - 1
        y = self.currXY["y"]
        if self.can_move(x, y, self.blockXY):
            self.clear_block()
            self.currXY["x"] = x
            self.draw_block()

    def move_right(self):
        x = self.currXY["x"] + 1
        y = self.currXY["y"]
        if self.can_move(x, y, self.blockXY):
            self.clear_block()
            self.currXY["x"] = x
            self.draw_block()

    def move_down(self):
        x = self.currXY["x"]
        y = self.currXY["y"] + 1
        if self.can_move(x, y, self.blockXY):
            self.clear_block()
            self.currXY["y"] = y
            self.draw_block()

    def can_move(self, newx, newy, blockXY):
        for elem in blockXY:
            x = elem["x"] + newx
            y = elem["y"] + newy
            if x < 0 or x >= COL_NUM or y < 0 or y >= ROW_NUM or not self.board[y][x]["Empty"]:
                return False
        return True

    def clear_block(self):
        for xy in self.blockXY:
            y = self.currXY["y"] + xy["y"]
            x = self.currXY["x"] + xy["x"]
            self.board[y][x]["Button"].config(bg=DEFAULT_COLOR)

    def draw_block(self):
        for xy in self.blockXY:
            y = self.currXY["y"] + xy["y"]
            x = self.currXY["x"] + xy["x"]
            self.board[y][x]["Button"].config(bg=self.color)


class App:
    def __init__(self):
        self.wnd = Tk()
        Label(self.wnd, text="Tetris game...", fg="green", font=("Helvetica", 16)).grid(row=0)
        self.hiButton = Button(self.wnd, text="Start", fg="blue", padx=30, font=("Helvetica", 12), command=self.play)
        self.hiButton.grid(row=2, sticky=W)
        self.qButton = Button(self.wnd, text="Quit", fg="red", padx=30, font=("Helvetica", 12), command=self.wnd.quit)
        self.qButton.grid(row=2, sticky=E)
        self.frame = Frame(self.wnd, borderwidth=3, relief="sunken", width=200, height=400)
        self.frame.grid(row=1)

        self.board = []
        self.create()
        self.started = False
        self.score = 0
        self.speed = 500
        self.block = Block(self.board)

        self.wnd.bind("<Key>", self.key_pressed)
        self.wnd.mainloop()

    def create(self):
        global DEFAULT_COLOR
        for r in range(ROW_NUM):
            line = []
            for c in range(COL_NUM):
                idx = r * COL_NUM + c
                b = Button(self.frame, state=DISABLED, height=1, width=1)
                b.grid(row=r, column=c)
                line.append({"Button": b, "Empty": True})
                #if DEFAULT_COLOR is None:
                DEFAULT_COLOR = b.cget("background")
            self.board.append(line)

    def reset(self):
        for b in self.fields:
            b["Button"].config(bg=DEFAULT_COLOR)

    def end_game(self):
        messagebox.showinfo("Game Over", "Your score is " + str(self.score))
        self.started = False
        self.hiButton.config(state=NORMAL)

    def next_move(self):
        self.block.move_down()
        self.check_block()

    def timer(self):
        if self.started:
            self.next_move()
            self.wnd.after(self.speed, self.timer)

    def play(self):
        self.score = 0
        self.started = True
        self.hiButton.config(state=DISABLED)
        self.wnd.after(500, self.timer)
        self.block.draw_block()

    def key_pressed(self, ev):
        if ev.keysym == "Left":
            self.block.move_left()
        elif ev.keysym== "space":
            self.block.rotate()
        elif ev.keysym == "Right":
            self.block.move_right()
        elif ev.keysym == "Down":
            self.block.move_down()

    def new_block(self):
        self.block = Block(self.board)
        self.block.draw_block()
        if self.is_floor():
            self.end_game()

    def count_row(self, row):
        val = 0
        for el in row:
            if not el["Empty"]:
                val += 1
        return val

    def clear_row(self, row):
        for el in row:
            el["Empty"] = True
            el["Button"].config(bg=DEFAULT_COLOR)

    def fallBoard(self, row):
        bCont = True
        while row >= 0 and bCont:
            bCont = False
            for i, el in enumerate(self.board[row]):
                if row > 0:
                    if not self.board[row - 1][i]["Empty"]:
                        bCont = True
                    el["Button"].config(bg=self.board[row - 1][i]["Button"].cget("bg"))
                    el["Empty"] = self.board[row - 1][i]["Empty"]
                else:
                    el["Button"].config(DEFAULT_COLOR)
                    el["Empty"] = True
            row -= 1

    def check_board(self):
        row = ROW_NUM - 1
        while row >= 0:
            notEmptyBlocks = self.count_row(self.board[row])
            if notEmptyBlocks == 0:
                break
            elif notEmptyBlocks == COL_NUM:
                self.fallBoard(row)
                self.score += 1
            else:
                row -= 1

    def check_block(self):
        if self.is_floor():
            self.leave_block()
            self.check_board()
            self.new_block()

    def leave_block(self):
        for elem in self.block.blockXY:
            y = elem['y'] + self.block.currXY['y']
            x = elem['x'] + self.block.currXY['x']
            self.board[y][x]["Empty"] = False

    def is_floor(self):
        for elem in self.block.blockXY:
            y = elem['y'] + self.block.currXY['y']
            x = elem['x'] + self.block.currXY['x']
            if y >= ROW_NUM - 1 or not self.board[y + 1][x]["Empty"]:
                return True
        return False


app = App()
