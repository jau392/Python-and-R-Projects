#  File: CubeRoot.py

#  Description:

#  Student Name: Jeremy Ulfohn

#  Student UT EID: jau392

#  Course Name: CS 313E

#  Unique Number: 52240

#  Date Created: 3 March 2021

import sys

#   Input: n is a floating point number
#   Output: returns the cube root of n for a given tolerance

# Returns !absolute value! of |n - mid|
def diff(n, mid) :
    if (n > (mid * mid * mid)) :
        return (n - (mid * mid * mid))
    else :
        return ((mid * mid * mid) - n)

def cube_root(n):
    start = 0.0
    orig_n = abs(n)
    end = abs(n)
    e = 10 ** (-6)
    # Not found if low exceeds high
    while True:
        mid = (start + end) / 2
        error = diff(orig_n, mid)

        if error <= e:
            if n < 0:
                mid *= (-1)
            return mid
        if mid ** 3 > orig_n:
            end = mid
        else: # If n is GrEqual to mid^3
            start = mid


def main():
    #  read n
    line = sys.stdin.readline()
    line = line.strip()
    n = float(line)

    # compute the cube root of n and print result
    print(cube_root(n))

if __name__ == "__main__":
    main()
