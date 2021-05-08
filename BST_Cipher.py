#  File: BST_Cipher.py

#  Description: encryption/decryption using BST

#  Student Name: Jeremy Ulfohn

#  Student UT EID: jau392

#  Course Name: CS 313E

#  Unique Number: 52240

#  Date Created: 20 April 2021

#  Date Last Modified: 20 April 2021

import sys
# list of operators for self.decrypt(st)
OPERATORS = ['<','>','*','!']

# create Node() class, as with previous assignments
#   attributes: data, lChild, rChild
class Node(object):
    def __init__(self, data):
        self.data = data
        self.lChild = None
        self.rChild = None

    def __str__(self):
        return str(self.data)


class Tree(object):
    # the init() function creates the binary search tree with the
    # encryption string. If the encryption string contains any
    # character other than the characters 'a' through 'z' or the
    # space character drop that character.
    def __init__(self, encrypt_str):
        self.root = None # start out empty

        for ch in encrypt_str:
            if ord(ch) == 32: # if is_space_character
                self.insert(ch.lower())
            elif ord(ch) >= 97 and ord(ch) <= 122:
                self.insert(ch.lower())
            else: # here, ch does NOT belong in the tree; move until we find one that does
                continue
        return


    # the insert() function adds a Node() containing a character in
    # the binary search tree. If the character already exists, it
    # does not add that character. There are no duplicate characters
    # in the binary search tree.
    def insert(self, ch):
        if self.find(ch) is not None:
            return # do nothing if character already is in BST
        # else
        newNode = Node(ch)
        if self.root is None: # empty case; simply make newNode the root
            self.root = newNode

        else: # normal case
            current = self.root
            parent = self.root
            while current is not None:
                parent = current # move down the tree
                if ch < current.data:
                    current = current.lChild
                else:
                    current = current.rChild # rChild covers the equal case, i.e. favor right

            # at this point, we're at BST bottom - the insert location
            if ch < parent.data:
                parent.lChild = newNode
            else:
                parent.rChild = newNode


    # define find, which is a helper function to check duplicate
    #      OUTPUT: node with key, given INPUT: key, BST
    def find(self, key):
        current = self.root
        while current is not None and current.data != key: # move through BST
            if key < current.data: # go either left or right, favouring right
                current = current.lChild
            else:
                current = current.rChild
        return current # returns either current Node(), or None


    # the search() function will search for a character in the binary
    # search tree and...
    # RETURN: a string containing a series of lefts, rights == '<', '>'
    # or: blank '' string if self.find() is None
    # or: '*' if self.root == char
    def search(self, ch):
        if self.root.data == ch:
            return '*'
        if self.find(ch) is None:
            return ''
        else:
            return self.search_rec(self.root, ch, '')


    def search_rec(self, node, ch, str):
        if node is None or node.data == ch:
            return str
        if node.data <= ch:
            return self.search_rec(node.rChild, ch, str + '>')
        return self.search_rec(node.lChild, ch, str + '<')


    # the traverse() function will take string composed of a series of
    # lefts (<) and rights (>) and return the corresponding
    # character in the binary search tree. It will return an empty string
    # if the input parameter does not lead to a valid character in the tree.
    #       NOTE: self.traverse() is the opposite of self.search()
    def traverse(self, st):
        current = self.root
        # case of route starting with the root
        if st[0] == '*':
            return current.data

        for i in range(len(st)):
            # LEFT (<) case
            if st[i] == '<' and current.lChild is not None:
                current = current.lChild # update current
            elif st[i] == '>' and current.rChild is not None:
                current = current.rChild
            else: # if neither of these are true, then the input parameter is invalid => blank string
                return ''
        return current.data


    # the encrypt() function will take a string as input parameter, convert
    # it to lower case, and return the encrypted string. It will ignore
    # all digits, punctuation marks, and special characters
    #       DELIMITER :== '!'
    def encrypt(self, st):
        crypt = '' # crypt will be returned
        st = st.lower()
        delim = '!'

        for ch in st:
            if (ord(ch) == 32) or (ord(ch) in range(97, 123)):
                path = self.search(ch)
                if path:
                    crypt += path + delim

        return crypt[:-1] # return everything but crypt[-1] == final '!'


    # the decrypt() function will take a string as input parameter, and
    # return the decrypted string.
    # example input: "*!<!<!>!<<!*!<" <==> "meet me"
    def decrypt(self, st):
        decrypt = ''
        # empty case
        if st == '':
            return decrypt
        st = st.split('!') # split on '!', making LIST of str(chars)

        for i in range(len(st)):
            is_valid = True # valid (Boolean) will check if the character is in OPERATORS
            for j in range(len(st[i])):
                if st[i][j] not in OPERATORS:
                    # if st[i][j] is invalid, add the character to decrypt but do not traverse
                    # i.e, make valid = False
                    decrypt += st[i][j] # add this character, then...
                    is_valid = False
            if is_valid:
                decrypt += self.traverse(st[i])

        return decrypt


def main():
    # read encrypt string
    line = sys.stdin.readline()
    encrypt_str = line.strip()

    # modify encrypt_str to include nothing but a -> z and ' '


    # create a Tree object
    the_tree = Tree(encrypt_str)

    # read string to be encrypted
    line = sys.stdin.readline()
    str_to_encode = line.strip()

    # print the encryption
    print(the_tree.encrypt(str_to_encode))

    # read the string to be decrypted
    line = sys.stdin.readline()
    str_to_decode = line.strip()

    # print the decryption
    print(the_tree.decrypt(str_to_decode))

if __name__ == "__main__":
    main()