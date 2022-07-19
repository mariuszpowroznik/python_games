import math
import sys
import random
from tkinter import *
from tkinter import messagebox

class App:
	def __init__(self):
		self.wnd = Tk()
		self.title = Label(self.wnd, text="Snake game...", fg="green", font=("Helvetica", 16)).grid(row=0)
		self.hiButton = Button(self.wnd, text="Start", fg="blue", padx=50, font=("Helvetica", 12), command=self.play)
		self.hiButton.grid(row=2, sticky=W)
		self.qButton = Button(self.wnd, text="Quit", fg="red", padx=50, font=("Helvetica", 12), command=self.wnd.quit)
		self.qButton.grid(row=2, sticky=E)
		self.frame = Frame(self.wnd, borderwidth=3, relief="sunken", width=400, height=400)
		self.frame.grid(row=1)
		self.ROW_NUM = self.COL_NUM = 20
		
		self.fields = []
		self.empty_fields = []
		self.snake_fields = []
		self.direction = "right"
		self.default_color = None
		self.food = None
		self.started = False
		self.can_change_direction = True

		self.wnd.bind("<Key>", self.key_pressed)
		self.create()
		self.wnd.mainloop()

	def create(self):
		for r in range(self.ROW_NUM):
			for c in range(self.COL_NUM):
				idx = r*self.COL_NUM + c
				b = Button(self.frame, state=DISABLED, height=1, width=2)
				b.grid(row=r, column=c)
				self.fields.append({"Button":b, "y":r, "x":c, "idx":idx})
				self.empty_fields.append(idx)
				if self.default_color == None:
					self.default_color = b.cget("background")

		self.set_head()

	def reset(self):
		for b in self.fields:
			b["Button"].config(bg=self.default_color)
		self.snake_fields.clear()
		self.empty_fields=[i for i in range(self.ROW_NUM*self.COL_NUM)]
		self.direction = "right"

	def set_head(self):
		head = 4*self.ROW_NUM+4
		self.snake_fields.append(head)
		self.empty_fields.remove(head)
		self.fields[head]["Button"].config(bg="black")

	def end_game(self):
		messagebox.showinfo("Game Over", "Your score is " + str(len(self.snake_fields)))
		self.started = False
		self.hiButton.config(state=NORMAL)
		self.reset()
		self.set_head()

	def move_snake(self):
		self.can_change_direction = True
		end_of_game = False
		head = None
		if self.direction == "right":
			if self.fields[self.snake_fields[0]]["x"] == self.COL_NUM-1:
				end_of_game = True
			else:
				head = self.fields[self.snake_fields[0]]["idx"] + 1
		elif self.direction == "left":
			if self.fields[self.snake_fields[0]]["x"] == 0:
				end_of_game = True
			else:
				head = self.fields[self.snake_fields[0]]["idx"] -1
		elif self.direction == "up":
			if self.fields[self.snake_fields[0]]["y"] == 0:
				end_of_game = True
			else:
				head = self.fields[self.snake_fields[0]]["idx"] - self.COL_NUM
		elif self.direction == "down":
			if self.fields[self.snake_fields[0]]["y"] == self.ROW_NUM-1:
				end_of_game = True
			else:
				head = self.fields[self.snake_fields[0]]["idx"] + self.COL_NUM

		if head in self.snake_fields:
			end_of_game = True
		
		if not end_of_game:
			self.fields[head]["Button"].config(bg="black")
			self.snake_fields.insert(0, head)
			self.empty_fields.remove(head)

			if head != self.food:
				self.fields[self.snake_fields[-1]]["Button"].config(bg=self.default_color)
				self.empty_fields.append(self.snake_fields.pop())
			else:
				self.add_food()
		else:
			self.end_game()

	def timer(self):
		if self.started:
			self.move_snake()
			self.wnd.after(150, self.timer)

	def play(self):
		self.started = True
		self.hiButton.config(state=DISABLED)
		self.wnd.after(500, self.timer)
		self.add_food()

	def add_food(self):
		self.food = random.choice(self.empty_fields)
		self.fields[self.food]["Button"].config(bg="gray")

	def key_pressed(self, ev):
		if self.can_change_direction:
			if ev.keycode == 37 and self.direction != "right":
				self.direction = "left"
				self.can_change_direction = False
			elif ev.keycode == 38 and self.direction != "down":
				self.direction = "up"
				self.can_change_direction = False
			elif ev.keycode == 39 and self.direction != "left":
				self.direction = "right"
				self.can_change_direction = False
			elif ev.keycode == 40 and self.direction != "up":
				self.direction = "down"
				self.can_change_direction = False
		
app = App()

