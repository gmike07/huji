package Parser;

import java.util.ArrayList;

public class Review
{
    private String productID;
    private int helpfulnessNumerator, helpfulnessDenominator;
    private byte score;
    private ArrayList<String> tokens;

    /**
     * @param pid a product id
     * @param helpN the helpfulness numerator
     * @param helpD the helpfulness denominator
     * @param score the score
     * @param tokens the tokens
     */
    public Review(String pid, int helpN, int helpD, byte score, ArrayList<String> tokens)
    {
        productID = pid;
        helpfulnessNumerator = helpN;
        helpfulnessDenominator = helpD;
        this.score = score;
        this.tokens = tokens;
    }

    /**
     * @return the product id of the current review
     */
    public String getProductID() {
        return productID;
    }

    /**
     * @return the helpfulness numerator of the current review
     */
    public int getHelpfulnessNumerator() {
        return helpfulnessNumerator;
    }

    /**
     * @return the helpfulness denominator of the current review
     */
    public int getHelpfulnessDenominator() {
        return helpfulnessDenominator;
    }

    /**
     * @return the score of the current review
     */
    public byte getScore() {
        return score;
    }

    /**
     * @return the tokens of the current review
     */
    public ArrayList<String> getTokens() {
        return tokens;
    }

    /**
     * prints the review to debug
     */
    public void printReview()
    {
        System.out.println("PID: " + productID);
        System.out.println("Helpfulness: " + String.valueOf(helpfulnessNumerator) + "/" + String.valueOf(helpfulnessDenominator));
        System.out.println("Score: " + String.valueOf(score));
        System.out.println("Text: " + tokens.toString());
    }

}
