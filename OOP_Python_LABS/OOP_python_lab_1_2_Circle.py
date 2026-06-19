import turtle
import math
import asyncio

screen = turtle.Screen()
screen.title("Move of circles in gravity tension")
screen.setup(width=800, height=600)
bg_color = "green"
screen.bgcolor(bg_color)
screen.tracer(0)

axes_t = turtle.Turtle()
axes_t.hideturtle()
axes_t.speed(0)
axes_t.width(1)

t = turtle.Turtle()
t.speed(0)
t.width(2)
t.hideturtle()

class Circle():
    __moving = False

    def __init__(self, coord_tuple: tuple[float|int, float|int], radius: float|int, our_color:str):
        self.set_params(coord_tuple, radius, our_color)

    def set_params(self, coord_tuple: tuple[float|int, float|int], radius: float|int, our_color:str):
        if Circle.isvalid(coord_tuple, radius, our_color):
            self.x, self.y = coord_tuple
            self.radius = radius
            self.our_color = our_color

            self.t = turtle.Turtle()
            self.t.speed(0)
            self.t.width(2)
            self.t.hideturtle()
    
    def get_params(self):
        return self.x, self.y, self.radius, self.our_color
        

    @staticmethod
    def isvalid(coord_tuple: tuple[float|int, float|int], radius: float|int, our_color:str):
        try:
            valid_1 = all(isinstance(elem, (int,float)) for elem in coord_tuple)
            valid_2 = isinstance(radius, (int,float)) and radius > 0
            valid_3 = False
            try:
                t.pencolor(our_color)
            except turtle.TurtleGraphicsError:
                print(f"Error: Color {our_color} is not valid")
            else:
                valid_3 = True
        except Exception as e:
            print(f"Validation error: {e}")

        return valid_1 and valid_2 and valid_3
        
    def __draw(self, color=None):
        draw_color = color if color else self.our_color
        self.t.color(draw_color)
        self.t.penup()
        self.t.goto(self.x,self.y - self.radius)
        self.t.pendown()
        self.t.begin_fill()
        self.t.circle(self.radius)
        self.t.end_fill()
    
    def __erase(self):
        self.t.clear()
    
    def __move_up(self, pixel_amount: int):
            self.y += pixel_amount
    
    def __move_down(self, pixel_amount: int):
            self.y -= pixel_amount
    
    def __move_right(self, pixel_amount: int):
            self.x += pixel_amount
    
    def __move_left(self, pixel_amount: int):
            self.x -= pixel_amount
    
    @staticmethod
    def draw_axes():
        Circle.__moving = True
        
        axes_t.color("black")
        axes_t.penup()
        axes_t.goto(-350, 0)
        axes_t.pendown()
        axes_t.goto(350, 0)
        axes_t.write("X", font=("Arial", 12, "bold"))

        axes_t.penup()
        axes_t.goto(0,-250)
        axes_t.pendown()
        axes_t.goto(0,250)
        axes_t.write("Y", font=("Arial", 12, "bold"))

        for x in range(-300, 301, 20):
                if x == 0: continue
                
                axes_t.penup()
                axes_t.goto(x, -5)
                axes_t.pendown()
                axes_t.goto(x, 5)

                axes_t.penup()
                axes_t.goto(x, -20)
                axes_t.write(x, align="center", font=("Arial", 8, "normal"))

        for y in range(-200, 201, 20):
                if y == 0: continue
                
                axes_t.penup()
                axes_t.goto(-5, y)
                axes_t.pendown()
                axes_t.goto(5, y)

                axes_t.penup()
                axes_t.goto(-20, y)
                axes_t.write(y, align="right", font=("Arial", 8, "normal"))
            
                axes_t.goto(-10, -20)
                axes_t.write("0", align="center")
        
        axes_t.color("red")
        axes_t.penup()
        axes_t.goto(-400,-215)
        axes_t.pendown()
        axes_t.goto(400,-215)
        axes_t.penup()
        axes_t.goto(300,-200)
        axes_t.pendown()
        axes_t.write("Ground", font=("Arial", 15, "normal"))
        
        screen.update()

    async def move_in_gravity_field(self, height: int, angle: int, speed: int, gravity_tension: float):
        if not Circle.__moving:
            self.draw_axes()
            Circle.__moving = True

        angle_rad = math.radians(angle)
        g = gravity_tension
        dt = 0.05
        self.__erase()
        self.y = height

        v_x = speed * math.cos(angle_rad)
        v_y = speed * math.sin(angle_rad)

        running = True
        while running:
            self.__erase()

            dx = v_x * dt
            dy = v_y * dt

            steps_x = abs(dx)
            if dx > 0:
                self.__move_right(steps_x)
            elif dx < 0:
                self.__move_left(steps_x)

            if dy > 0:
                self.__move_up(abs(dy))
            else:
                self.__move_down(abs(dy))
            
            self.__draw()
            screen.update()

            v_y -= (g * dt)

            if self.y < -200:
                running = False
            
            await asyncio.sleep(0.01)

async def main():
    A = Circle((-123,200), 10, "yellow")
    B = Circle((-234,132), 10, "purple")
    C = Circle((-150,230), 10, "blue")
    await asyncio.gather(
    A.move_in_gravity_field(height=200, angle=260, speed=40, gravity_tension=9.8),
    B.move_in_gravity_field(height=250, angle=60, speed=35, gravity_tension=9.8),
    C.move_in_gravity_field(height=150, angle=70, speed=30, gravity_tension=9.8) )

    Circle.__moving = False
    turtle.done()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except turtle.Terminator():
        #без помилки при закритті вікна
        pass