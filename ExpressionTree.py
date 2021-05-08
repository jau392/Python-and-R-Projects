#  File: ExpressionTree.py

#  Description:

#  Student's Name: Jeremy Ulfohn

#  Student's UT EID: jau392

#  Course Name: CS 313E

#  Unique Number:

#  Date Created:

#  Date Last Modified:

import sys

operators = ['+', '-', '*', '/', '//', '%', '**']


class Stack(object):
    def __init__(self):
        self.stack = []

    def push(self, data):
        self.stack.append(data)

    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        else:
            return None

    def is_empty(self):
        return len(self.stack) == 0


class Node(object):
    def __init__(self, data=None, lChild=None, rChild=None):
        self.data = data
        self.lChild = lChild
        self.rChild = rChild


class Tree(object):
    def __init__(self):
        self.root = Node(None)

    # input: infix expression with parentheses amd spaces btwn all (string)
    # output: expression tree - Tree() object
    def create_tree(self, expr):
        expression = expr.split() # split on spaces (which we assume expr has)
        parent = Stack()
        current = self.root # start with current == root, # Node() object

        for token in expression:
            # (1) token begins expression
            if token == '(': # opening parenthesis <=> beginning an expression
                parent.push(current)
                current.lChild = Node(None) # create lChild
                current = current.lChild

            # (2) token in OPS
            elif token in operators:
                current.data = token # current (in OPS) will be a parent w 2 children
                parent.push(current) # push onto parent stack
                current.rChild = Node(None)
                current = current.rChild # give operator a right child, move curr here

            # (3) token is numeric (integer or float, with decimal)
            elif token.isdigit() or '.' in token:
                current.data = token # fill current in with operand (number)
                current = parent.pop() # now, assign current to parent

            # (4) token is closing ')'
            elif token == ')':
                if not parent.is_empty():
                    current = parent.pop() # if parent exists, assign current -> parent
                else:
                    break # if it is empty, tree is finished

        return expr


    # this function should evaluate the tree's expression
    # returns the value of the expression after being calculated
    #       one case per OP in OPS
    #       recursively calculate the operators' child nodes (== numbers)
    def evaluate(self, aNode):
        if aNode.data == '+':
            return self.evaluate(aNode.lChild) + self.evaluate(aNode.rChild)
        elif aNode.data == '-':
            return self.evaluate(aNode.lChild) - self.evaluate(aNode.rChild)
        elif aNode.data == '*':
            return self.evaluate(aNode.lChild) * self.evaluate(aNode.rChild)
        elif aNode.data == '/':
            return self.evaluate(aNode.lChild) / self.evaluate(aNode.rChild)
        elif aNode.data == '//':
            return self.evaluate(aNode.lChild) // self.evaluate(aNode.rChild)
        elif aNode.data == '%':
            return self.evaluate(aNode.lChild) % self.evaluate(aNode.rChild)
        elif aNode.data == '**':
            return self.evaluate(aNode.lChild) ** self.evaluate(aNode.rChild)
        # else aNode.is_numerical() case
        elif aNode.data.isdigit() or '.' in aNode.data:
            return eval(aNode.data) * 1.0 # want in float format


    # this function should generate the preorder notation of
    # the tree's expression
    # returns a string of the expression written in preorder notation
    def pre_order(self, aNode):
        pre_list = []
        if aNode.data in operators: # for each operator, append then check L, R children
            pre_list.append(aNode.data) # if not operator, node is LEAF node. thus no need to check L, R
            pre_list.append(self.pre_order(aNode.lChild))
            pre_list.append(self.pre_order(aNode.rChild)) # this means append L and R, but L priority
            # i.e. only when L is None will list.append() move on to R
        else:
            pre_list.append(aNode.data) # appends either a NUMBER or NONE
        # return result
        return ' '.join(pre_list) # join with spaces in between each


    # this function should generate the postorder notation of
    # the tree's expression
    # returns a string of the expression written in postorder notation
    def post_order(self, aNode):
        post_list = []
        if aNode.data in operators:  # moving left to right, add operators AND their children
            post_list.append(self.post_order(aNode.lChild))
            post_list.append(self.post_order(aNode.rChild))
            post_list.append(aNode.data)
        else:
            post_list.append(aNode.data)  # if not operator, numerical or None. thus, simply append
        # return result
        return ' '.join(post_list)  # join with spaces in between each


# you should NOT need to touch main, everything should be handled for you
# you should NOT need to touch main, everything should be handled for you
def main():
    # read infix expression
    line = sys.stdin.readline()
    expr = line.strip()

    tree = Tree()
    tree.create_tree(expr)

    # evaluate the expression and print the result
    print(expr, "=", str(tree.evaluate(tree.root)))

    # get the prefix version of the expression and print
    print("Prefix Expression:", tree.pre_order(tree.root).strip())

    # get the postfix version of the expression and print
    print("Postfix Expression:", tree.post_order(tree.root).strip())


if __name__ == "__main__":
    main()