#!/usr/bin/python3

from HashMap import HashMap


def main(filename):
    hashmap = HashMap()
    with open(filename, 'r') as reader:
        for line in reader:
            if line.startswith('+'):
                k, v = line[1:].strip().split()
                hashmap[k] = v
            elif line.startswith('-'):
                del hashmap[line[1:].strip()]
    print(hashmap)
    print("size:", len(hashmap))
    print(sorted(hashmap.keys()))
    print("load:", hashmap.load())


if __name__ == '__main__':
    main('phoneticsizes.txt')
