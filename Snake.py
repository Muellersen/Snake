"""
Copyright 2020 Patrick Müller
Snake
"""
from tkinter import *
from Graphic import *

# ----------------------------------------------------------------------------
root = Tk()
root.geometry("1028x720+100+0")
root.title("Snake - The Game")
root.iconbitmap("images/logoicon.ico")
root.resizable(0, 0)
root.configure(bg="dark green")
# ----------------------------------------------------------------------------
score = 0
logo = PhotoImage(file="images/snakelogo2.gif")
with open("highscore.txt", "r") as f:
    highscore = f.readline()
    f.close()

copyright_label = Label(root, text="Made by Patrick Müller",
                        bg="dark green", fg="black", font="20")
controls_label = Label(root, text="Controls:\nMove with the arrow keys!",
                       bg="dark green", fg="black", font="20",
                       anchor=W, justify=LEFT)
snake_label = Label(root, text="Snake",
                    fg="black", bg="dark green", font="70")
snake_logo = Label(root, image=logo)
score_label = Label(root, text="Score: " + str(score), bg="dark green",
                    fg="black", font="20")
highscore_label = Label(root, text="Highscore: " + str(highscore),
                        bg="dark green",
                        fg="black", font="20")

copyright_label.place(x=20, y=690)
controls_label.place(x=20, y=550)
snake_label.place(x=65, y=360)
snake_logo.place(x=20, y=20)
score_label.place(x=20, y=460)
highscore_label.place(x=20, y=500)
# ----------------------------------------------------------------------------


def start_game():
    start_button.config(state=DISABLED)  # no accidental presses while play
    game = Gamelogic(34, 34)
    game.add_rand()
    graphic = Graphic(34, 34, game, root)
    graphic.init_graphic(320, 20)
    while True:
        while graphic.pause:
            graphic.update_graphic()
            graphic.root.update_idletasks()
            graphic.root.update()
            
        graphic.root.after(50)
        graphic.game.update_field()
        graphic.game.found_piece()
        graphic.update_graphic()
        score_label.config(text="Score: " + str(graphic.game.score))
        score_label.place(x=20, y=460)
        graphic.root.update_idletasks()
        graphic.root.update()
        if graphic.game.is_lost() is True:
            break
    graphic.root.after(500, graphic.end())
    start_button.config(state="normal")
    if graphic.game.score > int(highscore):
        highscore_label.config(text="Highscore: " + str(graphic.game.score))
        highscore_label.place(x=20, y=500)
        with open("highscore.txt", "w") as f:
            f.write(str(graphic.game.score))
            f.close()


start_button = Button(root, text="Start", command=start_game,
                      bg="green", fg="black", width=20)
start_button.place(x=20, y=400)


root.mainloop()
