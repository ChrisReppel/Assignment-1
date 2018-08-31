"""
Name: Chris Reppel
Date due: 31/8/18
Details: Reading Tracker
GitHub URL:
"""


import csv


MENU = """Menu: 
L - List all books
A - Add new book
M - Mark a book as read
Q - Quit"""  # Defines the menu

"""
The main function. This is where the user is displayed a menu and is asked for their input. If the input is the 
letter L, it will display a list of books from a loaded csv file and and then the user will be prompted again.
The user can then choose to mark the book as read, add a new book to the list or quit the program. 
"""


def main():
    print("Reading Tracker 1.0 - by Chris Reppel")
    book_list = load_books()  # Load the books from the csv file
    print(MENU)  # Display the menu
    choice = input(">>> ").upper()  # Ask the user for the input
    while choice != "Q":  # While the users input is not Q, continue displaying the menu
        if choice == "L":
            list_books(book_list)  # List the books when user chooses L
        elif choice == "A":
            add_new_book(book_list)  # Add a new book to the list when the user chooses A
        elif choice == "M":
            list_books(book_list)  # Mark a book in the list as read when the user chooses M
            print('Enter the number of a book to mark as completed')
            check_unread_books(book_list)  # Check if the book has already been marked read or not
        else:
            print("Invalid menu choice")
        print(MENU)  # Display invalid for every other option and show the menu again
        choice = input(">>> ").upper()
    save_books(book_list)
    print("Have a nice day :)")  # When the user chooses Q, save the new list to the csv file and close


"""
The load books function, open the csv file and loads the books by removing the commas and creating a list. It converts
 the page numbers from being a string to an integer. After this it displays a message letting the user know how many 
 books were loaded form the file.
"""


def load_books():
    book_list = []
    for book in open('books.csv', 'r'):  # Open and read the csv file
        book = book.rstrip('\n').split(",")
        book_list.append(book)
    for book in book_list:
        book[2] = int(book[2])  # Change the page numbers from a string to an integer
    print('{} books loaded from books.csv'.format(len(book_list)))  # Display the number of books loaded from csv file
    return book_list


"""
The list function, displays the books in a list. It formats the table to the specific size of the longest book title 
for the first column and then the second column is formatted with the longest author's name. The third column is 
formatted depending on the length of the page numbers with the word pages always being line up. The books are ordered 
with a number in front of them and the books that haven't been read have an asterisks in front of them. The end message 
will display how many books there are in the list and it will either show that there are no more to read so the user 
should add one of what books are left to read and how many pages there are all up.
"""


def list_books(book_list):  # Display the books in a list when prompted from the user with the menu
    unread_pages = 0
    unread_books = 0
    longest_title = 0
    longest_author = 0
    book_index = 1

    for book in book_list:  # Format the first column of the table with the longest titled book
        if len(book[0]) > longest_title:
            longest_title = len(book[0])
        if book[3] == 'r':  # Calculate the number of books that are unread and the pages that need to be read all up
            unread_books += 1
            unread_pages += book[2]
        if len(book[1]) > longest_author:  # Format the second column with the longest author name
            longest_author = len(book[1])
    for book in book_list:  # Display the books in: Title, Author, Pages. With asterisks to display if read or not
        print(("*" if (book[3] is 'r') else " "), " {}.".format(book_index),
              book[0], " " * (longest_title - len(book[0])), " by ", book[1], " " * (longest_author + 1 - len(book[1])),
              " " * (4 - len(str(book[2]))), book[2], " pages")
        book_index += 1
    print(book_index - 1, " books.")  # Display how many books are in the list
    if unread_books == 0:  # If no books left to read, prompt to add a new one to the list
        print('No books left to read. Why not add a new book?')
    else:  # Display the number of books to read and total number of pages left
        print("You need to read", unread_pages, "pages in", unread_books, "books.")


"""
The add book function, allows the user to add a book to the list. The user will be asked for a title, an author and the 
number of pages the book has. The book will be automatically set as needing to be read. The book will then be appended 
to the list and set out in the correct format and order. 
"""


def add_new_book(book_list):  # Add a new book to the list when prompted by the user
    title = record_user_input("Title:")
    author = record_user_input("Author:")
    page_number = record_user_input("Pages:")
    new_book = [title, author, page_number, 'r']  # New book will be displayed in the order: Title, Author, Page number
    book_list.append(new_book)


"""
The record user input function, states that the page numbers and book index should be integers and everything else 
is a string. This function works with the verify user input to check if the users input is correct or if they 
should try again.
"""


def record_user_input(input_type):  # Record the users input and display either an error message or continue
    if input_type == "Pages:" or input_type == 'book_index':
        data_type = int

    else:
        data_type = str

    if input_type == 'book_index':
        input_type = '>>>'

    user_input = input("{} ".format(input_type))
    while verify_user_input(user_input, data_type) == 0:  # If data is returned as false display error message
        user_input = input("{} ".format(input_type))
    if data_type == int:
        user_input = int(user_input)
    return user_input  # If the data is returned as true continue with the users input


"""
The verify user input function, makes sure that the input form the user is in the format it should be. It checks if 
its a blank answer, a string when it should be an integer, an integer when it needs to be a string and if the number 
is greater than zero but not higher than the number of books in the list. If the user does use the wrong format, it 
will display an error message and will ask the user again for another input. 
"""


def verify_user_input(user_input, data_type):  # Error messages for if the user uses wrong formats for answers
    if data_type == str:
        if not user_input.strip():
            print('Input can not be blank')
            return False
        else:
            return True
    else:
        try:
            user_input = int(user_input)
            if user_input <= 0:
                print("Number must be > 0")
                return False
            else:
                return True
        except ValueError:
            print("Invalid input; enter a valid number")
            return False


"""
The check if book are unread function, checks to see if the books have been read or not. If they haven't then the 
function just hits the break point and stops. If they have all been read then the function displays that there are 
no books left to be read.
"""


def check_unread_books(book_list):  # Check if all the books have been read
    unread = 0
    for book in book_list:
        if book[3] == 'r':
            unread += 1
            read_book(book_list)
            break
    if unread == 0:  # If all the books have been read this message is displayed
        print('No required books')


"""
The read books function, allows the user to mark books that they have read as completed. If the number they choose is 
not in the list they will be shown an invalid message and be asked again. If the book has already been read then the 
user will be told this and asked again. When the book is marked as read the user will be displayed a message that 
says they have completed that book.
"""


def read_book(book_list):  # Mark the books completed when prompted by the user
    user_input = record_user_input('book_index')  # Check back to verify if the data is in the right format
    if user_input > len(book_list):  # Invalid number if its greater than the actual number of the books in the list
        print('Invalid book number')
        read_book(book_list)  # Loop back to beginning after displaying an invalid message to the user
    elif book_list[user_input - 1][3] == 'c':  # If the user chooses to mark a book that is already complete
        print('That book is already completed')
    else:  # User input minus 1 because data starts at 0 not 1!!
        print(book_list[user_input - 1][0], "by", book_list[user_input - 1][1], "completed!")
        book_list[user_input - 1][3] = 'c'  # Mark the prompted book now as completed in the list


"""
The save books function, will save the new list, convert it back into a csv file and then save and overwrite the 
original file. It will display to the user how many book were saved into the file and a goodbye message.
"""


def save_books(book_list):  # Save and overwrite the new list to the csv file and close the menu when prompted by user
    for book in book_list:
        book[2] = str(book[2])  # Change the page number back to a string for the csv file
    output_file = open('books.csv', 'w')  # Save back to original file
    for book in book_list:
        print(','.join(book), file=output_file)
    output_file.close()  # Close the file
    print(len(book_list), ' books saved to books.csv')  # Display the amount of books saved into the new list


main()

