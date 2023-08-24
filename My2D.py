##
# 2D Transformation helper methods
##

import math

ROT = [[math.cos, lambda theta: -1*math.sin(theta)], [math.sin, math.cos]]
def rotatePoint(p, theta):
    return [ ROT[0][0](theta)*p[0] + ROT[0][1](theta)*p[1],
             ROT[1][0](theta)*p[0] + ROT[1][1](theta)*p[1] ]

def rotatePoly(polygon, theta):
    for i in range(0, len(polygon), 2):
        polygon[i:i+2] = rotatePoint([polygon[i], polygon[i+1]], theta)

def movePoly(polygon, dx, dy):
    polygon[0::2] = [ x+dx for x in polygon[0::2] ]
    polygon[1::2] = [ y+dy for y in polygon[1::2] ]

def degToRad(deg):
    return deg*math.pi/180
