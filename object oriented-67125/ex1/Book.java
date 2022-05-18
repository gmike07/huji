/**
 * This class represents a book, which has a title, author, year of publication and different literary aspects
 */
class Book {

    /** The title of this book. */
    final String title;

    /** The name of the author of this book. */
    final String author;

    /** The year this book was published. */
    final int yearOfPublication;

    /** The comic value of this book. */
    int comicValue;

    /** The dramatic value of this book. */
    int dramaticValue;

    /** The educational value of this book. */
    int educationalValue;

    /** The id of the current borrowe of this book. */
    int currentBorrowerId = -1;

    /*----=  Constructors  =-----*/

    /**
     * Creates a new book with the given characteristic.
     * @param bookTitle The title of the book.
     * @param bookAuthor The name of the author of the book.
     * @param bookYearOfPublication The year the book was published.
     * @param bookComicValue The comic value of the book.
     * @param bookDramaticValue The dramatic value of the book.
     * @param bookEducationalValue The educational value of the book.
     */
    Book(String bookTitle, String bookAuthor, int bookYearOfPublication, int bookComicValue,
         int bookDramaticValue, int bookEducationalValue){
        yearOfPublication = bookYearOfPublication;
        title = bookTitle;
        author = bookAuthor;
        comicValue = bookComicValue;
        dramaticValue = bookDramaticValue;
        educationalValue = bookEducationalValue;
    }

    /*----=  Instance Methods  =-----*/

    /**
     * Returns a string representation of the book, which is a sequence
     * of the title, author, year of publication and the total literary value of the book, separated by
     * commas, inclosed in square brackets. For example, if the book is
     * titled "Monkey Feet", was written by Ernie Douglas, published in 1987 and has a comic value of 7,
     * dramatic value of 3 and an educational value of 1, this method will return the string:
     * "[MonkeyFeet,Ernie Douglas,1987,11]"
     * @return the String representation of this book.
     */
    String stringRepresentation(){
        return "["+title+","+author+","+yearOfPublication+","+getLiteraryValue()+"]";
    }

    /**
     * @return the literary value of this book, which is defined as the sum of its comic value, its dramatic
     * value and its educational value.
     */
    int getLiteraryValue(){
        return comicValue + dramaticValue + educationalValue;
    }

    /**
     * Sets the given id as the id of the current borrower of this book, -1 if no patron is currently
     * borrowing it.
     * @param borrowerId
     */
    void setBorrowerId(int borrowerId){
        currentBorrowerId = borrowerId;
    }

    /**
     * @return the id of the current borrower of this book.
     */
    int getCurrentBorrowerId(){
        return currentBorrowerId;
    }

    /**
     * Marks this book as returned.
     */
    void returnBook(){
        currentBorrowerId = -1;
    }

    /**
     * @return the comic value of this book
     */
    int getComicValue() {
        return comicValue;
    }

    /**
     * @return the dramatic value of this book
     */
    int getDramaticValue() {
        return dramaticValue;
    }

    /**
     * @return the Educational value of this book
     */
    int getEducationalValue() {
        return educationalValue;
    }

}