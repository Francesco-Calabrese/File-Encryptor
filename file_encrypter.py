import os
import sys
from tkinter import *

def open_file_and_rot(file_location, encrypt_flag):
    '''This method takes in 2 parameters, the file location to encrypt/decrypt
    and the encryption flag. Using ROT13, the method encrypts or decrypts the
    file supplied in the argument.
    '''

    with open(file_location, "r+b") as file:

        # if the file does not produce an error (not in use)
        try:            
            
            data = file.read()          
            file_write = open(file_location, "wb")          

            rotted_string = bytes(0)

            # goes through each item from the read file
            for item in data:           
                if encrypt_flag:  # if encrypt is chosen
                    rotted_value = item + 13
                else:  # if decryption is chosen
                    rotted_value = item - 13

                # if the end of the ascii table is reached
                if rotted_value > 255:  
                    rotted_value = rotted_value - 256  # returns to beginning
                
                # if numbers are before the beginning of the ascii table 
                if rotted_value < 0:  
                    rotted_value = 256 + rotted_value  # moves to the end

                rotted_string += rotted_value.to_bytes(1, "big")

            # overwrites the file with the rotated values
            file_write.write(rotted_string)         

            file.close() 
            file_write.close() 

            # prints that encryption or decryption has completed
            if encrypt_flag:            
                print("File Encrypted!", file_location)
            else:
                print("File Decrypted!", file_location)

        except:  # on error continue
            pass

def get_file(encryption_flag):
    '''This method takes the encrypton flag as an argument and recursively
    gets every file in the file structure. Each file is fed into the 
    open_file_and_rot method with the path of the file and the encryption
    flag. Once there are no more directories the method ends.
    '''
    
    global stack
    global current_dir

    # gets the list of items in the directory
    items_in_directory = os.listdir()      

    for item in items_in_directory:
        # sets the path for each item in the directory
        path = current_dir + "\\" + item        
        # checks to see if the item is a directory
        if os.path.isdir(path): 
            # change directory to new path 
            os.chdir(path)  
            # sets the new working directory
            current_dir = os.getcwd()  
            # adds the directory to the "stack"
            stack.append(current_dir)  
            # uses recursion to get more files
            get_file(encryption_flag)  
        else:  # the items is not a directory
            # opens the file and encrypts/decrypts
            open_file_and_rot(path, encrypt_flag)          
            continue
    # no more files/folders in the path, removes the top directory
    stack.pop()         
    if len(stack) > 0:  # while the stack is not empty
        # changes the directory to the top item on the stack
        current_dir = stack[len(stack)-1]           

def set_encrypt():
    '''Sets the encryption flag to true to encrypt files.'''

    global encrypt_flag
    encrypt_flag = True
    
def set_decrypt():
    '''Sets the encryption flag to false to decrypt files.'''

    global encrypt_flag
    encrypt_flag = False

def on_button_click():
    '''Checks that a location has been added and either encrypt or decrypt has
    been selected. Sets the root directory for the encryption/decryption 
    process.
    '''

    global root_directory
    global encrypt_flag

    # gets the directory set by the user in the entry box
    root_directory = root_dir.get()         

    # checks the user entered a value
    if root_directory != "":  
         # checks the user selected encryption or decryption
        if encrypt_flag == "": 
            # if encryption or decryption not set, closes the program
            sys.exit("Select encrypt or decrypt. Exiting.")         
    else:
        # if no location set, exits the program
        sys.exit("Enter a location to start. Exiting.")         

    window.destroy()  # closes the window
    

encrypt_flag = ""  # sets encryption flag to empty
root_directory = ""  # sets the root directory to empty

# uses tkinter to create a window with an entry box, button, and radiobuttons
window = Tk()
radio = IntVar()
window.geometry('300x200')
window.eval('tk::PlaceWindow . center')
window.title('Encrypt/Decrypt Files')
radio1 = Radiobutton(window, text='Encrypt Files', variable=radio, value=1, 
    command=lambda: set_encrypt()).pack(anchor=W)
radio2 = Radiobutton(window, text='Decrypt Files', variable=radio, value=2, 
    command=lambda: set_decrypt()).pack(anchor=W)
location_label = Label(window, text="Enter a location to start").pack()
root_dir = Entry(window, width=40)
root_dir.pack()
button = Button(window, text='Start', width=25, command=on_button_click)
button.pack()
window.mainloop()

try:
    # sets the top directory to begin the file search
    os.chdir(root_directory)            

    # sets the current working directory
    current_dir = os.getcwd()           

    stack = []
    # adds the current directory to the stack
    stack.append(current_dir)           
                
    # starts the process of recursively getting every file from the cwd
    get_file(encrypt_flag)          

    if encrypt_flag:
        print("All files have been encrypted!")
    else:
        print("All files have been decrypted!")
except:
    print("location does not exist")
