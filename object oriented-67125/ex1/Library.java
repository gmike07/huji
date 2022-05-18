/**
 * This class represents a library, which hold a collection of books. Patrons can register at the library
 * to be able to check out books, if a copy of the requested book is available.
 */
public class Library {

    /** The maximal number of books this library allows a single patron to borrow at the same time. */
    final int borrowedCapacity;


    /** The books in the library */
    Book[] books;

    /** The patrons in the library */
    Patron[] patrons;

    /**Creates a new library with the given parameters.
     * @param maxBookCapacity The maximal number of books this library can hold.
     * @param maxBorrowedBooks The maximal number of books this library allows a single patron to borrow at
     *                         the same time.
     * @param maxPatronCapacity The maximal number of registered patrons this library can handle.
     */
    Library(int maxBookCapacity, int maxBorrowedBooks, int maxPatronCapacity){
        borrowedCapacity = maxBorrowedBooks;
        books = new Book[maxBookCapacity];
        patrons = new Patron[maxPatronCapacity];
    }

    /**Adds the given book to this library, if there is place available, and it isn't already in the library.
     * @param book The book to add to this library.
     * @return a non-negative id number for the book if there was a spot and the book was successfully added,
     * or if the book was already in the library;
     * a negative number otherwise.
     */
    int addBookToLibrary(Book book){
        for(int i = 0; i < books.length; i++)
            if(books[i] == book || books[i] == null) {
                books[i] = book;
                return i;
            }
        return -1;
    }

    /**Returns true if the given number is an id of some book in the library, false otherwise.
     * @param bookId The id to check.
     * @return true if the given number is an id of some book in the library, false otherwise.
     */
    boolean isBookIdValid(int bookId){
        if(bookId < 0 || bookId >= books.length)
            return false;
        return books[bookId] != null;
    }

    /**Returns the non-negative id number of the given book if he is owned by this library, -1 otherwise.
     * @param book The book for which to find the id number.
     * @return a non-negative id number of the given book if he is owned by this library, -1 otherwise.
     */
    int getBookId(Book book){
        for(int i = 0; i < books.length; i++)
            if(books[i] == book)
                return i;
        return -1;
    }

    /**Returns true if the book with the given id is available, false otherwise.
     * @param bookId The id number of the book to check.
     * @return true if the book with the given id is available, false otherwise.
     */
    boolean isBookAvailable(int bookId){
        if(!isBookIdValid(bookId))
            return false;
        return books[bookId].getCurrentBorrowerId() == -1;
    }

    /**Registers the given Patron to this library, if there is a spot available.
     * @param patron patron - The patron to register to this library.
     * @return a non-negative id number for the patron if there was a spot and the patron was successfully
     * registered, a negative number otherwise.
     */
    int registerPatronToLibrary(Patron patron){
        for(int i = 0; i < patrons.length; i++)
            if(null == patrons[i] || patrons[i] == patron) {
                patrons[i] = patron;
                return i;
            }
        return -1;
    }

    /**Returns true if the given number is an id of a patron in the library, false otherwise.
     * @param patronId The id to check.
     * @return true if the given number is an id of a patron in the library, false otherwise.
     */
    boolean isPatronIdValid(int patronId){
        if(patronId < 0 || patronId >= patrons.length)
            return false;
        return patrons[patronId] != null;
    }

    /**Returns the non-negative id number of the given patron if he is registered to this library, -1
     * otherwise.
     * @param patron The patron for which to find the id number.
     * @return a non-negative id number of the given patron if he is registered to this library, -1 otherwise.
     */
    int getPatronId(Patron patron){
        for(int i = 0; i < patrons.length; i++)
            if(patrons[i] == patron)
                return i;
        return -1;
    }

    /**Marks the book with the given id number as borrowed by the patron with the given patron id, if this
     * book is available, the given patron isn't already borrowing the maximal number of books allowed, and if
     * the patron will enjoy this book.
     * @param bookId The id number of the book to borrow.
     * @param patronId The id number of the patron that will borrow the book.
     * @return true if the book was borrowed successfully, false otherwise.
     */
    boolean borrowBook(int bookId, int patronId){
        if(isBookAvailable(bookId) && isPatronIdValid(patronId) &&
                patronBorrowNum(patronId) < borrowedCapacity &&
                patrons[patronId].willEnjoyBook(books[bookId])){
            books[bookId].setBorrowerId(patronId);
            return true;
        }
        return false;
    }

    /**Returns the number of borrowed books of this patron
     * @param patronId The id number of the patron that will borrow the book.
     * @return the number of borrowed books of this patron
     */
    int  patronBorrowNum(int patronId){
        int borrowNum = 0;
        for(int i = 0; i < books.length; i++)
            if(books[i].getCurrentBorrowerId() == patronId)
                borrowNum++;
        return borrowNum;
    }

    /**
     * Return the given book.
     * @param bookId The id number of the book to return.
     */
    void returnBook(int bookId){
        if(isPatronIdValid(bookId))
            books[bookId].returnBook();
    }

    /**
     * Suggest the patron with the given id the book he will enjoy the most, out of all available books he
     * will enjoy, if any such exist.
     * @param patronId The id number of the patron to suggest the book to.
     * @return The available book the patron with the given will enjoy the most. Null if no book is available.
     */
    Book suggestBookToPatron(int patronId){
        Book bestBook = null;
        int bestScore = 0;
        if(isPatronIdValid(patronId))
            for(int i = 0; i < books.length; i++)
                if(isBookAvailable(i) && patrons[patronId].getBookScore(books[i]) > bestScore){
                        bestScore = patrons[patronId].getBookScore(books[i]);
                        bestBook = books[i];
                }
        return bestBook;
    }
}
