"""
Copyright 2020 Patrick Müller
Snake - Graphic
"""

from tkinter import *
import time
from GameLogic import *


class Graphic:
    """
    This is the graphical part of Snake
    """

    def __init__(self, x, y, game: Gamelogic, root: Tk):
        """
        x and y are standing for the size of the field where the
        snake can move they represent the number of tiles on the x
        and y axis
        """
        self.root = root
        # they have to be multiplied by 20 because one tile is 20x20
        self.x = x * 20
        self.y = y * 20
        self.game = game
        self.pause = False

    def end(self):
        self.canvas.destroy()

    def right(self, event):
        """
        The unbinds are for the correct movement, so there cant be 2 inputs
        at once
        """
        self.root.unbind("<Right>")
        self.root.unbind("<Left>")
        self.root.unbind("<Up>")
        self.root.unbind("<Down>")
        if self.game.snake.direction != 1:
            self.game.snake.change_direction(0)

    def left(self, event):
        self.root.unbind("<Right>")
        self.root.unbind("<Left>")
        self.root.unbind("<Up>")
        self.root.unbind("<Down>")
        if self.game.snake.direction != 0:
            self.game.snake.change_direction(1)

    def up(self, event):
        self.root.unbind("<Right>")
        self.root.unbind("<Left>")
        self.root.unbind("<Up>")
        self.root.unbind("<Down>")
        if self.game.snake.direction != 3:
            self.game.snake.change_direction(2)

    def down(self, event):
        self.root.unbind("<Right>")
        self.root.unbind("<Left>")
        self.root.unbind("<Up>")
        self.root.unbind("<Down>")
        if self.game.snake.direction != 2:
            self.game.snake.change_direction(3)

    def toggle_pause(self, event):
        self.pause = not self.pause

    def init_graphic(self, placex, placey):
        self.canvas = Canvas(self.root, height=self.y, width=self.x)
        self.canvas.focus()
        for x in range(0, self.x, 20):
            for y in range(0, self.y, 20):
                if self.game.field[(x / 20, y / 20)] == 0:
                    color = "black"
                elif self.game.field[(x / 20, y / 20)] == 1:
                    color = "green"
                elif self.game.field[(x / 20, y / 20)] == 2:
                    color = "red"
                self.canvas.create_rectangle(x, y, x + 20, y + 20,
                                             fill=color)
        self.canvas.place(x=placex, y=placey)
        self.root.bind("<Right>", self.right)
        self.root.bind("<Left>", self.left)
        self.root.bind("<Up>", self.up)
        self.root.bind("<Down>", self.down)
        self.root.bind("<Escape>", self.toggle_pause)


    def update_graphic(self):
        self.canvas.delete(ALL)
        for a in self.game.field:
            if self.game.field[a] == 0:
                color = "black"
            elif self.game.field[a] == 1:
                color = "green"
            elif self.game.field[a] == 2:
                color = "red"
            self.canvas.create_rectangle(a[0] * 20, a[1] * 20, a[0] * 20 + 20,
                                         a[1] * 20 + 20, fill=color)
        # needs to rebind as it will be unbinded after a change of direction
        self.root.bind("<Right>", self.right)
        self.root.bind("<Left>", self.left)
        self.root.bind("<Up>", self.up)
        self.root.bind("<Down>", self.down)
        self.root.bind("<Escape>", self.toggle_pause)
