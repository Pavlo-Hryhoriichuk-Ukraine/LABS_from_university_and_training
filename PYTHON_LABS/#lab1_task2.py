#lab1_task2 (тіло, кинуте під кутом до горизонту)

import math

g = 10
t = int(input('Input time moment: '))
h0 = int(input('Input beginning height: '))
v0 = int(input('Input beginning speed: '))
a = int(input('Input beginning angle: '))

v_x_t = v0 * math.cos(a)
x_t_ = v_x_t * t
T = (v0 * math.sin(a)) / g
v_y_t = (v0 * math.sin(a)) - (g * t)
y_t_ = (v_y_t * t) + h0
if t > T:
    y_t_ = 0
h_max = (((v0 ** 2)  *  (math.sin(a) ** 2)) / (2 * g)) + h0
v_t_= ((v_x_t ** 2) + (v_y_t ** 2)) ** 0.5
l_max = v_x_t * T

print(f"Coordinates of the body at the moment {t} are {round(x_t_, 3)} and {round(y_t_, 3)}")
print(f"The speed of the body at the time moment {t} is {round(v_t_, 3)}")
print(f'The maximum height is {round(h_max, 3)}')
print(f'The maximum lenght is {round(l_max, 3)}')