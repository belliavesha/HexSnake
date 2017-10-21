from time import sleep
from random import random as rnd
from numpy import zeros
import pygame 
from pygame.locals import *

further = lambda x, y, d: {
    0: (x ,y-1),	
    1: (x-1,y-1),
    2: (x-1 ,y),
    3: (x,y+1),
    4: (x+1 ,y+1),
    5: (x+1 ,y)
    }[d]

def dir(x,y,i,j):
    d=3 if abs(x-i)>1 or abs(y-j)>1 else 0 
    v=(x-i)/abs(x-i) if x!=i else 0 
    h=(y-j)/abs(y-j) if y!=j else 0
    return (d+{
        (0,-1):0,
        (-1,-1):1,
        (-1,0):2,
        (0,1):3,    
        (1,1):4,
        (1,0):5
        }[(v,h)])%6

if True: # objects
    HEAD=-3 
    BODY=-2
    TAIL=-1
    APPLE=1
    BORDER=-10
    KILLER=-20
    EXTRAAPPLE=11
    EXTRABORDER=12
    LENGTHEN=13
    SHORTEN=14
    REVERSE=15
    EXTRAKILLER=16
    EXTRASCORE=17
    BONUS=10
    EMPTY=0

if True: # colors
    colorSnake=(2,250,200)
    colorGrass=(0,100,20)
    colorBorder=(250,120,0)
    colorApple=(250,0,0)
    colorMouth=(250,200,200)
    colorBonus=(40,0,240)
    colorText=(240,240,10)

if True:
    s=int(raw_input("What is field size? (more than 2) : "))
    loop={'y':False,'n':True}[raw_input("Do borders kill? ('y' or 'n') : ")[0]] # read params
    difficulty=int(raw_input("""
    0 - "peaceful" : bonuses only make better
    1 - "easy" : choose to eat a bonus would be well more often
    2 - "medium" : bonuces are good or evil fifty fifty 
    3 - "hard" : basically, eat a bonus is of no benefit
    4 - "insane" : the game is droven crazy
    How difficult will the game be? (a digit) : """))
    bonus_frequency=3
    bonuses={ 0 : [EXTRAAPPLE,SHORTEN,REVERSE,EXTRASCORE],
    1: [EXTRAAPPLE,SHORTEN,REVERSE,EXTRASCORE,EXTRABORDER,LENGTHEN,SHORTEN,EXTRAAPPLE],
    2: [EXTRAAPPLE,SHORTEN,REVERSE,EXTRASCORE,EXTRABORDER,LENGTHEN,EXTRAKILLER],
    3: [EXTRAAPPLE,SHORTEN,REVERSE,EXTRABORDER,LENGTHEN,EXTRAKILLER],
    4: [EXTRAAPPLE,REVERSE,REVERSE,EXTRABORDER,LENGTHEN,EXTRAKILLER],
    }[difficulty]
    ZEROSPEED=35
    speedlevel=s#15# float(raw_input("How fast does the snake crawl? \n"))

    lose=False
    pause = False


if True: # pygame init
    pygame.init()
    display_width = 800
    display_height = int(display_width*0.85)
    screen = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption('HexoSnake')

    fontPause = pygame.font.SysFont("monospace", 40)
    fontRules = pygame.font.SysFont("monospace", 13)

    textGO = fontPause.render("GAME OVER!", 1, colorText)
    textPause = fontPause.render("Paused...", 1, colorText)
    textScore = fontRules.render("Score : ",1,colorText)
    textSpeed = fontRules.render("Speed : ",1,colorText)
    Rules = ["Controls:",
        "q / e : left/right ",
        "a / d : left/right x2 ",
        "w / s : speed up/down ",
        "p : pause",
        "esc : quit"]
    textRules=[fontRules.render(rule, 1, colorText)for rule in Rules]

class Snake:
    field_size=1
    field_dimension=1
    field =  zeros((1,1))
    display_width_step=display_width
    display_height_step=display_height

    def __init__(self,x,y,sc,d):
        self.score=sc
        self.body=[(x,y)]*sc
        self.cdir=d

    def initfield(self,s):
        n=2*s-1
        self.field_size=s
        self.field_dimension=n
        self.field = zeros((n,n))
        self.display_width_step=display_width/n
        self.display_height_step=display_height/n
    
    def out(self,x,y):
        s=self.field_size
        n=self.field_dimension
        if x<0 or y<0: return True
        if x>=n or y>=n: return True
        if x>=s and y<=x-s : return True
        if y>=s and x<=y-s : return True
        if self.field[x][y]==BORDER : return True
        return False

    def setobj(self,a,t):
        while a>0:
            i=int(self.field_dimension*rnd())
            j=int(self.field_dimension*rnd())
            if self.field[i][j]==EMPTY  and not self.out(i,j):  
                a=a-1
                self.field[i][j]=t

    def display_crds(self,x,y):
        n=self.field_dimension
        return (1+display_width/(4*n)+display_width/4
          +x*display_width/(n)-display_width*y/2/(n),
         1+display_height/(2*n)+y*display_height/(n))

    def drawsymbol(self,i,j):
        l=self.field[i][j]
        crds=self.display_crds(i,j)
        dw=self.display_width_step
        dh=self.display_height_step
        if l==TAIL:
            pygame.draw.circle(screen, colorSnake, crds, dh/2, 0)
        if l==BODY:
            pygame.draw.circle(screen, colorSnake, crds, dw/2, 0)
        if l==HEAD:
            x,y=further(i,j,self.cdir)
            x,y=self.display_crds(x,y)
            mcrds=((x+2*crds[0])/3,(y+2*crds[1])/3)
            pygame.draw.circle(screen, colorSnake, crds, dw/2, 0)
            pygame.draw.circle(screen, colorMouth, mcrds, dw/6, 0)
        if l==APPLE :
            pygame.draw.circle(screen, colorApple, crds, dh/2, 0)
        if l==EMPTY:
            return 
        if l==KILLER:
            cx,cy=crds
            pygame.draw.line(screen,colorBorder,(cx-dh/2,cy),(cx+dh/2,cy),2)
            pygame.draw.line(screen,colorBorder,(cx,cy-dh/2),(cx,cy+dh/2),2)
            pygame.draw.line(screen,colorBorder,(cx-dh/3,cy-dh/3),(cx+dh/3,cy+dh/3),2)
            pygame.draw.line(screen,colorBorder,(cx+dh/3,cy-dh/3),(cx-dh/3,cy+dh/3),2)
        if l==BORDER:
            pygame.draw.circle(screen, colorBorder, crds, dh/2, 0)
        if l==EXTRABORDER or l==EXTRAAPPLE :
            cx,cy=crds
            pygame.draw.line(screen,colorBonus,(cx-dh/2,cy),(cx+dh/2,cy),2)
            pygame.draw.line(screen,colorBonus,(cx,cy-dh/2),(cx,cy+dh/2),2)
        if l==SHORTEN or l==LENGTHEN :
            cx,cy=crds
            pygame.draw.line(screen,colorBonus,(cx-dh/2,cy),(cx+dh/2,cy),2)
            pygame.draw.line(screen,colorBonus,(cx,cy-dh/2),(cx,cy+dh/2),2)
            pygame.draw.line(screen,colorBonus,(cx-dh/3,cy-dh/3),(cx+dh/3,cy+dh/3),2)
            pygame.draw.line(screen,colorBonus,(cx+dh/3,cy-dh/3),(cx-dh/3,cy+dh/3),2)
        if l==REVERSE or l==EXTRAKILLER :
            cx,cy=crds
            pygame.draw.line(screen,colorBonus,(cx-dh/3,cy-dh/3),(cx+dh/3,cy+dh/3),2)
            pygame.draw.line(screen,colorBonus,(cx+dh/3,cy-dh/3),(cx-dh/3,cy+dh/3),2)
        if l==BONUS or l==EXTRASCORE:
            pygame.draw.circle(screen, colorBonus, crds, dh/2, 0)
        return 

    def drawfield(self):
        n=self.field_dimension
        s=self.field_size
        ds=self.drawsymbol
        screen.fill((0,0,0))
        pygame.draw.polygon(screen, colorGrass, [
            (0,display_height/2),
            (display_width/4.,0),
            (display_width*3./4.,0),
            (display_width,display_height/2),
            (display_width*3./4.,display_height),
            (display_width/4.,display_height)], 0)
        for j in range(n): ds(s-1,j)
        for i in range(s-1): 
            for j in range(s+i): ds(i,j)
            for j in range(i+1,n): ds(i+s,j)

    def next(self,x,y,d):
        rx, ry= further(x,y,d)
        if self.out(rx,ry):
            while (not self.out(x,y) ) :
                x,y= further(x,y,(d+3)%6)
            rx, ry= further(x,y,d)
            if not loop:
                self.field[rx][ry]=KILLER
        return rx,ry

    def crawl(self):
        f=self.field
        x,y=self.body[-1]
        if f[x][y]==BODY: f[x][y],t=TAIL,[(x,y)] 
        else : f[x][y],t=EMPTY,[]
        x,y=self.body[0]
        if f[x][y]!=BODY:
            f[x][y]=TAIL
        x,y=self.next(x,y,self.cdir)
        self.body=[(x,y)]+self.body[:-1]+t
        return self.eat(x,y) 

    def eat(self,x,y):
        a=self.field[x][y]
        if a in [BODY,HEAD,TAIL,KILLER,BORDER] :
            # snake=[]
            self.field[x][y]=EMPTY
            return True
        else :
            self.field[x][y]=-3
        if a == APPLE : 
            self.field[x][y]=-2
            self.score+=1
            self.setobj(1,APPLE)
            if self.score%bonus_frequency==0 : self.setobj(1,BONUS) # balance?  
            if difficulty==4:
                if rnd()<.5: self.setobj(2,BORDER)
                if rnd()<.5: self.setobj(2,KILLER)
                if rnd()<.2: self.setobj(1,SHORTEN)
                if rnd()<.2: self.setobj(1,LENGTHEN)
        if a == BONUS :
            a=bonuses[int(len(bonuses)*rnd())]      
            if difficulty==4:
                if rnd()<.4: self.setobj(1,REVERSE)
                if rnd()<.3: self.setobj(3,EXTRASCORE)
        if a == EXTRAAPPLE :
            self.setobj(1,APPLE)
        if a == EXTRABORDER :
            self.setobj(1,BORDER if loop else KILLER)
        if a == EXTRASCORE :
            self.score+=bonus_frequency
        if a == EXTRAKILLER :
            self.setobj(1,KILLER)
        if a == SHORTEN :
            for c in self.body[len(self.body)/2+1:]:
                self.field[c[0]][c[1]]=EMPTY
            self.body=self.body[:len(self.body)/2+1]
        if a == LENGTHEN :
            for c in self.body[1:]:
                self.field[c[0]][c[1]]=BODY
        if a == REVERSE :
            self.field[x][y]=-1
            self.body=self.body[::-1]
            x,y=self.body[0]
            i,j=self.body[1]
            self.cdir=dir(x,y,i,j)
            self.field[x][y]=-3
        return False
        
def drawtext():    
    for i in range(len(Rules)):
        screen.blit(textRules[i], (0, 15*i))
    screen.blit(textScore, (display_width-100, 5))
    screen.blit(fontPause.render(str(snake.score),1,colorText),(display_width-90, 20))
    screen.blit(textSpeed, (display_width-100, display_height-65))
    screen.blit(fontPause.render(str(speedlevel),1,colorText),(display_width-90, display_height-50))
    if pause: 
        screen.blit(textPause, (display_width/2-100,display_height/2))    
    if lose:
        screen.blit(textGO, (display_width/2-100,display_height/2-40))       
    
           
snake = Snake(s,s,2,1)
snake.initfield(s)
snake.crawl()
snake.setobj(1,APPLE)

while True: # Game loop
    if not pause and not lose: lose = snake.crawl()
    snake.drawfield()
    drawtext()
    pygame.display.update()
    pygame.time.wait(int(1.25**(ZEROSPEED-speedlevel))) 
    for event in pygame.event.get():
        if event.type == QUIT :
            pygame.quit()
            quit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE : 
                pygame.quit()
                quit()
            if event.key==K_p : 
                pause= not pause
            if event.key==K_r : 
                lose= not lose
            if event.key in [K_q,K_a,K_e,K_d]:
                snake.cdir-={K_q:-1,K_a:-2,K_e:1,K_d:2}[event.key]
                snake.cdir%=6
            if event.key in [K_w,K_s]:
                speedlevel +={K_w:1,K_s:-1}[event.key]
                if speedlevel<1:
                    speedlevel=1
                    pause= not pause

