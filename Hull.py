#  File: Hull.py

#  Description:

#  Student Name: Jeremy Ulfohn

#  Student UT EID: jau392

#  Partner Name: Courtney Poche

#  Partner UT EID: cnp846

#  Course Name: CS 313E

#  Unique Number: 52240

#  Date Created: 21 Feb 2021

#  Date Last Modified: 25 Feb 2021

import sys
import math


class Point(object):
    # constructor
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    # get the distance to another Point object
    def dist(self, other):
        return math.hypot(self.x - other.x, self.y - other.y)

    # string representation of a Point
    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'

    # equality tests of two Points
    def __eq__(self, other):
        tol = 1.0e-8
        return ((abs(self.x - other.x) < tol) and (abs(self.y - other.y) < tol))

    def __ne__(self, other):
        tol = 1.0e-8
        return ((abs(self.x - other.x) >= tol) or (abs(self.y - other.y) >= tol))

    def __lt__(self, other):
        tol = 1.0e-8
        if (abs(self.x - other.x) < tol):
            if (abs(self.y - other.y) < tol):
                return False
            else:
                return (self.y < other.y)
        return (self.x < other.x)

    def __le__(self, other):
        tol = 1.0e-8
        if (abs(self.x - other.x) < tol):
            if (abs(self.y - other.y) < tol):
                return True
            else:
                return (self.y <= other.y)
        return (self.x <= other.x)

    def __gt__(self, other):
        tol = 1.0e-8
        if (abs(self.x - other.x) < tol):
            if (abs(self.y - other.y) < tol):
                return False
            else:
                return (self.y > other.y)
        return (self.x > other.x)

    def __ge__(self, other):
        tol = 1.0e-8
        if (abs(self.x - other.x) < tol):
            if (abs(self.y - other.y) < tol):
                return True
            else:
                return (self.y >= other.y)
        return (self.x >= other.x)


# Input: p, q, r are Point objects
# Output: compute the determinant and return the value
# Since points only have (x, y), the last column is all 1's
def det(p, r, q):
    return (q.x * r.y - q.y * r.x) - p.x * (r.y - q.y) + p.y * (r.x - q.x)


# Input: sorted_points is a sorted list of Point objects
# Output: computes the convex hull of a sorted list of Point objects
#         convex hull is a list of Point objects starting at the
#         extreme left point and going clockwise in order
#         returns the convex hull
def convex_hull(sorted_points):
    upper_hull = []
    # Append first 2 points to upper_hull
    for p in range(2):
        upper_hull.append(sorted_points[p])
    # Changed: list starts at p3, which is points[2] in python!
    for p in range(2, len(sorted_points)):
        # Append list[p] to upper_hull
        upper_hull.append(sorted_points[p])
        # Determinant notes:
        #   if determinant of r is zero, 3 points are in a straight line
        #   (+) is LEFT side of line / CCW torque
        #   (-) is RIGHT side of line / CW torque
        # While last 3 do NOT make a right turn (i.e. det not negative)...
        while len(upper_hull) >= 3 and det(upper_hull[-1], upper_hull[-2], upper_hull[-3]) >= 0:
            del upper_hull[-2]

    # Create lower_hull to store lower_hull vertices, starting with LAST two
    lower_hull = []
    for p in range(1, 3):
        lower_hull.append(sorted_points[-p])
    for p in range(3, len(sorted_points) + 1):
        lower_hull.append(sorted_points[-p])
        # While last 3 in *lower* do NOT make a right turn...
        while len(lower_hull) >= 3 and det(lower_hull[-1], lower_hull[-2], lower_hull[-3]) >= 0:
            del lower_hull[-2]
    # Remove the first and last points in lower_hull to avoid дупликацию с верхным
    lower_hull = lower_hull[1:-1]
    # This is now the full convex hull:
    return upper_hull + lower_hull



# Input: convex_poly is  a list of Point objects that define the
#        vertices of a convex polygon in order
# Output: computes and returns the area of a convex polygon
def area_poly(convex_poly):
    # Vertices given by p1, p2, ..., pn
    # Initialize x, y, and area
    x = []
    y = []
    n = len(convex_poly)
    area = 0.0
    for p in convex_poly:
        x.append(p.x)
        y.append(p.y)
    j = n - 1
    for i in range(n):
        area += (x[j] + x[i]) * (y[j] - y[i])
        # j is the previous vertex to i, with j=i we can finish the formula
        # in a single loop
        j = i
    return abs(area / 2.0)


# Input: no input
# Output: a string denoting all test cases have passed
def test_cases():
    # write your own test cases
    p = Point(0, 0)
    q = Point(0, 3)
    r = Point(3, 3)
    sl = [p, q, r]
    print(area_poly(sl))
    assert area_poly(sl) == 4.5

    return "all test cases passed"


def main():
    # create an empty list of Point objects
    points_list = []

    # read number of points
    line = sys.stdin.readline()
    line = line.strip()
    num_points = int(line)

    # read data from standard input
    for i in range(num_points):
        line = sys.stdin.readline()
        line = line.strip()
        line = line.split()
        x = int(line[0])
        y = int(line[1])
        points_list.append(Point(x, y))

    # sort the list according to x-coordinates
    sorted_points = sorted(points_list)
    '''
    FIXME:
    # print the sorted list of Point objects
    for p in sorted_points:
      print (str(p)) ^^
    '''
    # get the convex hull
    hull = convex_hull(sorted_points)
    # run your test cases

    # print your results to standard output
    # This means simply print? Since it goes to stdout by default in Python 3?



    # print the convex hull
    print("Convex Hull")
    for p in hull:
        print(p)
    print()

    # get the area of the convex hull
    area = area_poly(hull)
    # print the area of the convex hull
    print('Area of Convex Hull = {0:0.1f}'.format(area))


if __name__ == "__main__":
    main()
