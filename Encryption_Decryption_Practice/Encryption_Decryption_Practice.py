import random

letters = ["a b c d e f g h i j k l m n o p q r s t u v w x y z"]




def main():
    user_inp = str(input("Please enter a password: "))

    encrypted_set = Encryption(user_inp)
    encrypted_password = encrypted_set[0]
    pass_key = encrypted_set[1]
    decrypted_word = Decryption(encrypted_password, pass_key)

    failed_attempt = Failed_Decryption(encrypted_password)

    #plaintext = Decryption(encrypted_password)
    #print("Enc: ", encrypted_password)
    #print("Plain: ", plaintext)
    
    


def Encryption(password):

    encrypted_word = ""

    for letter in password:
        encrypted_word += str(ord(letter)) + " "

    #Split the encrypted word by spacing into a list. Convert to binary.
    #Perform operation on binary. Spit out encrypted output.
    encrypted_letter_list = encrypted_word.split()

    new_string = "".join(["{0:b}".format(int(letter)) for letter in encrypted_letter_list])


    test_string = new_string

    #Here's how we're going to implement this encryption. Select a random number
    #from 0 to the length of the string. Use a for loop to iterate through the entire
    #string. On each character in the string, swap the current character with the
    #character position which was randomly generated. perform the swap to generate
    #an encrypted message.


    encrypted_string = ""
    encryption_key = ""



    i = 0
    for char in new_string:
        rand_num = random.randrange(0, len(new_string))
        temp_char = new_string[i]

        switch_string = list(new_string)
        switch_string[i] = new_string[rand_num]
        switch_string[rand_num] = temp_char
        switch_string = "".join(switch_string)


        
        #switch_string = new_string[:i] + new_string[rand_num] + new_string[i+1:]
        #switch_string = switch_string[:rand_num] + temp_char + switch_string[rand_num+1:]
        new_string = switch_string
        encryption_key += str(rand_num) + " "
        i = i + 1
        

  

    cipher_key_pair = [new_string, encryption_key]

    return cipher_key_pair



def Failed_Decryption(cipher):
    
    craft_word = ""
    i = 0
    for element in cipher:
        if (i != 0) and (i%7 == 0):
            craft_word += " "

        craft_word += element
            
        i = i + 1


    testing = craft_word.split()
    decrypted_word = []
    for t in testing:
        decrypted_word.append(chr(int(t,2)))

    decrypted_word = "".join(decrypted_word)

    print("\n")
    print("THIS IS YOUR DECRYPTED WORD!!!!-----> ", decrypted_word)
    
 


def Decryption(cipher, encryption_key):


    listed_key = encryption_key.split()
    
    listed_key.reverse()

    new_key_list = []
    
    for key in listed_key:
        new_key_list.append(int(key))
    reversed_key = new_key_list
    

 

    # Use i as the end index of the cipher (decrypt in reverse)
    end_i = len(cipher)-1
    for num in reversed_key:
        temp_char = cipher[end_i]
        switch_string = list(cipher)
        switch_string[end_i] = cipher[num]
        switch_string[num] = temp_char
        switch_string = "".join(switch_string)
        cipher = switch_string
        end_i = end_i - 1

    craft_word = ""
    i = 0
    for element in switch_string:
        if (i != 0) and (i%7 == 0):
            craft_word += " "

        craft_word += element
            
        i = i + 1

    
    testing = craft_word.split()
    decrypted_word = []
    for t in testing:
        decrypted_word.append(chr(int(t,2)))

    decrypted_word = "".join(decrypted_word)

    print("\n")
    print("Actual Decryption: ", decrypted_word)
        
    
            
    

main()
    
