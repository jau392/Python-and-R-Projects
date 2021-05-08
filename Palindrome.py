#  File: Palindrome.py

#  Description: This program returns the smallest palindromic string, derived from an input string.

#  Student Name: Jeremy Ulfohn

#  Student UT EID: jau392

#  Partner Name:

#  Partner UT EID:

#  Course Name: CS 313E

#  Unique Number: 52240

#  Date Created: 23 Feb 2021

#  Date Last Modified: 7 Mar 2021

# Input: a lowercase string with no digits, punctuation marks, or spaces
# Output: a string that is the smallest palindrome that can be
#         made by adding characters to the start of the input string

# Helper function for longest palindromic substring:
import sys
def longest_pal_subs(str):
    n = len(str)
    # Shortest/null pal length is 1
    max_length = 1
    start = 0

    # Keep track of start, end indices
    for i in range(n):
        # i is the START index of the pal substring
        # j is the LENGTH of the palindromic portion
        for j in range(i, n):
            # bookmark is a Boolean marker, it must start out true and at left
            bookmark = 1
            # Check is_palindrome
            # k is the MIDPOINT of the palindrome
            for k in range((j - i) // 2 + 1):
                # i.e. if first half != second half:
                if str[i + k] != str[j - k]:
                    bookmark = 0
            # If this actually is the largest palindrome:
            if bookmark == 1 and (j - i + 1) > max_length:
                start = i
                max_length = j - i + 1

    # Create result
    pal = ''
    for i in range(start, start + max_length):
        pal += str[i]
    # Return 3-member tuple with all information needed: string, low, and high
    if start == 0: # If the palindrome starts at the FIRST char like needed
        result = (pal, start, start + max_length)
    else: # Else we ignore this result and return str[0]
        result = (str[0], 0, 1)
    # The "HIGH" in the tuple is actually the index of the first NON-pal letter
    return result

# For use in main, we need to reverse the non-palindromic portion:
def reverse(str):
    result = ''
    for char in str:
        # Add to LEFT of result
        result = char + result
    return result


def smallest_palindrome(str):
    # Keep will contain range of indices to keep
    keep = longest_pal_subs(str)
    non_pal = ''
    n = len(str)
    # Non-pal will ALWAYS be added at beginning of str
    for i in range(keep[2], n):
        non_pal += str[i]
    rev = reverse(non_pal)
    # Add rev of end to beginning:
    result = rev + keep[0] + non_pal
    return result


# Input: no input
# Output: a string denoting all test cases have passed
def test_cases():
  # write your own test cases
  assert smallest_palindrome("cbabcde") == "edcbabcde"

  return "all test cases passed"

def main():
    # read the data
    while True:
        line = sys.stdin.readline()
        line = line.rstrip('\n')
        if not line:
            break
        print(smallest_palindrome(line))

if __name__ == "__main__":
  main()