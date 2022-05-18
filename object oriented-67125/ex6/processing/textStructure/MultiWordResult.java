package processing.textStructure;

import utils.ToolBox;

import java.io.IOException;
import java.io.RandomAccessFile;
import java.util.Arrays;

/**
 * This class defines a query result for multiple non-consecutive words.
 */
public class MultiWordResult extends WordResult implements Comparable<MultiWordResult> {
	private long[] wordPositions;
	/* the confidence of this object */
	private int confidence;
	/* the pairs of this multi word result */
	private Pair[] pairs;

	private MultiWordResult(Block blk, String[] query, long idx) {
		super(blk, query, idx);
	}

	/**
	 * Constructor
	 * @param query The list of query words
	 * @param block The block where this result came from
	 * @param locs  The indices of the words in the block
	 */
	public MultiWordResult(String[] query, Block block, long[] locs) {
		super(block);
		pairs = new Pair[locs.length];
		for (int i = 0; i < pairs.length; i++)
			pairs[i] = new Pair(query[i], locs[i]);
		initConfidenceNumber();
	}

	/**
	 * this function initializes the confidence of this multi word
	 */
	private void initConfidenceNumber() {
		Arrays.sort(pairs);
		confidence = 0;
		for (int i = 1; i < pairs.length; i++)
			//the distance is this start - before.end (before.end = before.start + before.length)
			confidence += (int)(pairs[i].number - (pairs[i - 1].number + pairs[i - 1].string.length()));
	}
	/**
	 * Calculate the confidence level of a result, defined by the sum of word distances.
	 * @param locs  The locations of the query words in the text
	 * @return  The sum of distances
	 */
	private int calcConfidence(long[] locs) {
		return confidence;
	}

	/**
	 * Comparator for multy-word results
	 * @param o The other result to compare against
	 * @return  int representing comparison result, according to the comparable interface.
	 */
	@Override
	public int compareTo(MultiWordResult o) {
		return this.calcConfidence(wordPositions) - o.calcConfidence(wordPositions);
	}

	/**
	 * Extract a string that contains all words in the multy-word-result
	 * This should be a sentance starting at the word with the minimal location (index) and ending
	 * at the first line-break after the last word
	 * @return  A piece of text containing all query words
	 */
	@Override
	public String resultToString() throws IOException {
		RandomAccessFile file = location.getRAF();
		long startIndex = location.getStartIndex() + pairs[0].number;
		Pair lastQuery = pairs[pairs.length - 1];
		//length = last.endIndex - first.startIndex (last.endIndex = last.startIndex + last.length)
		int length = (int)(lastQuery.number + lastQuery.string.length() - pairs[0].number);
		String result = ToolBox.readFromFile(file, startIndex, length);
		char newChar = (char) file.readByte();
		while (newChar != '\n' && newChar != '\r'){
			result += newChar;
			newChar = (char) file.readByte();
		}
		return ToolBox.convertToString(location.getMetadata()) + "The result that was found is: " + result
				+ "\n" + SPACES;
	}

	/* represents a tuple of (string, long) which can be sorted by the longs */
	private class Pair implements Comparable<Pair>{
		/* the string in the pair */
		final String string;
		/* the long in the pair */
		final long number;

		Pair(String string, long number) {
			this.string = string;
			this.number = number;
		}

		/**
		 * @param o another pair
		 * @return which one is smaller as an int
		 */
		public int compareTo(Pair o){
			return (int)(this.number - o.number);
		}
	}
}
