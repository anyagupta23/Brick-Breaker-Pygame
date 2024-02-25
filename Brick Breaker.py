from tkinter import *
import random
import time
FPS = 45
tk = Tk()
canvas = Canvas(tk, width = 500, height = 400)
canvas.pack()
tk.update()
wid = canvas.winfo_width()
hei = canvas.winfo_height()
gamename = "Brick Breaker"
total_score = 0
level = 1
keyPressed = False
b_font = ("Pursia", 28)
s_font = ("Pursia", 18)
colors = ["cornflowerblue", "mediumspringgreen", "cyan", "magenta", "orchid", "pink", "lightcoral", "orange", "khaki"]


class Ball:
    def __init__(self, canvas, paddle, brick, score, color):
        self.canvas = canvas
        self.paddle = paddle
        self.brick = brick
        self.score = score
        self.color = color
        start = [150, 200]
        r= 8
        rect = (start [0] - r, start[1] - r, start[0] + r, start[1] + r)
        choice = colors[random.randint(0,8)]
        self.id = canvas.create_oval(rect, fill = choice)
        self.xspeed = 3
        self.yspeed = 3
        self.x = self.xspeed
        self.y = self.yspeed
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False

    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                return True
        return False

    def draw(self):
        pos = self.canvas.coords(self.id)
        brick = self.hit_brick(pos)
        if(brick!=None):
            self.brick_angle(pos, brick)
            self.score.add_score()
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
        if self.hit_paddle(pos):
            self.y = -self.yspeed
            self.x = self.edge_hit(pos, self.paddle)
        if pos[1] <= 0:
            self.y = self.yspeed
        if pos[0] <= 0 or pos[2] >= self.canvas_width:
            self.x = -(self.x)
        self.canvas.move(self.id, self.x, self.y)

    def edge_hit(self, pos, paddle):
        paddle_pos = self.canvas.coords(paddle.id)
        b_x = (pos[0] + pos [2]) / 2
        p_x = (paddle_pos[0] + paddle_pos [2]) / 2
        direction =0
        speed = abs(self.x)
        if (speed !=0):
            direction = self.x/speed
        distance = 25
        if b_x < p_x - distance:
            direction = -1
            speed+=1
        if b_x > p_x + distance:
            direction = 1
            speed+=1
        return direction * speed

    def hit_brick(self, pos):
        hits = self.canvas.find_overlapping(pos[0], pos[1], pos[2], pos[3])
        if len(hits) > 1:
            for b in self.brick.id:
                if b in hits:
                    return b
        return None

    def brick_angle(self, pos, b):
        x = (pos[0] + pos[2])/2
        y= (pos[1] + pos[3])/2
        xspeed = abs(self.x)
        yspeed = abs(self.y)
        brick_pos = self.canvas.coords(b)
        self.canvas.delete(b)
        self.brick.id.remove(b)
        if(x>= brick_pos[0] and x <=brick_pos[2]):
            self.y = -(self.y)
        elif(y>= brick_pos[1] and x <=brick_pos[3]):
            self.x = -(self.x)
        else:
            if(x < brick_pos[0] and y < brick_pos[1]):
                self.x = -xspeed
                self.y = -yspeed
            if(x < brick_pos[0] and y < brick_pos[3]):
                self.x = -xspeed
                self.y = yspeed
            if(x < brick_pos[2] and y < brick_pos[1]):
                self.x = xspeed
                self.y = -yspeed
            if(x < brick_pos[2] and y < brick_pos[3]):
                self.x = xspeed
                self.y = yspeed

class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.color = color
        start = [200, 300]
        width, height = 100, 10
        rect = (start[0], start[1], start[0]+width, start[1]+height)
        choice = colors[random.randint(0,8)]
        self.id = canvas.create_rectangle(rect, fill = choice)
        self.x = 0
        self.speed = 4.5
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)

    def draw(self):
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0 and self.x < 0:
            self.x = 0
        elif pos [2] >= self.canvas_width and self.x > 0:
            self.x = 0
        self.canvas.move(self.id, self.x, 0)

    def turn_left(self, evt):
        self.x = -self.speed

    def turn_right(self, evt):
        self.x = self.speed

class Brick:
    def __init__(self, canvas, columns, rows):
        self.canvas = canvas
        self.id = []
        self.canvas_width = self.canvas.winfo_width()
        self.columns = columns
        self.rows = rows
        array_height = 100
        self.h = int(array_height / rows)
        self.w = int(self.canvas_width/columns)
        
    def create(self):
        for i in range(self.columns):
            for j in range(self.rows):
                x1, y1 = i*self.w, j*self.h
                x2, y2 = x1+self.w, y1+self.h
                rect = (x1, y1, x2, y2)
                choice = colors[random.randint(0,8)]
                b = self.canvas.create_rectangle(rect, fill = choice)
                self.id.append(b)

class Score:
    def __init__(self, canvas, score, level):
        self.canvas = canvas
        self.score = score
        text = "Score: " + str(self.score)
        self.scoretext = self.canvas.create_text(wid/4, hei - 20, font = s_font, text = text)
        text = "Level: " + str(level)
        self.leveltext = self.canvas.create_text(3*wid/4, hei - 20, font = s_font, text = text)

    def add_score(self):
        self.score+=1
        text = "Score: " + str(self.score)
        self.canvas.itemconfig(self.scoretext, text = text)
    
def main():
    tk.title(gamename)
    showStartScreen()
    while True:
        runGame()
        showGameOver()

def runGame():
    global total_score, level
    score = Score(canvas, total_score, level)
    brick = Brick(canvas, level + 1, level+1)
    brick.create()
    paddle = Paddle(canvas, 'green')
    ball = Ball(canvas, paddle, brick, score, 'red')
    while ball.hit_bottom == False and len(brick.id) !=0:
        ball.draw()
        paddle.draw()
        tk.update()
        time.sleep(1/FPS)
    if ball.hit_bottom ==True:
        total_score=0
        level =1
    else:
        total_score +=score.score
        level +=1
        canvas.delete("all")
        runGame()

def showPressKey():
    text = "Press a key to play."
    canvas.create_text(wid/2, hei - 50, font = s_font, text = text)

def keypress(event):
    global keyPressed
    keyPressed = True

def showStartScreen():
    global keyPressed
    keyPressed = False
    canvas.bind_all('<KeyPress>', keypress)
    canvas.create_text(wid/2, hei/2 - 50, font = b_font, text = "Welcome to")
    canvas.create_text(wid/2, hei/2 + 50, font = b_font, text = gamename)
    showPressKey()
    while keyPressed == False:
        tk.update()
    canvas.delete("all")

def showGameOver():
    global keyPressed
    keyPressed = False
    canvas.unbind_all('<KeyPress-Left>')
    canvas.unbind_all('<KeyPress-Right>')
    canvas.bind_all('<KeyPress>', keypress)
    canvas.create_text(wid/2, hei/2,font = b_font, text = "Game Over!")
    showPressKey()
    while keyPressed == False:
        tk.update()
    canvas.delete("all")

if __name__== '__main__':
    main()



















    
