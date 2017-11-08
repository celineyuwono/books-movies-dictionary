__author__ = 'Celine Yuwono, yuwono@live.unc.edu, Onyen = yuwono'

import csv
import os
import pprint

# Loads a single collection and returns the data as a list.  Upon error, None is returned.
def load_collection(file_name):
    max_id = -1
    try:
        # Create an empty collection.
        collection = []

        # Open the file and read the field names
        collection_file = open(file_name, "r")
        field_names = collection_file.readline().rstrip().split(",")

        # Read the remaining lines, splitting on commas, and creating dictionaries (one for each item)
        for item in collection_file:
            field_values = item.rstrip().split(",")
            collection_item = {}
            for index in range(len(field_values)):
                if (field_names[index] == "Available") or (field_names[index] == "Copies") or (field_names[index] == "ID"):
                    collection_item[field_names[index]] = int(field_values[index])
                else:
                    collection_item[field_names[index]] = field_values[index]
            # Add the full item to the collection.
            collection.append(collection_item)
            # Update the max ID value
            max_id = max(max_id, collection_item["ID"])

        # Close the file now that we are done reading all of the lines.
        collection_file.close()
    # Catch IO Errors, with the File Not Found error the primary possible problem to detect.
    except FileNotFoundError:
        print("File not found when attempting to read", file_name)
        return None
    except IOError:
        print("Error in data file when reading", file_name)
        collection_file.close()
        return None

    # Return the collection.
    return collection, max_id

def load_collections():
    # Load the two collections.
    book_collection, max_book_id = load_collection("books.csv")
    movie_collection, max_movie_id = load_collection("movies.csv")

    # Check for error.
    if (book_collection is None) or (movie_collection is None):
        return None, None

    # Return the composite dictionary.
    return{"books": book_collection, "movies": movie_collection}, max(max_book_id, max_movie_id)

def prompt_user_with_menu():
    print("\n\n********** Welcome to the Collection Manager. **********")
    print("COMMAND         FUNCTION")
    print("  ci         Check in an item")
    print("  co         Check out an item")
    print("  ab         Add a new book")
    print("  am         Add a new movie")
    print("  db         Display books")
    print("  dm         Display movies")
    print("  qb         Query for books")
    print("  qm         Query for movies")
    print("  x          Exit")
    return input("Please enter a command to proceed: ")

is_loaded = False
dict_books = None
dict_movies = None

def load_book_dict():
    dict_x, max = load_collections()
    dict_books = dict_x["books"]
    return dict_books

def load_movie_dict():
    dict_x, max = load_collections()
    dict_movies = dict_x["movies"]
    return dict_movies

def main():
    global is_loaded, max, dict_x,  dict_books, dict_movies
    # Load the collections, and check for an error.
    library_collections, max_existing_id = load_collections()
    if library_collections is None:
        print("The collections could not be loaded. Exiting.")
        return
    print("The collections have loaded successfully.")
    # Load
    if(is_loaded == False):
        dict_books = load_book_dict()
        dict_movies = load_movie_dict()
    is_loaded = True
    # Select from menu
    menu_selection = prompt_user_with_menu()
    try:
        while menu_selection != "x":
            if menu_selection == "ci":
                check_in()
            elif menu_selection == "co":
                check_out()
            elif menu_selection == "ab":
                add_book()
            elif menu_selection == "am":
                add_movie()
            elif menu_selection == "db":
                display_books()
            elif menu_selection == "dm":
                display_movies()
            elif menu_selection == "qb":
                query_books()
            elif menu_selection == "qm":
                query_movies()
            elif menu_selection == "x":
                break
            else:
                print("Unknown command.  Please try again.")
                input("Press enter to go back to menu.")
                main()
    except ValueError:
        print("Unknown command.  Please try again.")
        input("Press enter to go back to menu.")
        main()
    # Mark the end of the program
    print('\nEnd of program. \nBy Celine Yuwono.')

    # Prompt to exit Python
    input("Press Enter to exit.")

def check_in():
    global dict_books, dict_movies
    x = True
    while x:
        idx = int(input("Search ID: "))
        for p in dict_books:
            if idx == p["ID"]:
                p["Available"] += 1
                print(p)
                print('Updated.')
        for p in dict_movies:
            if idx == p["ID"]:
                p["Available"] += 1
                print(p)
                print('Updated.')
        x = input("Try again (Y/N)? ").lower()
        if x == "n":
            main()
        while x != "y" and x != "x":
            x = input("Try again (Y/N)? ").lower()

def check_out():
    global dict_books, dict_movies
    x = True
    while x:
        idx = int(input("Search ID: "))
        for p in dict_books:
            if idx == p["ID"]:
                p["Available"] -= 1
                print(p)
                print('Updated.')
        for p in dict_movies:
            if idx == p["ID"]:
                p["Available"] -= 1
                print(p)
                print('Updated.')
        x = input("Try again (Y/N)? ").lower()
        if x == "n":
            main()
        while x != "y" and x != "x":
            x = input("Try again (Y/N)? ").lower()

def add_book():
    global dict_books, dict_movies
    # Prompt input from user
    title = input("Enter Title: ")
    author = input("Enter Author: ")
    publisher = input("Enter Publisher: ")
    # INPUT INTEGER ONLY for pages, year, and copies
    x = True
    while x:
        try:
            pages = int(input("Enter Pages: "))
            year = int(input("Enter Year: "))
            copies = int(input("Enter Copies: "))
            available = int(input("Enter Availability: "))
        except ValueError:
            print("The input must be an integer. Try again. ")
        else:
            x = False

    # Find length of dict_movies
    dict_books_length = len(dict_books)
    dict_movies_length = len(dict_movies)

    # set ID to be equal to the last ID in the dictionary + 1
    id = max(dict_books[dict_books_length - 1]['ID'] + 1, dict_movies[dict_movies_length - 1]['ID'] + 1)

    # Display user entry to user
    print("Title       :",title)
    print("Author      :",author)
    print("Publisher   :",publisher)
    print("Pages       :",pages)
    print("Year        :",year)
    print("Copies      :",copies)
    print("Available   :",available)
    print("ID          :",id)
    prompt = input("Add this entry (Y/N/Exit)").lower() # LOWERCASE!!
    if prompt == "y":
        # Append user entry to dictionary book
        dict_books.append({"Title":title,"Author":author,"Publisher":publisher,
                           "Pages":pages,"Year":year,"Copies":copies,"Availability":available,"ID":id})
        print("Succeed adding book.")
        b = input("Go back to menu (Y/N)? ").lower()
        if b == "y":
            main()
    if prompt == "n":
        b = input("Go back to menu (Y/N)? ").lower()
        if b == "y":
            main() # Redo the add program
    if prompt == "exit":
        main()

def add_movie():
    global dict_books, dict_movies
    # Prompt input from user
    title = input("Enter Title: ")
    director = input("Enter Director: ")

    y = True
    while y:
        try:
            length = int(input("Enter Length (in minutes): "))
        except ValueError:
            print("The input must be an integer. Try again. ")
        else:
            y = False
    genre = input("Enter Genre: ")
    # INPUT INTEGER ONLY for pages, year, and copies
    x = True
    while x:
        try:
            year = int(input("Enter Year: "))
            copies = int(input("Enter Copies: "))
            available = int(input("Enter Available: "))
        except ValueError:
            print("The input must be an integer. Try again. ")
        else:
            x = False
    # Find length of dict_movies
    dict_books_length = len(dict_books)
    dict_movies_length = len(dict_movies)
    # set ID to be equal to the last ID in the dictionary + 1
    id = max(dict_books[dict_books_length - 1]['ID'] + 1,dict_movies[dict_movies_length - 1]['ID'] + 1)

    # Display user entry to user
    print("Title       :", title)
    print("Director    :", director)
    print("Length      :", length)
    print("Genre       :", genre)
    print("Year        :", year)
    print("Copies      :", copies)
    print("Available   :", available)
    print("ID          :", id)
    prompt = input("Add this entry (Y/N/Exit)").lower()  # LOWERCASE!!
    if prompt == "y":
        # Append user entry to dictionary movies
        dict_movies.append({"Title": title, "Director": director, "Length": length,
                           "Genre": genre, "Year": year, "Copies": copies, "Available": available, "ID": id})
        print("Succeed adding movie.")
        b = input("Go back to menu (Y/N)? ").lower()
        if b == "y":
            main()
    if prompt == "n":
        b = input("Go back to menu (Y/N)? ").lower()
        if b == "y":
            main()
    if prompt == "exit":
        main()

def display_books():
    from itertools import islice
    inputx = ''
    x = 0
    y = 10
    #pretty_print = pprint.PrettyPrinter(indent=4)
    #pretty_print.pprint()
    while inputx != 'm':
        for values in islice(dict_books, x, y):
            print(values)
        x += 10
        y += 10
        inputx = input("Press 'Enter' to next, 'm' to exit to menu, 'r' to read from top. ").lower()
        if x > len(dict_books):
            print('No more records.')
        if inputx == 'r':
            x = 0
            y = 10
    main()

def display_movies():
    from itertools import islice
    inputx = ''
    x = 0
    y = 10
    while inputx != 'm':
        # Load dictionary
        dict_x, max = load_collections()
        dict_movies = dict_x["movies"]
        for value in islice(dict_movies, x, y):
            print(value)
        x += 10
        y += 10
        inputx = input("Press 'Enter' to next, 'm' to exit to menu, 'r' to read from top. ").lower()
        if x > len(dict_movies):
            print('No more records.')
        if inputx == 'r':
            x = 0
            y = 10
    main()

def query_books():
    # Ask user string to search
    user_input = input("Input title or author: ").lower()
    L = True
    while L:
        for p in dict_books:
            if (user_input.lower() in p["Title"].lower()) or (user_input.lower() in p["Author"].lower()):
                print(p)
        fofofo = input("Try again (Y/N)? ").lower()
        if fofofo == "n":
            main()
        if fofofo == "y":
            break
        while fofofo != "n" and fofofo != "y":
            fofofo = input("Try again (Y/N)? ").lower()

def query_movies():
    # Ask user string to search
    user_input = input("Input title or director: ").lower()
    L = True
    while L:
        for p in dict_movies:
            if (user_input.lower() in p["Title"].lower()) or (user_input.lower() in p["Director"].lower()):
                print(p)
        fofofo = input("Try again (Y/N)? ").lower()
        if fofofo == "n":
            main()
        if fofofo == "y":
            break
        while fofofo != "n" and fofofo != "y":
            fofofo = input("Try again (Y/N)? ").lower()

main()
