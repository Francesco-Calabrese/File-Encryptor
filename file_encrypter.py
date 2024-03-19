import os
import sys
from tkinter import *

def open_file_and_rot(file_location, encrypt_flag):
    '''This method takes in 2 parameters, the file location to encrypt/decrypt
    and the encryption flag. Using ROT13, the method encrypts or decrypts the
    file supplied in the argument.
    '''

    with open(file_location, "r+b") as file:

        try:            # if the file does not produce an error (not in use)
            data = file.read()          # reads the file and saves it as data
            file_write = open(file_location, "wb")          # overwrites the file and saves it as file_write

            rotted_string = bytes(0)            # initalizes a string for the rotted data

            for item in data:           # goes through each item from the read file
                if encrypt_flag:            # if encrypt is chosen
                    rotted_value = item + 13            # adds 13 to the decimal value
                else:           # decryption is chosen
                    rotted_value = item - 13            # subtracts 13 from the decimal value

                if rotted_value > 255:          # if the end of the ascii table is reached
                    rotted_value = rotted_value - 256           # start back from the beginning
                
                if rotted_value < 0:            # if numbers before the beginning of the ascii table are reached
                    rotted_value = 256 + rotted_value           # move to the end

                rotted_string += rotted_value.to_bytes(1, "big")            # addes the rotated value

            file_write.write(rotted_string)         # overwrites the file with the rotated values

            file.close()            # closes the reading file
            file_write.close()      # closes the writing file

            if encrypt_flag:            # prints that encryption or decryption has completed
                print("File Encrypted!", file_location)
            else:
                print("File Decrypted!", file_location)

        except:         # on error continue
            pass

def get_file(encryption_flag):
    '''This method takes the encrypton flag as an argument and recursively gets every file in the file structure. 
    Each file is fed into the open_file_and_rot method with the path of the file and the encryption flag. Once 
    there are no more directories the method ends.
    '''
    
    global stack
    global current_dir

    items_in_directory = os.listdir()       # gets the list of items in the directory

    for item in items_in_directory:
        path = current_dir + "\\" + item        # sets the path for each item in the directory
        if os.path.isdir(path):         # checks to see if the item is a directory
            os.chdir(path)          # if so, changes directory to the new directory found
            current_dir = os.getcwd()           # sets the current working directory
            stack.append(current_dir)           # adds the directory to the "stack"
            get_file(encryption_flag)           # calls uses recursion to follow this same process
        else:           # the items is not a directory
            open_file_and_rot(path, encrypt_flag)          # opens the file and encrypts/decrypts
            continue
    stack.pop()         # when there are no longer any files/folders in the path, removes the top directory
    if len(stack) > 0:          # while the stack is not empty
        current_dir = stack[len(stack)-1]           # changes the directory to the top item on the stack

def set_encrypt():
    '''Sets the encryption flag to true to encrypt files.'''

    global encrypt_flag
    encrypt_flag = True
    
def set_decrypt():
    '''Sets the encryption flag to false to decrypt files.'''

    global encrypt_flag
    encrypt_flag = False

def on_button_click():
    '''Checks that a location has been added and either encrypt or decrypt has been selected.
    Sets the root directory for the encryption/decryption process.
    '''

    global root_directory
    global encrypt_flag

    root_directory = root_dir.get()         # gets the directory set by the user in the entry box

    if root_directory != "":            # checks the user entered a value
        if encrypt_flag == "":          # checks the user selected encryption or decryption
            sys.exit("Select encrypt or decrypt. Exiting.")         # if encryption or decryption not set, closes the program
    else:
        sys.exit("Enter a location to start. Exiting.")         # if no location set, exits the program

    window.destroy()            # closes the window
    

encrypt_flag = ""           # sets encryption flag to empty
root_directory = ""         # sets the root directory to empty

# uses tkinter to create a window with an entry box, button, and radiobuttons
window = Tk()
radio = IntVar()
window.geometry('300x200')
window.eval('tk::PlaceWindow . center')
window.title('Encrypt/Decrypt Files')
radio1 = Radiobutton(window, text='Encrypt Files', variable=radio, value=1, command=lambda: set_encrypt()).pack(anchor=W)
radio2 = Radiobutton(window, text='Decrypt Files', variable=radio, value=2, command=lambda: set_decrypt()).pack(anchor=W)
location_label = Label(window, text="Enter a location to start").pack()
root_dir = Entry(window, width=40)
root_dir.pack()
button = Button(window, text='Start', width=25, command=on_button_click)
button.pack()
window.mainloop()

try:
    os.chdir(root_directory)            # sets the top directory to begin the file search

    current_dir = os.getcwd()           # sets the current working directory

    stack = []          # creates an empty list (stack)
    stack.append(current_dir)           # adds the current directory to the stack
                
    get_file(encrypt_flag)          # starts the process of recursively getting every file from the cwd

    if encrypt_flag:
        print("All files have been encrypted!")
    else:
        print("All files have been decrypted!")
except:
    print("location does not exist")