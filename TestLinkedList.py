#  File: TestLinkedList.py

#  Description: Create entire LinkedList class, outfitted with various methods. Then test it.

#  Student Name: Jeremy Ulfohn

#  Student UT EID: jau392

#  Course Name: CS 313E

#  Unique Number: 52240

#  Date Created: 9 April 2021

#  Date Last Modified: 26 April 2021 (for the regrade)

class Link(object):
    # attributes: data, and next. NO prev
    def __init__(self, data, next=None): # assign default value for next
        self.data = data
        self.next = next # links the list


class LinkedList(object):
    # create a linked list
    # you may add other attributes
    def __init__(self):
        self.first = None

    # want 10 items per line, 2 spaces in between
    def __str__(self):
        string = ""
        current = self.first
        if current is None:
            return ""
        items = 0 # items on the line so far

        while current is not None:
            string += str(current.data) + "  " # 2 spaces
            current = current.next
            items += 1
            if items == 10 and current is not None: # do NOT add new line if new curr is None
                string = string[:-2] # take OFF last 2 spaces in this case
                string += "\n" # instead, add in new line for next 10 items
                items = 0

        return string[:-2] # exclude the last space. works even with EMPTY string


    def __len__(self):
        current = self.first
        size = 0
        while current is not None: # while is not none, iterate through all items***
            size += 1
            current = current.next
        return size


    # get number of links
    def get_num_links(self):
        return len(self) # use private method 'len' above


    # add an item at the beginning of the list
    def insert_first(self, data):
        link = Link(data) # insert requires a link
        if self.is_empty():
            self.first = link
        else: # if list ain't empty
            link.next = self.first
            self.first = link # link data as self.first


    # add an item at the end of a list
    def insert_last(self, data):
        link = Link(data)
        if self.first is None:
            self.first = link # first == last case
            return

        current = self.first
        while current.next:
            current = current.next # move down list till empty spot
        current.next = link


    # add an item in an ordered list in ascending order
    # assume that the list is already sorted
    def insert_in_order(self, data):
        newlink = Link(data)
        current = self.first
        previous = self.first

        if (current is None) or (current.data >= data):
            newlink.next = self.first
            self.first = newlink
            return
        while current.next is not None:
            if current.data <= data:
                previous = current
                current = current.next # move forward with variable swap
            else:
                newlink.next = previous.next
                previous.next = newlink # move back 1
                return

        if current.data <= data:
            current.next = newlink
        else:
            newlink.next = previous.next
            previous.next = newlink
        return


    # search in an unordered list, return None if not found
    def find_unordered(self, data):
        current = self.first
        if current is None:
            return None # empty => not found

        while data != current.data: # Iterate through, naively
            if current.next is None:
                return None
            else:
                current = current.next

        return current

    # Search in an ordered list, return None if not found
    def find_ordered(self, data):
        # identical to find_unordered, per Piazza
        current = self.first
        if current is None:
            return None  # empty => not found

        while data != current.data:  # Iterate through, naively
            if current.next is None:
                return None
            else:
                current = current.next

        return current



    # Delete and return the first occurrence of a Link containing data
    # from an unordered list or None if not found
    def delete_link(self, data):
        current = self.first
        previous = self.first

        if current is None:
            return None

        while current.data != data:
            if current.next is None:
                return None
            else: # iterate through +1 if data might exist
                previous = current
                current = current.next

        # data found; current == data
        # delete at this location by reassigning current, previous
        if current == self.first:
            self.first = self.first.next
        else: # else skip previous forward +1
            previous.next = current.next
        return current


    # Copy the contents of a list and return new list
    # do not change the original list
    def copy_list(self):
        copy = LinkedList() # initialize eventual result
        current = self.first
        while current is not None:
            copy.insert_last(current.data)
            current = current.next
        return copy

    # Reverse the contents of a list and return new list
    # do not change the original list
    def reverse_list(self):
        new_list = LinkedList()

        if self.is_empty():
            return None

        current = self.first
        while current is not None:
            new_list.insert_first(current.data) # only change from copy_list: insertfirst
            current = current.next
        return new_list

    # Sort the contents of a list in ascending order and RETURN NEW LIST
    # do not change the original list
    def sort_list(self):
        result = LinkedList()
        current = self.first
        while current is not None:
            result.insert_in_order(current.data)
            if current.next is not None:
                current = current.next
            else:
                break # when current == None
        return result



    # Return True if a list is sorted in ascending order or False otherwise
    def is_sorted(self):
        current = self.first
        if self.is_empty() or self.get_num_links() == 1:
            return True

        for _ in range(self.get_num_links() - 1):
            if current.data > current.next.data: # check for order violation
                return False
            current = current.next
        # if loop succeeds...

        return True

    # Return True if a list is empty or False otherwise
    # is_empty helper method
    def is_empty(self):
        return self.first is None

    # Merge two sorted*** lists and return new list in ascending order
    # do not change the original lists
    def merge_list(self, other): # want: (self.first, other.first
        curr = other.first
        merged = self.copy_list().sort_list()

        if self.is_empty():
            if other.is_empty():
                return merged
            else:
                merged = other.copy_list()
                return merged
        elif other.is_empty():
            return merged

        for _ in range(other.get_num_links()):
            merged.insert_in_order(curr.data)
            curr = curr.next

        return merged

    # Test if two lists are equal, item by item and return True
    def is_equal(self, other):
        # two base cases where equality is impossible:
        if other.is_empty() and self.is_empty():
            return True
        elif len(self) != len(other) or other.is_empty() or self.is_empty():
            return False

        current_self = self.first
        current_other = other.first
        while current_self is not None and current_other is not None:
            if current_self.data != current_other.data:
                return False
            current_self = current_self.next
            current_other = current_other.next
        return True

    # Return a new list, keeping only the first occurence of an element
    # and removing all duplicates. Do not change the order of the elements
    def remove_duplicates(self):
        new_list = self.copy_list() # now, new_list == self
        previous = new_list.first
        current = new_list.first
        elements = [] # list to keep track of items and, thus, detect duplicate

        for _ in range(new_list.get_num_links()):
            if current.data in elements:
                current = current.next
                previous.next = current # skip the duplicate
            else:
                elements.append(current.data)
                previous = current
                current = current.next # add to new_list
        return new_list