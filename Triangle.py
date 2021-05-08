#  File: Triangle.py

#  Description: Uses 4 different methods to optimize path down triangle.

#  Student Name: Jeremy Ulfohn

#  Student UT EID: jau392

#  Course Name: CS 313E

#  Unique Number: 52240

#  Date Created: 28 Mar 2021

#  Date Last Modified: 28 Mar 2021

import sys

from timeit import timeit


# returns the greatest path sum using exhaustive search
# Just like divide and conquer, this will be RECURSIVE
#   - store all path sums, then find the maximum thereof
def brute_force(grid):
    # Base case: if the length of grid is 1
    if len(grid) == 1:
        # Return the maximum of this final line
        result = max(grid[0])
        return result
    else:
        # Leftmost number in grid[1]
        grid[1][0] += grid[0][0]

        # Rightmost number in grid[1]
        grid[1][-1] += grid[0][-1]

        # Central numbers
        for item in grid[1][1:-1]:
            # Keep track of which index we're at
            i = grid[1].index(item)
            # Add the correct items from previous row
            grid[1][i] += max(grid[0][i - 1], grid[0][i])
        # Finally, remove grid[0] entirely
        grid.remove(grid[0])
        # Every "if" statement must return something, otherwise nothing
        # will actually return!
        return brute_force(grid)


# returns the greatest path sum using greedy approach
def greedy(grid):
    # Return the top of the triangle + the highest adjacent in
    # the next row, which greedy_helper finds for us
    return grid[0][0] + greedy_helper(grid, 1, 0) # First row plus next row (if it exists)

# i is the row we're on, j is the column
def greedy_helper(grid, i, j): # <=> (grid, row, column)
    # Set the base case at the bottom of the triangle
    if i >= len(grid):
        # Add nothing, since there's no next row
        return 0
    else: # If i < len(grid), then we add the larger of the two choices to the sum
    # greedy_helper in actuality returns the SUM of the larger of two options
        # Make one of the two choices moving down the triangle
        if grid[i][j] > grid[i][j + 1]: # If left > right
            return grid[i][j] + greedy_helper(grid, i + 1, j) # Return self + next largest, moving down
        else: # If right >= left
            # Here we move down a row and also right 1 column
            return grid[i][j + 1] + greedy_helper(grid, i + 1, j + 1)


# returns the greatest path sum using divide and conquer (recursive) approach
#   - only gets back a single number, which is the maximum
def divide_conquer(grid):
    # For each recursion, we will find the maximum of the two mini tri sums
    return max(mini_tri(grid, 0, 0, 0))


# Helper function for division into smaller triangles
# As with above, i = row & j = col
def mini_tri(grid, i, j, sum): # Returns a LIST of sums
    # Base case - we've gone through the whole grid, so return
    if i >= len(grid):
        return [sum] # Sum must be an ITERABLE for "max" to work on it
    # Recursive case
    else:
        if i == len(grid) - 1: # If we're at the last row
            # Sends mini_tri() to base case, where max will be found
            return mini_tri(grid, i + 1, j, sum + grid[i][j]) # We have no choice, this [i, j] is IT
        else:
            # If we're not at the final row, we will append two lists
            # of which the max will eventually be found
            # ** These represent the two triangles on which each coord
            # sits **
            return (mini_tri(grid, i + 1, j, sum + grid[i][j]) +
                    mini_tri(grid, i + 1, j + 1, sum + grid[i][j])) # Add the two possible sums to the
                    # LIST of sums, of which we will at final find the maximum. This "splits" and tabulates
                    # every choice of sum we make


# returns the greatest path sum and the new grid using dynamic programming
def dynamic_prog(grid):
    # Here, we will go bottom-up
    for i in range(len(grid) - 2, -1, -1): # From SECOND last to first ( [0] )
    # To go from penultimate to first, the "first" must be 0 - 1 == -1
    # Range must be from the i BEFORE the last, since we will add this to grid[0][0]
    #   in our return statement
        for j in range(i + 1): # We have the following options:
            #   (1) j == i - 1 (left)
            #   (2) j == i (right)
            # Case 1: Left is bigger
            if grid[i + 1][j] > grid[i + 1][j + 1]:
                grid[i][j] += grid[i + 1][j] # Store sum in bottom row
            # Case 2: Right is = or bigger
            else:
                grid[i][j] += grid[i + 1][j + 1]
    # Finally, return the top left element which contains the max sum
    # This is once we've iterated through the full grid
    return grid[0][0]


# reads the file and returns a 2-D list that represents the triangle
def read_file():
    # read number of lines
    line = sys.stdin.readline()
    line = line.strip()
    n = int(line)

    # create an empty grid with 0's
    grid = [[0 for i in range(n)] for j in range(n)]

    # read each line in the input file and add to the grid
    for i in range(n):
        line = sys.stdin.readline()
        line = line.strip()
        row = line.split()
        row = list(map(int, row))
        for j in range(len(row)):
            grid[i][j] = grid[i][j] + row[j]

    return grid


def main():
    # read triangular grid from file
    grid = read_file()

    '''
    # check that the grid was read in properly
    print (grid)
    '''
    print(grid)  # REMOVEME

    # output greatest path from exhaustive search
    times = timeit('brute_force({})'.format(grid), 'from __main__ import brute_force', number=10)
    times = times / 10
    # print time taken using exhaustive search

    # output greatest path from greedy approach
    times = timeit('greedy({})'.format(grid), 'from __main__ import greedy', number=10)
    times = times / 10
    # print time taken using greedy approach

    # output greatest path from divide-and-conquer approach
    times = timeit('divide_conquer({})'.format(grid), 'from __main__ import divide_conquer', number=10)
    times = times / 10
    # print time taken using divide-and-conquer approach

    # output greatest path from dynamic programming
    times = timeit('dynamic_prog({})'.format(grid), 'from __main__ import dynamic_prog', number=10)
    times = times / 10
    # print time taken using dynamic programming


if __name__ == "__main__":
    main()
