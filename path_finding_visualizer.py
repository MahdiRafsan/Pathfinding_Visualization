from queue import PriorityQueue
from colors import *
import pygame
import random
import tkinter as tk
from tkinter.messagebox import *
  
class Grid():    
    def __init__(self, rows, cols, width):
        pygame.init()
        pygame.display.set_caption("Path Finding Visualization")
        
        self.window = pygame.display.set_mode((width, width))
                
        self.rows = rows
        self.cols = cols
        self.width = width
        self.gap = self.width // self.rows
    
    def draw_grid(self):
        for i in range(self.rows):
            pygame.draw.line(self.window, BLUE, (0, i * self.gap), (self.width , i * self.gap))
            for j in range(self.cols):
                pygame.draw.line(self.window, BLUE, (j * self.gap, 0), (j * self.gap, self.width))
                
    def get_square(self, grid):
        pos = pygame.mouse.get_pos()
        row, col = pos[0] // self.gap, pos [1] // self.gap
        return grid[row][col]
        
    def make_squares(self):
        grid = []
        for i in range(self.rows):
            grid.append([])
            for j in range(self.cols):
                square = Square(i, j, self.gap, self.rows)  
                grid[i].append(square)
        return grid
    
    def draw(self, grid):
        self.window.fill(WHITE)
        
        for row in grid:
            for square in row:
                square.draw(self.window)
    
        self.draw_grid()
        pygame.display.update()

class Square():
    def __init__(self, row, col, width, no_of_rows):
        self.row = row
        self.col = col
        self.width = width
       
        self.total_rows = no_of_rows
        
        self.x = row * self.width
        self.y = col * self.width
        
        self.color = WHITE
    
    def get_pos(self):
        return self.row, self.col

    def is_wall(self):
        return self.color == BLACK
        
    def mark_beginning(self):
        self.color = RED
     
    def mark_target(self):
        self.color = GREEN
        
    def create_wall(self):
        self.color = BLACK
   
    def draw_path(self):
        self.color = PURPLE
    
    def mark_open(self):
        self.color =  YELLOW
        
    def mark_closed(self):
        self.color = TURQUOISE
    
    def clear(self):
       self.color = WHITE
    
    def add_neighbors(self, square):
        self.neighbors = []
        
        # upper neighbor
        if self.row > 0 and square[self.row - 1][self.col].is_wall() == False:
            self.neighbors.append(square[self.row - 1][self.col])
        
        # lower neighbor
        if self.row < self.total_rows -1 and square[self.row + 1][self.col].is_wall() == False:
            self.neighbors.append(square[self.row + 1][self.col])
        
        #right neighbor  
        if self.col < self.total_rows - 1 and square[self.row][self.col + 1].is_wall() == False:
            self.neighbors.append(square[self.row][self.col + 1])
        
        # left neighbor
        if self.col > 0 and square[self.row][self.col - 1].is_wall() == False:
            self.neighbors.append(square[self.row][self.col - 1])
            
        # # diagonal neighbors
        
        # # upper right neighbor
        # if self.row > 0 and self.col < self.total_rows - 1 and not square[self.row - 1][self.col + 1].is_wall():
        #     self.neighbors.append(square[self.row-1][self.col+1])
         
        # # upper left neighbor
        # if self.row > 0 and self.col > 0 and not square[self.row - 1][self.col - 1].is_wall():
        #     self.neighbors.append(square[self.row-1][self.col-1])
        
        # # lower left neighbor
        # if self.row < self.total_rows - 1 and self.col > 0 and not square[self.row + 1][self.col - 1].is_wall():
        #     self.neighbors.append(square[self.row+1][self.col-1])
        
        # # lower right neighbor
        # if self.row < self.total_rows - 1 and self.col < self.total_rows - 1 and not square[self.row + 1][self.col + 1].is_wall():
        #     self.neighbors.append(square[self.row+1][self.col+1])
        
    def draw(self, win):
          pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def __lt__(self, other):
       return False


class Algorithms():
    def __init__(self, grid, start, end):
        self.run = RunApp()
        self.grid = self.run.grid
        
    def reconstruct_path(self, parent, current, grid):
        while current in parent:
            current = parent[current]
            current.draw_path()
            self.grid.draw(grid)
    
    def breadth_first_search(self, grid, start, end):
        
        queue = [start]
        visited = [start]  
        came_from = {}
       
        while queue:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                    pygame.quit()
                    
            current = queue.pop(0)
            if current == end:
                self.reconstruct_path(came_from, end, grid)
                end.mark_target()
                return True
            
            for neighbor in current.neighbors:
                if neighbor not in visited:            
                    came_from[neighbor] = current
                    visited.append(neighbor)
                    queue.append(neighbor)
                    neighbor.mark_open()
  
            self.grid.draw(grid)
           
            if current != start:
                current.mark_closed()
        
        tk.messagebox.showerror("No Solution", "Solution not found.")      
        return False 
    
    def depth_first_search(self, grid, start, end):
        
        stack = [start]
        visited = set()
        came_from = {}
        
        while stack:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                    pygame.quit()
    
            current = stack.pop()
            visited.add(current)
            if current == end:
                self.reconstruct_path(came_from, end, grid)
                end.mark_target()
                return True
            
            for neighbor in current.neighbors:
                if neighbor not in visited:
                    came_from[neighbor] = current
                    stack.append(neighbor)
                    neighbor.mark_open()
                    
            self.grid.draw(grid)
            
            if current != start:
                current.mark_closed()
                
        tk.messagebox.showerror("No Solution", "Solution not found.")      
        return False    
    
    def dijkstra(self, grid, start, end):
        
        count = 0
        open_set = PriorityQueue()
        
        came_from = {}
        cost_so_far = {square: float("inf") for row in grid for square in row}
        cost_so_far[start] = 0
        
        open_set.put((cost_so_far[start], count, start))
        
        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                    pygame.quit()
                    
            current = open_set.get()[2]
            
            if current == end:
                self.reconstruct_path(came_from, end, grid)
                end.mark_target()
                return True
            
            for neighbor in current.neighbors:
                new_cost = cost_so_far[current] + 1
                if new_cost < cost_so_far[neighbor]:
                    count += 1
                    came_from[neighbor] = current
                    cost_so_far[neighbor] = new_cost
                    open_set.put((cost_so_far[neighbor], count, neighbor))
                    neighbor.mark_open()
            
            self.grid.draw(grid)        
            if current != start:
                current.mark_closed()
                
        tk.messagebox.showerror("No Solution", "Solution not found.")            
        return False
           
    def heuristic(self, start, destination):
        x1, y1 = start.get_pos()
        x2, y2 = destination.get_pos()
        return abs(x1 - x2) + abs(y1 - y2)
    
    def a_star(self, grid, start, end):
        count = 0
        open_set = PriorityQueue()
        
        g_score = {square: float("inf") for row in grid for square in row}
        g_score[start] = 0
        
        f_score = {square: float("inf") for row in grid for square in row}
        f_score[start] = self.heuristic(start, end)
        
        came_from = dict()
        
        open_set.put((f_score[start], count, start))
        closed_set = {start}
        
        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                    pygame.quit()
                    
            current = open_set.get()[2]
            closed_set.remove(current)
            
            if current == end:
                self.reconstruct_path(came_from, end, grid)
                end.mark_target()
                return True
            
            for neighbor in current.neighbors:
                temp_g_score = g_score[current] + 1
                
                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + self.heuristic(neighbor, end)
                    
                    if neighbor not in closed_set:
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))    
                        closed_set.add(neighbor)
                        neighbor.mark_open()
            
            self.grid.draw(grid)
            
            if current != start:
                current.mark_closed()
        
        tk.messagebox.showerror("No Solution", "Solution not found.")
        return False
        
class RunApp():
    def __init__(self):
        self.rows, self.cols, self.width = 50, 50, 650
        self.grid = Grid(self.rows, self.cols, self.width)
        
    def run(self):
        
        squares = self.grid.make_squares()
        start, end = None, None
        running = True
        
        algorithm = Algorithms(squares, start, end)
        
        root = tk.Tk()#.withdraw()
        root.withdraw()
        tk.messagebox.showinfo("Instructions", "\nLEFT CLICK      - To place START/END points and DRAW walls"
                                        "\nRIGHT CLICK   - To erase START/END points and walls"
                                        "\nPRESS 1           - To run Breadth Frist Search Algorithm"
                                        "\nPRESS 2           - To run Depth First Search Algorithm"
                                        "\nPRESS 3           - To run Dijkstra Algorithm"
                                        "\nPRESS 4           - To run A-Star Search Algorithm"
                                        "\nPRESS R           - To generate random walls in the grid"
                                        "\nPRESS C           - To Clear the screen"
                                        "\nPRESS Q           - To Quit the program")
        while running:

            self.grid.draw(squares)
            square = self.grid.get_square(squares) 
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                    running = False    
                
                # draw start and end positions and walls    
                if pygame.mouse.get_pressed()[0]:
                    if not start and square != end and not square.is_wall():
                        start = square
                        start.mark_beginning()
                    
                    elif not end and square != start and not square.is_wall():
                        end = square
                        end.mark_target()
                    
                    elif square != start and square != end:
                        square.create_wall()
                
                # erase start/end positions and walls
                elif pygame.mouse.get_pressed()[2]:
                    square.clear()
                    if square == start:
                        start = None
                    if square == end:
                        end = None
                
                # run algorithms        
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1 or event.key == pygame.K_KP1 and start and end:
                        for row in squares:
                            for square in row:
                                square.add_neighbors(squares)
                        algorithm.breadth_first_search(squares, start, end)
                        start.mark_beginning()
                        
                    if event.key == pygame.K_2 or event.key == pygame.K_KP2 and start and end:
                        for row in squares:
                            for square in row:
                                square.add_neighbors(squares)        
                        algorithm.depth_first_search(squares, start, end)
                        start.mark_beginning()
                        
                    if event.key == pygame.K_3 or event.key == pygame.K_KP3 and start and end:
                        for row in squares:
                            for square in row:
                                square.add_neighbors(squares)  
                        algorithm.dijkstra(squares, start, end)
                        start.mark_beginning()
                        
                    if event.key == pygame.K_4 or event.key == pygame.K_KP4 and start and end:
                        for row in squares:
                            for square in row:
                                square.add_neighbors(squares)  
                        algorithm.a_star(squares, start, end)
                        start.mark_beginning()
                    
                    # create random walls
                    if event.key == pygame.K_r:
                        for i in range(self.rows):
                            for j in range(self.cols):
                                if random.randint(1, 3) == 3:
                                    squares[i][j].color = BLACK                
                    
                    # clear the board
                    if event.key == pygame.K_c:
                        start = None
                        end = None
                        squares = self.grid.make_squares()
        pygame.quit()
        
def main():
    
    algo = RunApp()
    algo.run()
    
if __name__ == "__main__":
    main()