# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 19:30:50 2018

@author: Avery
"""

from multiprocessing import Process
import sys
import time

def main():
    
    new_password = (str(input("Please enter a password: ")))
    P = Process(target=pass_crack, args=(new_password,))
    P.start()
    P.join()
   

    #pass_crack(new_password)
    time.sleep(100)
    

def pass_crack(password):
    print("-------------------------")
    print("Let's find some passwords")
    print("-------------------------")
    
    char_word = "a b c d e f g h i j k l m n o p q r s t u v w x y z 1 2 3 4 5 6 7 8 9 0"
    char_list = char_word.split(" ")
    
    
    craft_word = ["","","","","","","","","","","","",""]
    
    
 
    p1, p2, p3, p4, p5, p6, p7, p8 = 0, 0, 0, 0, 0, 0, 0, 0
    i, j = 0, 0
    c1, c2, c3, c4, c5, c6 = 0, 0 ,0, 0, 0, 0
    exit_step = 3000000000
    initial_step = 3000000000
    while True:
        #print(exit_step)
        #print("".join(craft_word))

        if "".join(craft_word) == password:
            print("Gotcha")
            sys.stdout.flush()
            print(craft_word)
            print("".join(craft_word))
            print(initial_step - exit_step)
            sys.stdout.flush()
            break
        
        
        
        if p6 == len(char_list) and p5 == len(char_list) and p4 == len(char_list) \
        and p3 == len(char_list) and p2 == len(char_list) and p1 == len(char_list):
            if i <= 6:
                i = 6
                c1 = 5
                c2 = 4
                c3 = 3
                c4 = 2
                c5 = 1
            p6 = 0
            craft_word[c6] = char_list[p7]
            p7 += 1
            
        
        
        if p5 == len(char_list) and p4 == len(char_list) and p3 == len(char_list) \
        and p2 == len(char_list) and p1 == len(char_list):
            if i <= 5:
                i = 5
                c1 = 4
                c2 = 3
                c3 = 2
                c4 = 1
            p5 = 0
            craft_word[c5] = char_list[p6]
            p6 += 1
            
        
        if p4 == len(char_list) and p3 == len(char_list) and p2 == len(char_list) and \
                                        p1 == len(char_list):
            if i <= 4:
                i = 4
                c1 = 3
                c2 = 2
                c3 = 1
            p4 = 0
            craft_word[c4] = char_list[p5]
            p5 += 1
            
        
        
        if p3 == len(char_list) and p2 == len(char_list) and p1 == len(char_list):
            if i <= 3:
                i = 3
                c1 = 2
                c2 = 1
                
            p3 = 0
            craft_word[c3] = char_list[p4]
            p4 += 1
        
        if p2 == len(char_list) and p1 == len(char_list):
            if i <= 2:
                i = 2
                c1 = 1
            p2 = 0
            craft_word[c2] = char_list[p3]
            p3 += 1
        
        
        if p1 == len(char_list):
            if i <= 1:
                i = 1
            p1 = 0
            craft_word[c1] = char_list[p2]
            p2 += 1
            
            
        craft_word[i] = char_list[p1]
        
        p1 += 1
        exit_step -= 1
        
        if exit_step == 0:
            print("Had to break. We don't go infinite here.")
            sys.stdout.flush()
            break
        
    

if __name__ == '__main__':

    main()