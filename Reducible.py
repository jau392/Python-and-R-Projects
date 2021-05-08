#  File: Reducible.py

#  Description: Returns longest words from dictionary that are reducible.

#  Student Name: Jeremy Ulfohn

#  Student UT EID: jau392

#  Course Name: CS 313E

#  Unique Number: 52240

#  Date Created: 31 Mar 2021

#  Date Last Modified:


import sys


# Input: takes as input a positive integer n
# Output: returns True if n is prime and False otherwise
def is_prime(n):
    if n == 1:
        return False

    limit = int(n ** 0.5) + 1
    div = 2
    while div < limit:
        if n % div == 0:
            return False
        div += 1
    return True


# Input: takes as input a string in lower case and the size
#        of the hash table
# Output: returns the index into which the string will hash
def hash_word(s, size):
    hash_idx = 0
    for i in range(len(s)):
        char_order = ord(s[i]) - 96
        hash_idx = (hash_idx * 26 + char_order) % size
    return hash_idx


# Input: takes as input a string in lower case and the constant
#        for double hashing
# Output: returns the step size for that string
def step_size(s, const):
    double_hash_idx = 0 # Initialize
    for i in range(len(s)):
        mod_order = ord(s[i]) - 96 # Since all char are lowercase
        double_hash_idx = (double_hash_idx * 26 + mod_order) % const
        # Same as 'hash_word()', but with const instead of size

    # Step-Size Formula: constant - (double hash index) mod (constant)
    double_step_size = const - (double_hash_idx % const)
    return double_step_size



# Input: takes as input a string and a hash table
# Output: no output; the function enters the string in the hash table,
# and it resolves collisions by double hashing
def insert_word(s, hash_table):
    # Position that the string would have been in before collision
    pos = hash_word(s, len(hash_table))
    if hash_table[pos] != " ": # If there is a collision
        new_pos = step_size(s, 17) # Set constant == 17
        inc = 1
        # While there continues to be a collision:
        # Note: double-hash position = (hash1 + (hash2 * factor)) % length
        while hash_table[(pos + new_pos * inc) % len(hash_table)] != " ":
            inc += 1
        # Once there's no collision, break loop:
        hash_table[(pos + new_pos * inc) % len(hash_table)] = s
    else: # If there is no collision, i.e. spot is empty:
        hash_table[pos] = s



# Input: takes as input a string and a hash table
# Output: returns True if the string is in the hash table
#         and False otherwise (Boolean)
def find_word(s, hash_table):
    pos = hash_word(s, len(hash_table))

    if hash_table[pos] == s: # If s is found in default position:
        return True
    if hash_table[pos] != " ": # If default position contains another word:
        new_pos = step_size(s, 17)
        inc = 1
        while hash_table[(pos + new_pos * inc) % len(hash_table)] != " ":
            if hash_table[(pos + new_pos * inc) % len(hash_table)] == s:
                return True # see if s is elsewhere b/c of collision
            inc += 1 # Continue until a BLANK space is reached

    # Else: word not in hash table at all!
    return False


# Input: string s, a hash table, and a hash_memo
#        recursively finds if the string is reducible
# Output: if the string is reducible it enters it into the hash memo
#         and returns True and False otherwise

# ~~~~~~~~~~ Description II copy/paste: ~~~~~~~~~~
# as you recursively remove one letter at a time check
# first if the sub-word exists in the hash_memo. if it does
# then the word is reducible and you do not have to test
# any further. add the word to the hash_memo.

def is_reducible(s, hash_table, hash_memo):
    # If the word is down to one valid letter AND not in memo already
    if s == "a" or s == "i" or s == "o":  # BASE CASE 1
        return True
    
    # BASE CASE 2: word is in hash dictionary
    elif find_word(s, hash_memo): # Check memo
        return True

    # RECURSIVE CASE: Do this as few times as possible
    for sub_word in check_sub_words(s, hash_table):
        # If sub-word in memo
        if is_reducible(sub_word, hash_table, hash_memo):
            insert_word(s, hash_memo) # Add sub-word to memo
            return True

    # Base case 3: all else fails; word irreducible
    return False

# Helper function for is_reducible()
# EDIT: added 'hash_memo' parameter
def check_sub_words(s, hash_table):
    # Create list to store the results of valid words
    valid_sub_words = []
    # Create loop that will pop one letter, then use find_word() to
    # check its validity/reducibility
    for i in range(len(s)):
        sub_word = s[:i] + s[i+1:] # Try pop at EACH position
        if find_word(sub_word, hash_table):
            valid_sub_words.append(sub_word)
    # Return aforementioned list
    return valid_sub_words




# Input: string_list a list of words, SORTED by length
# Output: returns a list of words that have the maximum length
def get_longest_words(string_list):
    max_len_words = [] # List that contains the longest words
    max_len = len(string_list[0]) # string_list has the longest at [0]
    for i in range(len(string_list)):
        if len(string_list[i]) == max_len:
            max_len_words.append(string_list[i])
        else: # Return instantly once length falls below max
            return max_len_words


def main():
    # create an empty word_list
    word_list = []

    # read words from words.txt and append to word_list
    for line in sys.stdin:
        line = line.strip()
        word_list.append(line)

    # Add single-letters to word_list
    one_let = ["a", "i", "o"]
    for letter in one_let:
        word_list.append(letter)

    # find length of word_list
    length = len(word_list)

    # determine prime number N that is greater than twice
    # the length of the word_list
    prime_n = length * 2
    # Increment prime_n until it actually IS prime
    while is_prime(prime_n) == False:
        prime_n += 1

    # create an empty hash_list
    hash_list = []

    # populate the hash_list with N blank strings
    for i in range(prime_n):
        hash_list.append(" ")

    # hash each word in word_list into hash_list
    #   - for collisions use double hashing
    for item in word_list:
        insert_word(item, hash_list)

    # create an empty hash_memo of size M
    hash_memo = []

    # we do not know a priori how many words will be reducible
    # let us assume it is 10 percent (fairly safe) of the words
    # then M is a prime number that is slightly greater than
    # 0.2 * size of word_list

    # populate the hash_memo with M blank strings
    for i in range(prime_n):
        hash_memo.append(" ")

    # create an empty list; 'reducible_words'
    reducible_words = []

    # for each word in the word_list recursively determine
    # if it is reducible, if it is, add it to reducible_words
    for item in word_list:
        if is_reducible(item, hash_list, hash_memo):
            reducible_words.append(item) # Idk what's wrong, but it fuckin' worked :)

    # as you recursively remove one letter at a time check
    # first if the sub-word exists in the hash_memo. if it does
    # then the word is reducible and you do not have to test
    # any further. add the word to the hash_memo.
    # ^^^ This is already done in is_reducible() though...?

    list_sort_len = []
    for item in reducible_words:
        # Append a TUPLE: (word's length, word) == ([0], [1])
        # This is in order that list.sort() work
        list_sort_len.append((len(item), item))
    # Put the longest words at the front of the list
    list_sort_len.sort(reverse=True) # Sort in descending order

    # Replace first i characters in reducible_words with those of
    # list_sort_len at tuple index [1]
    for i in range(len(list_sort_len)):
        reducible_words[i] = list_sort_len[i][1]

    # find the largest reducible words in reducible_words
    longest_words = get_longest_words(reducible_words)

    # print the reducible words in alphabetical order
    longest_words.sort()
    for item in longest_words:
        print(item) # one word per line, with normal print()


if __name__ == "__main__":
    main()
