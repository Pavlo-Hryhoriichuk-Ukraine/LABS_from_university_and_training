#lab2_task1 (чи належить точка фігурі)

while True:
    x = int(input("Input (x) coordinate of the point: "))
    y = int(input("Input (y) coordinate of the point: "))

    y_1_sec1_max = 5/2 * (x - 4)
    y_2_sec1_max = (2/6 * x) + 3

    sector1 = x >= 0 and y >= 0 and y_1_sec1_max < y and y_2_sec1_max > y
    sector2 = x <= 0 and y >= 0 and (x**2) + (y**2) <= 9
    sector3 = x <= 0 and y <= 0 and ((x**2) + (y**2) <= 5)
    sector4 = x >= 0 and y <= 0 and (x**2) + (y**2) <= 16

    if sector1 or sector2 or sector3 or sector4  == True:
        print ("The point is in the figure!")
    else:
        print('The point is not in the figure!')