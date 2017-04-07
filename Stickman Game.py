from tkinter import *
import random
import time

class Game:
    def __init__(self):
        self.tk=Tk()
        self.tk.title("Quas Wex EXORT")
        self.tk.resizable(0,0)
        self.tk.wm_attributes("-topmost", 1)
        self.canvas=Canvas(self.tk,width=1000,height=800,\
                           highlightthickness=0)
        self.canvas.pack()
        self.tk.update()
        self.canvas_height=800
        self.canvas_width=1000
        
        self.bg=PhotoImage(file="Graphics\\Background.gif")
        w=self.bg.width()
        h=self.bg.height()
        for x in range(0,5):
            for y in range(0,5):
                self.canvas.create_image(x*w,y*h,\
                                         image=self.bg,anchor='nw')
        self.sprites=[]
        self.running=True
        lines=["There, get youself a botox.", "At this rate, I'll open my own bank.", "Fonstinator takes round 1."]
        random.shuffle(lines)
        self.game_over_text = self.canvas.create_text(500, 250,text=lines[0],font=("Times",40),fill="red", state='hidden')
        
    def mainloop(self):
        while 1:
            if self.running==True:
                for sprite in self.sprites:
                    sprite.move()
            else:
                time.sleep(1)
                self.canvas.itemconfig(self.game_over_text, state='normal')
            self.tk.update_idletasks()
            self.tk.update()
            time.sleep(0.01)
class Coords:
    def __init__(self, x1=0, y1=0, x2=0, y2=0):
        
        self.x1=x1
        self.y1=y1
        self.x2=x2
        self.y2=y2

def within_x(co1, co2):
    if (co1.x1 > co2.x1 and co1.x1 < co2.x2)\
       or (co1.x2 > co2.x1 and co1.x2 < co2.x2)\
       or (co2.x1 > co1.x1 and co2.x1 < co1.x2)\
       or (co2.x2 > co1.x1 and co2.x2 < co1.x2):
        return True
    else:
        return False

def within_y(co1, co2):
    if (co1.y1 > co2.y1 and co1.y1 < co2.y2)\
       or (co1.y2 > co2.y1 and co1.y2 < co2.y2)\
       or (co2.y1 > co1.y1 and co2.y1 < co1.y2)\
       or (co2.y2 > co1.y1 and co2.y2 < co1.y2):
        return True
    else:
        return False

def collided_left(co1,co2):
    if within_y(co1,co2):
        if co1.x1 <= co2.x2 and co1.x1 >= co2.x1:
            return True
    return False

def collided_right(co1,co2):
    if within_y(co1,co2):
        if co1.x2 >= co2.x1 and co1.x2 <= co2.x2:
            return True
    return False

def collided_top(co1,co2):
    if within_x(co1,co2):
        if co1.y1 <= co2.y2 and co1.y1 >= co2.y1:
            return True
    return False

def collided_bottom(y,co1,co2):
    if within_x(co1,co2):
        y_calc=co1.y2+y
        if y_calc >= co2.y1 and y_calc <= co2.y2:
            return True
    return False

class Sprite:
    def __init__(self,game):
        self.game=game
        self.endgame=False
        self.coordinates=None
    def move(self):
        pass
    def coords(self):
        return self.coordinates

class PlatformSprite(Sprite):
    def __init__(self,game,photo_image,x,y,width,height):
        Sprite.__init__(self,game)
        self.photo_image=photo_image
        self.image=game.canvas.create_image(x,y, \
                                            image=self.photo_image,anchor='nw')
        self.coordinates=Coords(x,y,x+width,y+height)
        
class DoorSprite(Sprite):
    def __init__(self,game,x,y,width,height):
        Sprite.__init__(self,game)
        self.open_door=PhotoImage(file="Graphics\\Door-2.gif")
        self.closed_door=PhotoImage(file="Graphics\\Door-1.gif")
        self.image=game.canvas.create_image(x,y,\
                                            image=self.closed_door, anchor='nw')
        self.coordinates=Coords(x,y,x+(width/2),y+height)
        self.endgame=True
    def weldDoor(self):
        self.game.canvas.itemconfig(self.image, image=self.closed_door)
        self.game.tk.update_idletasks()
    def bustDoor(self):
        self.game.canvas.itemconfig(self.image, image=self.open_door)
        self.game.tk.update_idletasks()

class StickFigureSprite(Sprite):
    def __init__(self,game):
        Sprite.__init__(self,game)
        self.images_left=[
            PhotoImage(file="Graphics\\Figure-L1.gif"),
            PhotoImage(file="Graphics\\Figure-L2.gif"),
            PhotoImage(file="Graphics\\Figure-L3.gif")
        ]
        self.images_right=[
            PhotoImage(file="Graphics\\Figure-R1.gif"),
            PhotoImage(file="Graphics\\Figure-R2.gif"),
            PhotoImage(file="Graphics\\Figure-R3.gif")
        ]
        self.image=game.canvas.create_image(200,470, \
                                            image=self.images_left[0],anchor='nw')
        self.x=-2
        self.y=0
        self.current_image=0
        self.current_image_add=1
        self.jump_count=0
        self.last_time=time.time()
        self.coordinates=Coords()
        game.canvas.bind_all("<KeyPress-Left>", self.turn_left)
        game.canvas.bind_all("<KeyPress-Right>", self.turn_right)
        game.canvas.bind_all("<space>", self.jump)
    def turn_left(self,evt):
        if self.y == 0:
            self.x = -2
    def turn_right(self,evt):
        if self.y == 0:
            self.x = 2
    def jump(self,evt):
        if self.y==0:
            self.y=-10
            self.jump_count=0
    def animate(self):
        if self.x != 0 and self.y == 0:
            if time.time()-self.last_time > 0.1:
                self.last_time=time.time()
                self.current_image+=self.current_image_add
                if self.current_image >= 2:
                    self.current_image_add=-1
                if self.current_image <=0:
                    self.current_image_add=1
        if self.x<0:
            if self.y!=0:
                self.game.canvas.itemconfig(self.image,\
                                            image=self.images_left[2])
            else:
                self.game.canvas.itemconfig(self.image,\
                                            image=self.images_left[self.current_image])
        elif self.x>0:
            if self.y!=0:
                self.game.canvas.itemconfig(self.image,\
                                            image=self.images_right[2])
            else:
                self.game.canvas.itemconfig(self.image,\
                                            image=self.images_right[self.current_image])
    def coords(self):
        xy=self.game.canvas.coords(self.image)
        self.coordinates.x1=xy[0]
        self.coordinates.y1=xy[1]
        self.coordinates.x2=xy[0]+75
        self.coordinates.y2=xy[1]+138
        return self.coordinates

    def move(self):
        self.animate()
        if self.y<0:
            self.jump_count+=1
            if self.jump_count > 20:
                self.y=4
        if self.y>0:
            self.jump_count-=1
        co=self.coords()
        left=True
        right=True
        top=True
        bottom=True
        falling=True
        if self.y > 0 and co.y2 >= self.game.canvas_height:
            self.y=0
            bottom=False
        elif self.y < 0 and co.y1 <= 0:
            self.y=0
            top=False
        if self.x > 0 and co.x2 >= self.game.canvas_width:
            self.x = 0
            right=False
        elif self.x < 0 and co.x1 <=0:
            self.x=0
            left=False
        for sprite in self.game.sprites:
            if sprite == self:
                continue
            sprite_co=sprite.coords()
            if top and self.y <0 and collided_top(co,sprite_co):
                self.y=-self.y
                top=False
            if bottom and self.y > 0 and collided_bottom(self.y,\
                                                         co,sprite_co):
                self.y=sprite_co.y1-co.y2
                if self.y<0:
                    self.y=0
                bottom=False
                top=False
            if bottom and falling and self.y==0\
               and co.y2<self.game.canvas_height\
               and collided_bottom(1,co,sprite_co):
                falling=False
            if left and self.x < 0 and collided_left(co,sprite_co):
                self.x=0
                left=False
                if sprite.endgame:
                    if hasWelder == True:
                        self.end(sprite)
            if right and self.x > 0 and collided_right(co,sprite_co):
                self.x=0
                right=False
                if sprite.endgame:
                    self.end(sprite)
        if falling and bottom and self.y == 0\
           and co.y2 < self.game.canvas_height:
            self.y=4
        self.game.canvas.move(self.image,self.x,self.y)
    def end(self, sprite):
        self.game.running=False
        sprite.bustDoor()
        time.sleep(1)
        self.game.canvas.itemconfig(self.image, state='hidden')
        sprite.weldDoor()

g=Game()
platform1=PlatformSprite(g,PhotoImage(file="Graphics\\Platform-1.gif"),\
                         300,680,250,30)
platform2=PlatformSprite(g,PhotoImage(file="Graphics\\Platform-3.gif"),\
                         270,500,83,30)
platform3=PlatformSprite(g,PhotoImage(file="Graphics\\Platform-3.gif"),\
                         230,400,83,30)
platform4=PlatformSprite(g,PhotoImage(file="Graphics\\Platform-3.gif"),\
                         450,380,83,30)
platform5=PlatformSprite(g,PhotoImage(file="Graphics\\Platform-3.gif"),\
                         680,270,83,30)
platform6=PlatformSprite(g,PhotoImage(file="Graphics\\Platform-2.gif"),\
                        300,160,165,30)
platform7=PlatformSprite(g,PhotoImage(file="Graphics\\Platform-2.gif"),\
                        40,300,165,30)
welder=PlatformSprite(g,PhotoImage(file="Graphics\\Welder.gif"),\
                        680,235,58,40)
hasWelder = False

g.sprites.append(platform1)
g.sprites.append(platform2)
g.sprites.append(platform3)
g.sprites.append(platform4)
g.sprites.append(platform5)
g.sprites.append(platform6)
g.sprites.append(platform7)
g.sprites.append(welder)

door=DoorSprite(g,302,8,160,155)
g.sprites.append(door)
sf=StickFigureSprite(g)
g.sprites.append(sf)
g.mainloop()
