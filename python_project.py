class Book:
    def __init__(self, book_name, author, year, book_type):
        self.book_name = book_name
        self.author = author
        self.year = year
        self.book_type = book_type
        self._ratings = []

    def get_average_rate(self):
        if not self._ratings:
            return "No Rates Yet"
        return round(sum(self._ratings) / len(self._ratings), 2)

    def add_rating(self, rating):
        if 0 <= rating <= 5:
            self._ratings.append(rating)
            return True
        return False

    def show_info(self):
        print("\n--- Book Info ---")
        print("Book Name :", self.book_name)
        print("Author :", self.author)
        print("Year :", self.year)
        print("Type :", self.book_type)
        print("Average Rate :", self.get_average_rate())
        print("-----------------")



class Library:
    def __init__(self):
        self._books = []

    def _find_book(self, book_name):
        for book in self._books:
            if book.book_name.lower() == book_name.lower():
                return book
        return None



class Books(Library):

    def add_book(self):
        print("\nAdd New Book")
        book_name = input("Enter book name : ")
        author = input("Enter author : ")
        year = input("Enter year : ")
        book_type = input("Enter type : ")

        if self._find_book(book_name):
            print(f"\n '{book_name}'Book is already exists.\nTry another name.")

        book = Book(book_name, author, year, book_type)
        self._books.append(book)
        print(f"\nBook '{book_name}' added successfully!")

    def show_all_books(self):
        if not self._books:
            print("\nNo books found.")
            return

        print("\n=== All Books ===")
        for book in self._books:
            book.show_info()

    def search_book(self):
        book_name = input("\nEnter book name to search: ")
        book = self._find_book(book_name)

        if book:
            book._find_book(book_name).show_info()
        else:
            print(f"\n[✗]'{book_name}' not found.")

    def delete_book(self):
        book_name = input("\nEnter book name to delete: ")
        book = self._find_book(book_name)

        if book:
            self._books.remove(book)
            print(f"\n  '{book_name}' deleted successfully!")
        else:
            print(f"\n '{book_name}' not found.")

    def rate_book(self):
        book_name = input("\nEnter book name to rate: ")
        book = self._find_book(book_name)

        if not book:
            print(f"\n  '{book_name}' not found.")
            

        raiting = input("Enter rating (0-5): ")
        if book.add_rating(raiting):
            print(f"\nRating added. \nNew Average: {book.get_average_rate()}")
        else:
            print("\nRating must be between 0 and 5.")

    
    
        
    
def main():
    library = Books()

    while True:
        print("\n===== Library Management System =====")
        print("1. Add Book")
        print("2. Show All Books")
        print("3. Search Book")
        print("4. Delete Book")
        print("5. Rate a Book")
        print("6. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            library.add_book()

        elif choice == "2":
            library.show_all_books()

        elif choice == "3":
            library.search_book()

        elif choice == "4":
            library.delete_book()

        elif choice == "5":
            library.rate_book()

        elif choice == "6":
            print("\nExiting... Goodbye!")
            break

        else:
            print("\nInvalid choice. Try again.")


main()