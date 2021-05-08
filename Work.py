
#  File: Work.py

#  Description: Finds the minimum v such that n lines of code will still be written, via linear and bin
#  search.

#  Student Name: Jeremy Ulfohn

#  Student UT EID: jau392

#  Course Name: CS 313E

#  Unique Number: 52240

#  Date Created: 22 Feb 2021

#  Date Last Modified:

import sys

import time

# Input: v an integer representing the minimum lines of code and
#        k an integer representing the productivity factor
# Output: computes the sum of the series (v + v // k + v // k**2 + ...)
#         returns the sum of the series
# Purpose: helper function for how many lines are written before sleep
def sum_series(v, k):
    answer = 0
    p = 0
    # Find the correct p to use
    while (v // k ** p) > 0:
        answer += (v // k ** p)
        p += 1
    # He writes his last line of code at p-1, right before passing out
    return answer


# Input: n an integer representing the total number of lines of code
#        k an integer representing the productivity factor
# Output: returns v the minimum lines of code to write using linear search
def linear_search(n, k):
    v = 0
    while sum_series(v, k) < n:
        v += 1
    return v


# Input: n an integer representing the total number of lines of code
#        k an integer representing the productivity factor
# Output: returns v the minimum lines of code to write using binary search
def binary_search(n, k):
    # Establish parameters for recursive binary search
    # The "x" is the v for which sum_list first >= n
    low = 0
    high = n
    # Check base case
    while low <= high:
        mid = (high + low) // 2
        # If [mid - 1] > n, min can only be located in the left half
        if sum_series(mid, k) < n:
            low = mid + 1
        # Vice-versa:
        elif sum_series(mid - 1, k) >= n:
            high = mid - 1
        else:
            return mid
    # If no such mid exists (this shouldn't be possible):
    return -1


# Input: no input
# Output: a string denoting all test cases have passed
def test_cases():
    # write your own test cases
    assert linear_search(300, 2) == 152
    # assert binary_search(300, 2) == 152
    assert linear_search(59, 9) == 54
    assert binary_search(59, 9) == 54

    return "all test cases passed"


def main():
    print(test_cases())
    # read number of cases
    line = sys.stdin.readline()
    line = line.strip()
    num_cases = int(line)

    for i in range (num_cases):
        line = sys.stdin.readline()
        line = line.strip()
        inp = line.split()
        n = int(inp[0])
        k = int(inp[1])

        start = time.time()
        print("Binary Search: " + str(binary_search(n, k)))
        finish = time.time()
        print("Time: " + str(finish - start))

        print()

        start = time.time()
        print("Linear Search: " + str(linear_search(n, k)))
        finish = time.time()
        print("Time: " + str(finish - start))

        print()
        print()

if __name__ == "__main__":
    main()
