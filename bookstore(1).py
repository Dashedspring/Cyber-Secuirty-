import sqlite3

# Create connection to ebookstore database
def create_connection():
    conn = sqlite3.connect('ebookstore.db')
    return conn

# Creatting the book and author tables
def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    # Create book table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS book (
            id INTEGER PRIMARY KEY,
            title TEXT,
            author_id INTEGER,
            quantity INTEGER
        )
    ''')

    # Create author table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS author (
            id INTEGER PRIMARY KEY,
            name TEXT,
            country TEXT
        )
    ''')

    # Insert initial data
    cursor.executemany('''
        INSERT OR IGNORE INTO author (id, name, country)
        VALUES (?, ?, ?)
    ''', [
        (1, 'Charles Dickens', 'England'),
        (2, 'C.S. Lewis', 'Ireland'),
        (3, 'Lewis Carroll', 'England')
    ])
    # Creating additonal table. 
    cursor.executemany('''
        INSERT OR IGNORE INTO book (id, title, author_id, quantity)
        VALUES (?, ?, ?, ?)
    ''', [
        (1, 'The Tale of Two Cities', 1, 5),
        (2, 'The Lion, the Witch and the Wardrobe', 2, 3),
        (3, 'Alice\'s Adventures in Wonderland', 3, 7)
    ])

    conn.commit()
    conn.close()

# Create tables and populate them
create_tables()

def add_book():
    try:
        conn = create_connection()
        cursor = conn.cursor()
        title = input("Enter book title: ")
        author_id = int(input("Enter author ID: "))
        quantity = int(input("Enter quantity: "))
        # added insert or ignore to avoid errors. 
        cursor.execute('''
            INSERT OR IGNORE INTO book (title, author_id, quantity)
            VALUES (?, ?, ?)
        ''', (title, author_id, quantity))
        
        conn.commit()
        print("Book added successfully!")
    except ValueError:
        print("Invalid input. Please enter correct data types.")
    except Exception as e:
        print(f"Error: {e}")  # Error message for user clairty. 
    finally:
        conn.close()

def update_book():
    try:
        conn = create_connection()
        cursor = conn.cursor()
        book_id = int(input("Enter book ID to update: "))
        new_title = input("Enter new title: ")
        new_quantity = int(input("Enter new quantity: "))
        
        cursor.execute('''
            UPDATE book
            SET title = ?, quantity = ?
            WHERE id = ?
        ''', (new_title, new_quantity, book_id))
        
        if cursor.rowcount > 0:
            conn.commit()
            print("Book updated successfully!")
        else:
            print("Book ID not found.")
    except ValueError:
        print("Invalid input. Please enter correct data types.")
    except Exception as e:
        print(f"Error: {e}")  # Error message for user clairty. 
    finally:
        conn.close()

def delete_book():
    try:
        conn = create_connection()
        cursor = conn.cursor()
        book_id = int(input("Enter book ID to delete: "))
        
        cursor.execute('''
            DELETE FROM book
            WHERE id = ?
        ''', (book_id,))
        
        if cursor.rowcount > 0:
            conn.commit()
            print("Book deleted successfully!")
        else:
            print("Book ID not found.")
    except ValueError:
        print("Invalid input. Please enter correct data types.")
    except Exception as e:
        print(f"Error: {e}")  # Error message for user clairty. 
    finally:
        conn.close()

def search_books():
    try:
        conn = create_connection()
        cursor = conn.cursor()
        search_title = input("Enter title to search: ")
        
        cursor.execute('''
            SELECT * FROM book
            WHERE title LIKE ?
        ''', ('%' + search_title + '%',))
        
        results = cursor.fetchall()
        if results:
            for row in results:
                print(f"ID: {row[0]}, Title: {row[1]}, Author ID: {row[2]}, Quantity: {row[3]}")
        else:
            print("No books found with that title.")
    except Exception as e:
        print(f"Error: {e}")  # Error message for user clairty. 
    finally:
        conn.close()

def view_all_books():
    try:
        conn = create_connection()
        cursor = conn.cursor()
        # Gathering all infomration from tables. 
        cursor.execute(''' 
            SELECT book.title, author.name, author.country
            FROM book
            INNER JOIN author ON book.author_id = author.id
        ''')
        
        books = cursor.fetchall()
        for title, author_name, country in books:
            print(f"Title: {title}\nAuthor's Name: {author_name}\nAuthor's Country: {country}\n") #Printing results in easy to read maner
    except Exception as e:
        print(f"Error: {e}") # Error message for user clairty. 
    finally:
        conn.close()

import shutil
# using shutil to allow for backups. 
def backup_database():
    try:
        shutil.copy('ebookstore.db', 'ebookstore_backup.db') # creating new databse as backup. 
        print("Database backup successful.")
    except Exception as e:
        print(f"Error during backup: {e}")

def restore_database():
    try:
        shutil.copy('ebookstore_backup.db', 'ebookstore.db') # reastoring tro old backups. 
        print("Database restore successful.")
    except Exception as e:
        print(f"Error during restore: {e}")

# Creating main menu for user. 
def main_menu():
    while True:
        print("\nMain Menu")
        print("1. Enter book")
        print("2. Update book")
        print("3. Delete book")
        print("4. Search books")
        print("5. View details of all books")
        print("6. Backup database")
        print("7. Restore database")
        print("0. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            add_book()
        elif choice == "2":
            update_book()
        elif choice == "3":
            delete_book()
        elif choice == "4":
            search_books()
        elif choice == "5":
            view_all_books()
        elif choice == "6":
            backup_database()
        elif choice == "7":
            restore_database()
        elif choice == "0":
            print("Exiting the program.")
            break
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main_menu()
