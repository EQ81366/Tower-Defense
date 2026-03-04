import math

# finds the angle from an object towards the mouse
# will be replaced/copied and modified to make towers point towards enemies
def point_mouse(x : int, y : int, mouse_xy : list[int]):
    if mouse_xy[0]-x == 0:
        return -90-math.degrees(math.atan((mouse_xy[1]-y)))
    elif mouse_xy[0] < x:
        return 90-(math.atan((mouse_xy[1]-y)/(mouse_xy[0]-x)))*(180/math.pi)
    else:
        return -90-(math.atan((mouse_xy[1]-y)/(mouse_xy[0]-x)))*(180/math.pi)

# finds the angle between 2 objects
def point_enemy(x : int, y : int, x2 : int, y2 : int):
    # x2-x == 0 makes sure it doesn't try to divide by 0
    if x2-x == 0:
        return -90-math.degrees(math.atan((y2-y)))
    elif x2 < x:
        return 90-(math.atan((y2-y)/(x2-x)))*(180/math.pi)
    else:
        return -90-(math.atan((y2-y)/(x2-x)))*(180/math.pi)