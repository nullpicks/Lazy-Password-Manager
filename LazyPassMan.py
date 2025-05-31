import os 
import sys
from datetime import datetime
from cryptography.fernet import Fernet 

def timestring():
    timestamp =datetime.now()
    timestamp = timestamp.strftime("%c")
    return timestamp 

def encrypt_exisiting_file(filename):
    key = Fernet.generate_key()
    f = Fernet(key) 
    #Check to see if the file ends with .txt
    if not filename.endswith(".txt"):
       filename = filename + '.txt'
    #checks to see if the file exists 
    if not os.path.exists(filename): 
        print("File does not exists") 
        return False 
    #early checking can reduce code 
    #if conditions are not met, the program ends early. 

    while True: 
        userinput=input(f"Encrypting '{filename}', are you sure? (y/n) " ).lower().strip() 
        if userinput == 'y':
            break
            #break this loop to continue to the next loop
        elif userinput == 'n':
            return False 
        else: 
            print("Enter a valid answer") 
        
        #This shows the user what file we are encrypting. if yes, break loop and move to the next, if no return false, else, enter a valid option 
            
    while True: 
        if filename.endswith(".txt"): 
            filename =filename.replace('.txt','')
        if os.path.exists(filename + ".encrypted") or os.path.exists(filename +".key"): 
            choice = input(f"'{filename}'.encrypted or '{filename}'.key. Do you want to overwrite (y/n)? ") 
            if choice == 'y': 
                break
            elif choice == 'n': 
                print("Overwrite aborted")
                return False 
            else: 
                print("Enter a valid option") 
        else: 
            break
    #This is going to check to see if both the encrypted file or key exist. if either exist, prompt the user to choose to overwrite. if yes, break the while loop and move on to the next. if no, return a false value. 
    # if they don't exist, the loop breaks and we move on to the next loop. repromts for incorrect entry
    
    try: 
        with open(filename+".txt", 'r') as file: 
            content =file.read()
    except(PermissionError,OSError) as e: 
        print(f"Error '{e}'" ) 
        return False 
    #simple try except, if it can be open, the content of file is stored into the variable content. A single string is what is needed for Fernet
    if not content: 
        print("Content is empty, Not able to encrypt a blank file") 
        return False 
        #checks to see if content is empty 
    
    try: 
        content = content.encode("utf-8") 
        encrypt_bytes = f.encrypt(content) 
    except ValueError: 
            print("Error wth encryption") 
            return False 
    #this section encodes the content into a utf-8 format, stores that information into encrypt_bytes 

    try: 
        with open(filename + ".encrypted", 'wb') as encrypt_file: 
            if filename.endswith(".txt"):
                filename = filename.replace(".txt",'')
            encrypt_file.write(encrypt_bytes)
            print("File encrypted on: " + "" + timestring()) 
        with open(filename + '.key', 'wb') as key_file: 
            if filename.endswith(".txt"):
                filename = filename.replace(".txt",'')
            key_file.write(key)
            print("Key created on: " + ''+ timestring()) 
        print("Both filename and key written successfully") 
    except(PermissionError,OSError) as e:
        print("error") 
        return False 
        #This is a try except clause to create these files, written in binary. 
    return(encrypt_bytes,key)
#returns both the encrypted file and the key. both are seperatly written and stored 




#things i need to add 
#Check the file extension
#input handling, handle 'n' and invalid inputs
#Overwrite check
#error handling 
#return value




def decrypt_file(filename,key):
    try: 
        f = Fernet(key) 
        decrypted_content = None    
    
        if not filename.endswith(".encrypted"): 
            filename = filename + ".encrypted" 

        with open(filename, 'rb') as file: 
            encrypted_content =file.read()
        decrypted_content = f.decrypt(encrypted_content)
        decrypted_string = decrypted_content.decode('utf-8') 
        decrypted_string = decrypted_string.rstrip("\n") 

        print("Decrypted content: ") 
        print(decrypted_string.split('\n')) 
        return  decrypted_string
    except FileNotFoundError: 
        print("Error: Encrypted file not found") 
        return None
    except(PermissionError, OSError) as e: 
        print(f"Error, {e}") 
        return None
    except Exception as e: 
        print(f"Decryption Error: {e}") 
        return None

        
def password_db(): 
    database = {} 
    Special = ["!","@","#","$","%","&"]
    while True:
        website = input("Enter the name of the website").strip()
        website = website + ".com"
        if not website: 
            print("Website can not be empty")
            continue
        username = input("Enter a username for the website").strip()
        if not username: 
            print("Username cannot be blank")
            continue

        if ':' in website or ":" in username: 
            print("Error: Website and Username cannot contain : ")
            continue
        while True:
            password = input("Enter a password for the username").strip()
            if not password: 
                print("Password can not be left blank")
                continue
            if len(password) < 8 : 
                print("Password can not be less than 8 charaters") 
                continue 

            if not passcheck(password,Special): 
                print("Password is not strong enough")
                continue
            if passcheck(password,Special):
                break



        if website not in database: 
            database[website] = {}
        if username in database[website]: 
            while True: 
                answer = input("Do you want to overwrite the username? (y/n)").lower()
                if answer == 'y':
                    database[website][username]=password
                    break
                elif answer == 'n': 
                    break        
                else: 
                    print("enter a valid option")
        else: 
            database[website][username]= password
        answer=input("Continue? (y/n)").lower()
        if answer != 'n':
            continue
        return(database)


def passcheck(password,Special):
    found = False 
    for char in Special:
        if char in password:
            found = True 
            break
    return found
       #Passcheck is the function created to make sure that a password entered has at least one of the following
       #special characters. The idea is to check each individual character. If one is found, found is set to true
       #if not, found stays false. Found is returned as the appropriate value


def create_file():
    while True: 
        filename = input("Name this file").lower().strip()
        if filename.isdigit():
            print("Filename can not be a digit")
            continue
        else:
            break
    if os.path.exists(filename+'.txt'):
        while True: 
            answer =input("File already in use. Would you like to overwrite the existing file? (y/n)").lower()
            if answer == 'y': 
                print(f"You have chosen to overwrite '{filename}'")
                try: 
                    with open(filename + ".txt", 'w') as file: 
                        database = password_db()
                        for website, inner_key in database.items(): 
                            for username,password in inner_key.items():
                                file.write(f"{website}:{username}:{password}\n")
                        print(f"'{filename}' overwritten" + '' +  timestring()) 
                        return filename,database
                except (PermissionError, OSError) as e: 
                    print(f"Cannot overwrite  the file: '{e}'" )
                    return None
            if answer == 'n':   
                print("File Will not be overwritten")
                return None, {}
            if answer not in ['y','n']: 
                print("Please select a valid choice")
    else:
        print("The file does not exist. Creating the file now")
        try: 
            with open(filename + '.txt', 'w') as file:
            
                database = password_db()
                for website, inner_key in database.items():
                    for username,password in inner_key.items():
                        file.write(f"{website}:{username}:{password}\n") 
                print("Filename created successfully on "+ ' ' +  timestring())
                return filename, database
        except (PermissionError, OSError) as e: 
            print(f"Cannot create the file: '{e}'" )
            return None, {}



def read_file(filename):
    try:
        if not filename.endswith(".txt"):
            filename = filename + ".txt"
        with open(filename,'r') as file:   
            lines = file.readlines()
            for line in lines: 
                print(line)     
    except FileNotFoundError: 
        print("File not found")
        return False





def edit_file(filename,database):  
    if not filename.endswith(".txt"):
        filename = filename + ".txt"
    if os.path.exists(filename): 
        with open(filename, 'a') as file: 
            print(f"Appending file: '{filename}'")
            database = password_db()
            for website, inner_key in database.items():
                for username,password in inner_key.items(): 
                    file.write(f"{website}:{username}:{password}\n")
            print("File Edited successfully")


def delete_entry(filename):     
    if not filename.endswith(".txt"):
        filename = filename +".txt"
    database=load_file(filename)
    if not database:
        print("Database is empty")
        return None
    while True:    
         
        choice = input("Delete an entry(y/n)").lower()
        if not choice: 
            print("Text can not be left blank, Please select an answer")
        if choice == 'y': 
            try:
                delweb = input("Enter the website you want to remove")
                deluser = input("Enter the user you wish to delete ")
                if not delweb or  not deluser:
                    print("Entries can not be left blank")
                    continue
                if delweb in database and deluser in database[delweb]:
                    del database[delweb][deluser]
                    print(f"'{deluser}' deleted from '{delweb}'")
                    save_file(filename,database)
                    print("File saved on" + "" + timestring()) 
                else:
                    print("Website or Username not found")
                    continue
                if not database[delweb]:
                    del database[delweb]
                
                return True
            except(FileNotFoundError,PermissionError,OSError):
                print("Error: You got a problem somewhere. Do something other than what you did.")
        elif choice =='n':
            print('Entry will not be deleted')
            return False
        else: 
            print("Please Enter (y/n)")
       

def load_file(filename):
    database = {}
    try:
        if not filename.endswith(".txt"):
            filename = filename + ".txt"
        with open(filename, 'r') as file: 
            lines = file.readlines()
            if not lines:
                print("file is empty")
                return database
            for line in lines:
                try:
                    website,username,password=line.strip().split(":")
                    if  website not in database: 
                        database[website]= {}
                    database[website][username] = password
                except ValueError: 
                    print("Invalid File text")
            return database    
    except (PermissionError, OSError,FileNotFoundError):
        print("Error")
        return {}



#the function displayed here is going to read the contents of the file and split them up to store them in another database
#in memory for me to work with.


def save_file(filename, database):
    try:
        with open(filename, 'w') as file: 
            for website, inner_key in database.items():
                for username,password in inner_key.items():
                    file.write(f"{website}:{username}:{password}\n")
        print("File saved successfully")
        return True
    except(PermissionError, OSError):
        print("Error, Cannot save file")
        return False
    
       

     
def main():
    database = {}
    filename = None
    # Command-line lookup: filename and website
    if len(sys.argv) == 3:
        filename = sys.argv[1].strip()
        if filename.endswith(".txt"):
            filename = filename[:-4]
        website = sys.argv[2].strip()
        if not website.endswith(".com"):
            website += ".com"  # Match password_db format
        database = load_file(filename)
        found = False
        for web, users in database.items():
            if web == website:
                for username, password in users.items():
                    print(f"Website: '{website}', Username: '{username}', Password: '{password}'")
                found = True
        if not found:
            print(f"Website '{website}' not found in '{filename}.txt'")
        return
    
    # Handle single argument
    if len(sys.argv) == 2:
        print("Error: Please provide both filename and website (e.g., python Password.py password google.com)")
        return

    

    print("Welcome to Lazy Pass. This is a program designed to create,store and recall password information")
    print("*************************************************************************************************")
    print("Version 1 includes basic functionality and encryption")
    print("******************************************************************************************")
    print("*****************************************************************************")
    print(f"You are currently working with filename '{filename}'")


    while True:
        choice = input("1.Create a File\n2.Load a file\n3.Quit\n")
        if not choice: 
            print("Choice can not be blank")
        if not choice.isdecimal():
            print("Choice must be a digit")
            
        if choice == '1':
            filename,database = create_file()
            print("Thank you for using this feature")
    
        elif choice == '2': 
            while True: 
                targetfile = input("Type a File to Load: ") 
                targetfile = targetfile + ".txt"
                if not targetfile: 
                    print("Entry can not be blank")
                    continue
                if not os.path.exists(targetfile): 
                    print(f"'{targetfile}' does not exist")
                    continue
                if targetfile: 
                    break
            if not targetfile.endswith(".txt"):
                targetfile = targetfile +".txt"
            if os.path.exists(targetfile):
                #targetfile =  targetfile.replace(".txt", "")
                print(f"File: '{targetfile}' is found")
                database=load_file(targetfile) 
                if not database: 
                    print("Failed to load file contents, database is empty") 
                    continue
            else: 
                print("File not found") 
            while True:
                subChoice =input("1.Read\n2.Edit\n3.Quit\n")
            
                if subChoice == '1':
                    load_file(targetfile)
                    read_file(targetfile)
                elif subChoice == '2':
                    editchoice=input("1.Edit File\n2.Delete File\n3.Encrypt file\n4.Back\n: ")
                    if not editchoice: 
                        print("Entry can not be blank")
                    if editchoice =='1':
                        print("You have choosen edit")
                        load_file(targetfile)
                        edit_file(targetfile,database)
                        break
                    elif editchoice =='2': 
                        print("You have choosen delete")
                        delete_entry(targetfile)
                        break
                    elif editchoice =='3':
                        print("Welcome to the encryption part of this program." ) 
                        encryptchoice = input("1.Encrypt File\n2.Decrypt and Read a file\n3.Quit\n") 
                        
                        if encryptchoice == '1': 
                            if targetfile.endswith(".txt"):
                                   targetfile = targetfile.replace(".txt","")
                            encrypt_exisiting_file(targetfile)  
                            print("Done") 

                        elif encryptchoice == '2': 
                            try: 
                                if targetfile.endswith(".txt"): 
                                    targetfile = targetfile.replace('.txt',"")
                                with open(targetfile + ".key" ,'rb') as file:
                                
                                    key=file.read()
                                    decrypt_file(targetfile,key)  
                            except FileNotFoundError:
                                print("File Not Found Error")

                        elif encryptchoice == '3':
                            break
                        else:
                            print("Please select a valid option") 

                    elif editchoice =='4':
                        break
                    else: 
                        print("Please enter a valid answer")                    
                elif subChoice =="3":
                    break
                else: 
                    print("Please enter a correct input")
        elif choice == '3': 
            sys.exit()
        else: 
            print("Input invalid, please enter one of the choices above ")

    



if __name__ == "__main__":     
    main()
