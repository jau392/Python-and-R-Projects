#  File: Josephus.py

#  Description: Prints the order in which the Josephus soldiers perish.

#  Student Name: Jeremy Ulfohn

#  Student UT EID: jau392

#  Course Name: CS 313E

#  Unique Number: 52240

#  Date Created: 11 April 2021

#  Date Last Modified: 11 April 2021

import sys


class Link(object): # <==> Node()
    # all this needs is the private init method from A14
    def __init__(self, data, next=None): # data is at this location, right before link.next
        self.data = data
        self.next = next # next from default will point to head


class CircularList(object):
    # Constructor
    def __init__(self):
        self.first = None

    # Insert an element (value) in the list
    def insert(self, data):
        # forbid duplicates
        if self.find(data) is not None: # if data is already in list (no duplicates)
            return

        new_link = Link(data) # the new value needs a Link()
        current = self.first # initialize

        if current is None: # always check the null/base case
            self.first = new_link
            new_link.next = self.first # put new_link where self.first was
            return

        # iterated case
        while current.next != self.first: # since next == first when around the circle
            current = current.next # move forward one spot

        # now, current.next == self.first so we're at the end
        current.next = new_link
        new_link.next = self.first
        new_link.previous = current
        # return nothing; modify self in-place


    # Find the Link with the given data (value)
    # or return None if the data is not there
    def find(self, data):
        current = self.first

        # base and recursive cases, as with every method
        if current is None:
            return None

        while current.data != data:
            # we now have the additional case of having circumversed the circle:
            if current.next == self.first:
                return None
            else:
                current = current.next # simply move forward

        # if all else passes, current.data == data
        return current

    # Delete a Link with a given data (value) and return the Link
    # or return None if the data is not there
    def delete(self, data):
        current = self.first
        previous = self.first # need previous as well, as we're omitting one link

        if (self.find(data) is None) or (current is None):
            return None

        while previous.next != self.first: # move previous to first.prev
            previous = previous.next

        else:
            if current.next == current and current.data == data:
                # case of only one link (successful)
                self.first = None # AND, __str__(self) has condition of None
                return current

        while current.data != data:
            if current.next == self.first:
                return None
            else:
                previous = current
                current = current.next

        # at this point, current.data == data, i.e. found
        if current == self.first:
            self.first = self.first.next

        previous.next = current.next

        return current


    # Delete the nth Link starting from the Link start
    # Return the data of the deleted Link AND return the
    # next Link after the deleted Link in that order
#        i.e. return Tuple of (killed_soldier#, next_#_in_count)?
    def delete_after(self, start, n):
        current = self.first # == self.tail.next

        if self.first is None: # base null case
            return None

        # normal loop until elimination
        while current.data != start: # cycle until start is reached
            current = current.next

        # continue until the nth link is found
        count = 1
        while count != n:
            current = current.next
            count += 1

        # now soldiers == n, so this one (at current) dies
        self.delete(current.data)

        to_return = (current.data, current.next.data) # need X.data of each to loop
        # to_return tuple has (deleted link, new start with count == 1)
        return to_return


    # Return a string representation of a Circular List
    # The format of the string will be the same as the __str__
    # format for normal Python lists, e.g. '[1, 2, 3]'
    def __str__(self):
        if self.first is None:
            return '[]'
        # else create a string that resembles a list
        else:
            str_list = '['
            current = self.first
            while current.next != self.first: # while we haven't looped the whole circle
                str_list += (str(current.data) + ', ') # add in space and comma
                current = current.next # move current to next entry

            str_list += (str(current.data) + ']') # add in closing bracket
            return str_list


def main():
    # read number of soldiers
    line = sys.stdin.readline()
    line = line.strip()
    num_soldiers = int(line)

    # read the starting number
    line = sys.stdin.readline()
    line = line.strip()
    start_count = int(line)

    # read the elimination number
    line = sys.stdin.readline()
    line = line.strip()
    elim_num = int(line)

    # so far, we have: num_soldiers, start_count (place at which to start), elim_number (n)
    #       all 3 are of type 'int'
    # FIRST we will contruct the CircularList() on which to excecute the code
    results = CircularList()
    for i in range(1, num_soldiers + 1): # start at 1, end at num_soldiers
        results.insert(i)

    for _ in range(num_soldiers):
        tup = results.delete_after(start_count, elim_num) # get tuple
        start_count = tup[1] # modify start_count for next round
        print(tup[0]) # return deleted soldier

    return


if __name__ == "__main__":
    main()