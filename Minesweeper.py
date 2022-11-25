from pygame import *
import random
font.init()

bg_color = (192, 192, 192)
grid_color = (128, 128, 128)

game_width = 20
game_height = 20
numMine = 35
grid_size = 32
border = 16
top_border = 100
display_width = 700
display_height = 800
gameDisplay = display.set_mode((display_width, display_height))
timer = time.Clock()
display.set_caption("Сапер")

spr_emptyGrid = image.load("Sprites/empty.png")
spr_flag = image.load("Sprites/flag.png")
spr_grid = image.load("Sprites/Grid.png")
spr_grid1 = image.load("Sprites/grid1.png")
spr_grid2 = image.load("Sprites/grid2.png")
spr_grid3 = image.load("Sprites/grid3.png")
spr_grid4 = image.load("Sprites/grid4.png")
spr_grid5 = image.load("Sprites/grid5.png")
spr_grid6 = image.load("Sprites/grid6.png")
spr_grid7 = image.load("Sprites/grid7.png")
spr_grid8 = image.load("Sprites/grid8.png")
spr_grid7 = image.load("Sprites/grid7.png")
spr_mine = image.load("Sprites/mine.png")
spr_mineClicked = image.load("Sprites/mineClicked.png")
spr_mineFalse = image.load("Sprites/mineFalse.png")



grid = []
mines = []


def drawText(txt, s, yOff=0):
    screen_text = font.SysFont("Calibri", s, True).render(txt, True, (0, 0, 0))
    rect = screen_text.get_rect()
    rect.center = (game_width * grid_size / 2 + border, game_height * grid_size / 2 + top_border + yOff)
    gameDisplay.blit(screen_text, rect)


class Grid:
    def __init__(self, xGrid, yGrid, type):
        self.xGrid = xGrid
        self.yGrid = yGrid
        self.clicked = False
        self.mineClicked = False
        self.mineFalse = False
        self.flag = False
        self.rect = Rect(border + self.xGrid * grid_size, top_border + self.yGrid * grid_size, grid_size, grid_size)
        self.val = type

    def drawGrid(self):
        if self.mineFalse:
            gameDisplay.blit(spr_mineFalse, self.rect)
        else:
            if self.clicked:
                if self.val == -1:
                    if self.mineClicked:
                        gameDisplay.blit(spr_mineClicked, self.rect)
                    else:
                        gameDisplay.blit(spr_mine, self.rect)
                else:
                    if self.val == 0:
                        gameDisplay.blit(spr_emptyGrid, self.rect)
                    elif self.val == 1:
                        gameDisplay.blit(spr_grid1, self.rect)
                    elif self.val == 2:
                        gameDisplay.blit(spr_grid2, self.rect)
                    elif self.val == 3:
                        gameDisplay.blit(spr_grid3, self.rect)
                    elif self.val == 4:
                        gameDisplay.blit(spr_grid4, self.rect)
                    elif self.val == 5:
                        gameDisplay.blit(spr_grid5, self.rect)
                    elif self.val == 6:
                        gameDisplay.blit(spr_grid6, self.rect)
                    elif self.val == 7:
                        gameDisplay.blit(spr_grid7, self.rect)
                    elif self.val == 8:
                        gameDisplay.blit(spr_grid8, self.rect)

            else:
                if self.flag:
                    gameDisplay.blit(spr_flag, self.rect)
                else:
                    gameDisplay.blit(spr_grid, self.rect)

    def revealGrid(self):
        self.clicked = True
        if self.val == 0:
            for x in range(-1, 2):
                if self.xGrid + x >= 0 and self.xGrid + x < game_width:
                    for y in range(-1, 2):
                        if self.yGrid + y >= 0 and self.yGrid + y < game_height:
                            if not grid[self.yGrid + y][self.xGrid + x].clicked:
                                grid[self.yGrid + y][self.xGrid + x].revealGrid()
        elif self.val == -1:
            for m in mines:
                if not grid[m[1]][m[0]].clicked:
                    grid[m[1]][m[0]].revealGrid()

    def updateValue(self):
        if self.val != -1:
            for x in range(-1, 2):
                if self.xGrid + x >= 0 and self.xGrid + x < game_width:
                    for y in range(-1, 2):
                        if self.yGrid + y >= 0 and self.yGrid + y < game_height:
                            if grid[self.yGrid + y][self.xGrid + x].val == -1:
                                self.val += 1


def gameLoop():
    gameState = "Playing"
    mineLeft = numMine
    global grid
    grid = []
    global mines
    t = 0

    mines = [[random.randrange(0, game_width),
              random.randrange(0, game_height)]]

    for c in range(numMine - 1):
        pos = [random.randrange(0, game_width),
               random.randrange(0, game_height)]
        same = True
        while same:
            for i in range(len(mines)):
                if pos == mines[i]:
                    pos = [random.randrange(0, game_width), random.randrange(0, game_height)]
                    break
                if i == len(mines) - 1:
                    same = False
        mines.append(pos)

    for j in range(game_height):
        line = []
        for i in range(game_width):
            if [i, j] in mines:
                line.append(Grid(i, j, -1))
            else:
                line.append(Grid(i, j, 0))
        grid.append(line)

    for i in grid:
        for j in i:
            j.updateValue()

    while gameState != "Exit":
        gameDisplay.fill(bg_color)

        for e in event.get():
            if e.type == QUIT:
                gameState = "Exit"
            if gameState == "Game Over" or gameState == "Win":
                if e.type == KEYDOWN:
                    if e.key == K_r:
                        gameState = "Exit"
                        gameLoop()
            else:
                if e.type == MOUSEBUTTONUP:
                    for i in grid:
                        for j in i:
                            if j.rect.collidepoint(e.pos):
                                if e.button == 1:
                                    j.revealGrid()
                                    if j.flag:
                                        mineLeft += 1
                                        j.falg = False
                                    if j.val == -1:
                                        gameState = "Game Over"
                                        j.mineClicked = True
                                elif e.button == 3:
                                    if not j.clicked:
                                        if j.flag:
                                            j.flag = False
                                            mineLeft += 1
                                        else:
                                            j.flag = True
                                            mineLeft -= 1

        w = True
        for i in grid:
            for j in i:
                j.drawGrid()
                if j.val != -1 and not j.clicked:
                    w = False
        if w and gameState != "Exit":
            gameState = "Win"

        if gameState != "Game Over" and gameState != "Win":
            t += 1
        elif gameState == "Game Over":
            drawText("Ти програв", 50)
            drawText("R для рестарта", 55, 50)
            for i in grid:
                for j in i:
                    if j.flag and j.val != -1:
                        j.mineFalse = True
        else:
            drawText("Ти виграв!", 50)
            drawText("R для рестарта", 35, 50)
        s = str(t // 15)
        screen_text = font.SysFont("Calibri", 50).render(f"Час в гри: {s} cек, кiлькiсть мiн: {mineLeft.__str__()}", True, (0, 0, 0))
        gameDisplay.blit(screen_text, (border, border))

        display.update()

        timer.tick(15)


gameLoop()
quit()
