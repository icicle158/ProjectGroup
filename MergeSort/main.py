#!/usr/bin/python3

from alphabetizer import *

class Person:
    def __init__(self, first, last, email):
        self.first = first
        self.last = last
        self.email = email
    
    def __str__(self):
        return '{0} {1} <{2}>'.format(self.first, self.last, self.email)
        
    def __repr__(self):
        return '({0}, {1}, {2})'.format(self.first, self.last, self.email)
    
    def __eq__(self, other):
        return self.first == other.first and self.last == other.last and self.email == other.email
    
def load_file(filename):
    members = []
    with open(filename, 'r') as reader:
        for line in reader:
            if line.strip():
                (first, last, email) = line.split()
                members.append(Person(first, last, email[1:-1]))
    return members
    
def write_file(filename, memberlist):
    with open(filename, 'w') as writer:
        writer.writelines(str(member) + '\n' for member in memberlist)
            

def main(infile, outfile):
    order = order_first_name
    #order = order_second_name
    member_list = load_file(infile)
    (sorted_list, cost) = alphabetize(member_list, order)
    if not is_alphabetized(sorted_list, order):
        print('Sorting was not successful!')
    print(cost, 'comparisons were required')
    write_file(outfile, sorted_list)
    
if __name__ == '__main__':
    main('gryffindor.txt', 'sorted.txt')
    #main('short.txt', 'sorted.txt')
