package processing.textStructure;

import utils.ToolBox;

import java.io.IOException;
import java.io.RandomAccessFile;

/**
 * This class represents a result containing a single string (single word or multiple words treated as one)
 */
public class WordResult {
    /* The offset of the word within the block */
    private long idxInBlk;
    /* A reference for the containing Block object. */
    Block location;
    /* A string[] of length 1 that represents the content of the result. */
    protected String[] content;
    /* A string that the length of the split */
    private static final int NUMBER_OF_SPACES = 256;
    /* A string that the split string between results. */
    private static final String SPACE_CHAR = "=";
    /* A string that represents a split between results. */
    static String SPACES = initSpaces();

    /**
     * Simple constructor without index.
     * @param blk The block where this word was found
     * @param word  The word queried, represented as an array of size 1.
     */
    private WordResult(Block blk, String[] word){
        this.content = word;
        this.location = blk;
    }

    /**
     * Constructor containing index of word in block
     * @param blk The block where this word was found
     * @param word  The word queried, represented as an array of size 1.
     * @param idx   The index within the block where the word was found.
     */
    public WordResult(Block blk, String[] word, long idx) {
        this(blk, word);
        this.idxInBlk = idx;
    }

    /**
     * Constructor containing index of word in block
     * @param blk The block where this word was found
     */
    WordResult(Block blk) {
        this.location = blk;
    }

    /**
     * Getter for the result's block
     * @return  The block where this word was found.
     */
    public Block getBlock(){
        return this.location;
    }

	/**
	 * Getter for the queried word for this result
	 * @return The query word that generated this result
	 */
	public String[] getWord(){
        return this.content;
    }

	/**
	 * Method for printing the result
	 * @return The result representation as defined by the "printing results" requirement in the exercise
     * instructions.
	 * @throws IOException
	 */
	public String resultToString() throws IOException {
        RandomAccessFile file = location.getRAF();
        String result = ToolBox.readFromFile(file, location.getStartIndex() + idxInBlk,
                content[0].length());
        char newChar = (char) file.readByte();
        while(newChar != ' ' && newChar != '\r' && newChar != '\n'){
            result += newChar;
            newChar = (char) file.readByte();
        }
        return ToolBox.convertToString(location.getMetadata()) + "The result that was found is: " + result
                + "\n" + SPACES;
    }

    /**
     * it initializes the SPACES variable
     * @return the string that the spaces should contain
     */
    private static String initSpaces(){
        SPACES = "";
	    for (int i = 0; i < NUMBER_OF_SPACES; i++)
            SPACES += SPACE_CHAR;
	    return SPACES;
    }

}
