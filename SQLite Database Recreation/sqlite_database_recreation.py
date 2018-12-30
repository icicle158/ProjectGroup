"""
Name: Avery Berninger
Time To Completion: 45+ hours
Comments:

Sources:
"""
import string
from operator import itemgetter
from pprint import pprint

_ALL_DATABASES = {}


#After reading about it online, python 3 does not support
#none comparisons with other data types unlike python 2
#Thus,
def none_key(element):
    if element == None:
        return float("-inf")
        
    else:
        return element


class Connection(object):
    def __init__(self, filename):
        """
        Takes a filename, but doesn't do anything with it.
        (The filename will be used in a future project).
        """
        pass
    

    def execute(self, statement):
        """
        Takes a SQL statement.
        Returns a list of tuples (empty unless select statement
        with rows to return).
        """
        
        
        #We have to tokenize the input data, strip it
        #down to it's essential components
        tokenize = []
        temp_list = []
        
        temp_char_str = ""
      
        database = Database()
        
        if database.table_list:
            Tabletemp = database.table_list[len(database.table_list)-1]
            pass
        else:
            Tabletemp = Table("")
        
        temp_list = statement.split(" ")
        
        token_word = ""
        
        apost_check = False
        
        for item in temp_list:
            if item.isalpha():
                break
    
        #Tokenize process
        for item in temp_list:
            
            if item[1:].replace(",","").replace("'", "").isdigit() and item[0] == "-":
                
                if "," in item:
                    tokenize.append(str(item[:-1]))
                    tokenize.append(",")
                else:
                    tokenize.append(str(item))
                continue
                
            
            if item == "<":
                tokenize.append(item)
                
            if item == ">":
                tokenize.append(item)
                
            if item == "=":
                tokenize.append(item)
                
            if item == "!=":
                tokenize.append(item)
            
            if item.isalpha() and apost_check == False:
                tokenize.append(item)
                continue
            
            if item.replace("'","").replace(",","").replace(";","") == "NULL":
                    print(item)
                    tokenize.append(None)
                    #continue
                    
                    
    
            #PLEASE DONT FORGET TO IMPLEMENT THE REVERSE OF THIS!!!!!!!!!!!!!!!!!! 
            if (item[0] == "'" and item.find("'''") != 0 and "'''" in item and apost_check == False):
                new_item = item.replace("''", "'").replace(",","")
                tokenize.append(new_item[1:-1])
                if "," in item:
                        tokenize.append(",")
                continue
                    
            if item.count("'") == 2 and item[0] == "'" and item[len(item)-1] == "'":
                    tokenize.append(item.replace("'","").replace(",",""))
                    if "," in item:
                        tokenize.append(",")
                    continue
            
            if item.count("'''") == 2:
                tokenize.append(item.replace("'''", "'").replace(",",""))
                
                if "," in item:
                        tokenize.append(",")
                continue
            
                    
            if apost_check == True:
                #Checks if there is an end parenthesis in the word to 
                #be appended to the tokenize list
                end_paren = False
                end_semi = False
                if item.count("'") == 1:
                    
                    if ")" in item:
                        item = item.replace(")","")
                        end_paren = True
                        
                    if ";" in item:
                        item = item.replace(";","")
                        end_semi = True
                    
                    token_word += " " + item.replace("'", "").replace(",", "")
                    
                     
                    
                    apost_check = False
                    tokenize.append(token_word)
                    
                    if end_paren == True:
                        tokenize.append(")")
                        end_paren = False
                        
                    if end_semi == True:
                        tokenize.append(";")
                        end_semi = False
                    
                    token_word = ""
                    if "," in item:
                        tokenize.append(",")
                    continue
                         
                        
                #Checks if there is more than one apostrophe, whilst also 
                #checking to see if there is an apostrophe at the back
                if item.count("'") > 1 and (item.count("'") % 2) == 0:
                    token_word += " " + item.replace("''", "'").replace(",", "")
                    continue
                        
                        
                if item.count("'") > 1 and (item.count("'") % 2) == 1:
                     if (item[len(item)-1] == "'" or item[len(item)-2] == "'"):
                        token_word += " " + item.replace("''", "'").replace(",", "")
                        token_word = token_word[0:len(token_word)-1]
                        
                        apost_check = False
                        tokenize.append(token_word)
                        if "," in item:
                            tokenize.append(",")
                        
                        
                        
                token_word += " " + str(item)
                continue
                    
            
            temp_char_str = ""
            char_cnt = 0
            #Running a loop within a loop is very time intensive
            #Usually, not a good idea, but the input statements
            #are on the smaller side (only a few words
            #at a time)
            for char in item:
                
                if (char == "_") and (char_cnt == len(item)-1):
                    tokenize.append(temp_char_str)
                
                if char == "'":
                    
                    if item.count("'") % 2 == 1:
                        if item.count("'") == 1:
                            apost_rep = item.replace("'", "")
                            print(apost_rep)
                            token_word += apost_rep
                            apost_check = True
                        if item.count("'") == 5:
                            apost_rep = item.replace("''", "'")
                            print(apost_rep)
                            token_word += apost_rep[1:]
                            apost_check = True
                            break
                        if item.count("'") == 3:
                            apost_rep = item.replace("''", "'")
                            print(apost_rep)
                            token_word += apost_rep[1:]
                            apost_check = True
                            break
                            
                        if item.count("'") == 7:
                            apost_rep = item.replace("''", "'")
                            print(apost_rep)
                            token_word += apost_rep[1:]
                            apost_check = True
                            break
                        
                            
                    if char_cnt < len(item)-1:
                        if item[char_cnt+1] == "'":
                            temp_char_str += "'"
                    
                    if char_cnt == len(item)-1:
                        tokenize.append(temp_char_str)
                            
                    
                if char == ";":
                    
                    if item[char_cnt-1] == ")":
                        tokenize.append(char)
                    else:
                        tokenize.append(temp_char_str)
                        
                    if item[len(item)-1] == ";":
                        tokenize.append(char)
                        pass
                    
                
                
                #Very basic error checking, check this later
                if char == "(" or char == ")" or char == "," or char == "*":
                    
                    if item[char_cnt - 1] and char_cnt != 0:
                        if temp_char_str != '' and char != ",":
                            if temp_char_str == "NULL":
                                temp_char_str = None
                                
                            
                            tokenize.append(temp_char_str)
                        
                            
                        if temp_char_str != '' and char == ",":
                            if item[char_cnt - 1] == ")":
                                temp_char_str = ""
                                
                                #tokenize.append(temp_char_str)
                            else:

                                if temp_char_str == "NULL":
                                    temp_char_str = None
                                tokenize.append(temp_char_str)
                                
                                
            
                    #Put values into tokenize list
                    tokenize.append(char)
                    
                #Check if the value is alphanumeric
                if char.isalpha() and apost_check == False and tokenize[len(tokenize) - 1] != None:
                    temp_char_str += char
                    
                    if char_cnt == len(item)-1:
                        tokenize.append(temp_char_str)
                        
                if char.isdigit() and apost_check == False and tokenize[len(tokenize) - 1] != None:
                    temp_char_str += char
                    
                    if char_cnt == len(item)-1:
                        tokenize.append(temp_char_str)
                    #tokenize.append(char)
                    
                if char == ".":
                    temp_char_str += char
                    
                char_cnt += 1
        
        
        print("\n")
        print("---------------------------------------")
        print(tokenize)
        print("---------------------------------------")
        
                
        
        #These values are count trackers. The first is used
        #for iterating through tokenize, the second is to 
        #count how many times we've input a table's column's input data 
        #(name of row, type)
        tokenize_iter = 0
        val_cnt = 0
        
        #This keeps track of how many columns we are selecting
        select_cnt = 0
        
        #Boolean value used to see if an open parenthesis has been used
        val_check = False
        #Boolean value used to see if keyword CREATE is used
        create_check = False
        #Boolean value used to see if keyword INSERT is used
        insert_check = False
        #Boolean value used to see if keyword SELECT is used
        select_check = False
        
        order_check = False
        
        #Used to keep track of Inserting into different rows initially
        insert_reorder_check = False
        
        append_insert_check = False
        
        #Special count used to keep track of ordering
        order_cnt = 0
        
        #Special list used for reordering
        new_val_list = []
        
        #Also used for reordering, used to hold new_val_list
        special_total_list = []
        
        #New ordering list
        new_order = []
        
        #The final list used for shuffling data in lists
        final_list = []
        
        #Goes with ordering_dict (in Table class)
        reorder_cnt = 0
        
        #Used to see if part of the columns in the table have
        #been entered
        partial_col_check = False
        
        partial_col_cnt = 0
        
        original_col_cnt = 0
        
        #Used to check if deleting item
        delete_check = False
        
        #Used to check for keyword SET BUT ONLY WITH UPDATE
        set_check = False
        
        #Used for a where in a set check
        where_set_check = False
        
        #Used for holding values that are evaluated with a where statement
        where_set_list = []
        
        #Checks for the ACTUAL SET value in the tokenize list
        real_set_check = False
        
        distinct_check = False
        
        distinct_where_check = False
        
        distinct_where_list = []
        
        #LEFT OUTER JOIN check
        loj_check = False
        
        #Used for table joining. holds left and right table names
        left_table_name = ""
        right_table_name = ""
        #Holds the actual left and right tables
        left_table = None
        right_table = None
        
        
        #Used to hold the list values when LEFT OUTER JOIN is called
        special_total_list_left = []
        special_total_list_right = []
     
        
        for item in tokenize:
            
            if real_set_check == True:
                if item == "WHERE":
                    real_set_check = False
                else: 
                    where_set_list.append(item)
                
            
            if item == "SET":
                real_set_check = True
                
                
                
            #Need to find a way to use loj in conjunction with SELECT!!!!
            if loj_check == True:
                for table_item in Database.table_list:
                    if table_item.table_name == left_table_name:
                        left_table = table_item
                    if table_item.table_name == right_table_name:
                        right_table = table_item
                        
                
                        
                
                
            if item == "LEFT":
                if tokenize[tokenize_iter+1] == "OUTER":
                    if tokenize[tokenize_iter+2] == "JOIN":
                        loj_check = True
                        
                        left_table_name = tokenize[tokenize_iter-1]
                        right_table_name = tokenize[tokenize_iter+3]
                        
                        for stuff in Database.table_list:
                            print("Table Names: ", stuff.table_name)
                            print("\n")
                
            
            if set_check == True:
                
                if "WHERE" in tokenize:
                    where_set_check = True
                    set_check = False
                    tokenize_iter += 1
                    continue
              
                col_item = ""
                change_val = ""
                
                if item == "=":
                    col_item = tokenize[tokenize_iter-1]
                    change_val = tokenize[tokenize_iter+1]
                    
                print(item)
                
                if change_val == None:
                    change_val = float("-inf")
                    
                else:
                    if change_val.isdigit():
                        change_val = int(change_val)
                        
                    elif change_val.isalpha():
                        change_val = str(change_val)
                        
                    elif "." in change_val and not change_val.isalpha():
                        change_val = float(change_val)
                    
                
                if item == None:
                    item = float("-inf")
                    
                else:
                    if item.isdigit():
                        item = int(item)
                        
                    elif item.isalpha():
                        item = str(item)
                        
                    elif "." in item and not item.isalpha():
                        item = float(item)
        
                    
            
                y = 0
                for whole_list in Tabletemp.special_value_list:
                    x = 0
                    for column in Tabletemp.column_name_list:
                        if col_item == column or col_item == str(Tabletemp.table_name + "." + column) or column == str(Tabletemp.table_name + "." + col_item):
                            
                            Tabletemp.special_value_list[y][x] = change_val
                        x += 1
                    y += 1
                
            
            
            if item == "UPDATE":
                if tokenize[tokenize_iter+1] == Tabletemp.table_name:
                    if tokenize[tokenize_iter+2] == "SET":
                        set_check = True
                        
                pass
            
            if item == "DELETE":
                delete_check = True
                if tokenize[tokenize_iter+2] == Tabletemp.table_name:
                    if len(tokenize) >= 4:
                        if tokenize[tokenize_iter+3] == "WHERE":
                            pass
                        if tokenize[tokenize_iter+3] == ";":
                            Tabletemp.special_value_list = []
                        
            
            #This if statement returns a list based on 
            #specific criteria (when a statement has
            #the term ORDER BY and it is the end of
            #the input statement, return the output list)
            if item == ";":
                Tabletemp.insert_order_list = []
                return final_list
            
            #This if statement is used for ordering
            if order_check == True and item != "BY" and item != ",":
                
                ordered_list = []
                reordered_list = []
                rev_select_check = False
                
                #Run through a reversed list to catch specific values.
                #Again, loops in loops are BAD, but for such short
                #input statements, these loops don't take much time
                for reverse_iter in reversed(tokenize):
                    
                    if reverse_iter == ",":
                        continue
                    
                    if reverse_iter == "BY":
                        rev_select_check = False
                    
                    if rev_select_check == True:
                        ordered_list.append(reverse_iter)
                    
                    if reverse_iter == ";":
                        rev_select_check = True
                
                
                reorder_cnt = 0
                Tabletemp.ordering_dict = {}
                for element in new_order:
                    
                    Tabletemp.ordering_dict[element] = reorder_cnt
                    reorder_cnt += 1
                    
                
                print(";;;;;;;;", new_order)
          
                #Used for ordering values in the SELECT columns
                for rev_item in ordered_list:
                    for element in new_order:
                        print("HERE YA ARE MY MATIE: ", element)
                        
                        #This is used to check if the item being sorted
                        #is equivalent to the table name representation
                        if rev_item == element or rev_item == str(Tabletemp.table_name + "." + element) or element == str(Tabletemp.table_name + "." + rev_item):
                            
                            print("PICKLELOAF!!!!!!")
                            
                            
                            if loj_check == True:
                                col_cnt = 0
                                for column in Database.loj_proper_columns:
                                    if column == rev_item or column == str(left_table.table_name + "." + rev_item) or rev_item == str(left_table.table_name + "." + column) or column == str(right_table.table_name + "." + rev_item) or rev_item == str(right_table.table_name + "." + column):
                                        
                                        
                                        print(final_list)
                                        print(Database.loj_proper_columns)
                                        
                                        
                                        final_list.sort(key=lambda val: none_key(val[col_cnt]))
                                        break
                                    col_cnt += 1
                                
                          
                            if distinct_where_check == True:
                                temp_list = []
                                sec_list = []
                                for element in distinct_where_list:
                                    temp_list.append(element)
                                    sec_list.append(tuple(temp_list))
                                    temp_list = []
                                
                                final_list = sec_list
                                final_list.sort(key=itemgetter(0))
                                distinct_where_check = False
                            
                            elif distinct_check == True:
                                final_list.sort(key=itemgetter(0))
                                distinct_check = False
                            
                            else:
                                col_cnt = 0
                                for column in Tabletemp.proper_columns:
                                    if column == rev_item or column == str(Tabletemp.table_name + "." + rev_item) or rev_item == str(Tabletemp.table_name + "." + column):
                                        final_list.sort(key=lambda val: none_key(val[col_cnt]))
                                        break
                                    col_cnt += 1
                                
                     
                        elif element == "*":
                            
                            if distinct_where_check == True:
                                final_list = distinct_where_list
                                final_list.sort(key=itemgetter(0))
                                distinct_where_check = False
                            
                            if distinct_check == True:
                                final_list.sort(key=itemgetter(0))
                                distinct_check = False
                            else:
                                if not Tabletemp.orig_insert_order_list:
                                    for part in Tabletemp.column_name_list:
                                        if part == rev_item or part == str(Tabletemp.table_name + "." + rev_item) or rev_item == str(Tabletemp.table_name + "." + part):
                                            
                                            x = 0
                                            for col in Tabletemp.proper_columns:
                                                if part == col:
                                                    final_list.sort(key=lambda val: none_key(val[x]))
                                                    break
                                                x += 1
                                    
                                else:
                                    for part in Tabletemp.orig_insert_order_list:
                                        
                                        if part == rev_item or part == str(Tabletemp.table_name + "." + rev_item) or rev_item == str(Tabletemp.table_name + "." + part):
                                            
                                            x = 0
                                            for col in Tabletemp.column_name_list:
                                                if part == col:
                                                    final_list.sort(key=lambda val: none_key(val[x]))
                                                    break
                                                x += 1
                                
            if item == "WHERE":
                
                temp_list = []
                
                col_item = tokenize[tokenize_iter+1]
                
                operation = tokenize[tokenize_iter+2]
                
                change_val = tokenize[tokenize_iter+3]
             
                if change_val == "NULL" or change_val == "null" or change_val == None:
                    change_val = float("-inf")
                    
                else:
                
                    if change_val.isdigit():
                        change_val = int(change_val)
                        
                    if "." in str(change_val) and not str(change_val).isalpha():
                   
                        change_val = float(change_val)
                        
                    if str(change_val).isalpha():
                        
                        change_val == str(change_val)
                        
                if distinct_where_check == True:
                    
                    dw_cnt = 0
                    for element in tokenize:
                            
                        dw_col_item = ""
                        dw_change_val = ""
                        
                        if element == "=" or element == "<" or element == ">" or element == "!=" or element == "IS":
                            
                            print(element)
                            dw_col_item = tokenize[dw_cnt-1]
                            dw_change_val = tokenize[dw_cnt+1]
                            
                            if element == "IS":
                                if tokenize[dw_cnt+1] == "NOT":
                                    dw_change_val = where_set_list[dw_cnt+2]
                                else:
                                    dw_col_item = where_set_list[dw_cnt-1]
                                    dw_change_val = where_set_list[dw_cnt+1]
                          
                        
                        if dw_change_val == None:
                            dw_change_val = float("-inf")
                            
                        else:
                            if dw_change_val.isdigit():
                                dw_change_val = int(dw_change_val)
                                
                            elif dw_change_val.isalpha():
                                dw_change_val = str(dw_change_val)
                                
                            elif "." in dw_change_val and not dw_change_val.isalpha():
                                dw_change_val = float(dw_change_val)
                        
                        if element == None:
                            element = float("-inf")
                            
                        else:
                            if element.isdigit():
                                element = int(element)
                                
                            elif element.isalpha():
                                element = str(element)
                                
                            elif "." in element and not element.isalpha():
                                element = float(element)
                               
                        y = 0
                        for whole_list in Tabletemp.special_value_list:
                            x = 0
                            for column in Tabletemp.column_name_list:
                                if Tabletemp.distinct_col == column or Tabletemp.distinct_col == str(Tabletemp.table_name + "." + column) or column == str(Tabletemp.table_name + "." + Tabletemp.distinct_col):
                                    
                                    z = 0
                                    for where_column in Tabletemp.column_name_list:
                                        if where_column == col_item or where_column == str(Tabletemp.table_name + "." + col_item) or col_item == str(Tabletemp.table_name + "." + where_column):
                                            
                                            
                                            
                                            print(col_item)
                                            
                                            if operation == "<":
                                                if Tabletemp.special_value_list[y][z] < change_val:
                                                    if(Tabletemp.special_value_list[y][x] not in distinct_where_list):
                                                            distinct_where_list.append(Tabletemp.special_value_list[y][x])
                                                    
                                                    
                                            if operation == ">":
                                                if Tabletemp.special_value_list[y][z] > change_val:
                                                    if(Tabletemp.special_value_list[y][x] not in distinct_where_list):
                                                            distinct_where_list.append(Tabletemp.special_value_list[y][x])
                                                    
                                            if operation == "=":
                                                if Tabletemp.special_value_list[y][z] == change_val:
                                                    if(Tabletemp.special_value_list[y][x] not in distinct_where_list):
                                                            distinct_where_list.append(Tabletemp.special_value_list[y][x])
                                                    
                                            if operation == "!=":
                                                if Tabletemp.special_value_list[y][z] != change_val:
                                                    if(Tabletemp.special_value_list[y][x] not in distinct_where_list):
                                                            distinct_where_list.append(Tabletemp.special_value_list[y][x])
                                                    
                                            if operation == "IS":
                                                if tokenize[tokenize_iter+3] == "NOT":
                                                    change_val = tokenize[tokenize_iter+4]
                        
                                                    if change_val == "NULL" or change_val == "null":
                                                        change_val = float("-inf")
                                                    if Tabletemp.special_value_list[y][z] != change_val:
                                                        if(Tabletemp.special_value_list[y][x] not in distinct_where_list):
                                                            distinct_where_list.append(Tabletemp.special_value_list[y][x])
                                                        
                                                else:
                                                    if Tabletemp.special_value_list[y][z] == change_val:
                                                        if(Tabletemp.special_value_list[y][x] not in distinct_where_list):
                                                            distinct_where_list.append(Tabletemp.special_value_list[y][x])
                                          
                                        z += 1
                                x += 1
                            y += 1
                        dw_cnt += 1
                    
                        
                        
                if where_set_check == True:
                    
                    #WHERE SET count
                    ws_cnt = 0
                    for element in where_set_list:
                            
                        ws_col_item = ""
                        ws_change_val = ""
                        
                        if element == "=":
                            ws_col_item = where_set_list[ws_cnt-1]
                            ws_change_val = where_set_list[ws_cnt+1]
                      
                        
                        if ws_change_val == None:
                            ws_change_val = float("-inf")
                            
                        else:
                            if ws_change_val.isdigit():
                                ws_change_val = int(ws_change_val)
                                
                            elif ws_change_val.isalpha():
                                ws_change_val = str(ws_change_val)
                                
                            elif "." in ws_change_val and not ws_change_val.isalpha():
                                ws_change_val = float(ws_change_val)
                        
                        if element == None:
                            element = float("-inf")
                            
                        else:
                            if element.isdigit():
                                element = int(element)
                                
                            elif element.isalpha():
                                element = str(element)
                                
                            elif "." in element and not element.isalpha():
                                element = float(element)
                               
                        y = 0
                        for whole_list in Tabletemp.special_value_list:
                            x = 0
                            for column in Tabletemp.column_name_list:
                                if ws_col_item == column or ws_col_item == str(Tabletemp.table_name + "." + column) or column == str(Tabletemp.table_name + "." + ws_col_item):
                                    
                                    z = 0
                                    for where_column in Tabletemp.column_name_list:
                                        if where_column == col_item or where_column == str(Tabletemp.table_name + "." + col_item) or col_item == str(Tabletemp.table_name + "." + where_column):
                                            if operation == "<":
                                                if Tabletemp.special_value_list[y][z] < change_val:
                                                    Tabletemp.special_value_list[y][x] = ws_change_val
                                                    
                                            if operation == ">":
                                                if Tabletemp.special_value_list[y][z] > change_val:
                                                    Tabletemp.special_value_list[y][x] = ws_change_val
                                            if operation == "=":
                                                if Tabletemp.special_value_list[y][z] == change_val:
                                                    Tabletemp.special_value_list[y][x] = ws_change_val
                                            if operation == "!=":
                                                if Tabletemp.special_value_list[y][z] != change_val:
                                                    Tabletemp.special_value_list[y][x] = ws_change_val
                                            if operation == "IS":
                                                if tokenize[tokenize_iter+3] == "NOT":
                                                    change_val = tokenize[tokenize_iter+4]
                        
                                                    if change_val == "NULL" or change_val == "null":
                                                        change_val = float("-inf")
                                                    if Tabletemp.special_value_list[y][z] != change_val:
                                                        Tabletemp.special_value_list[y][x] = ws_change_val
                                                else:
                                                    if Tabletemp.special_value_list[y][z] == change_val:
                                                        Tabletemp.special_value_list[y][x] = ws_change_val
                                          
                                        z += 1
                                x += 1
                            y += 1
                        ws_cnt += 1
                    where_set_check = False
                    where_set_list = []
                        
                if delete_check == True:
                    
                    if operation == ">":
                        y = 0
                        for whole_list in Tabletemp.special_value_list:
                            x = 0
                            for column in Tabletemp.column_name_list:
                                if col_item == column or col_item == str(Tabletemp.table_name + "." + column) or column == str(Tabletemp.table_name + "." + col_item):
                                    if Tabletemp.special_value_list[y][x] == None:
                                        pass
                                    else:
                                        if Tabletemp.special_value_list[y][x] > change_val:
                                            temp_list.append(Tabletemp.special_value_list[y])
                                x += 1
                            y += 1
                    if operation == "<":
                        y = 0
                        for whole_list in Tabletemp.special_value_list:
                            x = 0
                            for column in Tabletemp.column_name_list:
                                if col_item == column or col_item == str(Tabletemp.table_name + "." + column) or column == str(Tabletemp.table_name + "." + col_item):
                                    if Tabletemp.special_value_list[y][x] == None:
                                        pass
                                    else:
                                        if Tabletemp.special_value_list[y][x] < change_val:
                                            temp_list.append(Tabletemp.special_value_list[y])
                                x += 1
                            y += 1
                    if operation == "IS":
                        if tokenize[tokenize_iter+3] == "NOT":
                            y = 0
                            for whole_list in Tabletemp.special_value_list:
                                x = 0
                                for column in Tabletemp.column_name_list:
                                    if col_item == column or col_item == str(Tabletemp.table_name + "." + column) or column == str(Tabletemp.table_name + "." + col_item):
                                        if Tabletemp.special_value_list[y][x] == None:
                                            if None != change_val:
                                                temp_list.append(Tabletemp.special_value_list[y])
                                        else:
                                            if Tabletemp.special_value_list[y][x] != change_val:
                                                temp_list.append(Tabletemp.special_value_list[y])
                                    x += 1
                                y += 1
                        else:
                            change_val = tokenize[tokenize_iter+3]
                            print(temp_list)
                            y = 0
                            for whole_list in Tabletemp.special_value_list:
                                x = 0
                                for column in Tabletemp.column_name_list:
                                    if col_item == column or col_item == str(Tabletemp.table_name + "." + column) or column == str(Tabletemp.table_name + "." + col_item):
                                        if Tabletemp.special_value_list[y][x] == None:
                                            if None == change_val:
                                                temp_list.append(Tabletemp.special_value_list[y])
                                        else:
                                            if Tabletemp.special_value_list[y][x] == change_val:
                                                temp_list.append(Tabletemp.special_value_list[y])
                                    x += 1
                                y += 1
                    
                    if operation == "=":
                        y = 0
                        for whole_list in Tabletemp.special_value_list:
                            x = 0
                            for column in Tabletemp.column_name_list:
                                if col_item == column or col_item == str(Tabletemp.table_name + "." + column) or column == str(Tabletemp.table_name + "." + col_item):
                                    if Tabletemp.special_value_list[y][x] == None:
                                        if None == change_val:
                                            temp_list.append(Tabletemp.special_value_list[y])
                                    else:
                                        if Tabletemp.special_value_list[y][x] == change_val:
                                            temp_list.append(Tabletemp.special_value_list[y])
                                x += 1
                            y += 1
                            
                    if operation == "!=":
                            y = 0
                            for whole_list in Tabletemp.special_value_list:
                                x = 0
                                for column in Tabletemp.column_name_list:
                                    if col_item == column or col_item == str(Tabletemp.table_name + "." + column) or column == str(Tabletemp.table_name + "." + col_item):
                                        if Tabletemp.special_value_list[y][x] == None:
                                            if None != change_val:
                                                temp_list.append(Tabletemp.special_value_list[y])
                                        else:
                                            if Tabletemp.special_value_list[y][x] != change_val:
                                                temp_list.append(Tabletemp.special_value_list[y])
                                    x += 1
                                y += 1
                    
                         
                    new_list = []
                    delete_cnt = 0
                    for value in Tabletemp.special_value_list:
                        if value not in temp_list:
                            new_list.append(value)
                    delete_cnt = len(Tabletemp.special_value_list) - len(new_list)
                    Tabletemp.special_value_list = new_list
                    
                    
                else:
                    if operation == ">":
                        
                        y = 0
                        for whole_list in final_list:
                            x = 0
                            for column in Tabletemp.column_name_list:
                                if col_item == column or col_item == str(Tabletemp.table_name + "." + column) or column == str(Tabletemp.table_name + "." + col_item):
                                    if final_list[y][x] == None:
                                        if float("-inf") > change_val:
                                            temp_list.append(final_list[y])
                                    else:
                                        if final_list[y][x] > change_val:
                                            temp_list.append(final_list[y])
                                x += 1
                            y += 1
                                    
                    if operation == "<":
                        
                        y = 0
                        for whole_list in final_list:
                            x = 0
                            for column in Tabletemp.column_name_list:
                                if col_item == column or col_item == str(Tabletemp.table_name + "." + column) or column == str(Tabletemp.table_name + "." + col_item):
                                    if final_list[y][x] == None:
                                        if float("-inf") < change_val:
                                            temp_list.append(final_list[y])
                                    else:
                                        if final_list[y][x] < change_val:
                                            temp_list.append(final_list[y])
                                x += 1
                            y += 1
                        
                        
                    if operation == "IS":
                        if tokenize[tokenize_iter+3] == "NOT":
                            
                            change_val = tokenize[tokenize_iter+4]
                            
                            if change_val == "NULL" or change_val == "null":
                                change_val = float("-inf")
                            
                            y = 0
                            for whole_list in final_list:
                                x = 0
                                for column in Tabletemp.column_name_list:
                                    if col_item == column or col_item == str(Tabletemp.table_name + "." + column) or column == str(Tabletemp.table_name + "." + col_item):
                                        if final_list[y][x] == None:
                                            if float("-inf") != change_val:
                                                temp_list.append(final_list[y])
                                        else:
                                            if final_list[y][x] != change_val:
                                                temp_list.append(final_list[y])
                                    x += 1
                                y += 1
                        
                        else:
                            y = 0
                            for whole_list in final_list:
                                x = 0
                                for column in Tabletemp.column_name_list:
                                    if col_item == column or col_item == str(Tabletemp.table_name + "." + column) or column == str(Tabletemp.table_name + "." + col_item):
                                        if final_list[y][x] == None:
                                            if float("-inf") == change_val:
                                                temp_list.append(final_list[y])
                                        else:
                                            if final_list[y][x] == change_val:
                                                temp_list.append(final_list[y])
                                    x += 1
                                y += 1
                            
                            
                    if operation == "=":
                        y = 0
                        for whole_list in final_list:
                            x = 0
                            for column in Tabletemp.column_name_list:
                                if col_item == column or col_item == str(Tabletemp.table_name + "." + column) or column == str(Tabletemp.table_name + "." + col_item):
                                    if final_list[y][x] == None:
                                        if float("-inf") == change_val:
                                            temp_list.append(final_list[y])
                                    else:
                                        if final_list[y][x] == change_val:
                                            temp_list.append(final_list[y])
                                x += 1
                            y += 1
                        
                        
                    if operation == "!=":
                        y = 0
                        for whole_list in final_list:
                            x = 0
                            for column in Tabletemp.column_name_list:
                                if col_item == column or col_item == str(Tabletemp.table_name + "." + column) or column == str(Tabletemp.table_name + "." + col_item):
                                    if final_list[y][x] == None:
                                        if float("-inf") != change_val:
                                            temp_list.append(final_list[y])
                                    else:
                                        if final_list[y][x] != change_val:
                                            temp_list.append(final_list[y])
                                x += 1
                            y += 1
                    
                    final_list = temp_list
            
            #Turn off value check when end parenthesis is found
            #Also turns off a lot of other boolean checks
            if item == ")":
                val_check = False
                create_check = False
                
                if insert_check == True:
                    
                    if insert_reorder_check == True:
                        if len(Tabletemp.insert_order_list) < len(Tabletemp.column_name_list):
                            
                            partial_col_check = True
                            
                            for element in Tabletemp.column_name_list:
                                print(element)
                                if element not in Tabletemp.insert_order_list:
                                    Tabletemp.insert_order_list.append(element)
                                    partial_col_cnt += 1
                                    #Used for multiple inserted column values
                                    original_col_cnt += 1
                            
                        
                            
                        insert_reorder_check = False
                        tokenize_iter += 1
                        continue
                    
                    if append_insert_check == True:
                        
                        
                        if partial_col_check == True:
                            while partial_col_cnt > 0:
                                Tabletemp.insert_col_val_list.append(None)
                                Tabletemp.value_list.append([])
                                partial_col_cnt -= 1
                      
        
                        if len(Tabletemp.value_list) < len(Tabletemp.insert_order_list):
                            Tabletemp.value_list.append([])
                            Tabletemp.insert_col_val_list.append(None)
                        
              
                        y = 0
                        for element in Tabletemp.insert_order_list:
                            
                            x = 0
                            for col in Tabletemp.column_name_list:
                                if element == col:
                                    Tabletemp.value_list[x].append(Tabletemp.insert_col_val_list[y])
                                x += 1
                            y += 1
                            
                        
                        ##BRAND New Stuff
                        Tabletemp.insert_col_val_list = []
                        
                        
                       
                        temp_list = []
                        for value in Tabletemp.value_list:
                            temp_list.append(value[0])
                            
                        Tabletemp.clear_value_list()
                        
                        for value in temp_list:
                            
                            if value is None:
                                Tabletemp.values(value)
                                continue
                            
                            if value[0] == "-":
                                if len(value) > 1:
                                    if value[1:].isdigit():
                                        if "." in value:
                                            Tabltemp.values(float(value))
                                        else:
                                            Tabletemp.values(int(value))
                            
                            if value.isdigit():
                                Tabletemp.values(int(value))
                            
                            if value.isalpha():
                                Tabletemp.values(str(value))
                                
                            if "'" in value and value.count("'") >= 1:
                                Tabletemp.values(str(value))
                                
                            if " " in value and "'" not in value:
                                Tabletemp.values(value)
                                
                            if ("." in value) and not value.isalpha():
                                Tabletemp.values(float(value))
                            
                        append_insert_check = False
                 
                    Tabletemp.special_value_list.append(Tabletemp.value_list)
                    
                    
                    Tabletemp.col_holder.append(Tabletemp.value_list)
                    Tabletemp.clear_value_list()
            
                    insert_check = False
                    
                    
            #This if statement is used for detecting open parenthesis
            if val_check == True:
                
                if item == ",":
                    val_cnt -= 1
                    
                #Catch specific values for the column names/types
                if create_check == True and val_cnt != 1 and item != ",":
                    
                    if val_cnt == 2:
                        val_cnt = 0
                    
                    Tabletemp.column_type(item, tokenize[tokenize_iter+1])
                    Tabletemp.column_name_list.append(item)
                    
                
                #Catch specific values for inserting into the table
                elif insert_check == True:
                    
                    #Used for the second part of inserting specific column
                    #values
                    if append_insert_check == True:
                        if item == "(":
                            tokenize_iter += 1
                            continue
                        if item == ",":
                            tokenize_iter += 1
                            continue
                        Tabletemp.insert_col_val_list.append(item)
                        Tabletemp.value_list.append([])
                        tokenize_iter += 1
                        continue
                            
                                
                    #First part of column sorting
                    if insert_reorder_check == True:
                        if item == ",":
                            tokenize_iter += 1
                            continue
                        Tabletemp.insert_order_list.append(item)
                        Tabletemp.orig_insert_order_list.append(item)
                        tokenize_iter += 1
                        continue
                    
                    print(tokenize[tokenize_iter-2])
                    if tokenize[tokenize_iter-2] == Tabletemp.table_name:
                        
                        #Set flag here for the next time you find an open
                        #parenthesis
                        insert_reorder_check = True
                        
                        Tabletemp.insert_order_list.append(item)
                        Tabletemp.orig_insert_order_list.append(item)
                        Tabletemp.column_name_list
                        tokenize_iter += 1
                        continue
                    
                    if item is None:
                        Tabletemp.values(item)
                        tokenize_iter += 1
                        continue
                    
                    if item[0] == "-":
                        if len(item) > 1:
                            if item[1:].isdigit():
                                if "." in item:
                                    Tabltemp.values(float(item))
                                else:
                                    Tabletemp.values(int(item))
                    
                    if item.isdigit():
                        Tabletemp.values(int(item))
                    
                    if item.isalpha() or item.replace(".", "").isalpha():
                        Tabletemp.values(str(item))
                        
                        
                    if "'" in item and item.count("'") >= 1:
                        Tabletemp.values(str(item))
                        
                    if " " in item and "'" not in item:
                        Tabletemp.values(item)
                        
                    if ("." in item) and not item.replace(".","").replace(" ","").isalpha():
                        print(item.replace(".",""))
                        Tabletemp.values(float(item))
                        
                    if item.isalnum() and not item.isalpha() and not item.isdigit():
                        Tabletemp.values(str(item))
                        
                        
                    Tabletemp.full_entry_list.append(Tabletemp.table_name_list)
                    Tabletemp.full_entry_list.append(Tabletemp.column_total_list)
                    Tabletemp.full_entry_list.append(Tabletemp.total_value_list)
             
                val_cnt += 1

            
            #If statement for keyword FROM
            #Also turns off keyword SELECT's boolean check
            if item == "FROM":
                
                if loj_check == True:
                    print("Popsickles")
                    on_index = tokenize.index("ON")
                    
                    #Checks for the equal sign, creates comparison values
                    if tokenize[on_index + 2] == "=":
                        left_table_comp_col = tokenize[on_index+1]
                        right_table_comp_col = tokenize[on_index+3]
                        
                        
                        left_compare = None
                        right_compare = None
                        
                        proper_dict = dict()
                    
                        proper_list = []
                        completed_list = []
                    
                    
                    
                   
                   
                    left_col_cnt = 0
                    for column_name in left_table.column_name_list:
                        if column_name == left_table_comp_col or column_name == str(left_table.table_name + "." + left_table_comp_col) or left_table_comp_col == str(left_table.table_name + "." + column_name):
                            left_compare = left_col_cnt
                        left_col_cnt += 1
                        
                        
                    right_col_cnt = 0
                    for column_name in right_table.column_name_list:
                        if column_name == right_table_comp_col or column_name == str(right_table.table_name + "." + right_table_comp_col) or right_table_comp_col == str(right_table.table_name + "." + column_name):
                            right_compare = right_col_cnt
                        left_col_cnt += 1
                    
                    
                    y = 0
                    for left in left_table.special_value_list:
                        x = 0
                        for right in right_table.special_value_list:
                            if left[left_compare] == right[right_compare]:
                                
                                for prop_col in Database.loj_proper_columns:
                                    
                                    l_cnt = 0
                                    for left_col in left_table.column_name_list:
                                        if prop_col == left_col or prop_col == str(left_table.table_name + "." + left_col) or left_col == str(left_table.table_name + "." + prop_col):
                                            
                                            
                                            proper_list.append(left_table.special_value_list[y][l_cnt]) 
                                        l_cnt += 1
                                        
                                    r_cnt = 0    
                                    for right_col in right_table.column_name_list:
                                        if prop_col == right_col or prop_col == str(right_table.table_name + "." + right_col) or right_col == str(right_table.table_name + "." + prop_col):
                                            
                                            
                                            proper_list.append(right_table.special_value_list[x][r_cnt])
                                        r_cnt += 1
                                        
                                special_total_list.append(proper_list)
                                proper_list = []
                            x += 1
                        y += 1    
                    
                    
                    
                    for element in special_total_list:
                        final_list.append(tuple(element))
                
                
                else:
                    for element in special_total_list:
                        final_list.append(tuple(element))
         
                select_check = False
                
            #This if statement is used for keyword SELECT
            if select_check == True:
                
                
                if "LEFT" in tokenize and "OUTER" in tokenize and "JOIN" in tokenize:
                    
                    if item == ",":
                        pass
                    else:
                        new_order.append(item)
                        Database.loj_proper_columns.append(item)
                    
                    
                    
                    
                    loj_check = True
                    
                    
                    l_table_index = tokenize.index("LEFT") - 1
                    r_table_index = tokenize.index("JOIN") + 1
                    left_table_name = tokenize[l_table_index]
                    right_table_name = tokenize[r_table_index]
                    
                    if loj_check == True:
                        for table_item in Database.table_list:
                            if table_item.table_name == left_table_name:
                                left_table = table_item
                            if table_item.table_name == right_table_name:
                                right_table = table_item
                                
             
                
                elif item == "DISTINCT":
                    
                    Tabletemp.distinct_col = tokenize[tokenize_iter+1]
                    distinct_list = []
                    distinct_where_list = []
                    
                    if "WHERE" not in tokenize:
                        distinct_check = True
                        
                    else:
                        distinct_where_check = True
                        
                      
                    if distinct_check == True:
                        if Tabletemp.special_value_list:
                            y = 0
                            for entry in Tabletemp.special_value_list:
                                x = 0
                                for col in Tabletemp.column_name_list:
                                    if Tabletemp.distinct_col == col or Tabletemp.distinct_col == str(Tabletemp.table_name + "." + col) or col == str(Tabletemp.table_name + "." + Tabletemp.distinct_col):
                                        
                                            list_temp = []
                                                
                                            temp_val = Tabletemp.special_value_list[y][x]
                                                
                                            list_temp.append(temp_val)
                                        
                                            if list_temp[0] not in distinct_list:
                                                special_total_list.append([])
                                                tup_val = list_temp[0]
                                                distinct_list.append(list_temp[0])
                                                list_temp = []
                                    x += 1
                                y += 1  
                            
                    print(special_total_list)
                    Tabletemp.distinct_value_list = distinct_list
                    
                
                    
                else:
                    
                    if item == ",":
                        pass
                    else:
                        new_order.append(item)
                        
            
                    if item == "*":
                        if Tabletemp.special_value_list:
                            place = 0
                            for entry in Tabletemp.special_value_list:
                                if special_total_list == []:
                                    #Finds the length of the list
                                    col_len = len(Tabletemp.col_holder)
                                    x = 0
                                    for val in Tabletemp.col_holder:
                                        if x == len(Tabletemp.col_holder):
                                            break
                                        special_total_list.append([])
                                        x += 1
                                
                               
                                for single in entry:
                                    if special_total_list:
                                        special_total_list[place].append(single)
                                        print("your spec: ", special_total_list)
                                place += 1
                            tokenize_iter += 1
                            
                            while [] in special_total_list:
                                special_total_list.remove([])
                        
                        for column in Tabletemp.column_name_list:
                            Tabletemp.proper_columns.append(column)
                        continue
                
                
                
                
                #This is a powerful (though slightly messy) sort
                #which creates a new list, and appends values from 
                #the unordered list, into the correct order based
                #off the column names
                if distinct_check == True:
                    for element in Tabletemp.full_entry_list[1]:
                        
                        if element[0] == item or item == str(Tabletemp.table_name + "." + element[0]) or element[0] == str(Tabletemp.table_name + "." + item):
                            
                            place = 0
                            for entry in Tabletemp.distinct_value_list:
                                special_total_list[place].append(entry)
                                place += 1
                            Tabletemp.proper_columns.append(item)
                            
                    tokenize_iter += 1
                    continue
               
                
                elif distinct_where_check == True:
                    tokenize_iter += 1
                    continue
                 
                elif loj_check == True:
                    tokenize_iter += 1
                    continue 
                    
                        
                else:
                    if special_total_list:
                        select_cnt = 0
                        for element in Tabletemp.full_entry_list[1]:
                            
                            if element[0] == item or item == str(Tabletemp.table_name + "." + element[0]) or element[0] == str(Tabletemp.table_name + "." + item):
                                
                                place = 0
                                for entry in Tabletemp.special_value_list:
                                    special_total_list[place].append(entry[select_cnt])
                                    place += 1
                                Tabletemp.proper_columns.append(item)
                                
                            select_cnt += 1
                        tokenize_iter += 1
                        continue
                    
                    
                    #This is the first part of the sort (mentioned above).
                    #This part of the sort actually starts adding data to 
                    #the initial list. The rest of the sort (above) appends
                    #data to the new list here
                    select_cnt = 0
                    for element in Tabletemp.full_entry_list[1]:
                        if element[0] == item or item == str(Tabletemp.table_name + "." + element[0]) or element[0] == str(Tabletemp.table_name + "." + item):
                            for entry in Tabletemp.special_value_list:
                                new_val_list.append(entry[select_cnt])
                                special_total_list.append(new_val_list)
                                new_val_list = []
                                pass
    
                        select_cnt += 1
                    Tabletemp.proper_columns.append(item)
                    
            #Sets order check for keyword ORDER
            if item == "ORDER":
                if tokenize[tokenize_iter+1] == "BY":
                    order_check = True
                    
                
            #Sets create check for keyword CREATE
            if item == "CREATE":
                if tokenize[tokenize_iter+1] == "TABLE":
                    database.table_list.append(Table(str(tokenize[tokenize_iter+2])))
                
                    for table_itemizer in database.table_list:
                        if table_itemizer.table_name == tokenize[tokenize_iter+2]:
                            Tabletemp = table_itemizer
                   
                    create_check = True
                    
            #Sets insert check for keyword CREATE
            if item == "INSERT":
                if tokenize[tokenize_iter+1] == "INTO":
                    
                    for tableiter in database.table_list:
                        if tableiter.table_name == tokenize[tokenize_iter+2]:
                
                            Tabletemp = tableiter
                            insert_check = True
                            continue
                        
            #Sets select check for keyword SELECT          
            if item == "SELECT":
                token_cnt = 0
                for item in tokenize:
                    if item == "FROM":
                        for tableiter in database.table_list:
                            if tableiter.table_name == tokenize[token_cnt+1]:
                                Tabletemp = tableiter
                    token_cnt += 1
                select_check = True
                            
            #Open parenthesis sets val_check (value check)
            #for data input
            if item == "(":
                
                if tokenize[tokenize_iter+1] == None:
                    val_check = True
                    tokenize_iter += 1
                    continue
                
                if tokenize[tokenize_iter+1].isalnum() or \
                    tokenize[tokenize_iter+1].isdigit():
                        val_check = True
                      
                if "." in tokenize[tokenize_iter+1]:
                    val_check = True
                
                if Tabletemp.insert_order_list:
                    val_check = True
                    append_insert_check = True
            
            
            if item == ",":
                if tokenize[tokenize_iter+1] == "(":
                    if Tabletemp.insert_order_list:
                        val_check = True
                        append_insert_check = True
                        insert_check = True
                        partial_col_cnt = original_col_cnt
                    else:
                        val_check = True
                        insert_check = True
                
            tokenize_iter += 1
                



    def close(self):
        """
        Empty method that will be used in future projects
        """
        pass


def connect(filename):
    """
    Creates a Connection object with the given filename
    """
    return Connection(filename)


class Database:
    #The Database class has a subtle but VERY important
    #feature: it holds the Table class instances. This
    #is important because without this class, data would
    #be overwritten
    table_list = []
    
    #In this database, we'll also put the proper column table for
    #LEFT OUTER JOIN because this is the place where many tables
    #are stored
    
    loj_proper_columns = []
    
    pass


#The Table class is another crucial class to this program.
#This class holds all of the Table instance data. Without it,
#manipulation of the input data would become significantly harder
class Table(object):
    
    #Initializer for the table
    def __init__(self, tables_name):
        
        self.table_name = ""
        
        self.table_name = str(tables_name)
        self.table_name_list = []
        self.column_total_list = []
        self.column_part_list = []
        self.value_list = []
        self.value_tuple = ()
        self.total_value_list = []
        self.special_value_list = []
        self.full_entry_list = []
        
        #A dictionary used to hold ordered data
        self.ordering_dict = {}
        
        self.column_name_list = []
        
        #This list (which should have initially been made a dictionary)
        #is used to contain the column values for the items in the final_list
        self.proper_columns = []
        
        self.col_holder = []
        
        self.insert_order_list = []
        self.insert_col_val_list = []
        
        self.orig_insert_order_list = []
        
        self.distinct_value_list = []
        
    
    
    #A special function used to clear the value list within
    #the table. This provides an easier way to manipulate data
    def clear_value_list(self):
        self.value_list = []
        return self.value_list
    
    #Holds name of table
    def name(self, tabled_name):
        
        self.table_name = tabled_name
        return self.table_name
        
    #Holds column name and column type
    def column_type(self, col_name, col_type):

        self.column_part_list.append(col_name)
        self.column_part_list.append(col_type)
        
        self.column_total_list.append(self.column_part_list)
        self.column_part_list = []
        
        return self.column_total_list
    
    #Holds all of the input values within columns
    def values(self, value):
        
        self.value_list.append(value)
        return self.value_list
        
    pass
