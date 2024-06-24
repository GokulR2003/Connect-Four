import tkinter as tk
from tkinter import messagebox
import pygame

pygame.mixer.init()
drop_sound = pygame.mixer.Sound('drop.wav')
win_sound = pygame.mixer.Sound('win.wav')

ROWS = 6
COLUMNS = 7
EMPTY = 0
PLAYER1 = 1
PLAYER2 = 2

class ConnectFour:
    def __init__(self, root):
        self.root = root
        self.root.title("Connect Four: The Classic Drop Challenge")
        self.current_player = PLAYER1
        self.board = [[EMPTY]*COLUMNS for _ in range(ROWS)]
        self.buttons = [tk.Button(root, text=f"Drop {i+1}", command=lambda col=i: self.drop_piece(col)) for i in range(COLUMNS)]
        for i, button in enumerate(self.buttons):
            button.grid(row=0, column=i)
        self.canvas = tk.Canvas(root, width=COLUMNS*100, height=ROWS*100, bg="blue")
        self.canvas.grid(row=1, columnspan=COLUMNS)
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        for row in range(ROWS):
            for col in range(COLUMNS):
                x0 = col * 100
                y0 = row * 100
                x1 = x0 + 100
                y1 = y0 + 100
                color = "white" if self.board[row][col] == EMPTY else "red" if self.board[row][col] == PLAYER1 else "yellow"
                self.canvas.create_oval(x0+10, y0+10, x1-10, y1-10, fill=color, outline="black")

    def drop_piece(self, col):
        for row in range(ROWS-1, -1, -1):
            if self.board[row][col] == EMPTY:
                self.board[row][col] = self.current_player
                self.draw_board()
                drop_sound.play()
                if self.check_winner(row, col):
                    win_sound.play()
                    messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                    self.reset_game()
                else:
                    self.current_player = PLAYER2 if self.current_player == PLAYER1 else PLAYER1
                return
        messagebox.showwarning("Column Full", "This column is full! Choose another one.")

    def check_winner(self, row, col):
        def count_pieces(delta_row, delta_col):
            count = 0
            for i in range(1, 4):
                r = row + delta_row * i
                c = col + delta_col * i
                if 0 <= r < ROWS and 0 <= c < COLUMNS and self.board[r][c] == self.current_player:
                    count += 1
                else:
                    break
            return count

        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dr, dc in directions:
            if count_pieces(dr, dc) + count_pieces(-dr, -dc) >= 3:
                return True
        return False

    def reset_game(self):
        self.board = [[EMPTY]*COLUMNS for _ in range(ROWS)]
        self.draw_board()
        self.current_player = PLAYER1

if __name__ == "__main__":
    root = tk.Tk()
    game = ConnectFour(root)
    root.mainloop()
