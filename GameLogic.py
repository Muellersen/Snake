"""
Copyright 2020 Patrick Müller
Snake Game Logic
"""
from random import choice


class SnakeElement:
    """
    This class is for one part of the snake
    """

    def __init__(self, coordinates: tuple, predecessor=None):
        self.coordinates = coordinates
        self.predecessor = predecessor

    def next(self):
        """
        This function represents the movement of the snake
        if next is called on each element of a snake.
        The current element self will get the coordinates of the
        predecessor

        Doctest:
        >>> x = SnakeElement((1,1))
        >>> y = SnakeElement((2,2), x)
        >>> y.next()
        >>> y.coordinates
        (1, 1)
        """
        self.coordinates = self.predecessor.coordinates


class Snake:
    """
    This class will represent the actual snake
    with a queue which takes tuples with two elements.
    The elements are representing the coordinates in the playgrid.

    Doctest for whole class:
    >>> x = SnakeElement((1,1))
    >>> snake = Snake(x)
    >>> snake.add_snake_element()
    >>> len(snake.list)
    2
    >>> snake.change_direction(0)
    >>> snake.list[0].predecessor.coordinates
    (2, 1)
    >>> snake.change_direction(1)
    >>> snake.list[0].predecessor.coordinates
    (0, 1)
    >>> snake.change_direction(2)
    >>> snake.list[0].predecessor.coordinates
    (1, 0)
    >>> snake.change_direction(3)
    >>> snake.list[0].predecessor.coordinates
    (1, 2)
    >>> snake.change_direction(0)
    >>> snake.move()
    >>> snake.get_coords()
    [(2, 1), (1, 1)]
    >>> snake.add_snake_element()
    >>> snake.move()
    >>> snake.get_coords()
    [(3, 1), (2, 1), (1, 1)]
    >>> snake.change_direction(3)
    >>> snake.move()
    >>> snake.get_coords()
    [(3, 2), (3, 1), (2, 1)]
    """

    def __init__(self, starting_point: SnakeElement):
        starting_point.predecessor = None
        self.list = [starting_point]
        self.direction = 0
        self.coords = starting_point.coordinates

    def add_snake_element(self):
        """
        Adds a new SnakeElement to the list. The predecessor of
        the added element is is the last element of the list.
        After its added the element wont be there but after the next move
        the added element will show up because the new element is added
        through the predecessor which is the last list element

        Doctest:
        >>> x = SnakeElement((0, 0))
        >>> snake = Snake(x)
        >>> snake.add_snake_element()
        >>> snake.list[1].predecessor.coordinates
        (0, 0)
        """
        pre = self.list[-1]
        new_element = SnakeElement(None, pre)
        self.list = self.list + [new_element]

    def change_direction(self, directions: int):
        """
        This function changes the direction by changing the predecessor
        of the first element (left) in the list.
        0 = right, 1 = left, 2 = up, 3 = down

        Doctest:
        #>>> x = SnakeElement(2,1)
        #>>> snake = Snake(x)
        #>>> snake.change_direction(0)
        #>>> snake.list[0].predecessor.coordinates
        #(3, 1)

        #>>> snake.change_direction(1)
        #>>> snake.list[0].predecessor.coordinates
        #(0, 1)
        #>>> snake.change_direction(2)
        #>>> snake.list[0].predecessor.coordinates
        #(1, 0)
        #>>> snake.change_direction(3)
        #>>> snake.list[0].predecessor.coordinates
        #(1, 2)
        extremely weird problem coords is a tuple
        so we could use indexing but doctest raises
        an error saying x = coords[0] is not subscriptable
        coords is a tuple but in the doctest its an integer
        i tested it manually and it worked...
        but as a doctest for the whole class it works??
        """
        coords = self.get_coords()[0]
        x = coords[0]
        y = coords[1]
        if directions == 0:
            self.direction = 0
            coords = (x + 1, y)  # rightward movement x + 1
        elif directions == 1:
            self.direction = 1
            coords = (x - 1, y)  # leftward movement x + 1
        elif directions == 2:
            self.direction = 2
            coords = (x, y - 1)  # upward movement y + 1
        elif directions == 3:
            self.direction = 3
            coords = (x, y + 1)  # downward movement y - 1
        else:
            return
        pre = SnakeElement(coords, None)
        self.list[0].predecessor = pre

    def move(self):
        """
        This function makes use of the linked lists function next()
        so each element will have the coordinates of the  predecessors.
        All together its like the snake moved for one tile.
        """
        self.list = self.list[::-1]
        for a in self.list:
            a.next()
        self.list = self.list[::-1]
        self.change_direction(self.direction)
        # new predecessor but same direction
        # for the next move if direction same

    def get_coords(self) -> list:
        return [a.coordinates for a in self.list]


class Gamelogic:
    """
    In this class the field of the game will be created and offers
    some functions for the graphic to print out the field and the random
    function for the pieces the snake has to pick up and the game logic

    Doctest for the whole class:

    >>> game = Gamelogic(3, 3)
    >>> game.update_field()
    >>> game.snake.get_coords()
    [(2, 1)]
    >>> game.piece = (2, 1)
    >>> game.found_piece()
    True
    >>> game.update_field()
    >>> game.snake.get_coords()
    [(3, 1), (2, 1)]
    >>> game.update_field()
    >>> game.is_lost()
    True
    """

    def __init__(self, x: int, y: int):
        field = {}
        self.x = x - 1  # x acsis
        self.y = y - 1  # y acsis
        s = SnakeElement((1, 1))
        snake = Snake(s)
        snake.change_direction(0)
        self.snake = snake
        for a in range(x):
            for b in range(y):
                field[(a, b)] = 0
        for a in snake.get_coords():
            if (a) in field:
                field[a] = 1
        self.field = field
        self.score = 0
        self.piece = None

    def update_field(self):
        """
        This function moves the Snake in the field and updates
        the field after the movement
        """
        for a in self.snake.get_coords():
            if a in self.field:
                if self.field[a] == 2:
                    continue
                self.field[a] = 0
        self.snake.move()
        for a in self.snake.get_coords():
            if a in self.field:
                self.field[a] = 1

    def is_lost(self) -> bool:
        """
        This function checks if the snake hit itself or hit the wall

        Doctest:

        >>> game = Gamelogic(10, 10)
        >>> game.piece = (1, 1)
        >>> game.found_piece()
        True
        >>> game.update_field()
        >>> game.piece = (2, 1)
        >>> game.found_piece()
        True
        >>> game.update_field()
        >>> game.piece = (3, 1)
        >>> game.found_piece()
        True
        >>> game.update_field()
        >>> game.piece = (4, 1)
        >>> game.found_piece()
        True
        >>> game.update_field()
        >>> game.piece = (5, 1)
        >>> game.found_piece()
        True
        >>> game.update_field()
        >>> game.snake.change_direction(3)
        >>> game.update_field()
        >>> game.snake.change_direction(1)
        >>> game.update_field()
        >>> game.snake.change_direction(2)
        >>> game.update_field()
        >>> game.is_lost()
        True
        """
        first_element = self.snake.get_coords()[0]
        rest = self.snake.get_coords()[1:]
        if first_element in rest:
            return True
        elif first_element[0] < 0 or first_element[1] < 0:
            return True
        elif first_element[0] > self.x or first_element[1] > self.y:
            return True
        else:
            return False

    def add_rand(self):
        """
        The sequence is made of the field where field[x] = 0
        which means there is nothing on that tile

        Doctest:

        how to test?

        """
        seq = []
        for a in self.field:
            if self.field[a] == 0:
                seq = seq + [a]
        piece_coords = choice(seq)
        self.field[piece_coords] = 2
        self.piece = piece_coords

    def found_piece(self):
        """
        This function checks if the piece was found
        If it was found the piece will be deleted and the snake
        will increase its length
        """
        if self.snake.get_coords()[0] == self.piece:
            self.snake.add_snake_element()
            self.field[self.piece] = 1
            # its 1 because there is the head of the snake now
            self.piece = None
            self.score += 1
            self.add_rand()
            return True
        else:
            return False

    def get_field(self) -> dict:
        return self.field


if __name__ == "__main__":
    import doctest
    doctest.testmod()
