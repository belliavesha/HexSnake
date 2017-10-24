from time import sleep
from random import random as rnd
from numpy import zeros
import pygame 
from pygame.locals import *
pygame.init()
display_width,display_height=800,680
# screen = pygame.display.set_mode((display_width, display_height))
# pygame.display.set_caption('NoGame')
ZEROSPEED=35
speedlevel=ZEROSPEED

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
    WHITE=(255,255,255)
    BLACK=(0,0,0)
    colorSnake=(2,250,200)
    colorGrass=(0,100,20)
    colorBorder=(250,120,0)
    colorApple=(250,0,0)
    colorMouth=(250,200,200)
    colorBonus=(40,0,240)
    colorText=(240,240,10)

class Element:
    state=0
    def show(self):
        pass
    def handle(self,event):
        pass
    def move(self):
        pass

class Content(Element): 
    def __init__(self,elements,handler=lambda event,list: None):
        self.handler = handler
        self.elements= elements
        

    def show(self):
        for element in self.elements:
            element.show()
    
    def handle(self, event):
        for element in self.elements:
            element.handle(event)
        return self.handler(event,self.elements)

    def move(self):
        for element in self.elements:
            element.move()
    


class Screen(Element):
    def __init__(self,name,size=(600,600),background=BLACK):
        self.display_width=size[0] 
        self.display_height=size[1]
        self.size=size
        self.background=background
        self.display=pygame.display.set_mode(size)
        pygame.display.set_caption(name)
        self.content=Content([])
        self.speedlevel=ZEROSPEED

    def fill(self,content):
        self.content=content
    
    def show(self):
        self.display.fill(self.background)
        self.content.show()
        pygame.display.update()

    def handle(self,event):
        if event.type == QUIT : close()
        self.content.handle(event)
    
    def move(self):
        self.content.move()
        pygame.time.wait(int(1.25**(ZEROSPEED-self.speedlevel))) 
        
screen=Screen('NoGame',(display_width,display_height))

class TextBox(Element):
    """TextBox"""
    def __init__(self,center,font,text,color=WHITE):
        self.text = text
        self.font = font
        self.color = color
        self.center=center
        self.surface = font.render(text, 1, color)
        rect = self.surface.get_rect()
        rect.center=center
        self.rect=rect

    def show(self):
        self.surface = self.font.render(self.text, 1, self.color)
        rect = self.surface.get_rect()
        rect.center=self.center
        self.rect=rect
        screen.display.blit(self.surface, self.rect)   
    
class Button(TextBox):

    showTextBox=TextBox.show
    def __init__(self,action,center,font,text,color=WHITE,K_BUTTON=None):
        TextBox.__init__(self,center,font,text,color)
        self.center=center
        self.action=action
        self.K_BUTTON=K_BUTTON

    def show(self):
        self.showTextBox()
        if self.state : 
            pygame.draw.polygon(screen.display, self.color, [
                self.rect.topleft,
                (self.rect.left-self.rect.height/2,self.rect.centery),
                self.rect.bottomleft], 0)
            pygame.draw.polygon(screen.display, self.color, [
                self.rect.topright,
                (self.rect.right+self.rect.height/2,self.rect.centery),
                self.rect.bottomright], 0)

    def handle(self, event):
        if event.type==MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.state=True
            else:
                self.state=False
        if event.type==MOUSEBUTTONDOWN:
            if event.button == 1 and self.state:
                self.action()
        if event.type==KEYDOWN:
            if (event.key == K_RETURN and self.state) or (event.key == self.K_BUTTON):
                self.action()

class Parameter:
    def __init__(self,name,span=['OFF','ON'],cur=0):
        self.name=name
        self.span=span
        self.cur=cur
        self.last=len(span)-1
        self.value=span[self.cur]

    def next(self):
        self.cur=min(self.cur+1,self.last)
        self.value=self.span[self.cur]

    def prev(self):
        self.cur=max(self.cur-1,0)
        self.value=self.span[self.cur]
    def __str__(self):
        return str(self.value)

class Option(Button):
    handleButton=Button.handle
    def __init__(self,parameter,center,font,color=WHITE):
        self.parameter=parameter
        Button.__init__(self,self.parameter.next,center,font,str(self),color)

    def handle(self, event):
        self.handleButton(event)
        if self.state:
            self.text=str(self)
        if event.type==KEYDOWN:
            if event.key == K_LEFT and self.state:
                self.parameter.prev()
                self.text=str(self)
            if event.key == K_RIGHT and self.state:
                self.parameter.next()
                self.text=str(self)
    def __str__(self):
        return self.parameter.name+": "+str(self.parameter.value)

sizeOption = 40
fontOption = pygame.font.SysFont("monospace",sizeOption)
fontBoxname = pygame.font.SysFont("monospace", 14)


size = Parameter('FIELD SIZE',range(3,41),12)
ticks = Parameter('BONUS RARENESS',range(3,16),7)
lethality=Parameter('BORDERS ARE LETHAL')
difficulty=Parameter('DIFFICULTY',['peaceful','easy','medium','hard','insane'])

def close():
    pygame.quit()
    quit()

def to_options():
    screen.fill(options)


def to_game():
    s=size.value-1
    screen.speedlevel=s
    snakes=[Snake((s,s))]
    snakes[0].setobj(1,APPLE)
    screen.fill(Content(snakes+
        [TextBox((30,10),fontBoxname,"Score: "),
        TextBox((display_width-30,10),fontBoxname,"Speed:")]))

def to_menu():
    screen.speedlevel=ZEROSPEED
    screen.fill(menu)

def vertical_list_handler(event,list):
    l=len(list)
    if event.type==KEYDOWN and l:
        d={K_DOWN:1,K_UP:-1}
        if event.key in d:
            for e in range(l):
                if list[e].state:
                    list[e].state=False
                    list[(e+d[event.key])%l].state=True
                    break 
            else:
                list[0].state=True

options=Content([Option(size,(display_width/2, display_height/2-sizeOption),fontOption),
    Option(lethality,(display_width/2, display_height/2),fontOption),
    Option(difficulty,(display_width/2, display_height/2+sizeOption),fontOption),
    Button(to_menu,(display_width/2, display_height/2+2*sizeOption),fontOption,"BACK",K_BUTTON=K_ESCAPE),
    ], vertical_list_handler)

menu=Content([Button(to_game,(display_width/2, display_height/2-sizeOption),fontOption,"PLAY"),
    Button(to_options,(display_width/2, display_height/2),fontOption,"OPTIONS"),
    Button(close,(display_width/2, display_height/2+sizeOption),fontOption,"QUIT",K_BUTTON=K_ESCAPE)
    ], vertical_list_handler)

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

class Snake(Element):
    def __init__(self,pos,sc=2,d=0):
        self.score=sc
        self.body=[pos]*sc
        self.cdir=d
        s=size.value
        n=2*s-1
        self.controls= dict(zip([K_q,K_a,K_w,K_s],[-1,-2,1,2]))
        self.field_size=s
        self.field_dimension=n
        self.field = zeros((n,n))
        self.difficulty=difficulty.value
        self.bonus_frequency=ticks.value
        self.display_width=screen.display_width
        self.display_height=screen.display_height
        self.display_width_step=screen.display_width/n
        self.display_height_step=screen.display_height/n
        self.loop={'OFF':True,"ON":False}[lethality.value]
        self.lost=False
        self.stopped = False
        self.bonuses = {'peaceful' : [EXTRAAPPLE,SHORTEN,REVERSE,EXTRASCORE],
                        'easy': [EXTRAAPPLE,SHORTEN,REVERSE,EXTRASCORE,EXTRABORDER,LENGTHEN,SHORTEN,EXTRAAPPLE],
                        'medium': [EXTRAAPPLE,SHORTEN,REVERSE,EXTRASCORE,EXTRABORDER,LENGTHEN,EXTRAKILLER],
                        'hard': [EXTRAAPPLE,SHORTEN,REVERSE,EXTRABORDER,LENGTHEN,EXTRAKILLER],
                        'insane': [EXTRAAPPLE,REVERSE,REVERSE,EXTRABORDER,LENGTHEN,EXTRAKILLER],
                        }[difficulty.value]
                        

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
        return (1+self.display_width/(4*n)+self.display_width/4
          +x*self.display_width/(n)-self.display_width*y/2/(n),
         1+self.display_height/(2*n)+y*self.display_height/(n))

    def next(self,x,y,d):
        rx, ry= further(x,y,d)
        if self.out(rx,ry):
            while (not self.out(x,y) ) :
                x,y= further(x,y,(d+3)%6)
            rx, ry= further(x,y,d)
            if not self.loop:
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
            if self.score%self.bonus_frequency==0 : self.setobj(1,BONUS) # balance?  
            if self.difficulty=='insane':
                if rnd()<.5: self.setobj(2,BORDER)
                if rnd()<.5: self.setobj(2,KILLER)
                if rnd()<.2: self.setobj(1,SHORTEN)
                if rnd()<.2: self.setobj(1,LENGTHEN)
        if a == BONUS :
            a=self.bonuses[int(len(self.bonuses)*rnd())]      
            if self.difficulty=='insane':
                if rnd()<.4: self.setobj(1,REVERSE)
                if rnd()<.3: self.setobj(3,EXTRASCORE)
        if a == EXTRAAPPLE :
            self.setobj(1,APPLE)
        if a == EXTRABORDER :
            self.setobj(1,BORDER if self.loop else KILLER)
        if a == EXTRASCORE :
            self.score+=self.bonus_frequency
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
    
    def drawsymbol(self,i,j):
        l=self.field[i][j]
        crds=self.display_crds(i,j)
        dw=self.display_width_step
        dh=self.display_height_step
        if l==TAIL:
            pygame.draw.circle(screen.display, colorSnake, crds, dh/2, 0)
        if l==BODY:
            pygame.draw.circle(screen.display, colorSnake, crds, dw/2, 0)
        if l==HEAD:
            x,y=further(i,j,self.cdir)
            x,y=self.display_crds(x,y)
            mcrds=((x+2*crds[0])/3,(y+2*crds[1])/3)
            pygame.draw.circle(screen.display, colorSnake, crds, dw/2, 0)
            pygame.draw.circle(screen.display, colorMouth, mcrds, dw/6, 0)
        if l==APPLE :
            pygame.draw.circle(screen.display, colorApple, crds, dh/2, 0)
        if l==EMPTY:
            return 
        if l==KILLER:
            cx,cy=crds
            pygame.draw.line(screen.display,colorBorder,(cx-dh/2,cy),(cx+dh/2,cy),2)
            pygame.draw.line(screen.display,colorBorder,(cx,cy-dh/2),(cx,cy+dh/2),2)
            pygame.draw.line(screen.display,colorBorder,(cx-dh/3,cy-dh/3),(cx+dh/3,cy+dh/3),2)
            pygame.draw.line(screen.display,colorBorder,(cx+dh/3,cy-dh/3),(cx-dh/3,cy+dh/3),2)
        if l==BORDER:
            pygame.draw.circle(screen.display, colorBorder, crds, dh/2, 0)
        if l==EXTRABORDER or l==EXTRAAPPLE :
            cx,cy=crds
            pygame.draw.line(screen.display,colorBonus,(cx-dh/2,cy),(cx+dh/2,cy),2)
            pygame.draw.line(screen.display,colorBonus,(cx,cy-dh/2),(cx,cy+dh/2),2)
        if l==SHORTEN or l==LENGTHEN :
            cx,cy=crds
            pygame.draw.line(screen.display,colorBonus,(cx-dh/2,cy),(cx+dh/2,cy),2)
            pygame.draw.line(screen.display,colorBonus,(cx,cy-dh/2),(cx,cy+dh/2),2)
            pygame.draw.line(screen.display,colorBonus,(cx-dh/3,cy-dh/3),(cx+dh/3,cy+dh/3),2)
            pygame.draw.line(screen.display,colorBonus,(cx+dh/3,cy-dh/3),(cx-dh/3,cy+dh/3),2)
        if l==REVERSE or l==EXTRAKILLER :
            cx,cy=crds
            pygame.draw.line(screen.display,colorBonus,(cx-dh/3,cy-dh/3),(cx+dh/3,cy+dh/3),2)
            pygame.draw.line(screen.display,colorBonus,(cx+dh/3,cy-dh/3),(cx-dh/3,cy+dh/3),2)
        if l==BONUS or l==EXTRASCORE:
            pygame.draw.circle(screen.display, colorBonus, crds, dh/2, 0)
        return 

    def show(self):
        n=self.field_dimension
        s=self.field_size
        ds=self.drawsymbol
        pygame.draw.polygon(screen.display, colorGrass, [
            (0,self.display_height/2),
            (self.display_width/4.,0),
            (self.display_width*3./4.,0),
            (self.display_width,self.display_height/2),
            (self.display_width*3./4.,self.display_height),
            (self.display_width/4.,self.display_height)], 0)
        for j in range(n): ds(s-1,j)
        for i in range(s-1): 
            for j in range(s+i): ds(i,j)
            for j in range(i+1,n): ds(i+s,j)


        textGO = fontOption.render("GAME OVER!", 1, colorText)
        textPause = fontOption.render("Paused...", 1, colorText)
        
        screen.display.blit(fontOption.render(str(self.score),1,colorText),(10, 20))
        screen.display.blit(fontOption.render(str(screen.speedlevel),1,colorText),(display_width-50, 20))
        if self.stopped: 
            screen.display.blit(textPause, (display_width/2-100,display_height/2))    
        if self.lost:
            screen.display.blit(textGO, (display_width/2-100,display_height/2-40))       
    

    def handle(self,event):    
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE : 
                to_menu()
            if event.key==K_p : 
                self.stopped= not self.stopped
            if event.key==K_r : 
                self.lost= not self.lost
            if event.key in self.controls.keys():
                self.cdir-=self.controls[event.key]
                self.cdir%=6
            if event.key in [K_UP,K_DOWN]:
                screen.speedlevel +={K_UP:1,K_DOWN:-1}[event.key]
                if screen.speedlevel<1:
                    screen.speedlevel=1
                    self.stopped= not self.stopped

    def move(self):
        if not self.stopped and not self.lost: self.lost = self.crawl()
        












screen.fill(menu)
print screen.content
while True: # Game loop
    screen.move()
    for event in pygame.event.get():
        screen.handle(event)
    screen.show()
        
       


