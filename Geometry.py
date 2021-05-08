import sys
import copy


class Queue(object):
    def __init__(self):
        self.queue = []

    # add an item to the end of the queue
    def enqueue(self, item):
        self.queue.append(item)

    # remove an item from the beginning of the queue
    def dequeue(self):
        return (self.queue.pop(0))

    # check if the queue if empty
    def is_empty(self):
        return (len(self.queue) == 0)

    # return the size of the queue
    def size(self):
        return (len(self.queue))


# Input: a is a list of strings that have either lower case
#        letters or digits
# Output: returns a sorted list of strings
def radix_sort(a):
    # initialize
    to_pass = copy.deepcopy(a)
    max_len = -1
    index = 1

    for item in to_pass:
        if len(item) > max_len:
            max_len = len(item) # max_len tells us what to iterate to

    while index <= max_len:
        to_pass = pass_sort(to_pass, index)
        index += 1
        print(to_pass)

    return to_pass

def pass_sort(str_list, index=1): # Takes Queue() object instead of list. Want index positive
    alphabetical = []
    # create queues for digits 0-9
    pass_queues = [Queue()] * 10
    # UNNEEDED?? end_pass = Queue()  # store the sorted result of each pass
    result = []

   # main loop
    for str in str_list:
        if index > len(str): # Freeze short strings where they are
            if str[0].isnumeric():
                pass_queues[int(str[0])].enqueue(str)
            else: # if is_alphabetical:
                pass_queues[9].enqueue(str)

        else: # if index <= len(str):
            if str[-index].isnumeric():  # CASE 1: str[index] is integer
                pass_queues[int(str[-index])].enqueue(str) # put str in the correct place in Q0 -> Q9

            else:  # CASE 2: str[index] is alphabetical
                alphabetical.append(str)
                alphabetical.sort(key=lambda alphabetical: alphabetical[-index])

    for str in alphabetical:
        pass_queues[9].enqueue(str)  # Enqueue sorted str with LETTERS in Q9

    for queue in pass_queues: # use "queue" until queue.is_empty
        while not queue.is_empty():
            result.append(queue.dequeue())
    # Want to return: a list after pass is complete
    return result

a = ['z34', '8fg6d', 'xc65ns3', 'plaq78d', 'sd67mn9', 'khbw']
b = ['311', '96', '495', '137', '158', '84', '145', '63']
