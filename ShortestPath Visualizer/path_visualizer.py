import math,random,sys
import pygame
from collections import deque 
from tkinter import messagebox,Tk

size = 675
win=pygame.display.set_mode((size,size))
pygame.display.set_caption("Path find visualizer")
clock=pygame.time.Clock

row=48
col=48

w=size//row
h=size//col

RED = (255,0,0)                        #colors
GREEN = (27, 194, 144)
BLUE = (36, 70, 156)
YELLOW = (255,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
L_PURPLE=(160, 113, 191)
D_PURPLE=(102, 1, 145)
ORANGE = (255,165,0)
GREY = (58, 70, 82)
TEAL = (91, 245, 245)

grid=[]                                #stores the spots
path=[]                                #stores the path from start to end
queue, visited = deque(), []
openSet,closeSet= [],[]

class spot:
    def __init__(self,row,col):
        self.x=row
        self.y=col
        self.f, self.g, self.h = 0, 0, 0
        self.visited=False
        self.wall=False
        self.neighbors = []
        self.prev = None
    
    def make_start(self):
        self.color=RED

    def show(self, win, color, shape= 1):
        if self.wall == True:
            color = BLACK
        if shape == 1:
            pygame.draw.rect(win, color, (self.x*w, self.y*h, w-1, h-1))
        else:
            pygame.draw.circle(win, color, (self.x*w+w//2, self.y*h+h//2), w//3)

    def add_neighbors(self, grid):
        if self.x < col - 1:
            self.neighbors.append(grid[self.x+1][self.y])
        if self.x > 0:
            self.neighbors.append(grid[self.x-1][self.y])
        if self.y < row - 1:
            self.neighbors.append(grid[self.x][self.y+1])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y-1])

    def add_diagonals(self,grid):
        if self.x < col - 1 and self.y < row - 1:
            self.neighbors.append(grid[self.x+1][self.y+1])
        if self.x < col - 1 and self.y > 0:
            self.neighbors.append(grid[self.x+1][self.y-1])
        if self.x > 0 and self.y < row - 1:
            self.neighbors.append(grid[self.x-1][self.y+1])
        if self.x > 0 and self.y > 0:
            self.neighbors.append(grid[self.x-1][self.y-1])

#To change the state of the wall true or false
def clickWall(pos, state,start,end):
    i = pos[0] // w
    j = pos[1] // h

    if grid[i][j]!=start and grid[i][j]!=end:
        grid[i][j].wall = state


def heuristics(a, b):
    return math.sqrt((a.x - b.x)**2 + abs(a.y - b.y)**2)


#make grid 
for i in range(col):
    arr = []
    for j in range(row):
        arr.append(spot(i, j))
    grid.append(arr)

#update neighbours
for i in range(col):
    for j in range(row):
        grid[i][j].add_neighbors(grid)


#Finding mouse position
def get_clicked_position(pos):
    y,x=pos

    row=y//h
    col=x//w

    return row,col


def main():
    flag = False
    noflag = True
    startflag1 = False
    startflag2 = False

    start=None
    end=None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in (1, 3):
                    pos=pygame.mouse.get_pos()
                    x,y=get_clicked_position(pos)
                    spot=grid[x][y]
                    if not start and spot!=end:   
                        start=spot
                        start.wall=False
                        start.visited = True
                    elif not end and spot!=start:
                        end=spot
                        end.wall=False              
                    elif spot!=end and spot!=start:     
                         clickWall(pygame.mouse.get_pos(), event.button==1,None,None)

            elif event.type == pygame.MOUSEMOTION:
                if event.buttons[0] or event.buttons[2]:
                    clickWall(pygame.mouse.get_pos(), event.buttons[0],start,end)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    openSet.append(start)
                    startflag2 = True

                    for i in range(col):
                        for j in range(row):
                            grid[i][j].add_diagonals(grid)

                elif event.key == pygame.K_d:
                    queue.append(start)
                    startflag1= True

        #dijkstra Algorithm
        if startflag1:
            if len(queue) > 0:
                current = queue.popleft()
                if current == end:
                    temp = current
                    while temp.prev:
                        path.append(temp.prev)
                        temp = temp.prev 
                    if not flag:
                        flag = True
                        print("Done")
                    elif flag:
                        continue
                if flag == False:
                    for i in current.neighbors:
                        if not i.visited and not i.wall:
                            i.visited = True
                            i.prev = current
                            queue.append(i)
            else:
                if noflag and not flag:
                    Tk().wm_withdraw()
                    messagebox.showinfo("No Solution", "There was no solution" )
                    noflag = False
                else:
                    continue

        #A* Pattern
        if startflag2:                                      #First Algorithm start
            if len(openSet) > 0:
                winner = 0
                for i in range(len(openSet)):
                    if openSet[i].f < openSet[winner].f:
                        winner = i

                current = openSet[winner]
                
                if current == end:
                    temp = current
                    while temp.prev:
                        path.append(temp.prev)
                        temp = temp.prev 
                    if not flag:
                        flag = True
                        print("Done")
                    elif flag:
                        continue

                if flag == False:
                    openSet.remove(current)
                    closeSet.append(current)

                    for neighbor in current.neighbors:
                        if neighbor in closeSet or neighbor.wall:
                            continue
                        tempG = current.g + 1

                        newPath = False
                        if neighbor in openSet:
                            if tempG < neighbor.g:
                                neighbor.g = tempG
                                newPath = True
                        else:
                            neighbor.g = tempG
                            newPath = True
                            openSet.append(neighbor)
                        
                        if newPath:
                            neighbor.h = heuristics(neighbor, end)
                            neighbor.f = neighbor.g + neighbor.h
                            neighbor.prev = current

            else:
                if noflag:
                    Tk().wm_withdraw()
                    messagebox.showinfo("No Solution", "There was no solution" )
                    noflag = False



        win.fill(BLACK)
        for i in range(col):
            for j in range(row):
                spot = grid[i][j]
                spot.show(win, GREY)
                if spot in path:
                    spot.show(win, L_PURPLE)
                    spot.show(win, D_PURPLE, 0)
                elif spot.visited:
                    spot.show(win, GREEN)
                if spot in queue and not flag:
                    spot.show(win, TEAL)
                    spot.show(win, BLUE, 0)
                if spot == start:
                    spot.show(win, RED)
                if spot == end:
                    spot.show(win, ORANGE)
                
                if spot in path:
                    spot.show(win, L_PURPLE)
                    spot.show(win, D_PURPLE, 0)
                elif spot in closeSet:
                    spot.show(win, GREEN)
                elif spot in openSet:
                    spot.show(win, BLUE, 0)
                    
                
                
        pygame.display.update()

main()


