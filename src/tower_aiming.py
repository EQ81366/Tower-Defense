import math

# finds the angle from an object towards the mouse
# will be replaced/copied and modified to make towers point towards enemies
def point_mouse(x : int, y : int, mouse_xy : list[int]):
    #mouse_xy = pygame.mouse.get_pos()
    if mouse_xy[0]-x == 0:
        direction = -90-math.degrees(math.atan((mouse_xy[1]-y)))
    else:
        if mouse_xy[0] < x:
            direction = 90-(math.atan((mouse_xy[1]-y)/(mouse_xy[0]-x)))*(180/math.pi)
        else:
            direction = -90-(math.atan((mouse_xy[1]-y)/(mouse_xy[0]-x)))*(180/math.pi)

    return direction

def point_enemy(x: int, y: int, x2: int, y2: int):
    # Compute horizontal and vertical differences
    dx = x2 - x
    dy = y2 - y

    # Special case: dx == 0 would cause division by zero in atan(dy/dx)
    if dx == 0:
        return -90 - math.degrees(math.atan(dy))

    # Compute the base angle using dy/dx
    angle = math.degrees(math.atan(dy / dx))

    # If the target is to the LEFT (dx < 0)
    if dx < 0:
        return 90 - angle

    # If the target is to the RIGHT (dx > 0)
    return -90 - angle