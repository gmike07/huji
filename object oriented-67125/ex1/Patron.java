/**
 * This class represents a library patron that has a name and assigns values to different literary aspects
 * of books.
 */
public class Patron {
    /** The first name of this patron. */
    final String firstName;

    /** The last name of this patron. */
    final String lastName;

    /** The comic tendency of this patron. */
    int comicTendency;

    /** The dramatic tendency of this patron. */
    int dramaticTendency;

    /** The educational tendency of this patron. */
    int educationalTendency;

    /** The enjoyment threshold of this patron. */
    final int enjoymentThreshold;

    /**
     * Creates a new patron with the given characteristic.
     * @param patronFirstName The first name of this patron.
     * @param patronLastName The last name of this patron.
     * @param comicTendencyPatron The comic tendency of this patron.
     * @param dramaticTendencyPatron The dramatic tendency of this patron.
     * @param educationalTendencyPatron The educational tendency of this patron.
     * @param patronEnjoymentThreshold The enjoyment threshold of this patron.
     */
    Patron(String patronFirstName, String patronLastName, int comicTendencyPatron, int dramaticTendencyPatron,
           int educationalTendencyPatron, int patronEnjoymentThreshold){
        firstName = patronFirstName;
        lastName = patronLastName;
        comicTendency = comicTendencyPatron;
        dramaticTendency = dramaticTendencyPatron;
        educationalTendency = educationalTendencyPatron;
        enjoymentThreshold = patronEnjoymentThreshold;
    }

    /**
     * @param book gets a book object
     * @return the literary value this patron assigns to the given book.
     */
    int getBookScore(Book book){
        return comicTendency * book.getComicValue()
                + dramaticTendency * book.getDramaticValue()
                + educationalTendency * book.getEducationalValue();
    }

    /**
     * @param book gets a book object
     * @return true if this patron will enjoy the given book, false otherwise.
     */
    boolean willEnjoyBook(Book book){
        return getBookScore(book) > enjoymentThreshold;
    }

    /**
     * @return Returns a string representation of the patron
     */
    String stringRepresentation(){
        return firstName + " " + lastName;
    }


}
