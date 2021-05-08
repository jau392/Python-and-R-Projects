#  File: Poly.py

#  Description:

#  Student Name: Jeremy Ulfohn

#  Student UT EID: jau392

#  Course Name: CS 313E

#  Unique Number: 52240

#  Date Created:

#  Date Last Modified:

import sys

class Link(object):
    # attributes co, exp, nxt
    def __init__(self, coeff=1, exp=1, next=None):
        self.coeff = coeff
        self.exp = exp
        self.next = next


    def __str__(self): # done, resembles the tuple (co, exp)
        return '(' + str(self.coeff) + ', ' + str(self.exp) + ')'


class LinkedList(object): # attribute first
    def __init__(self):
        self.first = None


    # keep Links in descending order of exponents**
    def insert_in_order(self, coeff, exp):
        if coeff == 0:
            return None # 0 coeff does not belong in polynomial, so return

        new_link = Link(coeff, exp) # put co, exp into link
        curr = self.first # == self.head
        prev = self.first

        # special empty LL case
        if curr is None:
            new_link.next = self.first
            self.first = new_link # new_link is the ONLY link

        # special LL with 1 link
        elif curr.exp <= exp:
            new_link.next = self.first # make new_link the first, for LL of size 2
            self.first = new_link

        else: # normal case, for all other LL's
            while curr.next is not None and curr.next.exp > exp:
                curr = curr.next # move current forward

            # now we've found where current should be: curr.next.exp <= exp
            new_link.next = curr.next
            curr.next = new_link # return nothing


    # add polynomial p to this polynomial and return the sum
    def add(self, p):
        # empty LL case for self, then p
        if self.first is None:
            return p
        elif p.first is None:
            return self

        else:
            sum = LinkedList() # initialize new LL for sum
            currs = self.first
            currp = p.first # curr for self and p, respectively

            while currs is not None and currp is not None:
                # case of immediate equality of curr
                if currs.exp == currp.exp:
                    sum.insert_in_order((currs.coeff + currp.coeff), currs.exp)
                    currs = currs.next
                    currp = currp.next
                # case of no match: add only high one for self, then p
                elif currs.exp > currp.exp:
                    sum.insert_in_order(currs.coeff, currs.exp)
                    currs = currs.next # move self's current to next (lower)
                else: # curr is higher, but same thing
                    sum.insert_in_order(currp.coeff, currp.exp)
                    currp = currp.next

            # cleanup: now one or both of self, p are empty,
            # but there may be leftovers. do self, then p
            while currs is not None:
                sum.insert_in_order(currs.coeff, currs.exp)
                currs = currs.next
            while currp is not None:
                sum.insert_in_order(currp.coeff, currp.exp)
                currp = currp.next
            return sum # return the full sum LL


    # multiply polynomial p to this polynomial and return the product
    def mult(self, p):
        # empty LL case for self, then p
        if self.first is None:
            return p
        elif p.first is None:
            return self
        else:
            product = LinkedList() # initialize product LL
            currs = self.first
            # basically for EACH term of self, multiply term by p terms until None
            while currs is not None:
                currp = p.first # when p runs out, reset curr back to p.first

                while currp is not None: # inner loop for LL p
                    new_coeff = currs.coeff * currp.coeff
                    new_exp = currs.exp + currp.exp # algebra rules
                    product.insert_in_order(new_coeff, new_exp)
                    currp = currp.next

                currs = currs.next # move through self until None
            return product # now, both self and p have run out. return


    # helper for simp(self), need to delete if coeff == 0
    def delete_link(self, coeff): # data = coefficient here
        current = self.first
        previous = self.first

        if current is None:
            return False

        while current.coeff != coeff:
            if current.next is None:
                return False
            else: # iterate through +1 if data might exist
                previous = current
                current = current.next

        # data found; current == coeff
        # delete at this location by reassigning current, previous
        if current == self.first:
            self.first = self.first.next
        else: # else skip previous forward +1
            previous.next = current.next


    def simp(self):
        # only for non-null LL as self; no null case needed
        if self.first is not None:
            curr = self.first
            while curr is not None: # i.e. for each current, check if there's same_exp
                same_exp = curr.next # initialize at 1 after current
                # for EACH curr, check curr.next for addition
                while same_exp is not None and same_exp.exp == curr.exp:
                    curr.coeff += same_exp.coeff
                    curr.next = same_exp.next # this effectively deletes a term
                    same_exp = same_exp.next # move to next same_exp

                curr = curr.next # "delete" all currs with an equal order term
                
        while self.delete_link(0) != False: # delete until delete_link == False
            self.delete_link(0)

        if self.first is None: # mod, since we're using it for sum as well
            return None


    # create a string representation of the polynomial
    # use f-strings. PURPOSE: quickly append strings containing an updating variable
    def __str__(self):
        # null case
        if self.first is None:
            return "" # is this right? Check

        curr = self.first
        str = f"{curr}" # start str as a float
        while curr.next is not None:
            curr = curr.next # move current over 1
            str += f" + {curr}"
        return str

# helper function for main. takes num_terms and a given file, 'f'
def create_list(num_terms, f):
    temp = LinkedList() # temp will be returned
    for _ in range(num_terms):
        coeff, exp = [int(loop) for loop in f.readline().strip().split(' ')]
        temp.insert_in_order(coeff, exp)
    return temp # turn poly.in into an actual LinkedList() object

def main():
    # get num_terms from file[0]
    f = sys.stdin
    num_terms = int(f.readline())

    # create polynomial p,
    # create polynomial q
    p = create_list(num_terms, f)
    # repeat for q
    f.readline()
    num_terms = int(f.readline())
    q = create_list(num_terms, f)

    # get sum of p and q and print sum
    summed = p.add(q)
    summed.simp()
    print(f"{summed}") # NOTE: use \n to print extra blank line afterward

    # get product of p and q and print product
    product = p.mult(q)
    product.simp() # mult() requires simplification, add() does not
    print(f"{product}")

if __name__ == "__main__":
    main()
