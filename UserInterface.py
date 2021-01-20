import tkinter as tk
from tkinter import messagebox

import keyboard

Width = 30
triangle_size = 0.1
(x, y) = (20, 16)
player = (1, 7)
actions = ["up", "down", "left", "right"]
# board=tk.Canvas(master, width=x*Width, height=y*Width)
border = []
c = open("path-coord.txt")
with open("path-coord.txt") as f:
    coords = [tuple(map(float, i.split(','))) for i in f]
walls = [
    (1, 15),
    (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 10), (2, 12), (2, 13), (2, 15), (2, 17), (2, 18),
    (3, 2), (3, 6), (3, 10), (3, 13),
    (4, 2), (4, 4), (4, 6), (4, 8), (4, 9), (4, 10), (4, 11), (4, 12), (4, 13), (4, 14), (4, 15), (4, 16), (4, 17),
    (5, 4), (5, 6), (5, 17),
    (6, 1), (6, 2), (6, 3), (6, 4), (6, 6), (6, 7), (6, 8), (6, 9), (6, 10), (6, 11), (6, 12), (6, 13), (6, 14),
    (6, 15), (6, 17),
    (7, 2), (7, 10), (7, 17),
    (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (8, 10), (8, 11), (8, 13), (8, 15), (8, 16), (8, 17),
    (9, 2), (9, 8), (9, 10), (9, 11), (9, 12), (9, 13), (9, 15), (9, 17),
    (10, 4), (10, 5), (10, 6), (10, 8), (10, 13), (10, 15),
    (11, 1), (11, 2), (11, 3), (11, 4), (11, 6), (11, 8), (11, 9), (11, 10), (11, 11), (11, 12), (11, 13), (11, 15),
    (11, 6), (11, 17),
    (12, 6), (12, 11), (12, 17),
    (13, 2), (13, 3), (13, 4), (13, 5), (13, 6), (13, 7), (13, 8), (13, 11), (13, 12), (13, 13), (13, 14), (13, 15),
    (13, 17),
    (14, 17),
    (15, 1), (15, 2), (15, 3), (15, 4), (15, 5), (15, 6), (15, 7), (15, 8), (15, 9), (15, 10), (15, 11), (15, 12),
    (15, 13), (15, 14), (15, 15), (15, 16), (15, 17), (15, 18)
]
specials = [(1, 7, "yellow", 1), (18, 13, "green", 1)]
cell_scores = {}
start = []
specialcoords = []
path_coordinates = []


class Game(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.can = tk.Canvas(self, width=x * Width, height=y * Width)
        self.can.pack(fill="both", expand=False)
        self.render_grid()
        self.resizable(False, False)
        self.title("A-Star GO Prototype by Emanuel Gheorghe")
        self.maxsize(604, 484)

        self.player = self.can.create_rectangle(player[0] * Width + Width * 2 / 10, player[1] * Width + Width * 2 / 10,
                                                player[0] * Width + Width * 8 / 10, player[1] * Width + Width * 8 / 10,
                                                fill="red", width=1)
        self.x = 1
        self.y = 7
        self.bind("<Key>", self.move_player)
        self.generateMaze()
        self.resize(104)
        #messagebox.showinfo("Some tips before you go on", "Welcome!\nBefore you start, some advice:\nPRESS SPACEBAR to see clues on the path towards the EXIT!\nLucky you, you have unlimited clues!")

    def resize(self, w):
        h = 484
        self.geometry(f"{w}x{h}")

    def render_grid(self):
        global specials, walls, Width, x, y, player
        for i in range(x):
            for j in range(y):
                self.can.create_rectangle(i * Width, j * Width, (i + 1) * Width, (j + 1) * Width, fill="white", width=1)
                # f.write("x")
                if (i == 0 or j == 0) or i == 19:
                    walls.append((j, i))
                # self.can.create_rectangle(i * Width, j * Width, (i + 1) * Width, (j + 1) * Width, fill="black", width=1)
            # f.write("\n")
        for (j, i) in walls:
            self.can.create_rectangle(i * Width, j * Width, (i + 1) * Width, (j + 1) * Width, fill="black", width=1)
        # f.write("#")
        for (i, j, c, w) in specials:
            specialcoords.append((j, i))
            self.can.create_rectangle(i * Width, j * Width, (i + 1) * Width, (j + 1) * Width, fill=c, width=1)
        self.initialize_path()
        self.hide_path()

    def waithere(self):
        var = tk.IntVar()
        self.after(3000, var.set, 1)
        #print("waiting...")
        self.wait_variable(var)

    def move_player(self, event):
        margin_right = 3
        key = event.keysym
        if key == "Left":
            self.x = self.x - 1
            #print("(To The Left)is valid? -> " + str(self.isValidMove()))
            if self.isValidMove():
                self.can.move(self.player, -30, 0)
                #print((self.x, self.y))
            else:
                self.x = self.x + 1
        elif key == "Right":
            self.x = self.x + 1
            #print("(To The Right)is valid? -> " + str(self.isValidMove()))
            if self.isValidMove():
                self.can.move(self.player, 30, 0)
                if self.x % margin_right == 0:
                    self.resize(self.winfo_width() + 100)
                    margin_right = margin_right * 2
                    #print("(X, MARGIN RIGHT): -> (" + str(self.x) + " ," + str(margin_right) + ")")
                #print((self.x, self.y))
            else:
                self.x = self.x - 1
        elif key == "Up":
            self.y = self.y - 1
            #print("(To The Sky)is valid? -> " + str(self.isValidMove()))
            if (self.isValidMove()):
                self.can.move(self.player, 0, -30)
                #print((self.x, self.y))
            else:
                self.y = self.y + 1
        elif key == "Down":
            self.y = self.y + 1
            #print("(To The Floor)is valid? -> " + str(self.isValidMove()))
            if self.isValidMove():
                self.can.move(self.player, 0, 30)
                #print((self.x, self.y))
            else:
                self.y = self.y - 1
            if self.x == 18 and self.y == 13:
                messagebox.showinfo("Congratulations! You WON", "YOU WON!\nYou reached the end of The Maze!")
        elif key == "space":
            self.display_path()
            #print("SHOW PATH")
            self.waithere()
            self.hide_path()

    def initialize_path(self):
        for (j, i) in coords:
            temp = self.can.create_rectangle(i * Width, j * Width, (i + 1) * Width, (j + 1) * Width, fill="purple",
                                             width=1)
            path_coordinates.append(temp)

    def display_path(self):
        for temp in path_coordinates:
            self.can.itemconfig(temp, fill='purple')

    def hide_path(self):
        for temp in path_coordinates:
            self.can.itemconfig(temp, fill='white')
            # self.can.create_rectangle(i * Width, j * Width, (i + 1) * Width, (j + 1) * Width, fill="white", width=1)

    def isValidMove(self):
        if (self.y, self.x) in walls:
            #print(self.x, self.y)
            return False
        #print(self.x, self.y)
        return True

    def generateMaze(self):
        maze = ""
        for i in range(y):
            for j in range(x):
                if (i, j) in specialcoords:
                    maze = maze + "@"
                elif (i, j) in walls:
                    maze = maze + "#"
                else:
                    maze = maze + " "
            maze = maze + "\n"
        #print(maze)
        f = open("maze-map.txt", "w")
        f.write(maze)


if __name__ == '__main__':
    game = Game()
    c = open("maze-map.txt", "r")
    #print(c.read())
    game.mainloop()
